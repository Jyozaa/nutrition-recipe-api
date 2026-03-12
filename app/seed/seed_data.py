import json
from pathlib import Path

from app.database import SessionLocal
from app.models.category import Category
from app.models.ingredient import Ingredient


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

    for ingredient_data in data["ingredients"]:
        exists = db.query(Ingredient).filter(
            Ingredient.name == ingredient_data["name"]
        ).first()
        if not exists:
            db.add(Ingredient(**ingredient_data))

    db.commit()
    db.close()
    print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed()