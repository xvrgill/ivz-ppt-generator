from flask import jsonify
from flask_restful import Resource
from api.controllers.air_table_controller import AirTableController


class Post(Resource):
    def get(self, id):
        controller = AirTableController()
        post_group = controller.get_post(str(id))
        return jsonify(post_group)
