from flask import Flask
from flask_cors import CORS
from flask_restful import Api

# * Reminder: To use config variables you can import app from another file and use the code - app.config['SOME_VARIABLE']

app = Flask(__name__)
app.config.from_object("config.HerokuProductionConfig")
api = Api(app)
CORS(app)

#! Consider adding error handlers with static templates - may need to specify behavior with application/json

# Resource Imports
from api.resources.index import Index
from api.resources.post_group import PostGroup
from api.resources.post import Post
from api.resources.pptx import PPT

# Resource Definitions
api.add_resource(Index, "/")
api.add_resource(PostGroup, "/post-group/<string:id>")
api.add_resource(Post, "/post/<string:id>")
api.add_resource(PPT, "/generate-powerpoint/<string:id>")
