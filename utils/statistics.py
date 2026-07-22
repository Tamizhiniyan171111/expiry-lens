# utils/statistics.py
# This file calculates food waste statistics: items saved/wasted,
# estimated money saved, estimated CO2 emissions saved, and 
# per-status breakdown counts (used for charts)

AVERAGE_COST_PER_ITEM = 40  # INR
AVERAGE_CO2_PER_ITEM_KG = 2.5


def calculate_statistics(items_with_status):
    """
    Takes the list of food items (each with a css_class status already
    calculated) and returns overall statistics: totals, money saved, 
    CO2 saved, and a breakdown of how many items fall into each status.
    """
    total_items = len(items_with_status)

    wasted_items = [item for item in items_with_status if item["css_class"] == "status-expired"]
    wasted_count = len(wasted_items)
    saved_count = total_items - wasted_count

    money_saved = saved_count * AVERAGE_COST_PER_ITEM
    co2_saved_kg = round(saved_count * AVERAGE_CO2_PER_ITEM_KG, 1)

    money_wasted = wasted_count * AVERAGE_COST_PER_ITEM
    co2_wasted_kg = round(wasted_count * AVERAGE_CO2_PER_ITEM_KG, 1)

    # NEW: count how many items fall into each individual status category
    # This powers the bar chart in Lesson 16
    fresh_count = len([i for i in items_with_status if i["css_class"] == "status-fresh"])
    warning_count = len([i for i in items_with_status if i["css_class"] == "status-warning"])
    urgent_count = len([i for i in items_with_status if i["css_class"] == "status-urgent"])
    expired_count = len([i for i in items_with_status if i["css_class"] == "status-expired"])

    return {
        "total_items": total_items,
        "saved_count": saved_count,
        "wasted_count": wasted_count,
        "money_saved": money_saved,
        "co2_saved_kg": co2_saved_kg,
        "money_wasted": money_wasted,
        "co2_wasted_kg": co2_wasted_kg,
        "fresh_count": fresh_count,
        "warning_count": warning_count,
        "urgent_count": urgent_count,
        "expired_count": expired_count,
    }


if __name__ == "__main__":
    test_items = [
        {"css_class": "status-fresh"},
        {"css_class": "status-fresh"},
        {"css_class": "status-expired"},
        {"css_class": "status-warning"},
    ]

    stats = calculate_statistics(test_items)
    print(stats)
    