import os
import sqlite3

# EDIT THIS FILE IF YOU NEED TO ADD EXTRA
# FUNCTIONALITY TO THE EMISSIONS CALCULATOR.


# class to make Emissions calculating easier.
class EmissionsCalculator:
    # EmissionsData is a class that holds the data for the emissions.
    def __init__(
        self,
        emissions_conversions=os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "databases",
                "fuel_type_conversions.db",
            )
        ),
        db_path=os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "databases", "emissions.db"
            )
        ),
    ):
        self.emissions_conversions = emissions_conversions
        self.db_path = db_path

        # calculates the emissions based on the fuel type and fuel used.
        """
         TODO: add functionality to able to change
         fuel_used to tonnes, gallons, etc.
        """

    def calculate_emissions(self, user_id, fuel_type, fuel_used: float):
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
        emissions = fuel_used * emissions_factor
        print(
            # outputs emissions in kg units of CO2
            f"Carbon dioxide emissions for {fuel_used} units "
            f"of {fuel_type}: {emissions} kg"
        )
        self.log_calculation(user_id, fuel_type, fuel_used, emissions)
        # We are returning the emissions value
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
