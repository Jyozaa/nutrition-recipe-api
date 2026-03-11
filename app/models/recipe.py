from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)

    servings = Column(Integer, nullable=False, default=1)
    prep_time_minutes = Column(Integer, nullable=False, default=0)
    cook_time_minutes = Column(Integer, nullable=False, default=0)

    difficulty_level = Column(String(20), nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    category = relationship("Category", back_populates="recipes")
    ingredient_links = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )