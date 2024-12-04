import json
import os
import sqlite3


def initialize_emissions_database():
    try:
        if not os.path.exists("databases"):
            os.makedirs("databases")

        db_path = os.path.join("databases", "emissions.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS emissions
        (user_id INTEGER PRIMARY KEY, fuel_type TEXT, fuel_used REAL,
        emissions REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(username))"""
        )
        """
        TODO user_id in the future should be
        a non changing unique identifier for each user
        """
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        print("Emissions database not initialized")
        return 0


def initialize_user_data_database():
    try:
        # Ensure the database folder exists
        if not os.path.exists("databases"):
            os.makedirs("databases")

        # Connect to the database in the database folder
        db_path = os.path.join("databases", "user_data.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table if it does not exist
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users
        (username TEXT PRIMARY KEY, password TEXT)"""
        )

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        print("User data database not initialized")
        return 0


# TODO standardize unit of CO2 per fuel type
def initialize_fuel_type_database():
    try:
        # Ensure the database folder exists
        if not os.path.exists("databases"):
            os.makedirs("databases")

        # Connect to the database in the database folder
        db_path = os.path.join("databases", "fuel_type_conversions.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table if it does not exist
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS
            fuel_types
            (fuel_type TEXT PRIMARY KEY, emissions_factor REAL)"""
        )

        # Load data from JSON file
        json_path = os.path.join("resources", "conversion_factors", "fuel_types.json")
        with open(json_path, "r") as file:
            fuel_data = json.load(file)

        # Insert data into table
        for fuel in fuel_data:
            cursor.execute(
                "INSERT OR IGNORE INTO fuel_types VALUES (?, ?)",
                (fuel["fuel_type"], fuel["emissions_factor"]),
            )

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        print("Fuel type database not initialized")
        return 0


# function to bundle initialization of all databases
def database_initialization():
    initialize_emissions_database()
    initialize_fuel_type_database()
    initialize_user_data_database()


# function to test initialization of all databases
# database_initialization()
