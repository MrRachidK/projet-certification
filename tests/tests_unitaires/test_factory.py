from flask import url_for
from flask import session
from pokemon_app.models import User
from flask_login import current_user
from werkzeug.security import check_password_hash

# Test du fonctionnement du client de test

def test_configtest(app):
    print(app.blueprints.keys())
    assert "auth" in app.blueprints
    assert "main" in app.blueprints

    assert app.config["TESTING"] == True