# utils/auth.py
# Handles user registration, login verification, and the users table

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_PATH = os.path.join("database", "expiry_lens.db")


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def initialize_users_table():
    """
    Creates the 'users' table if it doesn't already exist.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
    print("Users table is ready.")


def create_user(username, password):
    """
    Registers a new user. Returns True if successful, 
    False if the username is already taken.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # NEVER store the raw password - always hash it first
    # generate_password_hash() turns "mypassword123" into a long, 
    # irreversible scrambled string that's safe to store
    password_hash = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        connection.commit()
        success = True
    except sqlite3.IntegrityError:
        # This happens if the username already exists (UNIQUE constraint)
        success = False
    finally:
        connection.close()

    return success


def verify_user(username, password):
    """
    Checks if a username/password combination is correct.
    Returns True if valid, False otherwise.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    connection.close()

    if result is None:
        # No user found with that username
        return False

    stored_hash = result[0]

    # check_password_hash() safely compares the entered password 
    # against the stored hash, without ever un-scrambling it
    return check_password_hash(stored_hash, password)


if __name__ == "__main__":
    initialize_users_table()
    created = create_user("demo", "demo123")
    print(f"Demo user created: {created}")
    print(f"Login check (correct password): {verify_user('demo', 'demo123')}")
    print(f"Login check (wrong password): {verify_user('demo', 'wrongpass')}")
    