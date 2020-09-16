""" Search for cards based on their name.

"""
from flask_restful import Resource, reqparse
from flask_restful_swagger_3 import swagger
from bson import json_util
import json
from pymongo import MongoClient


class Search(Resource):
    @swagger.doc(
        {
            "tags": ["Search"],
            "parameters": [
                {
                    "name": "name",
                    "description": "A card name.",
                    "in": "query",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "responses": {},
        }
    )
    def get(self):
        """Queries ElasticSearch for cards titled `name`."""
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=False)
        args = parser.parse_args()
        card_name = args["name"]

        if card_name is None:
            return {
                "message": "Please define a query.",
                "query_opts": {"name": "Search based on the card name"},
            }

        # card_details = client.mtggg.cards.find_one({"name": card_name})
        query = {"name": {"$regex": f"{card_name}", "$options": "i"}}

        client = MongoClient()
        docs = client.mtggg.cards.find(query)

        if docs is not None:
            json_str = json_util.dumps(docs)
            json_obj = json.loads(json_str)

            result = {
                "query_name": card_name,
                "total_results": docs.count(),
                "results": json_obj,
            }
        else:
            result = {
                "query_name": card_name,
                "total_results": 0,
                "message": "Nothing found, yikes.",
            }

        return result
