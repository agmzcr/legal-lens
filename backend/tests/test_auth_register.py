import pytest

def test_register_success(client):
    payload = {"email": "user@test.com", "password": "secret123"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)

def test_register_duplicate_email(client):
    # Primero creamos el usuario
    payload = {"email": "dup@test.com", "password": "pass"}
    client.post("/auth/register", json=payload)

    # Intentamos de nuevo con el mismo email
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"