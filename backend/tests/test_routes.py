from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_endpoint():
    with open("tests/sample.pdf", "rb") as f:
        files = {"file": ("sample.pdf", f, "application/pdf")}
        response = client.post("/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "clauses" in data
    assert "red_flags" in data
