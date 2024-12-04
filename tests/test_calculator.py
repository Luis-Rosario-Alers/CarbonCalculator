import os
import sqlite3

import pytest

from src.core.emissions_calculator import EmissionsCalculator


@pytest.fixture
def emissions_calculator():
    return EmissionsCalculator()


# test for calculate emissions method
def test_calculate_emissions(
    emissions_calculator, fuel_type="gasoline", fuel_used: float = 10.0
):
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
