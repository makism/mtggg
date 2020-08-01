""" Resources for listing all the  cards in a specific set.

"""
from flask_restful import Resource
from bson import json_util
import json
from pymongo import MongoClient


class ListSets(Resource):
    def get(self):
        """ Return a list of all supported sets. """
        result = ["M21", "THB", "M20", "WAR"]
        return result

    @staticmethod
    def check_valid_keyrunecode(keyrune_code):
        return True


class List(Resource):
    def get(self, keyrune_code):
        """ """
        if not ListSets.check_valid_keyrunecode(keyrune_code):
            return "Error"

        client = MongoClient()
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
        """ """
        client = MongoClient()
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
