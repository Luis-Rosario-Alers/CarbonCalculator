import re
import sqlite3

# validates user input and database data


class DataValidator:
    def validate_fuel_type(fuel_type: str) -> bool:
        conn = sqlite3.connect("databases/fuel_type_conversions.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fuel_type FROM fuel_types")
        fuel_types = cursor.fetchall()
        conn.close()
        if (fuel_type,) in fuel_types:
            return True
        else:
            return False

    def validate_fuel_used(fuel_used):
        if not isinstance(fuel_used, (int, float)) or fuel_used <= 0:
            return False
        return True

    def validate_user_id(user_id):
        if not isinstance(user_id, int) or user_id <= 0:
            return False
        return True

    def validate_emissions(emissions):
        if not isinstance(emissions, (int, float)) or emissions < 0:
            return False
        return True
