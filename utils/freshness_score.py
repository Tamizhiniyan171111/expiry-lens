# utils/freshness_score.py
# This file calculates a 0-100 "Freshness Score" for a food item,
# based on how much of its shelf life remains and how it's stored

from datetime import datetime
from utils.shelf_life import get_estimated_shelf_life

# Storage conditions can slow down spoilage - this dictionary defines
# a "bonus multiplier" for each storage type. A value of 1.0 means no
# change; higher than 1.0 means the food effectively "loses freshness"
# more slowly when stored that way.
STORAGE_MULTIPLIER = {
    "room temperature": 1.0,
    "refrigerator": 1.3,
    "freezer": 1.8,
}


def calculate_freshness_score(food_name, scan_date_str, expiry_date_str, storage_type):
    """
    Returns a Freshness Score from 0 (expired/no freshness left) to 
    100 (freshly scanned, full shelf life remaining).
    """
    scan_date = datetime.strptime(scan_date_str, "%Y-%m-%d")
    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
    today = datetime.now()

    # Total shelf life in days, from scan date to expiry date
    total_shelf_life_days = (expiry_date - scan_date).days
    if total_shelf_life_days <= 0:
        # Avoid dividing by zero - if scan and expiry are the same day, 
        # or expiry is somehow before scan, treat as 1 day minimum
        total_shelf_life_days = 1

    # How many days have passed since scanning
    days_elapsed = (today - scan_date).days

    # What FRACTION of the shelf life has been used up so far (0.0 to 1.0+)
    fraction_used = days_elapsed / total_shelf_life_days

    # Convert to a 0-100 score: 0% used = 100 score, 100% used = 0 score
    raw_score = (1 - fraction_used) * 100

    # Apply the storage bonus - better storage slows the decline
    multiplier = STORAGE_MULTIPLIER.get(storage_type.lower(), 1.0)
    adjusted_score = raw_score * multiplier

    # Clamp the final score so it never goes below 0 or above 100
    final_score = max(0, min(100, adjusted_score))

    return round(final_score)


if __name__ == "__main__":
    today_str = datetime.now().strftime("%Y-%m-%d")

    score = calculate_freshness_score(
        food_name="banana",
        scan_date_str=today_str,
        expiry_date_str="2026-07-23",
        storage_type="Room Temperature"
    )
    print(f"Freshness Score: {score}/100")
    