def create_category(client, name="Dinner"):
    response = client.post("/categories/", json={"name": name})
    return response.json()["id"]


def create_ingredient(
    client,
    name,
    calories,
    protein,
    carbs,
    fat,
    cost,
    contains_gluten=False,
    contains_dairy=False,
    contains_nuts=False,
    contains_soy=False,
    contains_egg=False,
    is_vegan=True,
    is_vegetarian=True,
):
    response = client.post(
        "/ingredients/",
        json={
            "name": name,
            "calories_per_100g": calories,
            "protein_per_100g": protein,
            "carbs_per_100g": carbs,
            "fat_per_100g": fat,
            "estimated_cost_per_100g": cost,
            "contains_gluten": contains_gluten,
            "contains_dairy": contains_dairy,
            "contains_nuts": contains_nuts,
            "contains_soy": contains_soy,
            "contains_egg": contains_egg,
            "is_vegan": is_vegan,
            "is_vegetarian": is_vegetarian
        }
    )
    return response.json()["id"]


def create_recipe(
    client,
    name,
    category_id,
    difficulty_level="easy",
    prep_time_minutes=10,
    cook_time_minutes=20,
    servings=2,
):
    response = client.post(
        "/recipes/",
        json={
            "name": name,
            "description": f"{name} description",
            "instructions": "Prepare ingredients. Cook. Serve.",
            "servings": servings,
            "prep_time_minutes": prep_time_minutes,
            "cook_time_minutes": cook_time_minutes,
            "difficulty_level": difficulty_level,
            "category_id": category_id
        }
    )
    return response


def add_ingredient_to_recipe(client, recipe_id, ingredient_id, quantity_g):
    return client.post(
        f"/recipes/{recipe_id}/ingredients",
        json={"ingredient_id": ingredient_id, "quantity_g": quantity_g}
    )


def test_create_recipe(client):
    category_id = create_category(client)
    response = create_recipe(client, "Chicken Rice Bowl", category_id)
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
    recipe_id = create_recipe(client, "Chicken Rice Bowl", category_id).json()["id"]
    ingredient_id = create_ingredient(
        client,
        name="Chicken Breast",
        calories=165,
        protein=31,
        carbs=0,
        fat=3.6,
        cost=1.2,
        is_vegan=False,
        is_vegetarian=False,
    )

    first = add_ingredient_to_recipe(client, recipe_id, ingredient_id, 100)
    assert first.status_code == 201

    second = add_ingredient_to_recipe(client, recipe_id, ingredient_id, 100)
    assert second.status_code == 400
    assert second.json()["detail"] == "This ingredient is already linked to the recipe."


def test_recipe_detail_contains_ingredients(client):
    category_id = create_category(client)
    recipe_id = create_recipe(client, "Chicken Rice Bowl", category_id).json()["id"]
    ingredient_id = create_ingredient(
        client,
        name="Rice",
        calories=130,
        protein=2.7,
        carbs=28,
        fat=0.3,
        cost=0.25,
    )

    add_ingredient_to_recipe(client, recipe_id, ingredient_id, 150)

    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Chicken Rice Bowl"
    assert len(data["ingredients"]) == 1
    assert data["ingredients"][0]["ingredient_name"] == "Rice"


def test_filter_recipes_by_vegan_only(client):
    category_id = create_category(client, "Lunch")

    tofu_id = create_ingredient(
        client,
        name="Tofu",
        calories=76,
        protein=8,
        carbs=1.9,
        fat=4.8,
        cost=0.5,
        contains_soy=True,
        is_vegan=True,
        is_vegetarian=True,
    )
    chicken_id = create_ingredient(
        client,
        name="Chicken Breast",
        calories=165,
        protein=31,
        carbs=0,
        fat=3.6,
        cost=1.2,
        is_vegan=False,
        is_vegetarian=False,
    )

    vegan_recipe_id = create_recipe(client, "Tofu Bowl", category_id).json()["id"]
    non_vegan_recipe_id = create_recipe(client, "Chicken Bowl", category_id).json()["id"]

    add_ingredient_to_recipe(client, vegan_recipe_id, tofu_id, 150)
    add_ingredient_to_recipe(client, non_vegan_recipe_id, chicken_id, 150)

    response = client.get("/recipes/?vegan_only=true")
    assert response.status_code == 200

    recipe_names = [recipe["name"] for recipe in response.json()]
    assert "Tofu Bowl" in recipe_names
    assert "Chicken Bowl" not in recipe_names


def test_filter_recipes_by_gluten_free_only(client):
    category_id = create_category(client, "Breakfast")

    bread_id = create_ingredient(
        client,
        name="Bread",
        calories=265,
        protein=9,
        carbs=49,
        fat=3.2,
        cost=0.2,
        contains_gluten=True,
    )
    rice_id = create_ingredient(
        client,
        name="Rice",
        calories=130,
        protein=2.7,
        carbs=28,
        fat=0.3,
        cost=0.25,
        contains_gluten=False,
    )

    toast_recipe_id = create_recipe(client, "Toast Plate", category_id).json()["id"]
    rice_recipe_id = create_recipe(client, "Rice Plate", category_id).json()["id"]

    add_ingredient_to_recipe(client, toast_recipe_id, bread_id, 80)
    add_ingredient_to_recipe(client, rice_recipe_id, rice_id, 150)

    response = client.get("/recipes/?gluten_free_only=true")
    assert response.status_code == 200

    recipe_names = [recipe["name"] for recipe in response.json()]
    assert "Rice Plate" in recipe_names
    assert "Toast Plate" not in recipe_names


def test_filter_recipes_by_max_calories(client):
    category_id = create_category(client, "Dinner")

    olive_oil_id = create_ingredient(
        client,
        name="Olive Oil",
        calories=884,
        protein=0,
        carbs=0,
        fat=100,
        cost=0.6,
    )
    lettuce_id = create_ingredient(
        client,
        name="Lettuce",
        calories=15,
        protein=1.4,
        carbs=2.9,
        fat=0.2,
        cost=0.18,
    )

    high_cal_recipe_id = create_recipe(client, "Oil Plate", category_id, servings=1).json()["id"]
    low_cal_recipe_id = create_recipe(client, "Lettuce Plate", category_id, servings=1).json()["id"]

    add_ingredient_to_recipe(client, high_cal_recipe_id, olive_oil_id, 100)
    add_ingredient_to_recipe(client, low_cal_recipe_id, lettuce_id, 100)

    response = client.get("/recipes/?max_calories=100")
    assert response.status_code == 200

    recipe_names = [recipe["name"] for recipe in response.json()]
    assert "Lettuce Plate" in recipe_names
    assert "Oil Plate" not in recipe_names


def test_filter_recipes_by_max_cost(client):
    category_id = create_category(client, "Dinner")

    salmon_id = create_ingredient(
        client,
        name="Salmon",
        calories=208,
        protein=20,
        carbs=0,
        fat=13,
        cost=1.8,
        is_vegan=False,
        is_vegetarian=False,
    )
    potato_id = create_ingredient(
        client,
        name="Potato",
        calories=77,
        protein=2,
        carbs=17,
        fat=0.1,
        cost=0.18,
    )

    expensive_recipe_id = create_recipe(client, "Salmon Plate", category_id, servings=1).json()["id"]
    cheap_recipe_id = create_recipe(client, "Potato Plate", category_id, servings=1).json()["id"]

    add_ingredient_to_recipe(client, expensive_recipe_id, salmon_id, 100)
    add_ingredient_to_recipe(client, cheap_recipe_id, potato_id, 100)

    response = client.get("/recipes/?max_cost=0.50")
    assert response.status_code == 200

    recipe_names = [recipe["name"] for recipe in response.json()]
    assert "Potato Plate" in recipe_names
    assert "Salmon Plate" not in recipe_names