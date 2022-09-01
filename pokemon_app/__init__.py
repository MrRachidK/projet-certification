import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from .models import init_db

def create_app(mode='development'):

    # Upload env variables
    load_dotenv()

    sentry_sdk.init(
        dsn="https://e519098cadb945139dc117c34caf4fbe@o1360069.ingest.sentry.io/6647818",
        integrations=[
            FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

    # Create app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

    # Select config
    if mode == "development":
        app.config.from_object('config.DevelopmentConfig')
    elif mode == "test":
        app.config.from_object('config.TestingConfig')
    elif mode == "production":
        app.config.from_object('config.ProductionConfig')

    db = SQLAlchemy(app)

    with app.app_context():
        init_db()

    # Connect to log manager with flask login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
        return models.User.query.get(int(user_id))

    from pokemon_app import models

    @app.cli.command("init_db")
    def init_db():
        models.init_db()

    # blueprint for auth routes in our app
    from pokemon_app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from pokemon_app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app