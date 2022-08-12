from pokemon_app.models import User

#def test_profile_template_context(client, captured_templates):
#    with client.application.app_context():
#        User(last_name = "Mister", first_name = "T", email = "test@example.com", username = "MT", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
#        client.get('/profile')
#        template, context = captured_templates[0]
#        assert template.name == 'profile.html'
#        assert context['user'].username == 'MT'
#        assert context['user'].email == 'test@example.com'
#        assert context['user'].first_name == 'T'
#        assert context['user'].last_name == 'Mister'
#        assert context['user'].id == 1

# def test_profile_template_context_no_user(client, captured_templates):
#    with client.application.app_context():
#        client.get('/profile')
#        template, context = captured_templates[0]
#        assert template.name == 'profile.html'
#        assert context['user'] == None