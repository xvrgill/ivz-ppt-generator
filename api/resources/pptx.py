"""Resource that generates ppt from post group"""
import json
from scripts.ppt_generator import PowerPointGenerator
from flask_restful import Resource
from api import app
import requests
from flask import jsonify


class PPT(Resource):
    def get(self, id):
        root_url = app.config["ROOT_URL"]
        post_group_url = root_url + "/post-group/" + id
        post_group = requests.get(post_group_url)
        # Todo: Use post group to get data from linked posts and process further
        return post_group.json()
