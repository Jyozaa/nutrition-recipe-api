def test_create_ingredient(client):
    response = client.post(
        "/ingredients/",
        json={
            "name": "Rice",
            "calories_per_100g": 130,
            "protein_per_100g": 2.7,
            "carbs_per_100g": 28,
            "fat_per_100g": 0.3,
            "estimated_cost_per_100g": 0.25,
            "contains_gluten": False,
            "contains_dairy": False,
            "contains_nuts": False,
            "contains_soy": False,
            "contains_egg": False,
            "is_vegan": True,
            "is_vegetarian": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Rice"


def test_negative_nutrition_rejected(client):
    response = client.post(
        "/ingredients/",
        json={
            "name": "Bad Ingredient",
            "calories_per_100g": -1,
            "protein_per_100g": 0,
            "carbs_per_100g": 0,
            "fat_per_100g": 0,
            "estimated_cost_per_100g": 0,
            "contains_gluten": False,
            "contains_dairy": False,
            "contains_nuts": False,
            "contains_soy": False,
            "contains_egg": False,
            "is_vegan": True,
            "is_vegetarian": True
        }
    )
    assert response.status_code == 422