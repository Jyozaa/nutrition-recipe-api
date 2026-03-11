from pydantic import BaseModel, Field


class IngredientBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    calories_per_100g: float = 0.0
    protein_per_100g: float = 0.0
    carbs_per_100g: float = 0.0
    fat_per_100g: float = 0.0

    estimated_cost_per_100g: float = 0.0

    contains_gluten: bool = False
    contains_dairy: bool = False
    contains_nuts: bool = False
    contains_soy: bool = False
    contains_egg: bool = False

    is_vegan: bool = False
    is_vegetarian: bool = False


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass


class IngredientResponse(IngredientBase):
    id: int

    model_config = {"from_attributes": True}