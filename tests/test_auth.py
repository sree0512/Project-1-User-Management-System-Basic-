import pytest
from conftest import client

@pytest.mark.parametrize("payload,expected_status", [
    ({"username": "", "email": "a@b.com", "password": "pass"}, 400),
    ({"username": "user", "email": "", "password": "pass"}, 400),
    ({"username": "user", "email": "a@b.com", "password": ""}, 400),
])
def test_register_invalid(client, payload, expected_status):
    response = client.post("/register", json=payload)
    assert response.status_code == expected_status

def test_register_and_login(client):
    # Register new user
    response = client.post("/register", json={
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "pass123"
    })
    assert response.status_code == 201

    # Duplicate registration
    response_dup = client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "pass123"
    })
    assert response_dup.status_code == 400
    
    # Missing  fields 
    response = client.post("/register", json ={
        "username": "test3",
        "email": "",
        "password": "pass123"
    })
    assert response.status_code == 400

    # Login success
    response_login = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "pass123"
    })
    assert response_login.status_code == 200
    token = response_login.get_json()["access_token"]

    # Login wrong password
    response_wrong = client.post("/login", json={
        "email": "testuser@example.com",
        "password": "wrongpass"
    })
    assert response_wrong.status_code == 401

    


"""
Use the client fixture from conftest.py.
Test cases to include:
Successful registration → 201
Registration with duplicate email → 400
Registration with missing fields → 400
Successful login → 200
Login with wrong password → 401
Login with non-existent user → 401
Hint: Use client.post("/auth/register", json=...) and client.post("/auth/login", json=...).
"""