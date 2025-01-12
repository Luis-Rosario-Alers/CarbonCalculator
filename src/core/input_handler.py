from data.data_validator import DataValidator

# ! DEPRECATED - This class is no longer used in the emissions calculator.
# It has been replaced by the InputForms class.


class InputHandler:
    @staticmethod
    def get_user_input() -> tuple[int, str, float]:
        """Get user input for the emissions' calculator.
        Returns:
            Tuple[int, str, float]: A tuple containing the user input.
        """
        while True:
            try:
                user_id = int(input("Enter your user ID: "))
                if DataValidator.validate_user_id(user_id):
                    break
                print("Invalid user ID. Please enter a numeric value.")
            except ValueError as e:
                print(f"User ID: {e}")

        while True:
            fuel_type = input("Enter the fuel type: ")
            if DataValidator.validate_fuel_type(fuel_type):
                break
            print("Invalid fuel type. Please enter a valid fuel type.")

        while True:
            try:
                fuel_used = float(input("Enter the fuel used: "))
                if DataValidator.validate_fuel_used(fuel_used):
                    break
                print("Fuel used must be a positive number")
            except ValueError:
                print("Invalid input. Please enter a numeric value for fuel used.")

        return user_id, fuel_type, fuel_used
