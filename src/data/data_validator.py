import logging
import os

import aiosqlite

from data.database import application_path

# validates user input and database data

logger = logging.getLogger("data")


class DataValidator:
    @staticmethod
    async def validate_fuel_type(fuel_type: str) -> bool:
        logger.info("validating fuel_type")
        db_path = os.path.join(
            application_path, "databases", "fuel_type_conversions.db"
        )
        async with aiosqlite.connect(db_path) as conn:
            cursor = await conn.execute("SELECT fuel_type FROM fuel_types")
            fuel_types = await cursor.fetchone()
            logger.info("fuel_type_conversions.db accessed")
            logger.info(f"fuel_type accessed: {fuel_type}")
            if fuel_type in fuel_types:
                logger.info("fuel_type validated")
                await conn.close()
                return True
            else:
                logger.error("fuel_type invalid")
                await conn.close()
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
    def validate_emissions(self, emissions):
        if not isinstance(emissions, (int, float)) or emissions < 0:
            logger.error("emissions is not int or float")
            return False
        return True

    @staticmethod
    def validate_integer(self, integer):
        min_value = -9223372036854775808
        max_value = 9223372036854775807
        if not (min_value <= integer <= max_value):
            raise ValueError(f"{integer} is not a valid integer")
        return True
