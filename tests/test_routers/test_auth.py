import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


#tester la creation d'un compte avec succes puis l'effacer apres le test
def test_create_account_success(cleanup):
    response = client.post("/auth/signup", json={"email": "test_tapha@gmail.com", "password": "test1234"})
    assert response.status_code == 201
    assert "message" in response.json()
    assert "id" in response.json()["message"]


# Tester si un compte existe déja
def test_create_account_conflict(cleanup):
    response = client.post("/auth/signup", json={"email": "test123@example.com", "password": "test1234"})
    assert response.status_code == 409  # Conflict

#tester la connexion avec un user existant
def test_login(cleanup):
    response_create = client.post("/auth/signup", json={"email": "test_tapha@gmail.com", "password": "test1234"})
    assert response_create.status_code == 201

    response_login = client.post("/auth/login", data={"username": "test_tapha@gmail.com", "password": "test1234"})
    assert response_login.status_code == 200
    assert "access_token" in response_login.json()

