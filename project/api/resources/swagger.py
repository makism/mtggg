from flask import render_template, make_response, Response
from flask_restful import Resource


class ApiSwagger(Resource):
    def get(self):
        """Render a return an swagger-ui single page."""
        config = {"swagger_json": f"http://0.0.0.0:5000/v1/api/swagger.json"}
        response = Response(response=render_template("swagger.j3", **config))
        return response
