from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.recipe import (
    RecipeCreate,
    RecipeIngredientCreate,
    RecipeIngredientResponse,
    RecipeIngredientUpdate,
    RecipeResponse,
    RecipeUpdate,
)

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe_data: RecipeCreate, db: Session = Depends(get_db)):
    recipe = Recipe(**recipe_data.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.get("/", response_model=list[RecipeResponse])
def list_recipes(
    category_id: int | None = Query(default=None),
    max_prep_time: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)

    if category_id is not None:
        query = query.filter(Recipe.category_id == category_id)

    if max_prep_time is not None:
        query = query.filter(Recipe.prep_time_minutes <= max_prep_time)

    return query.all()


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found."
        )
    return recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    recipe_data: RecipeUpdate,
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found."
        )

    for key, value in recipe_data.model_dump().items():
        setattr(recipe, key, value)

    db.commit()
    db.refresh(recipe)
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found."
        )

    db.delete(recipe)
    db.commit()
    return None


@router.post(
    "/{recipe_id}/ingredients",
    response_model=RecipeIngredientResponse,
    status_code=status.HTTP_201_CREATED
)
def add_ingredient_to_recipe(
    recipe_id: int,
    link_data: RecipeIngredientCreate,
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found."
        )

    ingredient = db.query(Ingredient).filter(
        Ingredient.id == link_data.ingredient_id
    ).first()
    if not ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found."
        )

    link = RecipeIngredient(
        recipe_id=recipe_id,
        ingredient_id=link_data.ingredient_id,
        quantity_g=link_data.quantity_g
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.get("/{recipe_id}/ingredients", response_model=list[RecipeIngredientResponse])
def list_recipe_ingredients(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found."
        )

    return recipe.ingredient_links


@router.put(
    "/{recipe_id}/ingredients/{link_id}",
    response_model=RecipeIngredientResponse
)
def update_recipe_ingredient(
    recipe_id: int,
    link_id: int,
    link_data: RecipeIngredientUpdate,
    db: Session = Depends(get_db)
):
    link = db.query(RecipeIngredient).filter(
        RecipeIngredient.id == link_id,
        RecipeIngredient.recipe_id == recipe_id
    ).first()

    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe ingredient link not found."
        )

    link.quantity_g = link_data.quantity_g
    db.commit()
    db.refresh(link)
    return link


@router.delete(
    "/{recipe_id}/ingredients/{link_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_recipe_ingredient(recipe_id: int, link_id: int, db: Session = Depends(get_db)):
    link = db.query(RecipeIngredient).filter(
        RecipeIngredient.id == link_id,
        RecipeIngredient.recipe_id == recipe_id
    ).first()

    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe ingredient link not found."
        )

    db.delete(link)
    db.commit()
    return None