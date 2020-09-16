""" Resources for listing all the  cards in a specific set.

"""
from flask_restful import Resource
from flask_restful_swagger_3 import swagger
from bson import json_util
import json
from pymongo import MongoClient

import sys

from list_endpoint import ListSets as ModelListSets


class ListSets(Resource):
    """List the sets."""

    @swagger.doc(
        {
            "tags": ["List"],
            "responses": {
                "200": {
                    "description": "",
                    "content": {
                        "application/json": {
                            "schema": ModelListSets,
                            "examples": {
                                "DefaultReply": {
                                    "summary": "Lists all available sets",
                                    "value": {"sets": ("M21", "THB", "M20", "WAR")},
                                }
                            },
                        }
                    },
                }
            },
        }
    )
    def get(self):
        """Return a list of all supported sets."""
        result = {"sets": ["M21", "THB", "M20", "WAR"]}
        return result

    @staticmethod
    def check_valid_keyrunecode(keyrune_code):
        return True


class List(Resource):
    @swagger.doc(
        {
            "tags": ["List"],
            "parameters": [
                {
                    "name": "keyrune_code",
                    "description": "A valid keyrune code; i.e. M20",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                }
            ],
            "responses": {},
        }
    )
    def get(self, keyrune_code):
        """Fetches all the cards for the given `keyrune_code`."""
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
    @swagger.doc(
        {
            "tags": ["List"],
            "parameters": [
                {
                    "name": "keyrune_code",
                    "description": "A valid keyrune code; i.e. M20",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                },
                {
                    "name": "page",
                    "description": "Page number.",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "int", "default": 1},
                },
            ],
            "responses": {},
        }
    )
    def get(self, keyrune_code, page):
        """Fetches all the cards, paginated, in page `page` for the given keyrune_code."""
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
