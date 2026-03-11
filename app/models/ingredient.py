from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    calories_per_100g = Column(Float, nullable=False, default=0.0)
    protein_per_100g = Column(Float, nullable=False, default=0.0)
    carbs_per_100g = Column(Float, nullable=False, default=0.0)
    fat_per_100g = Column(Float, nullable=False, default=0.0)

    estimated_cost_per_100g = Column(Float, nullable=False, default=0.0)

    contains_gluten = Column(Boolean, nullable=False, default=False)
    contains_dairy = Column(Boolean, nullable=False, default=False)
    contains_nuts = Column(Boolean, nullable=False, default=False)
    contains_soy = Column(Boolean, nullable=False, default=False)
    contains_egg = Column(Boolean, nullable=False, default=False)

    is_vegan = Column(Boolean, nullable=False, default=False)
    is_vegetarian = Column(Boolean, nullable=False, default=False)

    recipe_links = relationship("RecipeIngredient", back_populates="ingredient")