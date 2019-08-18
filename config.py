""" Config
"""
from pathlib import Path

HOME_PATH = Path(__file__).parent
INSTANCE_PATH = HOME_PATH / 'instance'


class Config:
    """ Default Settings
    """
    INSTANCE_PATH = INSTANCE_PATH
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(INSTANCE_PATH / 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'This is a very strong secret key!'

    # SQLALCHEMY_ECHO = True

    PROPAGATE_EXCEPTIONS = True

    SWAGGER_URL = '/api/docs'
    SWAGGER_API_URL = 'http://127.0.0.1:5000/static/swagger.json'
