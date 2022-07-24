import os
from dotenv import load_dotenv
import tempfile

from requests import Session
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'Ma base de données en prod'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

class TestingConfig(Config):
    db_fd, db_path = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path
    TESTING = True
    LIVESERVER_PORT = 8943
    LIVESERVER_TIMEOUT = 10

