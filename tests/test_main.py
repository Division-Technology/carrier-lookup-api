from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/api/v1/phone/carrier-lookup")
    assert response.status_code == 405  # Method Not Allowed for GET
