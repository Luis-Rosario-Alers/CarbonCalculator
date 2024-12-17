import os
import shutil
import sqlite3
import time

import pytest

from core.emissions_calculator import EmissionsCalculator
from data.database import initialize_emissions_database, initialize_fuel_type_database

# ! BEWARE THAT RUNNING THESE TESTS WILL DELETE THE DATABASES FOLDER AND ALL ITS CONTENTS.
# ! MAKE SURE TO BACKUP ANY IMPORTANT DATA BEFORE RUNNING THESE TESTS.
# ! RUNNING THESE TEST CONCURRENTLY WILL NOT WORK. idk why.


# path to database folder
db_folder = os.path.join(os.path.dirname(__file__), "..", "databases")


@pytest.fixture
def emissions_calculator():
    return EmissionsCalculator()


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


# * If this test fails, check the calculate_emissions module for logic changes such as math operator changing
def test_calculate_emissions(
    emissions_calculator, fuel_type="gasoline", fuel_used: float = 10.0
):
    try:
        # initializes fuel type databases necessary for test
        initialize_fuel_type_database()

        # absolute path to databases
        db_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "databases",
            "fuel_type_conversions.db",
        )
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # find fuel_type emissions factor
        cursor.execute(
            "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
            (fuel_type,),
        )

        # simulate expected function logic
        emissions_factor = cursor.fetchone()[0]
        emissions = fuel_used * emissions_factor

        # assert that expected function logic is equal to actual function logic
        assert emissions == emissions_calculator.calculate_emissions(
            1, fuel_type, fuel_used
        )
    finally:
        # Ensure the connection is closed
        if conn:
            conn.commit()
            conn.close()

        time.sleep(0.1)


# if this test fails, most likely conversion rates have changed
# or sql execution has had an error
def test_log_calculation(
    emissions_calculator, fuel_type="gasoline", fuel_used: float = 10.0
):
    try:
        # Initialize databases
        initialize_fuel_type_database()
        initialize_emissions_database()

        # paths to databases
        emissions_db_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "databases", "emissions.db"
        )
        fuel_type_db_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "databases",
            "fuel_type_conversions.db",
        )

        with sqlite3.connect(fuel_type_db_path, timeout=20) as conn_fuel:
            cursor_fuel = conn_fuel.cursor()
            cursor_fuel.execute(
                "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
                (fuel_type,),
            )
            fuel_type_result = cursor_fuel.fetchone()
            emissions_factor = fuel_type_result[0]
            emissions = fuel_used * emissions_factor

            if not fuel_type_result:
                raise ValueError(f"Fuel type {fuel_type} not found in the database")

        with sqlite3.connect(emissions_db_path, timeout=20) as conn_emissions:
            cursor_emissions = conn_emissions.cursor()
            # Clear existing data
            time.sleep(0.1)
            cursor_emissions.execute("DELETE FROM emissions")
            # Insert new test data
            cursor_emissions.execute(
                "INSERT INTO emissions (user_id, fuel_type, fuel_used, emissions) "
                "VALUES (?, ?, ?, ?)",
                (1, fuel_type, fuel_used, emissions),
            )
            cursor_emissions.execute("SELECT * FROM emissions")
            conn_emissions.commit()
            expected_result = cursor_emissions.fetchall()
        conn_emissions.close()
        conn_fuel.close()

        # Test the actual function
        real_result = emissions_calculator.log_calculation(
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
