from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.analytics import (
    AllergenResponse,
    CategoryCountResponse,
    CostResponse,
    DifficultyResponse,
    NutritionResponse,
    RecipeSummaryResponse,
)
from app.services.allergen_service import calculate_recipe_allergens
from app.services.cost_service import calculate_recipe_cost
from app.services.difficulty_service import calculate_recipe_difficulty
from app.services.nutrition_service import calculate_recipe_nutrition

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_recipe_or_404(recipe_id: int, db: Session):
    recipe = db.query(Recipe).options(
        joinedload(Recipe.category),
        joinedload(Recipe.ingredient_links).joinedload(RecipeIngredient.ingredient)
    ).filter(Recipe.id == recipe_id).first()

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


@router.get("/recipes/top-protein", response_model=list[RecipeSummaryResponse])
def top_protein_recipes(
    limit: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    recipes = db.query(Recipe).options(
        joinedload(Recipe.ingredient_links).joinedload(RecipeIngredient.ingredient)
    ).all()

    summaries = []
    for recipe in recipes:
        nutrition = calculate_recipe_nutrition(recipe)
        summaries.append(
            RecipeSummaryResponse(
                recipe_id=recipe.id,
                recipe_name=recipe.name,
                value=nutrition["total_protein"]
            )
        )

    summaries.sort(key=lambda item: item.value, reverse=True)
    return summaries[:limit]


@router.get("/recipes/lowest-cost", response_model=list[RecipeSummaryResponse])
def lowest_cost_recipes(
    limit: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    recipes = db.query(Recipe).options(
        joinedload(Recipe.ingredient_links).joinedload(RecipeIngredient.ingredient)
    ).all()

    summaries = []
    for recipe in recipes:
        cost = calculate_recipe_cost(recipe)
        summaries.append(
            RecipeSummaryResponse(
                recipe_id=recipe.id,
                recipe_name=recipe.name,
                value=cost["total_cost"]
            )
        )

    summaries.sort(key=lambda item: item.value)
    return summaries[:limit]


@router.get("/recipes/by-category", response_model=list[CategoryCountResponse])
def recipe_count_by_category(db: Session = Depends(get_db)):
    recipes = db.query(Recipe).options(joinedload(Recipe.category)).all()

    counts = {}
    for recipe in recipes:
        category_name = recipe.category.name if recipe.category else "Uncategorised"
        counts[category_name] = counts.get(category_name, 0) + 1

    return [
        CategoryCountResponse(category_name=name, recipe_count=count)
        for name, count in sorted(counts.items())
    ]