""" Query similar cards using NLP

"""
from flask_restful import Resource
from bson import json_util
import json
from pymongo import MongoClient


class QuerySimilar(Resource):
    def get(self, card_id):
        """ """
        client = MongoClient()

        card_details = client.mtggg.cards.find_one({"number": card_id})
        json_str = json_util.dumps(card_details)
        card_details_json_obj = json.loads(json_str)
        del card_details_json_obj["_id"]

        ml_similar = client.mtggg.ml.similar.find_one({"card_number": card_id})
        # json_str = json_util.dumps(ml_similar)
        # ml_similar_json_obj = json.loads(json_str)
        # del ml_similar_json_obj["card_number"]
        # del ml_similar_json_obj["_id"]

        if ml_similar is not None:
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
        else:
            result = {"message": "We couldn't find the card you asked for :/"}

        return result
