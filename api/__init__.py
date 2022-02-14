from flask import Flask
from flask_cors import CORS
from flask_restful import Api

# * Reminder: To use config variables you can import app from another file and use the code - app.config['SOME_VARIABLE']

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
api = Api(app)
CORS(app)


# Resource Imports
from api.resources.index import Index


# Resource Definitions
api.add_resource(Index, "/")
