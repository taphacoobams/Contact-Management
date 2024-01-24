import pytest
from fastapi.testclient import TestClient
from main import app
import httpx
from fastapi.testclient import TestClient
from firebase_admin import auth
from database.firebase import authContact


client = TestClient(app)

#test pour faire un get all sur les contacts
def test_get_all_contacts(cleanup):
    client.post("/auth/signup", json={"email": "test_tapha@gmail.com", "password": "test1234"})
    
    auth_token = authContact.sign_in_with_email_and_password(email="test_tapha@gmail.com", password="test1234")['idToken']
    auth_headers= {"Authorization": f"Bearer {auth_token}"}

    response = client.get("/contacts/", headers=auth_headers)
    assert response.status_code == 200

#test pour ajouter un nouveau contact
def test_add_new_contact(cleanup ):
    client.post("/auth/signup", json={"email": "test_tapha@gmail.com", "password": "test1234"})
    
    #Creation les données du contact
    auth_token = authContact.sign_in_with_email_and_password(email="test_tapha@gmail.com", password="test1234")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
    
    contact_data = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@gmail.com",
        "phone_number": "+33798654321",
        "address": "123 Baker Street London"
    }
    response = client.post("/contacts/", headers=auth_headers, json=contact_data)
    assert response.status_code == 201

#test pour faire un get by id
def test_get_contact_by_id(cleanup ):
    # Créez un utilisateur de test
    client.post("/auth/signup", json={"email": "test_tapha@gmail.com", "password": "test1234"})
    auth_token = authContact.sign_in_with_email_and_password(email="test_tapha@gmail.com", password="test1234")['idToken']
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
      
    # Créez un test_contact pour le test
    contact_data = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@gmail.com",
        "phone_number": "+33798654321",
        "address": "123 Baker Street London"
    }

    # Envoyer la requête POST avec le paramètre json
    response = client.post("/contacts/", headers=auth_headers, json=contact_data)
    assert response.status_code == 201
    contact_id = response.json()["id"]

    # Appelez la fonction get_contact_by_id pour obtenir les détails du contact
    response = client.get(f"/contacts/{contact_id}", headers=auth_headers)
    #requête a réussi (code de statut 200)
    assert response.status_code == 200
    ####----supprimez le contact après ------####
    response = client.delete(f"/contacts/{contact_id}", headers=auth_headers)
    assert response.status_code == 200

