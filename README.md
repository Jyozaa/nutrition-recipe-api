# Nutrition and Recipe Analytics API

A FastAPI-based web API for managing recipes and ingredients, backed by SQLite, with analytics endpoints for nutrition, allergens, cost, and difficulty.

## Features
- Recipe CRUD
- Ingredient CRUD
- Category CRUD
- Add ingredients to recipes
- Nutrition analytics
- Allergen analysis
- Cost estimates
- Difficulty estimates

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload