# utils/notifications.py
# This file calculates the "freshness status" of a food item based on 
# how close it is to its expiry date - powers our notification badges

from datetime import datetime


def get_expiry_status(expiry_date_str):
    """
    Takes an expiry date (as text, "YYYY-MM-DD") and returns a dictionary
    describing its status: how many days are left, a status label,
    and a CSS class name we'll use for color-coding on the dashboard.
    """
    # Convert the stored expiry date TEXT into a real date object
    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")

    # Get today's date (without the time portion, just the calendar date)
    today = datetime.now()

    # Subtract today's date FROM the expiry date
    # This gives us a "timedelta" object representing the difference
    # .days extracts just the number of whole days from that difference
    days_remaining = (expiry_date - today).days

    # Now we categorize based on how many days are left
    if days_remaining < 0:
        # A negative number means the expiry date has ALREADY PASSED
        status_label = "Expired"
        css_class = "status-expired"
    elif days_remaining == 0:
        status_label = "Expires Today!"
        css_class = "status-urgent"
    elif days_remaining == 1:
        status_label = "Expires Tomorrow!"
        css_class = "status-urgent"
    elif days_remaining <= 3:
        status_label = f"Expiring Soon ({days_remaining} days left)"
        css_class = "status-warning"
    else:
        status_label = f"Fresh ({days_remaining} days left)"
        css_class = "status-fresh"

    # We return all this info together as a dictionary, so our app.py
    # and dashboard.html can easily access whichever piece they need
    return {
        "days_remaining": days_remaining,
        "status_label": status_label,
        "css_class": css_class
    }


# Test code - only runs when this file is executed directly
if __name__ == "__main__":
    # A few test dates to see our function in action
    test_dates = ["2026-07-10", "2026-07-17", "2026-07-18", "2026-07-19", "2026-08-01"]

    for date in test_dates:
        result = get_expiry_status(date)
        print(f"Expiry: {date} -> {result['status_label']} (class: {result['css_class']})")
        