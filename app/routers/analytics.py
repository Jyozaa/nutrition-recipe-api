from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.recipe import Recipe
from app.schemas.analytics import (
    AllergenResponse,
    CostResponse,
    DifficultyResponse,
    NutritionResponse,
)
from app.services.allergen_service import calculate_recipe_allergens
from app.services.cost_service import calculate_recipe_cost
from app.services.difficulty_service import calculate_recipe_difficulty
from app.services.nutrition_service import calculate_recipe_nutrition

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_recipe_or_404(recipe_id: int, db: Session):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    return recipe


@router.get("/recipes/{recipe_id}/nutrition", response_model=NutritionResponse)
def get_recipe_nutrition(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_recipe_or_404(recipe_id, db)
    return calculate_recipe_nutrition(recipe)


@router.get("/recipes/{recipe_id}/allergens", response_model=AllergenResponse)
def get_recipe_allergens(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_recipe_or_404(recipe_id, db)
    return calculate_recipe_allergens(recipe)


@router.get("/recipes/{recipe_id}/cost", response_model=CostResponse)
def get_recipe_cost(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_recipe_or_404(recipe_id, db)
    return calculate_recipe_cost(recipe)


@router.get("/recipes/{recipe_id}/difficulty", response_model=DifficultyResponse)
def get_recipe_difficulty(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_recipe_or_404(recipe_id, db)
    return calculate_recipe_difficulty(recipe)