import sqlite3


class inputhandler:

    @staticmethod
    def fuel_type_check(fuel_type):
        conn = sqlite3.connect("databases/fuel_type_conversions.db")
        cursor = conn.cursor()
        cursor.execute("SELECT fuel_type FROM fuel_types ")
        fuel_types = cursor.fetchall()
        conn.close()
        if (fuel_type,) in fuel_types:
            return fuel_type
        else:
            print("Fuel type not found")
            return False

    @staticmethod
    def get_user_input() -> tuple[str, str, float]:
        """Get user input for the emissions' calculator.

        Returns:
            Tuple[str, str, float]: A tuple containing the user input.
        """
        while True:
            try:
                user_id = input("Enter your user ID: ")
                user_id = float(user_id)
                if user_id > 0:
                    break
                else:
                    print("User ID must be a positive integer")
            except ValueError as e:
                print(f"User ID: {e}")
        while True:
            try:
                fuel_type = input("Enter the fuel type: ")
                fuel_check = inputhandler.fuel_type_check(fuel_type)
                if not fuel_check:
                    print("invalid fuel type.")
                    print("try again")
                else:
                    break
            except ValueError as e:
                print(f"Fuel Type: {e}")
        while True:
            try:
                fuel_used = float(input("Enter the fuel used: "))
                if fuel_used <= 0:
                    print("Fuel used must be a positive number")
                else:
                    break
            except ValueError as e:
                print(f"Fuel Used: {e}")
        return user_id, fuel_type, fuel_used
