import logging
import os
import sqlite3

from data.data_validator import DataValidator

# * EDIT THIS FILE IF YOU NEED TO ADD EXTRA FUNCTIONALITY TO THE EMISSIONS CALCULATOR.

logger = logging.getLogger("core")


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

    def calculate_emissions(
        self,
        user_id,
        fuel_type,
        fuel_used: float,
        temperature=None,
        temperature_type=None,
    ):
        """
        Calculate the emissions based on the fuel type, fuel used, and optional temperature data.

        Parameters:
        user_id (str): The ID of the user.
        fuel_type (str): The type of fuel used.
        fuel_used (float): The amount of fuel used.
        temperature (float, optional): The temperature at which the fuel is used. Defaults to None.
        temperature_type (int, optional): The type of temperature provided (0 for Celsius, 1 for Fahrenheit, 2 for Kelvin). Defaults to None.

        Returns:
        tuple: A tuple containing user_id, fuel_type, fuel_used, and calculated emissions.

        Raises:
        ValueError: If any of the inputs are invalid or if the calculated emissions data is invalid.
        """
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
        emissions_factor = cursor.fetchone()[0]
        conn.close()
        # * Check This ⬇️ if emissions tests have failed
        if temperature is not None and temperature_type is not None:
            logger.info("Temperature data available, adjusting emissions factor")
            baseline_temperature = [
                15,
                59,
                288.15,
            ]  # Baseline temperatures in Celsius, Fahrenheit, and Kelvin
            temp_deviation = (
                temperature - baseline_temperature[temperature_type]
            ) / baseline_temperature[temperature_type]
            adjusted_emissions_factor = emissions_factor * (1 + temp_deviation**2)
            emissions = fuel_used * adjusted_emissions_factor
            if not data_validator.validate_emissions(emissions):
                raise ValueError("Invalid emissions data")
            self.log_calculation(user_id, fuel_type, fuel_used, emissions)
            return user_id, fuel_type, fuel_used, emissions
        else:
            logger.info(
                "Temperature data not available, using standard emissions factor"
            )
            emissions = fuel_used * emissions_factor
            if not data_validator.validate_emissions(emissions):
                raise ValueError("Invalid emissions data")
            self.log_calculation(user_id, fuel_type, fuel_used, emissions)
            return user_id, fuel_type, fuel_used, emissions

    # logs the calculation into the database.
    def log_calculation(self, user_id, fuel_type, fuel_used, emissions):
        try:
            # ? I would validate inputs here but im not sure.
            # What do you think I should do?

            logger.info("Logging calculation")
            logger.info(
                f"User ID: {user_id}, Fuel Type: {fuel_type}, Fuel Used: {fuel_used}, Emissions: {emissions}"
            )

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
        except sqlite3.Error or OverflowError as e:
            logging.getLogger("data").error(f"Database error: {e}")
