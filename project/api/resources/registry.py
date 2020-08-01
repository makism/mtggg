"""

"""
from flask_restful import Resource


class RegistryList(Resource):
    def get(self):
        registry = {
            "ml": {"/similar/": "<int:card_id>/", "/generate/random/": None},
            "search": "?name=",
            "list": ["/string:keyruneCode/", "/string:keyruneCode/<int:page>/"],
        }
        return registry
