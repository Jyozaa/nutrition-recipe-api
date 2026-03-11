from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    instructions: str = Field(min_length=1)

    servings: int = Field(ge=1)
    prep_time_minutes: int = Field(ge=0)
    cook_time_minutes: int = Field(ge=0)

    difficulty_level: str | None = None
    category_id: int | None = None


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class RecipeResponse(RecipeBase):
    id: int

    model_config = {"from_attributes": True}


class RecipeIngredientCreate(BaseModel):
    ingredient_id: int
    quantity_g: float = Field(gt=0)


class RecipeIngredientUpdate(BaseModel):
    quantity_g: float = Field(gt=0)


class RecipeIngredientResponse(BaseModel):
    id: int
    ingredient_id: int
    quantity_g: float

    model_config = {"from_attributes": True}