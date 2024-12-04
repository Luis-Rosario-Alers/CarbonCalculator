from src.core.emissions_calculator import EmissionsCalculator
from src.core.input_handler import input_handler
from src.data.database import database_initialization

# introduction phase
print("Welcome to the Emissions Calculator!")
print("Please follow the instructions to calculate your emissions.")

# initialization phase
database_initialization()

# working phase
emissions_calculator = EmissionsCalculator()
userinput = input_handler.get_user_input()
result = emissions_calculator.calculate_emissions(
    userinput[0], userinput[1], userinput[2]
)
print("Emissions calculated successfully")
print(result)
