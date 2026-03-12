def create_category(client):
    response = client.post("/categories/", json={"name": "Dinner"})
    return response.json()["id"]


def create_ingredient(client, name="Chicken Breast"):
    response = client.post(
        "/ingredients/",
        json={
            "name": name,
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
    )
    return response.json()["id"]


def create_recipe(client, category_id):
    response = client.post(
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
    )
    return response


def test_create_recipe(client):
    category_id = create_category(client)
    response = create_recipe(client, category_id)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Chicken Rice Bowl"


def test_create_recipe_with_invalid_category(client):
    response = client.post(
        "/recipes/",
        json={
            "name": "Invalid Recipe",
            "description": "Bad category",
            "instructions": "Do something.",
            "servings": 1,
            "prep_time_minutes": 5,
            "cook_time_minutes": 5,
            "difficulty_level": "easy",
            "category_id": 999
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."


def test_add_duplicate_recipe_ingredient_rejected(client):
    category_id = create_category(client)
    recipe_id = create_recipe(client, category_id).json()["id"]
    ingredient_id = create_ingredient(client)

    first = client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": ingredient_id, "quantity_g": 100}
    )
    assert first.status_code == 201

    second = client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": ingredient_id, "quantity_g": 100}
    )
    assert second.status_code == 400
    assert second.json()["detail"] == "This ingredient is already linked to the recipe."


def test_recipe_detail_contains_ingredients(client):
    category_id = create_category(client)
    recipe_id = create_recipe(client, category_id).json()["id"]
    ingredient_id = create_ingredient(client, "Rice")

    client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": ingredient_id, "quantity_g": 150}
    )

    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Chicken Rice Bowl"
    assert len(data["ingredients"]) == 1
    assert data["ingredients"][0]["ingredient_name"] == "Rice"