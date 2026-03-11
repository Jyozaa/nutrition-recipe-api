def calculate_recipe_nutrition(recipe):
    total_calories = 0.0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0

    for link in recipe.ingredient_links:
        ingredient = link.ingredient
        multiplier = link.quantity_g / 100.0

        total_calories += ingredient.calories_per_100g * multiplier
        total_protein += ingredient.protein_per_100g * multiplier
        total_carbs += ingredient.carbs_per_100g * multiplier
        total_fat += ingredient.fat_per_100g * multiplier

    servings = recipe.servings if recipe.servings > 0 else 1

    return {
        "total_calories": round(total_calories, 2),
        "total_protein": round(total_protein, 2),
        "total_carbs": round(total_carbs, 2),
        "total_fat": round(total_fat, 2),
        "calories_per_serving": round(total_calories / servings, 2),
        "protein_per_serving": round(total_protein / servings, 2),
        "carbs_per_serving": round(total_carbs / servings, 2),
        "fat_per_serving": round(total_fat / servings, 2),
    }