import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
    app.config.from_object('config')

    db = SQLAlchemy()
    db.init_app(app)

    # Connect to log manager with flask login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from pokemon_app import db

    @login_manager.user_loader
    def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
        return db.User.query.get(int(user_id))

    @app.cli.command("init_db")
    def init_db():
        db.init_db()

    # blueprint for auth routes in our app
    from pokemon_app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from pokemon_app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app