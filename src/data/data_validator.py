import sqlite3

# validates user input and database data


class DataValidator:
    def validate_fuel_type(self, fuel_type: str) -> bool:
        conn = sqlite3.connect("databases/fuel_type_conversions.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fuel_type FROM fuel_types")
        fuel_types = cursor.fetchall()
        conn.close()
        if (fuel_type,) in fuel_types:
            return True
        else:
            return False

    def validate_fuel_used(self, fuel_used):
        if not isinstance(fuel_used, (int, float)) or fuel_used <= 0:
            return False
        if not self.validate_integer(fuel_used):
            return False
        return True

    def validate_user_id(self, user_id):
        if not isinstance(user_id, int) or user_id <= 0:
            return False
        if not self.validate_integer(user_id):
            return False
        return True

    def validate_emissions(self, emissions):
        if not isinstance(emissions, (int, float)) or emissions < 0:
            return False
        return True

    def validate_integer(self, integer):
        min_value = -9223372036854775808
        max_value = 9223372036854775807
        if not (min_value <= integer <= max_value):
            raise ValueError(f"{integer} is not a valid integer")
        return True
