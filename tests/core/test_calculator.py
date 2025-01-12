import asyncio
import os
import shutil
import sqlite3
import time

import aiosqlite
import pytest

from core.emissions_calculator import calculate_emissions
from data.database import log_calculation
from data.database import initialize_emissions_database, initialize_fuel_type_database

# ! BEWARE THAT RUNNING THESE TESTS WILL DELETE THE DATABASES FOLDER AND ALL ITS CONTENTS.
# ! MAKE SURE TO BACKUP ANY IMPORTANT DATA BEFORE RUNNING THESE TESTS.
# ! RUNNING THESE TEST CONCURRENTLY WILL NOT WORK. idk why.


# path to database folder
db_folder = os.path.join(os.path.dirname(__file__), "..", "data", "databases")




@pytest.fixture(autouse=True)
def cleanup_database():
    # Create a fresh database folder if it doesn't exist
    os.makedirs(db_folder, exist_ok=True)

    yield  # Run the test

    # Cleanup after test
    time.sleep(0.1)  # Allow time for file handles to be released
    try:
        if os.path.exists(db_folder):
            # Remove all files in the database folder
            shutil.rmtree(db_folder)
    except PermissionError as e:
        print(f"Warning: Could not delete database folder: {e}")


# * If this test fails, check the calculate_emissions module for logic changes such as math operator changing\
@pytest.mark.asyncio
async def test_calculate_emissions(
        fuel_type="gasoline", fuel_used: float = 10.0
):
    try:
        # initializes fuel type databases necessary for test
        await initialize_fuel_type_database()

        # absolute path to databases
        db_path = os.path.join(db_folder, "fuel_type_conversions.db")
        async with aiosqlite.connect(db_path) as conn:
            async with conn.cursor() as cursor:
                # find fuel_type emissions factor
                await cursor.execute(
                    "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
                    (fuel_type,),
                )

                # simulate expected function logic
                emissions_factor = (await cursor.fetchone())[0]
                emissions = fuel_used * emissions_factor
                expected_emissions = await calculate_emissions(
                    1, fuel_type, fuel_used
                )

        # assert that expected function logic is equal to actual function logic
        assert emissions == expected_emissions[3]
    finally:
        # Ensure the connection is closed
        if conn:
            await conn.commit()
            await conn.close()

        time.sleep(0.1)


# if this test fails, most likely conversion rates have changed
# or sql execution has had an error
@pytest.mark.asyncio
async def test_log_calculation(
        fuel_type="gasoline", fuel_used: float = 10.0
):
    try:
        # Initialize databases
        await initialize_fuel_type_database()
        await initialize_emissions_database()

        # paths to databases
        emissions_db_path = os.path.join(
            db_folder, "emissions.db"
        )
        fuel_type_db_path = os.path.join(
            db_folder, "fuel_type_conversions.db"
        )

        async with aiosqlite.connect(fuel_type_db_path) as conn_fuel:
            async with conn_fuel.cursor() as cursor_fuel:
                await cursor_fuel.execute(
                    "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
                    (fuel_type,),
                )
                fuel_type_result = await cursor_fuel.fetchone()
                emissions_factor = fuel_type_result[0]
                emissions = fuel_used * emissions_factor

                if not fuel_type_result:
                    raise ValueError(f"Fuel type {fuel_type} not found in the database")

        async with aiosqlite.connect(emissions_db_path) as conn_emissions:
            async with conn_emissions.cursor() as cursor_emissions:
                # Clear existing data
                await asyncio.sleep(0.1)
                await cursor_emissions.execute("DELETE FROM emissions")
                # Insert new test data
                await cursor_emissions.execute(
                    "INSERT INTO emissions (user_id, fuel_type, fuel_used, emissions) "
                    "VALUES (?, ?, ?, ?)",
                    (1, fuel_type, fuel_used, emissions),
                )
                await cursor_emissions.execute("SELECT * FROM emissions")
                await conn_emissions.commit()
                expected_result = await cursor_emissions.fetchall()
                await conn_emissions.close()
                await conn_fuel.close()

        # Test the actual function
        real_result = await log_calculation(
            2, fuel_type, fuel_used, emissions
        )
        print(expected_result)
        print(real_result)

        assert real_result[0][1] == expected_result[0][2]
        assert real_result[0][2] == expected_result[0][3]
        assert real_result[0][0] == expected_result[0][1]

    except Exception as e:
        print(f"Error during test: {e}")
        raise
