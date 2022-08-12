import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask_sqlalchemy import SQLAlchemy
import pytest
from flask import template_rendered

from pokemon_app import create_app, init_db

@pytest.fixture
def app():

    app = create_app('test')
    
    with app.app_context():
        init_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
