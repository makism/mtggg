import numpy as np
from flask import Flask
from flask_restful import Resource, Api, reqparse
from jinja2 import Environment, FileSystemLoader, Template
from pymongo import MongoClient
from bson import json_util
from operator import itemgetter
import json
import shutil
from flask_httpauth import HTTPBasicAuth
from datetime import datetime as dt
import uuid


import sys

sys.path.append("../config/")
import config

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
client = MongoClient()


@auth.verify_password
def verify_password(username, password):
    # if username in users:
    # return check_password_hash(users.get(username), password)
    # return False
    return True


class GenerateRandom(Resource):
    decorators = [auth.login_required]

    def check_airflow_is_alive(self):
        import requests

        query = requests.get("http://localhost:8080//api/experimental/test")

        if query["status"] == "Ok":
            return True
        else:
            return False

    def create_dag(self, uuid, dt, deploy=False):
        tpl_file = "rest_api_generate.py.tpl"

        env = Environment(loader=FileSystemLoader(f"{config.AIRFLOW_PROJECT_DIR}"))
        tpl = env.get_template(tpl_file)

        dt_now = dt.now()

        dag = tpl.render(
            dag_name=f"dag_ml_generate_{uuid}",
            uuid=uuid,
            parse_datetime=dt,
            conf_dt_Y=dt.year,
            conf_dt_m=dt.month,
            conf_dt_d=dt.day,
            conf_user_name=f"mtggg_ml",
        )

        tmp_dag = f"{config.TEMP}/dag_ml_generate_{uuid}.py"
        dst_dag = f"/home/vagrant/airflow/dags/dag_ml_generate_{uuid}.py"
        with open(tmp_dag, "w") as fp:
            fp.write(dag)

        shutil.copy(src=tmp_dag, dst=dst_dag)

        pass

    def get(self):
        # Now
        now = dt.now()

        # Return message Template
        result_tpl = {"when": f"{now}", "message": "{}"}
        result = result_tpl

        # Check if airflow is running
        if self.check_airflow_is_alive is False:
            result["message"] = result["message"].format(
                "Airflow is not running. Sorry."
            )
            return result

        # Generate a unique hash
        # request_id = uuid.uuid4()
        request_id = "b7893317-afc3-489a-aa3c-76d6f5109aa9"

        self.create_dag(uuid=request_id, dt=now, deploy=True)

        # Return this unique hash
        result["request_id"] = f"{request_id}"
        result["message"] = result["message"].format(
            "Your request has been scheduled. Please check back again in a bit at http://localhost:5000/v1/generate/random/ with POST {'request_id': '%s'}."
            % request_id
        )

        return result

    def post(self):
        # Now
        now = dt.now()

        # Return message Template
        result_tpl = {"when": f"{now}", "message": "{}"}
        result = result_tpl

        if self.check_airflow_is_alive is False:
            result["message"] = result["message"].format(
                "Airflow is not running. Sorry."
            )
            return result

        parser = reqparse.RequestParser()
        parser.add_argument("request_id", type=str, location="json", required=True)
        args = parser.parse_args()

        uuid = args.request_id

        #
        db = client["mtggg"]
        col = db["api_jobs"]
        col2 = db["api_results"]

        query = col.find_one({"uuid": f"{uuid}"})
        if query is None:
            result["message"] = result["message"].format(
                "No results for the given request-id."
            )
            return result

        if query["status"] == "queued":
            result["message"] = result["message"].format(
                "Sorry, we are still working on your request. Try again later."
            )
            return result

        query = col2.find_one({"uuid": f"{uuid}"})
        if query is not None:
            result["message"] = result["message"].format(
                "Done, check out the random card names we've generated for you."
            )
            result["card_names"] = query["response"]
            return result

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("request_id", type=str, location="json", required=True)
        args = parser.parse_args()

        uuid = args.request_id

        #
        db = client["mtggg"]
        col = db["api_jobs"]
        col2 = db["api_results"]

        # Remove records from MongoDB
        col.delete_many({"uuid": f"{uuid}"})
        col2.delete_many({"uuid": f"{uuid}"})

        # Remove the dags from Airflow
        #
        import requests

        requests.delete(
            f"http://localhost:8080/api/experimental/dags/dag_ml_generate_{uuid}"
        )


class Search(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True)
        args = parser.parse_args()

        card_name = args["name"]
        # card_details = client.mtggg.cards.find_one({"name": card_name})

        query = {"name": {"$regex": f"{card_name}", "$options": "i"}}
        docs = client.mtggg.cards.find(query)

        json_str = json_util.dumps(docs)
        json_obj = json.loads(json_str)

        result = {
            "query_name": card_name,
            "total_results": docs.count(),
            "results": json_obj,
        }

        return result


class List(Resource):
    def get(self, keyrune_code):
        cards = client.mtggg.cards.find()
        count_cards = cards.count()
        cards = cards.skip(0).limit(10).sort("name")
        cards = list(cards)

        json_str = json_util.dumps(cards)
        json_obj = json.loads(json_str)

        result = {
            "set": keyrune_code,
            "page": 1,
            "total_cards": count_cards,
            "cards": json_obj,
        }

        return result


class ListPage(Resource):
    def get(self, keyrune_code, page):
        cards = client.mtggg.cards.find()
        count_cards = cards.count()

        page = int(page)
        limit = 10
        total_pages = int(count_cards / 10.0)
        skip = int(page * 10.0)

        cards = cards.skip(skip).limit(limit).sort("name")
        cards = list(cards)

        json_str = json_util.dumps(cards)
        json_obj = json.loads(json_str)

        result = {
            "set": keyrune_code,
            "page": page,
            "total_cards": count_cards,
            "cards": json_obj,
        }

        return result


class QuerySimilar(Resource):
    def get(self, card_id):
        parser = reqparse.RequestParser()
        parser.add_argument("card_id", type=int, required=True)

        card_details = client.mtggg.cards.find_one({"number": card_id})
        json_str = json_util.dumps(card_details)
        card_details_json_obj = json.loads(json_str)
        del card_details_json_obj["_id"]

        ml_similar = client.mtggg.ml.similar.find_one({"card_number": card_id})
        # json_str = json_util.dumps(ml_similar)
        # ml_similar_json_obj = json.loads(json_str)
        # del ml_similar_json_obj["card_number"]
        # del ml_similar_json_obj["_id"]

        ml_similar_results = {}
        for similar_card_id in ml_similar["similar"]:
            card_details = client.mtggg.cards.find_one({"number": similar_card_id})

            if card_details is not None:
                del card_details["_id"]
                ml_similar_results[card_details["name"]] = card_details

        result = {
            "card_id": card_id,
            "card_details": card_details_json_obj,
            "similar": ml_similar_results,
        }

        return result


class RegistryList(Resource):
    def get(self):
        registry = {
            "ml": {"/similar/": "<int:card_id>/", "/generate/random/": None},
            "search": "?name=",
            "list": ["/string:keyruneCode/", "/string:keyruneCode/<int:page>/"],
        }
        return registry


api.add_resource(RegistryList, "/v1/registry")
api.add_resource(QuerySimilar, "/v1/ml/similar/<int:card_id>/")
api.add_resource(
    GenerateRandom, "/v1/ml/generate/random/", methods=["GET", "POST", "DELETE"]
)
api.add_resource(Search, "/v2/search/")
api.add_resource(List, "/v1/list/<string:keyrune_code>/")
api.add_resource(ListPage, "/v1/list/<string:keyrune_code>/<int:page>/")
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
