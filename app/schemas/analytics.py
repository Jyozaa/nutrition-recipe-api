from pydantic import BaseModel


class NutritionResponse(BaseModel):
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float
    calories_per_serving: float
    protein_per_serving: float
    carbs_per_serving: float
    fat_per_serving: float


class AllergenResponse(BaseModel):
    contains_gluten: bool
    contains_dairy: bool
    contains_nuts: bool
    contains_soy: bool
    contains_egg: bool
    is_vegan: bool
    is_vegetarian: bool


class CostResponse(BaseModel):
    total_cost: float
    cost_per_serving: float


class DifficultyResponse(BaseModel):
    score: int
    difficulty: str


class RecipeSummaryResponse(BaseModel):
    recipe_id: int
    recipe_name: str
    value: float


class CategoryCountResponse(BaseModel):
    category_name: str
    recipe_count: int