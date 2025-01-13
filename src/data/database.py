import asyncio
import json
import logging
import os
import sys

import aiofiles
import aiosqlite

logger = logging.getLogger("data")

# Get the directory of the current script or executable
if getattr(sys, "frozen", False):
    # If the application is run as a bundle (e.g., with PyInstaller)
    application_path = os.path.dirname(sys.executable)
else:
    # If the application is run as a script
    application_path = os.path.dirname(__file__)

databases_folder = os.path.join(application_path, "databases")


# function creates an emissions database during initialization of the program
async def initialize_emissions_database():
    try:
        os.makedirs(databases_folder, exist_ok=True)
        db_path = os.path.join(databases_folder, "emissions.db")

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
        databases_folder = os.path.join(application_path, "databases")
        os.makedirs(databases_folder, exist_ok=True)
        db_path = os.path.join(databases_folder, "user_data.db")

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
        databases_folder = os.path.join(application_path, "databases")
        os.makedirs(databases_folder, exist_ok=True)
        db_path = os.path.join(databases_folder, "fuel_type_conversions.db")

        async with aiosqlite.connect(db_path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """CREATE TABLE IF NOT EXISTS
                    fuel_types
                    (fuel_type TEXT PRIMARY KEY, emissions_factor REAL)"""
                )

                json_path = os.path.join(
                    application_path,
                    "resources",
                    "conversion_factors",
                    "fuel_types.json",
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


async def get_fuel_types():
    db_path = os.path.join(application_path, "databases", "fuel_type_conversions.db")
    conn = aiosqlite.connect(db_path)
    async with conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT fuel_type FROM fuel_types")
            fuel_types = await cursor.fetchall()
        return [fuel_type[0] for fuel_type in fuel_types]


async def get_emissions_factor(fuel_type: str) -> int:
    db_path = os.path.join(application_path, "databases", "fuel_type_conversions.db")
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
                (fuel_type,),
            )
            row = await cursor.fetchone()
            if row:
                return row[0]
            else:
                error = ValueError(
                    f"No emissions factor found for fuel type: {fuel_type}"
                )
                logger.error(error)


async def log_calculation(user_id, fuel_type, fuel_used, emissions):
    try:
        # ? I would validate inputs here but im not sure.
        # What do you think I should do?

        logger.info("Logging calculation")
        logger.info(
            f"User ID: {user_id}, Fuel Type: {fuel_type}, Fuel Used: {fuel_used}, Emissions: {emissions}"
        )
        db_path = os.path.join(application_path, "databases", "emissions.db")

        # connect to the database
        async with aiosqlite.connect(db_path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """INSERT INTO emissions
                    (user_id, fuel_type, fuel_used, emissions)
                    VALUES (?, ?, ?, ?)""",
                    (user_id, fuel_type, fuel_used, emissions),
                )
                # Commit the transaction
                await conn.commit()

                # Return the log for testing purposes
                await cursor.execute(
                    "SELECT fuel_type, fuel_used, emissions FROM emissions WHERE user_id = ? AND fuel_type = ? AND "
                    "fuel_used = ? AND emissions = ?",
                    (user_id, fuel_type, fuel_used, emissions),
                )
                log = await cursor.fetchall()
                return log
    except aiosqlite.Error as e:
        logger.error(f"Database error: {e}")
    except ValueError as e:
        logger.error(f"Value error: {e}")


# function to bundle initialization of all databases
async def database_initialization():
    await asyncio.gather(
        initialize_emissions_database(),
        initialize_user_data_database(),
        initialize_fuel_type_database(),
    )


# function to test initialization of all databases
# database_initialization()
