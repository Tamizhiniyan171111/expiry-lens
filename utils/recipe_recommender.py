# utils/recipe_recommender.py
# This file suggests simple recipes based on food items that are 
# expiring soon, using a small built-in "recipe book" (no paid API needed)

# ===================================
# OUR RECIPE BOOK
# A list of dictionaries - each one describes one recipe:
# its name, the ingredients it needs, and simple instructions.
# All ingredient names are lowercase, to match how YOLOv8 names food items.
# ===================================
RECIPE_BOOK = [
    {
        "name": "Banana Pancakes",
        "ingredients": ["banana"],
        "instructions": "Mash the banana, mix with pancake batter, and fry until golden."
    },
    {
        "name": "Apple Cinnamon Oatmeal",
        "ingredients": ["apple"],
        "instructions": "Dice the apple, cook with oats, water/milk, and a pinch of cinnamon."
    },
    {
        "name": "Fresh Orange Salad",
        "ingredients": ["orange"],
        "instructions": "Peel and slice the orange, toss with greens and a light dressing."
    },
    {
        "name": "Veggie Sandwich",
        "ingredients": ["sandwich", "carrot", "broccoli"],
        "instructions": "Layer fresh vegetables between bread slices with your favorite spread."
    },
    {
        "name": "Simple Fruit Smoothie",
        "ingredients": ["banana", "apple", "orange"],
        "instructions": "Blend any combination of these fruits with yogurt or milk until smooth."
    },
    {
        "name": "Leftover Pizza Bake",
        "ingredients": ["pizza"],
        "instructions": "Reheat pizza in the oven at 180°C for 8-10 minutes for a crispy finish."
    },
]


def get_recipe_suggestions(expiring_food_names):
    """
    Takes a list of food names that are expiring soon (e.g., ["banana", "apple"])
    and returns a list of matching recipes from our recipe book.

    A recipe "matches" if AT LEAST ONE of its required ingredients 
    is in our expiring food list - this keeps suggestions generous 
    and useful, rather than requiring a perfect exact match.
    """
    # Convert everything to lowercase for safe, consistent comparison
    expiring_food_names_lower = [name.lower() for name in expiring_food_names]

    matching_recipes = []

    for recipe in RECIPE_BOOK:
        # Check if ANY of this recipe's ingredients appear in our expiring list
        # any() returns True if at least one item in the list satisfies the condition
        has_matching_ingredient = any(
            ingredient in expiring_food_names_lower
            for ingredient in recipe["ingredients"]
        )

        if has_matching_ingredient:
            matching_recipes.append(recipe)

    return matching_recipes


# Test code - only runs when this file is executed directly
if __name__ == "__main__":
    # Simulate a user who has bananas and apples about to expire
    test_expiring_items = ["banana", "apple"]

    suggestions = get_recipe_suggestions(test_expiring_items)

    print(f"Expiring items: {test_expiring_items}")
    print(f"\nSuggested recipes ({len(suggestions)} found):")
    for recipe in suggestions:
        print(f"- {recipe['name']}: {recipe['instructions']}")
        