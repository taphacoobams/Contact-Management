import pytest
from fastapi.testclient import TestClient
from main import app
from firebase_admin import auth

client = TestClient(app)

@pytest.fixture
def cleanup(request):
    # Nettoyer la base de données une fois les tests terminés
    def remove_test_users():
        users = auth.list_users().iterate_all()
        for user in users:
            #logique de filtrage pour identifier les utilisateurs de test
            if user.email.startswith("test_"):
                auth.delete_user(user.uid)
    
    # la fonction de nettoyage pour qu'elle soit appelée à la fin des tests
    request.addfinalizer(remove_test_users)
