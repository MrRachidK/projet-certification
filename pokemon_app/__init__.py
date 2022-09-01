import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.security import generate_password_hash
import pandas as pd
from config import basedir

from .models import init_db, db

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

    from pokemon_app.models import Pokemon, User

    db.init_app(app)

    with app.app_context():
        db.create_all()
        pokemon_data = pd.read_csv(os.path.join(basedir, 'data/intermediate/pokemon.csv'), index_col=False, delimiter = ',')
        pokemon_data = pokemon_data.drop(['Number'], axis=1)
        # pokemon_data.to_sql('pokemon', db.engine, if_exists='append', index=False)
        pokemon_sql = pd.read_sql("SELECT * FROM pokemon", db.engine)
        if pokemon_sql.shape[0] == 0:
            pokemon_data.to_sql('pokemon', db.engine, if_exists='append', index=False)
        else:
            existing_pokemon = pd.read_sql("SELECT name FROM pokemon", db.engine)
            left_joined_pokemon = pokemon_data.merge(existing_pokemon, on='name', how='left', indicator=True)
            df = left_joined_pokemon.loc[left_joined_pokemon['_merge'] == 'left_only', 'name']
            new_pokemon = pokemon_data[pokemon_data['name'].isin(df)]
            new_pokemon.to_sql('pokemon', db.engine, if_exists='append', index=False)


        if not User.query.filter_by(email=os.environ["ADMIN_EMAIL"]).first():
            # create new user with the form data. Hash the password so plaintext version isn't saved.
            admin = User(last_name=os.environ['ADMIN_LAST_NAME'], first_name=os.environ['ADMIN_FIRST_NAME'], email=os.environ['ADMIN_EMAIL'], username=os.environ['ADMIN_USERNAME'], password=generate_password_hash(os.environ['ADMIN_PASSWORD'], method='sha256'), role='admin')
            # add the new user to the database
            db.session.add(admin)
            db.session.commit()

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