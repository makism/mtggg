""" A simple registry of the endpoints.

"""
from flask_restful import Resource


class RegistryList(Resource):
    def get(self):
        """Returns a simple list of all the endpoints."""
        registry = {
            "ml": {"/similar/": "<int:card_id>/", "/generate/random/": None},
            "search": "?name=",
            "list": ["/string:keyruneCode/", "/string:keyruneCode/<int:page>/"],
        }
        return registry
