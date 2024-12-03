import sqlite3

# EDIT THIS FILE IF YOU NEED TO ADD EXTRA
# FUNCTIONALITY TO THE EMISSIONS CALCULATOR.


class EmissionsData:
    def __init__(self, data):
        self.data = data

    def get_emissions_factor(fuel_type: str):
        try:
            # connects to fuel_type_conversions database.
            conn = sqlite3.connect("fuel_type_conversions.db")
            cursor = conn.cursor()
            # finds conversion for specified fuel type
            cursor.execute(
                "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
                (fuel_type,),
            )
            result = cursor.fetchone()
            conn.close()
            # ends query and returns result
            if result:
                return result[0]
            # else it will raise a ValueError
            else:
                raise ValueError(f"Invalid fuel type: {fuel_type}")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return 0
        except ValueError as e:
            print(e)
            return 0


# class to make Emissions calculating easier.
class EmissionsCalculator:
    # EmissionsData is a class that holds the data for the emissions.
    def __init__(self, emissions_data, db_path="databases/emissions.db"):
        self.emissions_data = EmissionsData(emissions_data)
        self.db_path = db_path

        # calculates the emissions based on the fuel type and fuel used.

    def calculate_emissions(self, user_id, fuel_type, fuel_used: float):
        emissions_factor = self.emissions_data.get_emissions_factor(fuel_type)
        emissions = fuel_used * emissions_factor
        print(
            f"Carbon dioxide emissions for {fuel_used} units "
            f"of {fuel_type}: {emissions} kg"
        )
        self.log_calculation(user_id, fuel_type, fuel_used, emissions)
        return emissions

        # logs the calculation into the database.

    def log_calculation(self, user_id, fuel_type, fuel_used, emissions):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO emissions
                (user_id, fuel_type, fuel_used, emissions)
                VALUES (?, ?, ?, ?)""",
                (user_id, fuel_type, fuel_used, emissions),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
