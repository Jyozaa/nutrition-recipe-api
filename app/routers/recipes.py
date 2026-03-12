from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.category import Category
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.recipe import (
    RecipeCreate,
    RecipeDetailIngredient,
    RecipeDetailResponse,
    RecipeIngredientCreate,
    RecipeIngredientResponse,
    RecipeIngredientUpdate,
    RecipeResponse,
    RecipeUpdate,
)

router = APIRouter(prefix="/recipes", tags=["Recipes"])


def build_recipe_detail(recipe: Recipe) -> RecipeDetailResponse:
    return RecipeDetailResponse(
        id=recipe.id,
        name=recipe.name,
        description=recipe.description,
        instructions=recipe.instructions,
        servings=recipe.servings,
        prep_time_minutes=recipe.prep_time_minutes,
        cook_time_minutes=recipe.cook_time_minutes,
        difficulty_level=recipe.difficulty_level,
        category_id=recipe.category_id,
        category_name=recipe.category.name if recipe.category else None,
        ingredients=[
            RecipeDetailIngredient(
                ingredient_id=link.ingredient_id,
                ingredient_name=link.ingredient.name,
                quantity_g=link.quantity_g,
            )
            for link in recipe.ingredient_links
        ],
    )


@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe_data: RecipeCreate, db: Session = Depends(get_db)):
    if recipe_data.category_id is not None:
        category = db.query(Category).filter(
            Category.id == recipe_data.category_id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
            )

    recipe = Recipe(**recipe_data.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.get("/", response_model=list[RecipeResponse])
def list_recipes(
    category_id: int | None = Query(default=None),
    max_prep_time: int | None = Query(default=None, ge=0),
    max_cook_time: int | None = Query(default=None, ge=0),
    difficulty_level: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)

    if category_id is not None:
        query = query.filter(Recipe.category_id == category_id)

    if max_prep_time is not None:
        query = query.filter(Recipe.prep_time_minutes <= max_prep_time)

    if max_cook_time is not None:
        query = query.filter(Recipe.cook_time_minutes <= max_cook_time)

    if difficulty_level:
        query = query.filter(Recipe.difficulty_level.ilike(difficulty_level.strip()))

    if search:
        query = query.filter(Recipe.name.ilike(f"%{search.strip()}%"))

    return query.order_by(Recipe.name.asc()).all()


@router.get("/{recipe_id}", response_model=RecipeDetailResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).options(
        joinedload(Recipe.category),
        joinedload(Recipe.ingredient_links).joinedload(RecipeIngredient.ingredient)
    ).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found."
        )

    return build_recipe_detail(recipe)


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

    if recipe_data.category_id is not None:
        category = db.query(Category).filter(
            Category.id == recipe_data.category_id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found."
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

    existing_link = db.query(RecipeIngredient).filter(
        RecipeIngredient.recipe_id == recipe_id,
        RecipeIngredient.ingredient_id == link_data.ingredient_id
    ).first()
    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This ingredient is already linked to the recipe."
        )

    link = RecipeIngredient(
        recipe_id=recipe_id,
        ingredient_id=link_data.ingredient_id,
        quantity_g=link_data.quantity_g
    )
    db.add(link)
    db.commit()
    db.refresh(link)

    return RecipeIngredientResponse(
        id=link.id,
        recipe_id=link.recipe_id,
        ingredient_id=link.ingredient_id,
        ingredient_name=ingredient.name,
        quantity_g=link.quantity_g
    )


@router.get("/{recipe_id}/ingredients", response_model=list[RecipeIngredientResponse])
def list_recipe_ingredients(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).options(
        joinedload(Recipe.ingredient_links).joinedload(RecipeIngredient.ingredient)
    ).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found."
        )

    return [
        RecipeIngredientResponse(
            id=link.id,
            recipe_id=link.recipe_id,
            ingredient_id=link.ingredient_id,
            ingredient_name=link.ingredient.name,
            quantity_g=link.quantity_g
        )
        for link in recipe.ingredient_links
    ]


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
    link = db.query(RecipeIngredient).options(
        joinedload(RecipeIngredient.ingredient)
    ).filter(
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

    return RecipeIngredientResponse(
        id=link.id,
        recipe_id=link.recipe_id,
        ingredient_id=link.ingredient_id,
        ingredient_name=link.ingredient.name,
        quantity_g=link.quantity_g
    )


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