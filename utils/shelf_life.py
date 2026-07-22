# utils/shelf_life.py
# This file estimates how many days a food item typically stays fresh,
# based on its detected type (from YOLOv8) and where it's stored.

# datetime lets us work with real calendar dates and do date math
from datetime import datetime, timedelta

# ===================================
# SHELF LIFE LOOKUP TABLE
# This is our "knowledge base" - real-world average shelf life 
# (in days) for common foods, at ROOM TEMPERATURE by default.
# These numbers are reasonable estimates based on common food safety guidance.
# ===================================
SHELF_LIFE_DAYS = {
    "banana": 6,
    "apple": 21,
    "orange": 14,
    "sandwich": 2,
    "pizza": 4,
    "cake": 4,
    "donut": 3,
    "carrot": 21,
    "broccoli": 7,
    "hot dog": 7,
    "bottle": 365,      # assuming a sealed drink/sauce bottle - long shelf life
    "bowl": 3,          # e.g. a bowl of prepared food
    "cup": 3,
}

# Fallback value if YOLOv8 detects something not in our table above
DEFAULT_SHELF_LIFE_DAYS = 7


def get_estimated_shelf_life(food_name):
    """
    Looks up how many days a given food name typically stays fresh.
    Falls back to a default value if the food isn't in our table.
    """
    # .lower() makes matching case-insensitive (e.g., "Banana" matches "banana")
    food_name_lower = food_name.lower()

    # .get() safely looks up a dictionary key - if it doesn't exist, 
    # it returns our DEFAULT instead of crashing with an error
    return SHELF_LIFE_DAYS.get(food_name_lower, DEFAULT_SHELF_LIFE_DAYS)


def calculate_estimated_expiry_date(food_name, scan_date_str):
    """
    Calculates an estimated expiry date, given a food name and the date it was scanned.
    scan_date_str should be in format "YYYY-MM-DD" (e.g., "2026-07-16")
    Returns the estimated expiry date as a string in the same format.
    """
    shelf_life_days = get_estimated_shelf_life(food_name)

    # Convert the scan date TEXT into a real Python date object we can do math on
    scan_date = datetime.strptime(scan_date_str, "%Y-%m-%d")

    # timedelta represents a SPAN of time (here, a number of days)
    # Adding it to a date gives us a new, future date
    estimated_expiry = scan_date + timedelta(days=shelf_life_days)

    # Convert back into a clean text format for storing/displaying
    return estimated_expiry.strftime("%Y-%m-%d")


# Test code - only runs when this file is executed directly
if __name__ == "__main__":
    today_str = datetime.now().strftime("%Y-%m-%d")

    test_food = "banana"
    result = calculate_estimated_expiry_date(test_food, today_str)
    print(f"Scanned on: {today_str}")
    print(f"Food: {test_food}")
    print(f"Estimated expiry date: {result}")
    