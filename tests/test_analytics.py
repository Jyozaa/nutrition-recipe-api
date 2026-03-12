def setup_recipe_with_ingredients(client):
    category_id = client.post("/categories/", json={"name": "Dinner"}).json()["id"]

    chicken_id = client.post(
        "/ingredients/",
        json={
            "name": "Chicken Breast",
            "calories_per_100g": 165,
            "protein_per_100g": 31,
            "carbs_per_100g": 0,
            "fat_per_100g": 3.6,
            "estimated_cost_per_100g": 1.2,
            "contains_gluten": False,
            "contains_dairy": False,
            "contains_nuts": False,
            "contains_soy": False,
            "contains_egg": False,
            "is_vegan": False,
            "is_vegetarian": False
        }
    ).json()["id"]

    rice_id = client.post(
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
    ).json()["id"]

    recipe_id = client.post(
        "/recipes/",
        json={
            "name": "Chicken Rice Bowl",
            "description": "Simple bowl",
            "instructions": "Cook rice. Grill chicken. Serve.",
            "servings": 2,
            "prep_time_minutes": 10,
            "cook_time_minutes": 20,
            "difficulty_level": "easy",
            "category_id": category_id
        }
    ).json()["id"]

    client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": chicken_id, "quantity_g": 200}
    )
    client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": rice_id, "quantity_g": 150}
    )

    return recipe_id


def test_recipe_nutrition_endpoint(client):
    recipe_id = setup_recipe_with_ingredients(client)
    response = client.get(f"/analytics/recipes/{recipe_id}/nutrition")
    assert response.status_code == 200
    data = response.json()
    assert data["total_calories"] > 0
    assert data["total_protein"] > 0


def test_recipe_cost_endpoint(client):
    recipe_id = setup_recipe_with_ingredients(client)
    response = client.get(f"/analytics/recipes/{recipe_id}/cost")
    assert response.status_code == 200
    data = response.json()
    assert data["total_cost"] > 0


def test_recipe_allergens_endpoint(client):
    recipe_id = setup_recipe_with_ingredients(client)
    response = client.get(f"/analytics/recipes/{recipe_id}/allergens")
    assert response.status_code == 200
    data = response.json()
    assert data["contains_gluten"] is False


def test_top_protein_endpoint(client):
    setup_recipe_with_ingredients(client)
    response = client.get("/analytics/recipes/top-protein")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "recipe_name" in data[0]