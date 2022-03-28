"""Configuration for flask app"""
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


# TODO: Use dataclass to avoid 'too few arguements lint error'
class DevelopmentConfig:
    # Air Table API
    AIR_TABLE_API_KEY = environ.get("AIR_TABLE_API_KEY")
    AIR_TABLE_BASE_ID = environ.get("AIR_TABLE_BASE_ID")
    POST_GROUPS_TABLE = environ.get("POST_GROUPS_TABLE")
    POSTS_TABLE = environ.get("POSTS_TABLE")


# Heroku Local Configuration
class HerokuLocalConfig:
    AIR_TABLE_API_KEY = environ.get("AIR_TABLE_API_KEY")
    AIR_TABLE_BASE_ID = environ.get("AIR_TABLE_BASE_ID")
    POST_GROUPS_TABLE = environ.get("POST_GROUPS_TABLE")
    POSTS_TABLE = environ.get("POSTS_TABLE")
    SECRET_KEY = environ.get("FLASK_SECRET_KEY")


# Heroku Production Configuration
class HerokuProductionConfig:
    # config has issues
    AIR_TABLE_API_KEY = environ.get("AIR_TABLE_API_KEY")
    AIR_TABLE_BASE_ID = environ.get("AIR_TABLE_BASE_ID")
    POST_GROUPS_TABLE = environ.get("POST_GROUPS_TABLE")
    POSTS_TABLE = environ.get("POSTS_TABLE")
    SECRET_KEY = environ.get("FLASK_SECRET_KEY")
