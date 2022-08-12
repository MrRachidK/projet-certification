import os
from dotenv import load_dotenv
import tempfile
import urllib

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    if os.environ.get('SQLALCHEMY_DATABASE_MSSQL'):
        params = urllib.parse.quote_plus(os.environ['SQLALCHEMY_DATABASE_MSSQL'])
        SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

class TestingConfig(Config):
    db_fd, db_path = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    TESTING = True
    LIVESERVER_PORT = 8943
    LIVESERVER_TIMEOUT = 10

