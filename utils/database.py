# utils/database.py
# This file handles ALL database operations for Expiry Lens

import sqlite3
import os

DATABASE_PATH = os.path.join("database", "expiry_lens.db")


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection


def initialize_database():
    """
    Creates the 'food_items' table if it doesn't already exist,
    and adds a 'username' column to link each item to its owner.
    """
    connection = get_connection()
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS food_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL DEFAULT 'unknown',
        food_name TEXT NOT NULL,
        expiry_date TEXT NOT NULL,
        scan_date TEXT NOT NULL,
        image_path TEXT,
        storage_type TEXT DEFAULT 'Room Temperature'
    )
    """
    cursor.execute(create_table_query)

    # If the table already existed WITHOUT a username column (from before
    # this update), this adds it safely without losing existing data.
    # We wrap it in try/except because SQLite throws an error if the 
    # column already exists - this makes the function safe to run 
    # multiple times.
    try:
        cursor.execute("ALTER TABLE food_items ADD COLUMN username TEXT DEFAULT 'unknown'")
    except sqlite3.OperationalError:
        # Column already exists - completely fine, nothing to do
        pass

    connection.commit()
    connection.close()

    print("Database initialized successfully! Table 'food_items' is ready.")


def add_food_item(username, food_name, expiry_date, scan_date, image_path, storage_type="Room Temperature"):
    """
    Inserts a new food item into the database, linked to a specific user.
    """
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO food_items (username, food_name, expiry_date, scan_date, image_path, storage_type)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_query, (username, food_name, expiry_date, scan_date, image_path, storage_type))

    connection.commit()
    connection.close()

    print(f"Added '{food_name}' to the database for user '{username}'.")


def get_all_food_items(username):
    """
    Retrieves ONLY the food items belonging to the given username.
    """
    connection = get_connection()
    cursor = connection.cursor()

    select_query = "SELECT * FROM food_items WHERE username = ? ORDER BY expiry_date ASC"
    cursor.execute(select_query, (username,))

    all_items = cursor.fetchall()
    connection.close()

    return all_items


if __name__ == "__main__":
    initialize_database()

    add_food_item(
        username="demo",
        food_name="Test Milk",
        expiry_date="2026-07-25",
        scan_date="2026-07-16",
        image_path="static/uploads/test_milk.jpg",
        storage_type="Refrigerator"
    )

    items = get_all_food_items("demo")
    print("\nAll items for user 'demo':")
    for item in items:
        print(item)
        