import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import url_for
from flask import session
from pokemon_app.models import User
from flask_login import current_user
from werkzeug.security import check_password_hash


##################### Test des routes de main #####################

### Test de Index

def test_home(client):
    route = "/home"
    response = client.get(route)
    assert response.status_code == 302

### Test de Profile sans être connecté

def test_profile_not_logged(client):
    route = "/profile"
    # sans login, le profile nous redirige vers le login, on utilise le paramètre follow_redirects pour que la redirection soit effectuée
    response = client.get(route, follow_redirects=True) 
    assert response.status_code == 200 # unauthorize
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # On vérifie qu'on est bien redirigé vers le login
    assert response.request.path == "/login"


