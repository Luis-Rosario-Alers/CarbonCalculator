import asyncio
import json
import logging
import os
import sys

import aiofiles
import aiosqlite

logger = logging.getLogger("data")


def determine_application_path():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        logger.info("Running as a PyInstaller bundle")
        application_path = sys._MEIPASS
        databases_folder = os.path.join(application_path, "databases")
        logger.info(f"Application path set to: {application_path}")
        logger.info(f"Databases folder set to: {databases_folder}")
    else:
        logger.info("Running as a script")
        application_path = os.path.dirname(__file__)
        databases_folder = os.path.join(application_path, "databases")
        logger.info(f"Application path set to: {application_path}")
        logger.info(f"Databases folder set to: {databases_folder}")
    return application_path, databases_folder


application_path, databases_folder = determine_application_path()


def setup_databases_folder():
    if os.path.exists(databases_folder):
        pass
    elif not os.path.exists(databases_folder):
        os.makedirs(databases_folder, exist_ok=True)


# function creates an emissions database during initialization of the program
async def initialize_emissions_database():
    try:
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
    global settings_path
    try:
        db_path = os.path.join(databases_folder, "fuel_type_conversions.db")

        # Ensure settings directory exists
        settings_dir = os.path.join(application_path, "resources", "config")
        os.makedirs(settings_dir, exist_ok=True)

        # Settings file path
        settings_path = os.path.join(settings_dir, "settings.json")

        # Default conversion factors path
        default_factors_path = os.path.join(
            application_path, "resources", "config", "conversion_factors"
        )
        os.makedirs(default_factors_path, exist_ok=True)

        async with aiosqlite.connect(db_path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """CREATE TABLE IF NOT EXISTS
                    fuel_types
                    (fuel_type TEXT PRIMARY KEY, emissions_factor REAL)"""
                )
                try:
                    async with aiofiles.open(settings_path, "r") as file:
                        settings = json.loads(await file.read())
                        json_path = settings.get("emissions_factors_path")
                        logger.info(f"Settings loaded: {settings}")
                        if not json_path:
                            # Create default settings if not exists
                            json_path = os.path.join(
                                default_factors_path, "fuel_types.json"
                            )
                            json_path = os.path.normpath(json_path)
                            os.makedirs(
                                os.path.dirname(json_path), exist_ok=True
                            )
                            # Save the default settings back to the settings file
                            settings["emissions_factors_path"] = json_path
                            async with aiofiles.open(
                                settings_path, "w"
                            ) as settings_file:
                                await settings_file.write(
                                    json.dumps(settings, indent=4)
                                )
                except json.JSONDecodeError:
                    logger.error("Error loading settings file")
                    return 0

                try:
                    async with aiofiles.open(json_path, "r") as file:
                        fuel_data = json.loads(await file.read())
                except json.JSONDecodeError:
                    print("Error loading fuel type data")
            try:
                for fuel in fuel_data:
                    await cursor.execute(
                        "INSERT OR IGNORE INTO fuel_types VALUES (?, ?)",
                        (fuel["fuel_type"], fuel["emissions_factor"]),
                    )
                    await conn.commit()
            except UnboundLocalError as e:
                logger.error(f"Error: {e}")
                logger.error("Fuel type data path does not contain valid data")
                return 0
    except aiosqlite.Error as e:
        logger.error(f"Database error: {e}")
        logger.error("Fuel type database not initialized")
        return 0
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.error(f"JSON error: {e}")
        logger.error("Fuel type data was not loaded correctly")
        return 0


async def get_fuel_types():
    db_path = os.path.join(databases_folder, "fuel_type_conversions.db")
    conn = aiosqlite.connect(db_path)
    async with conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT fuel_type FROM fuel_types")
            fuel_types = await cursor.fetchall()
        return [fuel_type[0] for fuel_type in fuel_types]


async def get_emissions_factor(fuel_type: str) -> int:
    db_path = os.path.join(databases_folder, "fuel_type_conversions.db")
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
        db_path = os.path.join(databases_folder, "emissions.db")

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
    if os.path.exists(databases_folder):
        await initialize_fuel_type_database()
    elif not os.path.exists(databases_folder):
        setup_databases_folder()
        logger.info("Initializing databases"),
        await asyncio.gather(
            initialize_emissions_database(),
            initialize_user_data_database(),
            initialize_fuel_type_database(),
        )
    logger.info("Databases initialized")


# function to test initialization of all databases
# database_initialization()
