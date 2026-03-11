def calculate_recipe_cost(recipe):
    total_cost = 0.0

    for link in recipe.ingredient_links:
        ingredient = link.ingredient
        multiplier = link.quantity_g / 100.0
        total_cost += ingredient.estimated_cost_per_100g * multiplier

    servings = recipe.servings if recipe.servings > 0 else 1

    return {
        "total_cost": round(total_cost, 2),
        "cost_per_serving": round(total_cost / servings, 2),
    }