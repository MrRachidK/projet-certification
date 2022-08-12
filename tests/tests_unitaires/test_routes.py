import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import url_for
from flask import session
from pokemon_app.models import User
from flask_login import current_user
from werkzeug.security import check_password_hash
from decouple import config


def _login_user(client, email, password):
    response = client.post(
        "/login", data=dict(email=email, password=password), follow_redirects=True
    )
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("Login User") == -1

def _create_user(client, last_name, first_name, email, username, password):
    response = client.post(
        "/signup", data=dict(last_name=last_name, first_name=first_name, email=email, username=username, password=password), follow_redirects=True
    )
    assert response.status_code == 200

def _logout_user(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200


##################### Test des routes de main #####################

### Test de Index

def test_home(client):
    route = "/home"
    response = client.get(route)
    assert response.status_code == 302

# Test de Login

### Test de Login - GET

def test_login_get(client):
    route = "/login"
    response = client.get(route)
    assert response.status_code == 200
    assert b"Login" in response.data

### Test de Login - POST

def test_login_post_success(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, "test@example.com", "123")

def test_login_post_fail(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    route = "/login"
    response = client.post(route, data=dict(email="test@example.com", password="1234"), follow_redirects=True)
    assert response.status_code == 200
    assert b"Please check your login details and try again." in response.data

def test_login_post_fail_no_user(client):
    route = "/login"
    response = client.post(route, data=dict(email="test@example.com", password="123"), follow_redirects=True)
    assert response.status_code == 200
    assert b"Please check your login details and try again." in response.data

# Test de Signup

### Test de Signup - GET

def test_signup_get(client):
    route = "/signup"
    response = client.get(route)
    assert response.status_code == 200
    assert b"Register" in response.data

### Test de Signup - POST

def test_signup_post_success(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")

def test_signup_post_already_user(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    route = "/signup"
    response = client.post(route, data=dict(last_name="Mister", first_name="T", email="test@example.com", username = "MT", password = '123'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Email address already exists" in response.data

# Test de Logout

### Test de Logout - GET

def test_logout_get(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, "test@example.com", "123")
    route = "/logout"
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"

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

### Test de Profile en étant connecté

def test_profile_logged(client):
    route = "/profile"
    # on crée un utilisateur
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    # on connecte l'utilisateur
    with client.application.app_context():
        _login_user(client, "test@example.com", "123")
        # on vérifie que la page profile est bien accessible
        response = client.get(route)
        assert response.status_code == 200
        assert response.request.path == "/profile"

# Test de Admin en étant connecté

def test_admin_logged(client):
    route = "/admin"
    _login_user(client, config('ADMIN_EMAIL'), config('ADMIN_PASSWORD'))
    response = client.get(route)
    assert response.status_code == 200

# Test de la restriction de l'accès à la page admin

def test_blocked_admin(client):
    route = "/admin"
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, "test@example.com", "123")
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/home"

    
    

    





