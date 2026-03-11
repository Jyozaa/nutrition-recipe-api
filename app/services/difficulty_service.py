def calculate_recipe_difficulty(recipe):
    score = 0

    ingredient_count = len(recipe.ingredient_links)
    instruction_steps = len(
        [step for step in recipe.instructions.split(".") if step.strip()]
    )

    if recipe.prep_time_minutes > 15:
        score += 1

    if recipe.cook_time_minutes > 30:
        score += 1

    if ingredient_count > 8:
        score += 1

    if instruction_steps > 6:
        score += 1

    if score <= 1:
        difficulty = "easy"
    elif score == 2:
        difficulty = "medium"
    else:
        difficulty = "hard"

    return {
        "score": score,
        "difficulty": difficulty,
    }