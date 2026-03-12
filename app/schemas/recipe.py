from pydantic import BaseModel, Field, field_validator


class RecipeBase(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    instructions: str = Field(min_length=1)

    servings: int = Field(ge=1)
    prep_time_minutes: int = Field(ge=0)
    cook_time_minutes: int = Field(ge=0)

    difficulty_level: str | None = None
    category_id: int | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Recipe name cannot be empty.")
        return cleaned

    @field_validator("instructions")
    @classmethod
    def validate_instructions(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Instructions cannot be empty.")
        return cleaned


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
    recipe_id: int
    ingredient_id: int
    ingredient_name: str
    quantity_g: float

    model_config = {"from_attributes": True}


class RecipeDetailIngredient(BaseModel):
    ingredient_id: int
    ingredient_name: str
    quantity_g: float


class RecipeDetailResponse(BaseModel):
    id: int
    name: str
    description: str | None
    instructions: str
    servings: int
    prep_time_minutes: int
    cook_time_minutes: int
    difficulty_level: str | None
    category_id: int | None
    category_name: str | None
    ingredients: list[RecipeDetailIngredient]