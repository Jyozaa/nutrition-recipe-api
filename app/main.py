from fastapi import FastAPI

from app.database import Base, engine
from app.models import Category, Ingredient, Recipe, RecipeIngredient
from app.routers.analytics import router as analytics_router
from app.routers.categories import router as categories_router
from app.routers.ingredients import router as ingredients_router
from app.routers.recipes import router as recipes_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nutrition and Recipe Analytics API",
    description="A database-backed RESTful API for recipes, ingredients, and nutrition analytics.",
    version="1.0.0"
)

app.include_router(categories_router)
app.include_router(ingredients_router)
app.include_router(recipes_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": "Nutrition and Recipe Analytics API is running."
    }