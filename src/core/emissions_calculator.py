import os
import sqlite3
import asyncio

from data.data_validator import DataValidator

# * EDIT THIS FILE IF YOU NEED TO ADD EXTRA FUNCTIONALITY TO THE EMISSIONS CALCULATOR.


# class to make Emissions calculating easier.
class EmissionsCalculator:
    # EmissionsData is a class that holds the data for the emissions.
    def __init__(
        self,
        # points to fuel_type_conversions.db
        emissions_conversions=os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "databases",
                "fuel_type_conversions.db",
            )
        ),
        # points to emissions.db
        db_path=os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "databases", "emissions.db"
            )
        ),
    ):
        self.emissions_conversions = emissions_conversions
        self.db_path = db_path

        # calculates the emissions based on the fuel type and fuel used.

        # TODO: add functionality to able to change fuel_used to tonnes, gallons, etc.

    def calculate_emissions(self, user_id, fuel_type, fuel_used: float):
        data_validator = DataValidator()
        # validate inputs
        if not data_validator.validate_fuel_type(fuel_type):
            raise ValueError("Invalid fuel type")
        if not data_validator.validate_fuel_used(fuel_used):
            raise ValueError("Invalid fuel used")
        if not data_validator.validate_user_id(user_id):
            raise ValueError("Invalid user ID")
        # connecting to the conversion database
        conn = sqlite3.connect(self.emissions_conversions)
        cursor = conn.cursor()
        # executing sql query to get the emissions factor for the fuel type.
        cursor.execute(
            "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
            (fuel_type,),
        )
        # fetching the emissions factor from the database.
        # TODO add error handling for when the fuel type is not found.
        emissions_factor = cursor.fetchone()[0]
        """
            emissions: calculating the emissions based
            on the fuel used and emissions factor.
        """
        # * Check This ⬇️ if emissions tests have failed
        emissions = emissions_factor * fuel_used
        emissions = round(emissions, 1)
        # checks if emissions data is valid
        if not data_validator.validate_emissions(emissions):
            raise ValueError("Invalid emissions data")
        print(
            # outputs emissions in kg units of CO2
            f"Carbon dioxide emissions for {fuel_used} units "
            f"of {fuel_type}: {emissions} kg"
        )
        self.log_calculation(user_id, fuel_type, fuel_used, emissions)
        # We are returning the emissions value
        return user_id, fuel_type, fuel_used, emissions

    # logs the calculation into the database.
    def log_calculation(self, user_id, fuel_type, fuel_used, emissions):
        try:
            # ? I would validate inputs here but im not sure.
            # What do you think I should do?

            # connect to the database
            with sqlite3.connect(self.db_path, timeout=30) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO emissions
                    (user_id, fuel_type, fuel_used, emissions)
                    VALUES (?, ?, ?, ?)""",
                    (user_id, fuel_type, fuel_used, emissions),
                )
                # return the log for testing purposes
                cursor.execute(
                    "SELECT fuel_type, "
                    "fuel_used, "
                    "emissions FROM "
                    "emissions WHERE "
                    "user_id = ? AND "
                    "fuel_type = ? AND "
                    "fuel_used = ? AND emissions = ?",
                    (user_id, fuel_type, fuel_used, emissions),
                )
            # used for testing purposes to assert accuracy of log
            log = cursor.fetchall()
            # commit and close database
            conn.commit()
            return log
        except sqlite3.Error as e:
            print(f"Database error: {e}")
