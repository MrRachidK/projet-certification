from mimetypes import init
import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask_sqlalchemy import SQLAlchemy
import pytest
from flask import template_rendered
from pokemon_app.models import init_db

from pokemon_app import create_app

@pytest.fixture
def app():

    app = create_app('test')
    
    with app.app_context():
        init_db()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()


