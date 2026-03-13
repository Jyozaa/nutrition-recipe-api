# Nutrition and Recipe Analytics API

A database-backed RESTful API built with FastAPI for managing recipes, ingredients, and categories, with analytical endpoints for nutrition, allergens, cost, difficulty, and advanced filtering.

---

## Overview

This API provides a structured backend for storing and analysing recipe data.

It supports:
- CRUD operations for recipes, ingredients, and categories
- many-to-many links between recipes and ingredients
- calculated nutrition summaries based on ingredient quantities
- allergen detection from ingredient flags
- cost estimation
- difficulty estimation
- advanced filtering by diet, allergens, time, calories, and cost

The API uses JSON-based request and response bodies and follows a resource-oriented design.

---

## Features

### Core CRUD functionality
- Recipe CRUD
- Ingredient CRUD
- Category CRUD
- Recipe-to-ingredient link CRUD

### Analytics functionality
- Total nutrition per recipe
- Per-serving nutrition
- Allergen analysis
- Cost estimation
- Difficulty scoring
- Summary analytics:
  - top protein recipes
  - lowest cost recipes
  - recipe counts by category

### Filtering functionality
- Filter by category
- Filter by search term
- Filter by preparation time
- Filter by cooking time
- Filter by difficulty level
- Filter by vegan / vegetarian suitability
- Filter by gluten-free / dairy-free / nut-free status
- Filter by maximum calories
- Filter by maximum cost

### Testing and demo support
- Seed data for realistic demo scenarios
- Automated tests with Pytest
- Interactive API documentation through Swagger UI and ReDoc

---

## Technology Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Pytest**
- **Uvicorn**

---

## API Design

This API uses resource-based endpoints and standard HTTP methods:

- `GET` for retrieval
- `POST` for creation
- `PUT` for updates
- `DELETE` for deletion

Responses are returned in JSON format for easy integration with clients and other services.

---

## Project Structure

```text
nutrition-recipe-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── ingredient.py
│   │   ├── recipe.py
│   │   └── recipe_ingredient.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   ├── category.py
│   │   ├── ingredient.py
│   │   └── recipe.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   ├── categories.py
│   │   ├── ingredients.py
│   │   └── recipes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── allergen_service.py
│   │   ├── cost_service.py
│   │   ├── difficulty_service.py
│   │   └── nutrition_service.py
│   └── seed/
│       ├── sample_data.json
│       └── seed_data.py
├── tests/
│   ├── conftest.py
│   ├── test_analytics.py
│   ├── test_categories.py
│   ├── test_ingredients.py
│   └── test_recipes.py
├── docs/
│   └── api_documentation.pdf
├── report/
├── slides/
├── requirements.txt
├── README.md
└── .gitignore

```

## Data Model Overview

The core relational model consists of four entities:

#### `Category`
Stores recipe categories such as breakfast, lunch, dinner, snack, and dessert.

#### `Ingredient`
Stores ingredient-level nutritional and dietary data, including:
- calories per 100g
- protein per 100g
- carbs per 100g
- fat per 100g
- estimated cost per 100g
- allergen flags
- vegan / vegetarian flags

#### `Recipe`
Stores recipe-level information such as:
- name
- description
- instructions
- servings
- preparation time
- cooking time
- difficulty level
- category

#### `RecipeIngredient`
A junction table linking recipes to ingredients, storing:
- recipe ID
- ingredient ID
- quantity in grams

---

## Setup Instructions

#### 1. Clone the repository

```
git clone https://github.com/Jyozaa/nutrition-recipe-api.git
```
```
cd nutrition-recipe-api
```
#### 2. Create a virtual environment
```
python3 -m venv .venv
```
#### 3. Activate the virtual environment
```
source .venv/bin/activate
```
#### 4. Install dependencies
```
pip install -r requirements.txt
```
#### 5. Run the API
```
uvicorn app.main:app --reload
```
Once the server starts, the API will be available at:
```
Swagger UI: http://127.0.0.1:8000/docs
```
```
ReDoc: http://127.0.0.1:8000/redoc
```

---

## Seeding Demo Data
```
python -m app.seed.seed_data
```

---

## Running Tests
```
pytest
```

## Documentation
Interactive API documentation is available after starting the server:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
#### Additional project documentation can be found in:
- docs/
- report/
- slides/