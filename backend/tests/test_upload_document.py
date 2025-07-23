from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_endpoint():
    # First register a test user
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "strongpassword"
    })
    # Then login to get token
    login_resp = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "strongpassword"
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Now open the file and upload with auth header
    with open("tests/sample.pdf", "rb") as f:
        files = {"file": ("sample.pdf", f, "application/pdf")}
        response = client.post("document/upload", files=files, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "clauses" in data
    assert "red_flags" in data
