import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from flask import url_for
from flask import session
from pokemon_app.models import User
from flask_login import current_user
from werkzeug.security import check_password_hash
import requests
import json


# Fonctions pour la réalisation des tests

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


##################### Tests de l'authentification #####################

# Test de Login

### Test de Login - GET

# Unitaire
def test_login_get(client):
    route = "/login"
    response = client.get(route)
    assert response.status_code == 200
    assert b"Login" in response.data

### Test de Login - POST

# Fonctionnel
def test_login_post_success(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, "test@example.com", "123")

# Fonctionnel
def test_login_post_fail(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    route = "/login"
    response = client.post(route, data=dict(email="test@example.com", password="1234"), follow_redirects=True)
    assert response.status_code == 200
    assert b"Please check your login details and try again." in response.data

# Fonctionnel
def test_login_post_fail_no_user(client):
    route = "/login"
    response = client.post(route, data=dict(email="test@example.com", password="123"), follow_redirects=True)
    assert response.status_code == 200
    assert b"Please check your login details and try again." in response.data

# Test de Signup

### Test de Signup - GET

# Unitaire
def test_signup_get(client):
    route = "/signup"
    response = client.get(route)
    assert response.status_code == 200
    assert b"Register" in response.data

### Test de Signup - POST

# Fonctionnel
def test_signup_post_success(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")

# Fonctionnel
def test_signup_post_already_user(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    route = "/signup"
    response = client.post(route, data=dict(last_name="Mister", first_name="T", email="test@example.com", username = "MT", password = '123'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Email address already exists" in response.data

# Test de Logout

### Test de Logout - GET

# Fonctionnel
def test_logout_get(client):
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, "test@example.com", "123")
    route = "/logout"
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"

##################### Tests des différentes routes de main #####################

### Test de Home - GET

# Home sans être connecté

# Unitaire
def test_home_get_not_logged(client):
    route = "/home"
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"

# Home en étant connecté

# Fonctionnel
def test_home_get(client):
    route = "/home"
    _login_user(client, os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])
    response = client.get(route)
    assert response.status_code == 200
    assert b"Home" in response.data

### Test du choix de mêmes Pokémon - POST

# Fonctionnel
def test_choose_same_pokemon_post(client):
    route = "/home"
    _login_user(client, os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])
    pokemon_data = {'first_pokemon': '1', 'second_pokemon': '1'}
    prediction_text = "Ivysaur"
    prediction_index = 2
    data_to_send = dict(pokemon_data=pokemon_data, prediction_text=prediction_text, prediction_index=prediction_index)
    response = client.post(route, data=data_to_send, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/home"
    
### Test de Home - POST

# Fonctionnel
def test_home_post_logged(client):
    route = "/home"
    _login_user(client, os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])
    pokemon_data = {'first_pokemon': '1', 'second_pokemon': '2'}
    prediction_text = "Ivysaur"
    prediction_index = 2
    data_to_send = dict(pokemon_data=pokemon_data, prediction_text=prediction_text, prediction_index=prediction_index)
    response = client.post(route, data=data_to_send, follow_redirects=True)
    assert response.status_code == 200
    assert b"Ivysaur" in response.data
    
### Test de Result - GET

# Fonctionnel
def test_result_get(client, requests_mock):
    route = "/result"
    url = "http://127.0.0.1:5000/result"
    _login_user(client, os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])
    with client.application.app_context():
        pokemon_data = {"first_pokemon": "1", "second_pokemon": "2"}
        prediction_text = "Ivysaur"
        prediction_index = "2"
        requests_mock.get(url, json={"pokemon_json": pokemon_data, "prediction_text": prediction_text, "prediction_index": prediction_index})
        r = requests.get(url)
        pokemon_json = r.json()["pokemon_json"]
        prediction_text = r.json()["prediction_text"]
        prediction_index = r.json()["prediction_index"]
        
        assert {'first_pokemon': '1', 'second_pokemon': '2'} == pokemon_json
        assert "2" == prediction_index
        assert "Ivysaur" == prediction_text

### Test de Profile sans être connecté

# Unitaire
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

# Fonctionnel
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

# Test de Admin sans être connecté

# Unitaire
def test_admin_not_logged(client):
    route = "/admin"
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"

# Test de Admin en étant connecté

# Fonctionnel
def test_admin_logged(client):
    route = "/admin"
    _login_user(client, os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])
    response = client.get(route)
    assert response.status_code == 200

# Test de la restriction de l'accès à la page admin

# Fonctionnel
def test_blocked_admin(client):
    route = "/admin"
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, "test@example.com", "123")
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/home"

# Test de la modification d'un utilisateur sans être connecté

# Unitaire
def test_update_user_not_logged(client):
    route = "/admin/update_user"
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"

# Test de la modification d'un utilisateur en étant connecté comme non admin

# Fonctionnel
def test_update_user_logged_user(client):
    route = "/admin/update_user"
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, "test@example.com", "123")
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/home"

# Test de la modification d'un utilisateur en étant connecté comme admin - GET

# Fonctionnel
def test_update_user_logged_admin(client):
    route = "/admin/update_user"
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/admin/update_user"

# Test de la modification d'un utilisateur en étant connecté comme admin - POST

# Fonctionnel
def test_update_user_logged_admin_post(client):
    with client.application.app_context():
        _login_user(client, os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])
        user_id = 1
        user = User.find_by_id(user_id)
        first_name = "Toto"
        data_to_send = {"first_name": first_name}
        response = client.post(f"/admin/update_user?user_id={user.id}", data = data_to_send, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/admin"
        assert User.query.filter(User.first_name == "Toto").first()

# Test de la suppression d'un utilisateur sans être connecté

# Unitaire
def test_delete_user_not_logged(client):
    route = "/admin/delete_user"
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"

# Test de la suppression d'un utilisateur en étant connecté comme non admin

# Fonctionnel
def test_delete_user_logged_user(client):
    route = "/admin/delete_user"
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, "test@example.com", "123")
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/home"

# Test de la suppression d'un utilisateur en étant connecté comme admin - GET

# Fonctionnel
def test_delete_user_logged_admin(client):
    route = "/admin/delete_user"
    _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
    _login_user(client, os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])
    response = client.get(route, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/admin/delete_user"

# Test de la suppression d'un utilisateur en étant connecté comme admin - POST

# Fonctionnel
def test_delete_user_logged_admin_post(client):
    with client.application.app_context():
        _create_user(client, "Mister", "T", "test@example.com", "MT", "123")
        _login_user(client, os.environ['ADMIN_EMAIL'], os.environ['ADMIN_PASSWORD'])
        user_id = 2
        user = User.find_by_id(user_id)
        response = client.post(f"/admin/delete_user?user_id={user.id}", follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/admin"
        assert not User.query.filter(User.id == user_id).first()

