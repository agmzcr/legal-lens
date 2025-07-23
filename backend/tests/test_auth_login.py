import pytest

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"

def test_login_success(client):
    # 1. First we register a user
    register_payload = {
        "email": "login@test.com",
        "password": "mypassword"
    }
    resp = client.post(REGISTER_URL, json=register_payload)
    assert resp.status_code == 201, resp.text

    # 2. Now we login with the same credentials
    login_payload = {
        "email": "login@test.com",
        "password": "mypassword"
    }
    resp = client.post(LOGIN_URL, json=login_payload)
    assert resp.status_code == 200, resp.text
    
    data = resp.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)

def test_login_invalid_password(client):
    # 1. We register the user with the correct password
    client.post(REGISTER_URL, json={
        "email": "wrongpass@test.com", 
        "password": "correctpass"
    })

    # 2. Now we try to login with the wrong password
    resp = client.post(LOGIN_URL, json={
        "email": "wrongpass@test.com",
        "password": "badpass"
    })
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"

def test_login_nonexistent_user(client):
    # We never register this email
    resp = client.post(LOGIN_URL, json={
        "email": "noone@test.com",
        "password": "nopass"
    })
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"