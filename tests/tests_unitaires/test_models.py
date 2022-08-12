import sys
import os
from flask import session
from pokemon_app.models import User
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))


#################  Test de User #################

def test_user_json(client):
    with client.application.app_context():
        User(id = 2, last_name = "Mister", first_name = "T", email = "test@example.com", username = "MT", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f', role = 'user').save_to_db()
        # Get the user from the database
        assert User.find_by_email("test@example.com").user_json() == {'id': 2, 'last_name': 'Mister', 'first_name': 'T', 'email': 'test@example.com', 'username': 'MT', 'role': 'user'}

def test_find_by_email(client):
    with client.application.app_context():
        User(last_name = "Mister", first_name = "T", email = "test@example.com", username = "MT", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
        assert User.find_by_email("test@example.com").username == "MT"

def test_find_by_id(client):
    with client.application.app_context():
        User(last_name = "Mister", first_name = "T", email = "test@example.com", username = "MT", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
        assert User.find_by_id(2).username == "MT"

def test_save_to_db(client):
    with client.application.app_context():
        User(last_name = "Mister", first_name = "T", email = "test@example.com", username = "MT", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
        assert User.find_by_email("test@example.com").username == "MT"

def test_delete_from_db(client):
    with client.application.app_context():
        User(last_name = "Mister", first_name = "T", email = "test@example.com", username = "MT", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
        User.find_by_email("test@example.com").delete_from_db()
        assert not User.find_by_email("test@example.com")

    

