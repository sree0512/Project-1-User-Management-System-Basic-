import pytest
from conftest import client
from app.schemas.user_schemas import RegisterRequest

@pytest.fixture
def test_user(client):
    # Create fresh user
    client.post("/register", json={
        "username": "tempuser",
        "email": "temp@example.com",
        "password": "pass123"
    })
    login_resp = client.post("/login", json={
        "email": "temp@example.com",
        "password": "pass123"
    })
    token = login_resp.get_json()["access_token"]
    yield token
    # Cleanup: delete user after test
    client.delete("/user/delete", headers={"Authorization": f"Bearer {token}"})


def test_profile(client, test_user):
    headers = {"Authorization": f"Bearer {test_user}"}
    response = client.get("/user/profile", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "temp@example.com"


def test_profile_no_jwt(client):
    response = client.get("/user/profile")
    assert response.status_code == 401


def test_update_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user}"}
    response = client.put("/user/update", headers=headers, json={
        "username": "Updated Name",
        "email": "temp@example.com"
    })
    assert response.status_code == 200

    # Verify DB change
    resp_profile = client.get("/user/profile", headers=headers)
    assert resp_profile.get_json()["username"] == "Updated Name"


def test_change_password(client, test_user):
    headers = {"Authorization": f"Bearer {test_user}"}
    # Change password
    response = client.put("/user/change-password", headers=headers, json={
        "old_password": "pass123",
        "new_password": "newpass123"
    })
    assert response.status_code == 200

    # Login with old password → fail
    resp_old = client.post("/login", json={
        "email": "temp@example.com",
        "password": "pass123"
    })
    assert resp_old.status_code == 401

    # Login with new password → succeed
    resp_new = client.post("/login", json={
        "email": "temp@example.com",
        "password": "newpass123"
    })
    assert resp_new.status_code == 200


def test_delete_user(client, test_user):
    headers = {"Authorization": f"Bearer {test_user}"}
    # Delete user
    response = client.delete("/user/delete", headers=headers)
    assert response.status_code == 200

    # Verify user removed
    resp_profile = client.get("/user/profile", headers=headers)
    assert resp_profile.status_code == 404









"""
Test cases to include:
Access /user/profile without JWT → 401
Access /user/profile with JWT → 200
Update user → 200, verify DB updated
Change password → 200, verify old password fails, new password works
Delete user → 200, verify user removed
Hint: Obtain a JWT token by logging in the test user first, then pass it in headers:
headers = {"Authorization": f"Bearer {token}"}
After /update, fetch user and assert the new username or full_name.
After /change-password, attempt login with old password → 401, new password → 200.
After /delete, attempt /profile → 404.
Isolation
Consider creating a fresh user for each test (via pytest fixture) and cleaning it up afterward to avoid conflicts.
Optional: use pytest.mark.parametrize to test multiple invalid inputs (missing fields, empty strings, wrong types).
"""