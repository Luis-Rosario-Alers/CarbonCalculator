import csv
import json
import logging
import os
import sqlite3

from data.database import databases_folder

logger = logging.getLogger("data")


class ImportManager:
    def __init__(self, input_path):
        self.input_path = input_path

    @staticmethod
    def insert_data(data):
        db_path = os.path.join(databases_folder, "emissions.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO emissions VALUES (?,?,?,?,?)", data)
        conn.commit()
        conn.close()

    def import_from_json(self):
        with open(self.input_path, "r") as f:
            data_dicts = json.load(f)

        required_keys = {
            "user_id",
            "fuel_type",
            "fuel_used",
            "emissions",
            "timestamp",
        }
        for entry in data_dicts:
            # Checks for missing keys by subtracting required
            # keys: 5 and entry.keys: 5 and then
            # assigns the difference of those 2 values to missing keys.
            missing_keys = required_keys - entry.keys()
            if (
                missing_keys
            ):  # if there are missing keys, it raises a value error with the amount missing.
                logger.error(f"Missing required keys: {missing_keys}")
                raise ValueError(f"Missing required keys: {missing_keys}")
            for (
                key
            ) in (
                required_keys
            ):  # iterates through each key and checks if they are null or empty.
                if key not in entry or entry[key] is None or entry[key] == "":
                    logger.error(f"Missing value for key: {key}")
                    raise ValueError(f"Missing value for key: {key}")

        # Convert data to a list of tuples
        data = [
            (
                entry["user_id"],
                entry["fuel_type"],
                entry["fuel_used"],
                entry["emissions"],
                entry["timestamp"],
            )
            for entry in data_dicts
        ]

        self.insert_data(data)
        logger.info(f"Data imported successfully from {self.input_path}")
        return data

    def import_from_csv(self):
        with open(self.input_path, mode="r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            data_dicts = [row for row in reader]
            # Check for required keys
            required_keys = {
                "user_id",
                "fuel_type",
                "fuel_used",
                "emissions",
                "timestamp",
            }
            for row in data_dicts:
                print(f"Processing row: {row}")
                # Checks for missing keys by subtracting
                # required keys: 5 and entry.keys: 5 and then
                # assigns the difference of those 2 values to missing keys.
                missing_keys = required_keys - row.keys()
                if missing_keys:  # if there are missing keys,
                    # it raises a value error with the amount missing.
                    logger.error(f"Missing required keys: {missing_keys}")
                    raise ValueError(f"Missing required keys: {missing_keys}")
                for key in required_keys:
                    # iterates through each key and checks if they are null or empty.
                    if key not in row or row[key] is None or row[key] == "":
                        logger.error(f"Missing value for key: {key}")
                        raise ValueError(f"Missing value for key: {key}")

            # Convert data to a list of tuples
        data = [
            (
                row["user_id"],
                row["fuel_type"],
                row["fuel_used"],
                row["emissions"],
                row["timestamp"],
            )
            for row in data_dicts
        ]

        print(f"Data to be inserted: {data}")
        self.insert_data(data)
        logger.info(f"Data imported successfully from {self.input_path}")
        return data
