# utils/database.py
# This file handles ALL database operations for Expiry Lens
# Keeping database code separate from app.py keeps our project organized

# sqlite3 is Python's BUILT-IN library for working with SQLite databases
# We don't need to "pip install" this - it comes with Python itself
import sqlite3

# os helps us build file paths that work correctly on any operating system
import os

# This builds the full path to where our database file will live
# os.path.join is safer than manually writing "database/expiry_lens.db"
# because it automatically uses the correct slash direction for Windows/Mac/Linux
DATABASE_PATH = os.path.join("database", "expiry_lens.db")


def get_connection():
    """
    Creates and returns a connection to our SQLite database.
    Think of a 'connection' like picking up the phone to talk to the database.
    """
    # sqlite3.connect() opens the database file if it exists,
    # or CREATES a new empty one automatically if it doesn't exist yet
    connection = sqlite3.connect(DATABASE_PATH)
    return connection


def initialize_database():
    """
    Creates the 'food_items' table if it doesn't already exist.
    This function is safe to run multiple times - it won't recreate
    or erase the table if it's already there.
    """
    # Step 1: Open a connection to the database
    connection = get_connection()

    # Step 2: A "cursor" is what actually lets us execute SQL commands
    # Think of connection = the phone line, cursor = your mouth speaking commands
    cursor = connection.cursor()

    # Step 3: Write the SQL command to create our table
    # CREATE TABLE IF NOT EXISTS means: only create it if it doesn't already exist
    # This prevents errors if we run this function multiple times
    create_table_query = """
    CREATE TABLE IF NOT EXISTS food_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT NOT NULL,
        expiry_date TEXT NOT NULL,
        scan_date TEXT NOT NULL,
        image_path TEXT,
        storage_type TEXT DEFAULT 'Room Temperature'
    )
    """
    # Let's break down each column we just defined:
    # id            -> a unique number automatically assigned to each row (like a row ID)
    # food_name     -> the name of the food item, e.g. "Milk", "Bread"
    # expiry_date   -> the expiry date read from the package (we'll store as text for now)
    # scan_date     -> the date the user scanned this item
    # image_path    -> where the uploaded photo is saved on disk
    # storage_type  -> e.g. "Refrigerator", "Freezer", "Room Temperature" - used later for Freshness Score

    # Step 4: Execute (run) that SQL command
    cursor.execute(create_table_query)

    # Step 5: Save (commit) the changes permanently to the database file
    connection.commit()

    # Step 6: Close the connection - always close connections when done,
    # just like hanging up the phone after a call
    connection.close()

    print("Database initialized successfully! Table 'food_items' is ready.")


def add_food_item(food_name, expiry_date, scan_date, image_path, storage_type="Room Temperature"):
    """
    Inserts (adds) a new food item into the database.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # INSERT INTO adds a new row to our table
    # The question marks (?) are PLACEHOLDERS - this is called a "parameterized query"
    # We NEVER put variables directly into SQL text (that's a security risk called SQL Injection)
    # Instead, we pass them safely as a separate tuple
    insert_query = """
    INSERT INTO food_items (food_name, expiry_date, scan_date, image_path, storage_type)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(insert_query, (food_name, expiry_date, scan_date, image_path, storage_type))

    connection.commit()
    connection.close()

    print(f"Added '{food_name}' to the database.")


def get_all_food_items():
    """
    Retrieves ALL food items currently stored in the database.
    Returns a list of rows (each row is one food item).
    """
    connection = get_connection()
    cursor = connection.cursor()

    # SELECT * FROM means "get every column, from every row"
    # ORDER BY expiry_date means results come back sorted soonest-expiring first
    select_query = "SELECT * FROM food_items ORDER BY expiry_date ASC"
    cursor.execute(select_query)

    # fetchall() collects every matching row into a Python list
    all_items = cursor.fetchall()

    connection.close()

    return all_items


# This block only runs if we execute database.py DIRECTLY (for testing)
# It will NOT run when other files import this file
if __name__ == "__main__":
    # Let's test our functions right here
    initialize_database()

    # Add a sample test item
    add_food_item(
        food_name="Test Milk",
        expiry_date="2026-07-25",
        scan_date="2026-07-16",
        image_path="static/uploads/test_milk.jpg",
        storage_type="Refrigerator"
    )

    # Retrieve and print everything in the database
    items = get_all_food_items()
    print("\nAll items currently in the database:")
    for item in items:
        print(item)