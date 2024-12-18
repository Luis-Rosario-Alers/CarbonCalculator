import asyncio
import json
import os

import aiofiles
import aiosqlite

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# function creates a emissions database during initialization of the program
async def initialize_emissions_database():
    try:
        db_path = os.path.join(root_dir, "databases", "emissions.db")
        db_folder = os.path.join(root_dir, "databases")
        if not os.path.exists(db_path):
            os.makedirs(db_folder, exist_ok=True)

        async with aiosqlite.connect(db_path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """CREATE TABLE IF NOT EXISTS emissions
                    (user_id INTEGER, fuel_type TEXT, fuel_used REAL,
                    emissions REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(username))"""
                )
                await conn.commit()
    except aiosqlite.Error as e:
        print(f"Database error: {e}")
        print("Emissions database not initialized")
        return 0


async def initialize_user_data_database():
    try:
        db_path = os.path.join(root_dir, "databases", "user_data.db")
        db_folder = os.path.join(root_dir, "databases")
        if not os.path.exists(db_path):
            os.makedirs(db_folder, exist_ok=True)

        async with aiosqlite.connect(db_path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY, password TEXT)"""
                )
                await conn.commit()
    except aiosqlite.Error as e:
        print(f"Database error: {e}")
        print("User data database not initialized")
        return 0


async def initialize_fuel_type_database():
    try:
        db_path = os.path.join(root_dir, "databases", "fuel_type_conversions.db")
        db_folder = os.path.join(root_dir, "databases")
        if not os.path.exists(db_path):
            os.makedirs(db_folder, exist_ok=True)

        async with aiosqlite.connect(db_path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """CREATE TABLE IF NOT EXISTS
                    fuel_types
                    (fuel_type TEXT PRIMARY KEY, emissions_factor REAL)"""
                )

                json_path = os.path.join(
                    root_dir, "resources", "conversion_factors", "fuel_types.json"
                )
                async with aiofiles.open(json_path, "r") as file:
                    fuel_data = json.loads(await file.read())

                for fuel in fuel_data:
                    await cursor.execute(
                        "INSERT OR IGNORE INTO fuel_types VALUES (?, ?)",
                        (fuel["fuel_type"], fuel["emissions_factor"]),
                    )
                await conn.commit()
    except aiosqlite.Error as e:
        print(f"Database error: {e}")
        print("Fuel type database not initialized")
        return 0
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"JSON error: {e}")
        print("Fuel type data was not loaded correctly")
        return 0


# function to bundle initialization of all databases
async def database_initialization():
    await asyncio.gather(
        initialize_emissions_database(),
        initialize_user_data_database(),
        initialize_fuel_type_database(),
    )


# function to test initialization of all databases
# database_initialization()
