"""
Generate fake emissions data for testing the CarbonCalculator application.
This script creates JSON and CSV files with fake emissions data that match the structure
expected by the application's import functionality.
"""

import datetime
import json
import os
import random  # nosec B311
from typing import Any, Dict, List


def generate_test_data(num_records: int = 100) -> List[Dict[str, Any]]:
    """
    Generate fake emissions data for testing.

    :param num_records: Number of records to generate (default: 100)

    :return: List of dictionaries containing fake emissions data
    """
    # Available options in the application
    fuel_types = [
        "gasoline",
        "diesel",
        "biodiesel",
        "natural gas",
        "propane",
        "ethanol",
    ]
    farming_techniques = [
        "Conventional",
        "Organic",
        "No-Till",
        "Conservation",
        "Precision",
    ]
    fuel_units = ["Liters", "Cubic Meters", "Cubic Feet"]
    emissions_units = ["Milligrams", "Grams", "Kilograms", "Metric Tons"]
    temperature_types = ["Celsius", "Fahrenheit", "Kelvin"]

    # User IDs range (1-10 for test data)
    user_ids = list(range(1, 11))

    # Baseline dates for the past year
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)

    test_data = []

    for _ in range(num_records):
        # Generate random timestamp within the past year
        random_days = random.randint(0, 365)
        timestamp = (start_date + datetime.timedelta(days=random_days)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Random selections
        user_id = random.choice(user_ids)
        fuel_type = random.choice(fuel_types)
        fuel_unit = random.choice(fuel_units)
        emissions_unit = random.choice(emissions_units)
        farming_technique = random.choice(farming_techniques)
        temperature_type = random.choice(temperature_types)

        # Random numeric values
        fuel_used = round(random.uniform(1.0, 100.0), 2)

        # Generate appropriate temperature based on the unit
        if temperature_type == "Celsius":
            temperature = round(random.uniform(-10.0, 45.0), 1)
        elif temperature_type == "Fahrenheit":
            temperature = round(random.uniform(0.0, 110.0), 1)
        else:  # Kelvin
            temperature = round(random.uniform(250.0, 320.0), 1)

        # Calculate fake emissions (simplified formula for test data)
        if emissions_unit == "Milligrams":
            emissions = round(fuel_used * random.uniform(100, 500), 2)
        elif emissions_unit == "Grams":
            emissions = round(fuel_used * random.uniform(10, 50), 2)
        elif emissions_unit == "Kilograms":
            emissions = round(fuel_used * random.uniform(0.1, 5.0), 2)
        else:  # Metric Tons
            emissions = round(fuel_used * random.uniform(0.0001, 0.01), 4)

        # Format values with units as stored in database
        fuel_used_formatted = f"{fuel_used} {fuel_unit}"
        emissions_formatted = f"{emissions:.2f}"
        temperature_formatted = f"{temperature}{temperature_type[0]}"

        record = {
            "user_id": user_id,
            "fuel_type": fuel_type,
            "fuel_used": fuel_used_formatted,
            "emissions": emissions_formatted,
            "emissions_unit": emissions_unit,
            "temperature": temperature_formatted,
            "farming_technique": farming_technique,
            "timestamp": timestamp,
        }

        test_data.append(record)

    return test_data


def save_to_json(
    data: List[Dict[str, Any]], filename: str = "test_emissions_data.json"
) -> str:
    """
    Save generated data to a JSON file.

    :param data: List of dictionaries containing emissions data
    :param filename: Output filename (default: test_emissions_data.json)

    :return: Path to the saved file
    """
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return filepath


def save_to_csv(
    data: List[Dict[str, Any]], filename: str = "test_emissions_data.csv"
) -> str:
    """
    Save generated data to a CSV file.

    :param data: List of dictionaries containing emissions data
    :param filename: Output filename (default: test_emissions_data.csv)

    :return: Path to the saved file
    """
    filepath = os.path.join(os.getcwd(), filename)

    # Create CSV header and rows
    header = "user_id,fuel_type,fuel_used,emissions,emissions_unit,temperature,farming_technique,timestamp\n"

    with open(filepath, "w") as f:
        f.write(header)
        for record in data:
            row = (
                f"{record['user_id']},{record['fuel_type']},{record['fuel_used']},"
                f"{record['emissions']},{record['emissions_unit']},{record['temperature']},"
                f"{record['farming_technique']},{record['timestamp']}\n"
            )
            f.write(row)

    return filepath


if __name__ == "__main__":
    # Generate 10,000 test records
    print("Generating fake emissions test data...")
    test_data = generate_test_data(1000)

    # Save as JSON
    json_path = save_to_json(test_data)
    print(f"JSON test data saved to: {json_path}")

    # Save as CSV
    csv_path = save_to_csv(test_data)
    print(f"CSV test data saved to: {csv_path}")

    print(f"Generated {len(test_data)} test records in both JSON and CSV formats.")
    print(
        "You can now import these files into your CarbonCalculator application for testing."
    )
