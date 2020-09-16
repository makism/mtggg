from flask import Flask
from flask_restful_swagger_3 import Api

from operator import itemgetter
import sys

sys.path.append("../config/")
sys.path.append("models/")
import config

app = Flask(__name__)
# api = Api(app)
api = Api(app, version="1.0", title="mtgggg", api_spec_url="/v1/api/swagger")


from api.resources.querysimilar import QuerySimilar
from api.resources.generaterandom import GenerateRandom
from api.resources.search import Search
from api.resources.list import List, ListSets, ListPage
from api.resources.swagger import ApiSwagger

# Main entrypoints
api.add_resource(QuerySimilar, "/v1/ml/similar/<int:card_id>/")
api.add_resource(
    GenerateRandom, "/v1/ml/generate/random/", methods=["GET", "POST", "DELETE"]
)
api.add_resource(Search, "/v1/search/")
api.add_resource(ListSets, "/v1/list/", methods=["GET"])
api.add_resource(List, "/v1/list/<string:keyrune_code>/", methods=["GET"])
api.add_resource(
    ListPage, "/v1/list/<string:keyrune_code>/<int:page>/", methods=["GET"]
)
# Helper
api.add_resource(ApiSwagger, "/v1/api/swagger-ui/", methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
