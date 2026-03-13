# Nutrition and Recipe Analytics API Documentation

## 1. Overview

The Nutrition and Recipe Analytics API is a database-backed RESTful API built with FastAPI for managing recipes, ingredients, and categories, while also providing analytical functionality such as nutrition summaries, allergen analysis, cost estimation, difficulty scoring, and advanced recipe filtering.

The API follows a resource-oriented design and uses JSON for request and response bodies.

### Base URL
Local development:

`http://127.0.0.1:8000`

### Interactive Documentation
- Swagger UI: `/docs`
- ReDoc: `/redoc`

### Content Type
All request and response bodies use JSON unless otherwise stated.

---

## 2. Authentication

This version of the API does **not** implement authentication.

All endpoints are currently publicly accessible in the local coursework version.

---

## 3. Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Request successful |
| 201 | Resource created successfully |
| 204 | Resource deleted successfully, no response body |
| 400 | Bad request / business rule violation |
| 404 | Resource not found |
| 422 | Validation error in request body or parameters |

---

## 4. Data Model Summary

### Category
Represents a recipe category such as breakfast, lunch, dinner, snack, or dessert.

Fields:
- `id`
- `name`

### Ingredient
Represents ingredient-level nutritional, dietary, and allergen data.

Fields:
- `id`
- `name`
- `calories_per_100g`
- `protein_per_100g`
- `carbs_per_100g`
- `fat_per_100g`
- `estimated_cost_per_100g`
- `contains_gluten`
- `contains_dairy`
- `contains_nuts`
- `contains_soy`
- `contains_egg`
- `is_vegan`
- `is_vegetarian`

### Recipe
Represents a recipe and its high-level details.

Fields:
- `id`
- `name`
- `description`
- `instructions`
- `servings`
- `prep_time_minutes`
- `cook_time_minutes`
- `difficulty_level`
- `category_id`

### RecipeIngredient
Represents the many-to-many relationship between recipes and ingredients, including quantity in grams.

Fields:
- `id`
- `recipe_id`
- `ingredient_id`
- `quantity_g`

---

## 5. Endpoints

# 5.1 Categories

## GET `/categories/`
Returns all categories.

### Response
**200 OK**
```json
[
  {
    "id": 1,
    "name": "Breakfast"
  },
  {
    "id": 2,
    "name": "Lunch"
  }
]
```

## POST `/categories/`
Creates a new category.

### Request Body
```json
{
  "name": "Dinner"
}
```
### Responses
**201 Created**
```json
{
  "id": 3,
  "name": "Dinner"
}
```
**400 Bad request**
```json
{
  "detail": "Category with this name already exists."
}
```
**422 Unprocessable Entity**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "name"],
      "msg": "Value error, Category name cannot be empty.",
      "input": "   "
    }
  ]
}
```

## GET `/categories/{category_id}`
Returns one category by ID.

### Responses
**200 OK**
```json
[
  {
    "id": 1,
    "name": "Breakfast"
  }
]
```
**404 Not Found**
```json
{
  "detail": "Category not found."
}
```

## PUT `/categories/{category_id}`
Updates an existing category.
#### Path parameters
- category_id (integer)
### Request Body
```json
{
  "name": "Brunch"
}
```
### Responses
**200 OK**
```json
{
  "name": "Brunch"
}
```
**400 Bad Request**
```json
{
  "detail": "Another category with this name already exists."
}
```
**404 Not Found**
```json
{
  "detail": "Category not found."
}
```

## DELETE `/categories/{category_id}`
Deletes a category.
#### Path parameters
- category_id (integer)

### Responses

**204 No content**

**400 Bad Request**
```json
{
  "detail": "Cannot delete category because recipes are still assigned to it."
}
```
**404 Not Found**
```json
{
  "detail": "Category not found."
}
```

# 5.2 ingredients

## GET `Ingredients`
Returns all ingredients.
#### Optional Query Parameters
- search (string)
- vegan_only (boolean)
#### Example
```
GET /ingredients/?search=rice
```
### Response
**200 OK**
```json
[
  {
    "id": 1,
    "name": "Rice",
    "calories_per_100g": 130.0,
    "protein_per_100g": 2.7,
    "carbs_per_100g": 28.0,
    "fat_per_100g": 0.3,
    "estimated_cost_per_100g": 0.25,
    "contains_gluten": false,
    "contains_dairy": false,
    "contains_nuts": false,
    "contains_soy": false,
    "contains_egg": false,
    "is_vegan": true,
    "is_vegetarian": true
  }
]
```
## POST `Ingredients`
Creates a new ingredient
#### Request Body
```json
{
  "name": "Rice",
  "calories_per_100g": 130,
  "protein_per_100g": 2.7,
  "carbs_per_100g": 28,
  "fat_per_100g": 0.3,
  "estimated_cost_per_100g": 0.25,
  "contains_gluten": false,
  "contains_dairy": false,
  "contains_nuts": false,
  "contains_soy": false,
  "contains_egg": false,
  "is_vegan": true,
  "is_vegetarian": true
}
```
### Responses
**201 Created**
```json
{
  "id": 5,
  "name": "Rice",
  "calories_per_100g": 130.0,
  "protein_per_100g": 2.7,
  "carbs_per_100g": 28.0,
  "fat_per_100g": 0.3,
  "estimated_cost_per_100g": 0.25,
  "contains_gluten": false,
  "contains_dairy": false,
  "contains_nuts": false,
  "contains_soy": false,
  "contains_egg": false,
  "is_vegan": true,
  "is_vegetarian": true
}
```
**400 Bad Request**
```json
{
  "detail": "Ingredient with this name already exists."
}
```
**422 Unprocessable Entity**
```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["body", "calories_per_100g"],
      "msg": "Input should be greater than or equal to 0",
      "input": -1
    }
  ]
}
```

## GET `/ingredients/{ingredient_id}`
Returns one ingredient by ID.
#### Path Parameters
- ingredient_id (integer)
### Responses
**200 OK**
```json
{
  "id": 1,
  "name": "Rice",
  "calories_per_100g": 130.0,
  "protein_per_100g": 2.7,
  "carbs_per_100g": 28.0,
  "fat_per_100g": 0.3,
  "estimated_cost_per_100g": 0.25,
  "contains_gluten": false,
  "contains_dairy": false,
  "contains_nuts": false,
  "contains_soy": false,
  "contains_egg": false,
  "is_vegan": true,
  "is_vegetarian": true
}
```
**404 Not Found**
```json
{
  "detail": "Ingredient not found."
}
```

## PUT `/ingredients/{ingredient_id}`
Updates an ingredient
#### Path parameters
- ingredient_id (integer)
#### Request Body
Use the same schema as ingredient creation.
### Responses
**200 OK**
Returns the updated ingredient.
**400 Bad Request**
```json
{
  "detail": "Another ingredient with this name already exists."
}
```
**404 Not Found**
```json
{
  "detail": "Ingredient not found."
}
```

## DELETE `/ingredients/{ingredient_id}`
Deletes an ingredient
#### Path parameters
- ingredient_id (integer)
#### Request Body
Use the same schema as ingredient creation.
### Responses
**204 No content**

**400 Bad Request**
```json
{
  "detail": "Cannot delete ingredient because it is used by one or more recipes."
}
```
**404 Not Found**
```json
{
  "detail": "Ingredient not found."
}
```

# 5.3 Recipes
#### GET /recipes/
Returns all recipes, with optional filtering.
#### Optional Query Parameters
- category_id (integer)
- max_prep_time (integer)
- max_cook_time (integer)
- difficulty_level (string)
- search (string)
- vegan_only (boolean)
- vegetarian_only (boolean)
- gluten_free_only (boolean)
- dairy_free_only (boolean)
- nut_free_only (boolean)
- max_calories (number)
- max_cost (number)

#### Example Requests
- GET /recipes/?search=bowl
- GET /recipes/?vegan_only=true
- GET /recipes/?gluten_free_only=true&max_calories=500
- GET /recipes/?category_id=1&max_prep_time=10

### Responses
**200 OK**
```json
[
  {
    "id": 1,
    "name": "Chicken Rice Bowl",
    "description": "Simple grilled chicken served with rice.",
    "instructions": "Cook the rice. Grill the chicken. Serve together.",
    "servings": 2,
    "prep_time_minutes": 10,
    "cook_time_minutes": 20,
    "difficulty_level": "easy",
    "category_id": 2
  }
]
```

## POST `/recipes/`
Creates a recipe
#### Request Body
```json
{
  "name": "Chicken Rice Bowl",
  "description": "Simple grilled chicken served with rice.",
  "instructions": "Cook the rice. Grill the chicken. Serve together.",
  "servings": 2,
  "prep_time_minutes": 10,
  "cook_time_minutes": 20,
  "difficulty_level": "easy",
  "category_id": 2
}
```
### Responses
**201 Created**
```json
{
  "id": 1,
  "name": "Chicken Rice Bowl",
  "description": "Simple grilled chicken served with rice.",
  "instructions": "Cook the rice. Grill the chicken. Serve together.",
  "servings": 2,
  "prep_time_minutes": 10,
  "cook_time_minutes": 20,
  "difficulty_level": "easy",
  "category_id": 2
}
```
**404 Not Found**
```json
{
  "detail": "Category not found."
}
```
**422 Unprocessable Entity**
```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["body", "servings"],
      "msg": "Input should be greater than or equal to 1",
      "input": 0
    }
  ]
}
```

## GET `/recipes/{recipe_id}`
Returns a detailed recipe view.
#### Path Parameters
- recipe_id (integer)
### Responses
**200 OK**
```json
{
  "id": 1,
  "name": "Chicken Rice Bowl",
  "description": "Simple grilled chicken served with rice.",
  "instructions": "Cook the rice. Grill the chicken. Serve together.",
  "servings": 2,
  "prep_time_minutes": 10,
  "cook_time_minutes": 20,
  "difficulty_level": "easy",
  "category_id": 2,
  "category_name": "Lunch",
  "ingredients": [
    {
      "ingredient_id": 1,
      "ingredient_name": "Chicken Breast",
      "quantity_g": 200.0
    },
    {
      "ingredient_id": 2,
      "ingredient_name": "Rice",
      "quantity_g": 150.0
    }
  ]
}
```
**404 Not Found**
```json
{
  "detail": "Recipe not found."
}
```

## PUT `/recipes/{recipe_id}`
Updates a recipe.
#### Path Parameters
- recipe_id (integer)
### Responses
**200 OK**
Returns the updated recipe.
**404 Not Found**
```json
{
  "detail": "Recipe not found."
}
```

## DELETE `/recipes/{recipe_id}`
Deletes a recipe.
#### Path Parameters
- recipe_id (integer)
### Responses
**204 No content**
**404 Not Found**
```json
{
  "detail": "Recipe not found."
}
```

# 5.4 Recipe Ingredient Links
## POST `/recipes/{recipe_id}/ingredients`
Adds an ingredient to a recipe.
#### Path parameters
- recipe_id (integer)
#### Request Body
```json
{
  "ingredient_id": 2,
  "quantity_g": 150
}
```
### Responses
**201 Created**
```json
{
  "id": 1,
  "recipe_id": 1,
  "ingredient_id": 2,
  "ingredient_name": "Rice",
  "quantity_g": 150.0
}
```
**400 Bad Request**
```json
{
  "detail": "This ingredient is already linked to the recipe."
}
```
**404 Not Found**
```json
{
  "detail": "Recipe not found."
}
```

## GET `/recipes/{recipe_id}/ingredients`
Returns all ingredients linked to a recipe.
#### Path parameters
- recipe_id (integer)

### Responses
**200 OK**
```json
[
  {
    "id": 1,
    "recipe_id": 1,
    "ingredient_id": 2,
    "ingredient_name": "Rice",
    "quantity_g": 150.0
  }
]
```
**404 Not Found**
```json
{
  "detail": "Recipe not found."
}
```

## PUT `/recipes/{recipe_id}/ingredients/{link_id}`
Updates the quantity of a linked ingredient.
#### Path parameters
- recipe_id (integer)
- link_id (integer)
#### Request Body
```json
{
  "quantity_g": 200
}
```
### Responses
**200 OK**
```json
{
  "id": 1,
  "recipe_id": 1,
  "ingredient_id": 2,
  "ingredient_name": "Rice",
  "quantity_g": 200.0
}
```
**404 Not Found**
```json
{
  "detail": "Recipe ingredient link not found."
}
```

## DELETE `/recipes/{recipe_id}/ingredients/{link_id}`
Deletes a recipe-ingredient link.
#### Path parameters
- recipe_id (integer)
- link_id (integer)
### Responses
**204 No Content**
**404 Not Found**
```json
{
  "detail": "Recipe ingredient link not found."
}
```

# 5.5 Analytics
## GET `/analytics/recipes/{recipe_id}/nutrition`
Returns total and per-serving nutritional values.

### Responses
**200 OK**
```json
{
  "total_calories": 525.0,
  "total_protein": 66.05,
  "total_carbs": 42.0,
  "total_fat": 7.65,
  "calories_per_serving": 262.5,
  "protein_per_serving": 33.03,
  "carbs_per_serving": 21.0,
  "fat_per_serving": 3.83
}
```
**404 Not Found**
```json
{
  "detail": "Recipe not found."
}
```

## GET `/analytics/recipes/{recipe_id}/allergens`
Returns allergen and dietary suitability data.

### Response
**200 OK**
```json
{
  "contains_gluten": false,
  "contains_dairy": false,
  "contains_nuts": false,
  "contains_soy": false,
  "contains_egg": false,
  "is_vegan": false,
  "is_vegetarian": false
}
```

## GET `/analytics/recipes/{recipe_id}/cost`
Returns cost estimates.

### Response
**200 OK**
```json
{
  "total_cost": 2.78,
  "cost_per_serving": 1.39
}
```

## GET `/analytics/recipes/{recipe_id}/difficulty`
Returns difficulty scoring output.

### Response
**200 OK**
```json
{
  "score": 1,
  "difficulty": "easy"
}
```

## GET `/analytics/recipes/top-protein`
Returns the top protein recipes.

#### Optional Query Parameters
- limit (integer, default 5, minimum 1, maximum 20)

### Response
**200 OK**
```json
[
  {
    "recipe_id": 1,
    "recipe_name": "Chicken Rice Bowl",
    "value": 66.05
  },
  {
    "recipe_id": 9,
    "recipe_name": "Chicken Pasta Plate",
    "value": 64.7
  }
]
```

## GET `/analytics/recipes/lowest-cost`
Returns difficulty scoring output.

#### Optional Query Parameters
- limit (integer, default 5, minimum 1, maximum 20)

### Response
**200 OK**
```json
[
  {
    "recipe_id": 7,
    "recipe_name": "Yogurt Berry Cup",
    "value": 1.26
  },
  {
    "recipe_id": 3,
    "recipe_name": "Peanut Banana Toast",
    "value": 1.31
  }
]
```

## GET `/analytics/recipes/by-category`
Returns difficulty scoring output.

### Response
**200 OK**
```json
[
  {
    "category_name": "Breakfast",
    "recipe_count": 4
  },
  {
    "category_name": "Dinner",
    "recipe_count": 3
  },
  {
    "category_name": "Lunch",
    "recipe_count": 3
  }
]
```

## 6. Error Handling Notes

The API uses both validation-level and business-rule-level errors.

### Validation Errors
Handled automatically by FastAPI and Pydantic, for example:
- empty names
- negative nutrition values
- invalid quantities
- zero servings

These return **422 Unprocessable Entity**.

### Business Rule Errors
Handled manually in the route logic, for example:
- duplicate category names
- duplicate ingredient names
- duplicate recipe-ingredient links
- deleting a category that is still linked to recipes
- deleting an ingredient that is still linked to recipes

These return **400 Bad Request**.

### Missing Resources
Requests for non-existent IDs return **404 Not Found**.

### Successful Requests
Typical successful responses use:
- **200 OK** for retrieval and updates
- **201 Created** for successful creation
- **204 No Content** for successful deletion

## 7. Example Workflow

A typical API workflow is:

1. Create a category using `POST /categories/`
2. Create ingredients using `POST /ingredients/`
3. Create a recipe using `POST /recipes/`
4. Link ingredients to the recipe using `POST /recipes/{recipe_id}/ingredients`
5. Retrieve recipe details using `GET /recipes/{recipe_id}`
6. Retrieve analytics using:
   - `GET /analytics/recipes/{recipe_id}/nutrition`
   - `GET /analytics/recipes/{recipe_id}/allergens`
   - `GET /analytics/recipes/{recipe_id}/cost`
   - `GET /analytics/recipes/{recipe_id}/difficulty`
7. Use filtering through `GET /recipes/` with query parameters such as:
   - `search`
   - `category_id`
   - `vegan_only`
   - `gluten_free_only`
   - `max_calories`
   - `max_cost`
8. Use summary analytics endpoints such as:
   - `GET /analytics/recipes/top-protein`
   - `GET /analytics/recipes/lowest-cost`
   - `GET /analytics/recipes/by-category`

## 8. Limitations

The current version of the API has the following limitations:

- No authentication or authorisation is implemented
- Analytics are calculated dynamically in Python rather than using optimised database queries
- No pagination is included for large result sets
- No deployment is included in this local coursework version
- Seed data is manually curated rather than imported from a live public dataset
- Nutritional analysis is limited to calories, protein, carbohydrates, fat, allergens, cost, and rule-based difficulty
- No user-specific features such as favourites or saved recipes are included

These limitations leave clear opportunities for future improvement, such as authentication, public dataset integration, deployment, pagination, and more advanced analytics.


PDF API documentation: [`docs/api_documentation.pdf`](docs/api_documentation.pdf)