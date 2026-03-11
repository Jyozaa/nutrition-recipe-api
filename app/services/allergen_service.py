def calculate_recipe_allergens(recipe):
    contains_gluten = False
    contains_dairy = False
    contains_nuts = False
    contains_soy = False
    contains_egg = False

    is_vegan = True
    is_vegetarian = True

    for link in recipe.ingredient_links:
        ingredient = link.ingredient

        contains_gluten = contains_gluten or ingredient.contains_gluten
        contains_dairy = contains_dairy or ingredient.contains_dairy
        contains_nuts = contains_nuts or ingredient.contains_nuts
        contains_soy = contains_soy or ingredient.contains_soy
        contains_egg = contains_egg or ingredient.contains_egg

        is_vegan = is_vegan and ingredient.is_vegan
        is_vegetarian = is_vegetarian and ingredient.is_vegetarian

    return {
        "contains_gluten": contains_gluten,
        "contains_dairy": contains_dairy,
        "contains_nuts": contains_nuts,
        "contains_soy": contains_soy,
        "contains_egg": contains_egg,
        "is_vegan": is_vegan,
        "is_vegetarian": is_vegetarian,
    }