from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_category():
    response = client.post("/categories/", json={"name": "Snacks"})
    assert response.status_code in [201, 400]