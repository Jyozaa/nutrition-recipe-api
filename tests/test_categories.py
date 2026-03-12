def test_create_category(client):
    response = client.post("/categories/", json={"name": "Dinner"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Dinner"
    assert "id" in data


def test_duplicate_category_rejected(client):
    client.post("/categories/", json={"name": "Dinner"})
    response = client.post("/categories/", json={"name": "Dinner"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Category with this name already exists."


def test_get_missing_category_returns_404(client):
    response = client.get("/categories/999")
    assert response.status_code == 404