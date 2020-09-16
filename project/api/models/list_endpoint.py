# author Avraam Marimpis <marimpis@brainvoyager.com>

from flask_restful_swagger_3 import Schema


class ListSets(Schema):
    type = "object"
    properties = {"sets": {"type": "array", "items": {"type": "string"}}}
    required = ["sets"]
