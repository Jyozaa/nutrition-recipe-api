import json
from pathlib import Path

from app.database import SessionLocal
from app.models.category import Category
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient


def seed():
    db = SessionLocal()

    data_path = Path(__file__).parent / "sample_data.json"
    with open(data_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for category_data in data["categories"]:
        exists = db.query(Category).filter(
            Category.name == category_data["name"]
        ).first()
        if not exists:
            db.add(Category(**category_data))

    db.commit()

    for ingredient_data in data["ingredients"]:
        exists = db.query(Ingredient).filter(
            Ingredient.name == ingredient_data["name"]
        ).first()
        if not exists:
            db.add(Ingredient(**ingredient_data))

    db.commit()

    for recipe_data in data["recipes"]:
        existing_recipe = db.query(Recipe).filter(
            Recipe.name == recipe_data["name"]
        ).first()
        if existing_recipe:
            continue

        category = db.query(Category).filter(
            Category.name == recipe_data["category_name"]
        ).first()

        recipe = Recipe(
            name=recipe_data["name"],
            description=recipe_data["description"],
            instructions=recipe_data["instructions"],
            servings=recipe_data["servings"],
            prep_time_minutes=recipe_data["prep_time_minutes"],
            cook_time_minutes=recipe_data["cook_time_minutes"],
            difficulty_level=recipe_data["difficulty_level"],
            category_id=category.id if category else None,
        )

        db.add(recipe)

    db.commit()

    for link_data in data["recipe_ingredients"]:
        recipe = db.query(Recipe).filter(
            Recipe.name == link_data["recipe_name"]
        ).first()
        ingredient = db.query(Ingredient).filter(
            Ingredient.name == link_data["ingredient_name"]
        ).first()

        if not recipe or not ingredient:
            continue

        existing_link = db.query(RecipeIngredient).filter(
            RecipeIngredient.recipe_id == recipe.id,
            RecipeIngredient.ingredient_id == ingredient.id
        ).first()

        if existing_link:
            continue

        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id,
            quantity_g=link_data["quantity_g"]
        )
        db.add(recipe_ingredient)

    db.commit()
    db.close()
    print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed()