import os
import shutil
import sqlite3

import pytest

from src.core.emissions_calculator import EmissionsCalculator
from src.data.database import (initialize_emissions_database,
                               initialize_fuel_type_database)

# path to database folder
db_folder = os.path.join(os.path.dirname(__file__), "..", "databases")


@pytest.fixture
def emissions_calculator():
    return EmissionsCalculator()


# if this test fails, check the calculate_emissions module for
# logic changes such as math operator changing
def test_calculate_emissions(
    emissions_calculator, fuel_type="gasoline", fuel_used: float = 10.0
):  # initializes fuel type databases necessary for test
    initialize_fuel_type_database()

    # path to database folder

    # absolute path to databases
    db_path = os.path.join(
        os.path.dirname(__file__), "..", "databases", "fuel_type_conversions.db"
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
    # deletes database folder after test is done
    shutil.rmtree(db_folder)


# if this test fails, most likely conversion rates have changed
# or sql execution has had an error
def test_log_calculation(
    emissions_calculator, fuel_type="gasoline", fuel_used: float = 10.0
):
    # initialize necessary databases for test
    initialize_fuel_type_database()
    initialize_emissions_database()

    # absolute path to databases
    emissions_db_path = os.path.join(
        os.path.dirname(__file__), "..", "databases", "emissions.db"
    )
    fuel_type_db_path = os.path.join(
        os.path.dirname(__file__), "..", "databases", "fuel_type_conversions.db"
    )
    conn_fuel = sqlite3.connect(fuel_type_db_path)
    cursor_fuel = conn_fuel.cursor()
    # Check if the fuel type exists in the fuel_type_conversions database
    cursor_fuel.execute(
        "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?", (fuel_type,)
    )
    fuel_type_result = cursor_fuel.fetchone()
    emissions_factor = fuel_type_result[0]
    print(fuel_type_result)
    # if calculator test fails, please remove this.
    # as it is now not valid
    emissions = fuel_used * emissions_factor
    # fetches fuel type value from database
    if not fuel_type_result:
        # if there is no result, raise ValueError
        raise ValueError(f"Fuel type {fuel_type} not found in the database")
    # connects to emissions database
    conn_emissions = sqlite3.connect(emissions_db_path)
    cursor_emissions = conn_emissions.cursor()
    user_id = 1
    # execute sql to insert parameters to the database
    cursor_emissions.execute(
        "INSERT INTO emissions (user_id, fuel_type, fuel_used, emissions) "
        "VALUES (?, ?, ?, ?)",
        (user_id, fuel_type, fuel_used, emissions),
    )
    # fetch results
    cursor_emissions.execute(
        "SELECT fuel_type, fuel_used, "
        "emissions FROM emissions WHERE user_id = ? AND fuel_type = ? AND fuel_used = ? AND emissions = ?",
        (user_id, fuel_type, fuel_used, emissions),
    )
    expected_result = cursor_emissions.fetchall()
    # commit and close the database
    conn_emissions.commit()
    conn_emissions.close()
    user_id = 2
    # use actual function
    real_result = emissions_calculator.log_calculation(
        user_id, fuel_type, fuel_used, emissions
    )
    print(f"real result: {real_result[0][2]}")
    print(f"expected result: {expected_result[0][2]}")
    # the real_result and expected_result are tuples and they store a list
    # please keep in mind you have to use [] <- 0 to select list [] <- to select element in list
    assert real_result[0] == expected_result[0]
    # deletes database folder after test is done
    shutil.rmtree(db_folder)
