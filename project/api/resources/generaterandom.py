""" Generate random card names

This endpoint works as follows:

1. A `PUT` request must be placed first, that will result in a job being scheduled on Airflow (if available).
   A unique `request_id` will be returned to the user which will be used to fetch the results and keep track of
   the progress.
2. A `GET` request alongside with a `request_id` may be performed to fetch the status and possible result of the
   scheduled job.
3. A `DELETE` request alongside with a `request_id` may be performed to clean up a job. This will remove all relevant
   records from MongoDB and delete the DAG from Apache Airflow.

"""
import numpy as np
from flask import Flask
from flask_restful import Resource, Api, reqparse
from jinja2 import Environment, FileSystemLoader, Template
from pymongo import MongoClient
from bson import json_util
from operator import itemgetter
import json
import shutil

# from flask_httpauth import HTTPBasicAuth
from datetime import datetime as dt
import uuid


import sys

sys.path.append("../../config/")
import config

# app = Flask(__name__)
# api = Api(app)
# auth = HTTPBasicAuth()
# client = MongoClient()


class GenerateRandom(Resource):
    # decorators = [auth.login_required]

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

        result = shutil.copy(src=tmp_dag, dst=dst_dag)

        return result

    def put(self):
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
        request_id = uuid.uuid4()

        self.create_dag(uuid=request_id, dt=now, deploy=True)

        # Return this unique hash
        result["request_id"] = f"{request_id}"
        result["message"] = result["message"].format(
            "Your request has been scheduled. Please check back again in a bit at http://localhost:5000/v1/generate/random/ with POST {'request_id': '%s'}."
            % request_id
        )

        return result

    def get(self):
        """  """
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
        client = MongoClient()
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
        """ Delete/Clean up a job/results given a `request_id` """
        parser = reqparse.RequestParser()
        parser.add_argument("request_id", type=str, location="json", required=True)
        args = parser.parse_args()

        uuid = args.request_id

        # Now
        now = dt.now()

        result = {"request_id": uuid, "when": f"{now}"}

        #
        client = MongoClient()
        db = client["mtggg"]
        col = db["api_jobs"]
        col2 = db["api_results"]

        # Remove records from MongoDB
        recs1 = col.delete_many({"uuid": f"{uuid}"})
        recs2 = col2.delete_many({"uuid": f"{uuid}"})

        result["mongodb"] = recs1.deleted_count + recs2.deleted_count

        # Remove the dags from Airflow
        #
        import requests

        response = requests.delete(
            f"http://localhost:8080/api/experimental/dags/dag_ml_generate_{uuid}"
        )

        result["airflow_api"] = response.ok
        import os

        fname_dag = f"/home/vagrant/airflow/dags/dag_ml_generate_{uuid}.py"
        if os.path.exists(fname_dag):
            result_remove = os.remove(fname_dag)
            result["airflow_delete"] = result_remove
        else:
            result["airflow_delete"] = "DAG does not exist."

        # curl -X DELETE http://localhost:8080/api/eaperimental/dags/dag_ml_generate_b7893317-afc3-489a-aa3c-76d6f5109aa9

        return result
