import logging
import os
import sqlite3

from data.database import databases_folder

# validates user input and database data

logger = logging.getLogger("data")


class DataValidator:
    @staticmethod
    def validate_fuel_type(fuel_type: str) -> bool:
        logger.info("validating fuel_type")
        db_path = os.path.join(databases_folder, "fuel_type_conversions.db")

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT fuel_type FROM fuel_types")
            fuel_types = cursor.fetchone()
            logger.info("fuel_type_conversions.db accessed")
            if fuel_type in fuel_types:
                logger.info(f"fuel_type accessed: {fuel_type}")
                logger.info("fuel_type validated")
                return True
            else:
                logger.info(f"fuel_type accessed: {fuel_type}")
                logger.error("fuel_type invalid")
                return False

    def validate_fuel_used(self, fuel_used):
        if not isinstance(fuel_used, (int, float)) or fuel_used <= 0:
            logger.error("fuel_used is not an int or float data type")
            return False
        if not self.validate_integer(fuel_used):
            return False
        logger.info("fuel_used validated")
        return True

    def validate_user_id(self, user_id):
        if not isinstance(user_id, int) or user_id <= 0:
            logger.error("user_id is not an int data type")
            return False
        if not self.validate_integer(user_id):
            return False
        logger.info("user_id validated")
        return True

    @staticmethod
    def validate_emissions_result(emissions):
        if not isinstance(emissions, (int, float)) or emissions < 0:
            logger.error("emissions is not int or float")
            return False
        return True

    @staticmethod
    def validate_integer(integer):
        min_value = -9223372036854775808  # minimum value for a 64-bit integer
        max_value = 9223372036854775807  # maximum value for a 64-bit integer
        if not (min_value <= integer <= max_value):
            raise ValueError(f"{integer} is not a valid integer")
        return True

    @staticmethod
    def validate_temperature_type(temperature_type):
        if not isinstance(temperature_type, str):
            raise ValueError(
                f"{temperature_type} is not a valid temperature type"
            )
        return

    @staticmethod
    def validate_temperature(temperature, temperature_type):
        if not isinstance(temperature, (int, float)) or not isinstance(
            temperature_type, str
        ):
            raise ValueError(f"{temperature} is not a valid temperature")
        if temperature_type == "Celsius":  # Celsius
            if temperature < -273.15:
                raise ValueError(f"{temperature} is not a valid temperature")
        elif temperature_type == "Fahrenheit":  # Fahrenheit
            if temperature < -459.67:
                raise ValueError(f"{temperature} is not a valid temperature")
        elif temperature_type == "Kelvin":  # Kelvin
            if temperature <= 0:
                raise ValueError(f"{temperature} is not a valid temperature")
        return True  # if all checks pass
