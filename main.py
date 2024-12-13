import os

from src.data.export_manager import ExportManager
from src.core.emissions_calculator import EmissionsCalculator
from src.core.input_handler import inputhandler
from src.data.database import database_initialization
from src.data.import_manager import importmanager

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Navigate up the directory tree to reach the root CarbonCalculator folder
root_dir = os.path.dirname(current_file_path)


# introduction phase
print("Welcome to the Emissions Calculator!")
print("Please follow the instructions to calculate your emissions.")

# initialization phase
database_initialization()

# working phase
emissions_calculator = EmissionsCalculator()
userinput = inputhandler.get_user_input()
result = emissions_calculator.calculate_emissions(
    userinput[0], userinput[1], userinput[2]
)
print("Emissions calculated successfully")
print(result)

# export phase
if input("Do you want to export the data? (y/n): ").lower() == "y":
    # TODO: eventually we will make the user be able to choose output directory and format
    output_path = input("Enter the path you want to export to: ")
    export_manager = ExportManager("databases/emissions.db")
    export_format = input("Do you want to export to JSON or CSV? (json/csv): ").lower()
    output_path = os.path.join(output_path, "output." + export_format)
    if export_format == "json":
        export_manager.export_to_json(output_path)
    elif export_format == "csv":
        export_manager.export_to_csv(output_path)
    else:
        print("Invalid format. Data not exported.")
        exit(1)
    print(f"Data exported to {output_path}")


# import phase
elif input("Do you want to import data? (y/n): ").lower() == "y":
    import_format = input(
        "Do you want to import from CSV or JSON? (csv/json): "
    ).lower()
    if import_format == "csv":
        input_path = input("Enter the path of the CSV file you want to import: ")
        import_manager = importmanager(input_path)
        import_manager.import_from_csv()
    elif import_format == "json":
        input_path = input("Enter the path of the JSON file you want to import: ")
        import_manager = importmanager(input_path)
        import_manager.import_from_json()
    else:
        print("Invalid format. Data not imported.")
        exit(1)

print("Thank you for using the Emissions Calculator!")
print("Goodbye!")
exit(0)
