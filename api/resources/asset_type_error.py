from flask import render_template, make_response
from flask_restful import Resource


class AssetTypeError(Resource):
    def __init__(self) -> None:
        pass

    def get(self):
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("asset_type_error.html"), 200, headers)
