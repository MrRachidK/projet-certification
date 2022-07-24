from pokemon_app.models import User

#################  Test de User #################

### Test de json

def test_user_json(client):
    User(last_name = "Mister", first_name = "T", email = "test@example.com", username = "MT", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
    # Get the user from the database
    assert User.find_by_email("test@example.com").user_json() == {'last_name': 'Mister', 'first_name': 'T', 'email': 'test@example.com', 'username': 'MT'}


def test_find_by_email(client):
    User(last_name = "Mister", first_name = "T", email = "test@example.com", username = "MT", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
    assert User.find_by_email("test@example.com").username == "MT"