import csv
import json
import sqlite3


class ImportManager:
    def __init__(self, input_path):
        self.input_path = input_path

    def insert_data(self, data):
        conn = sqlite3.connect("databases/emissions.db")
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO emissions VALUES (?,?,?,?,?)", data)
        conn.commit()
        conn.close()
        print(f"Data imported successfully from {self.input_path}")

    def import_from_json(self):
        with open(self.input_path, "r") as f:
            data_dicts = json.load(f)

        required_keys = {"user_id", "fuel_type", "fuel_used", "emissions", "timestamp"}
        for entry in data_dicts:
            # Checks for missing keys by subtracting required
            # keys: 5 and entry.keys: 5 and then
            # assigns the difference of those 2 values to missing keys.
            missing_keys = required_keys - entry.keys()
            if (
                missing_keys
            ):  # if there are missing keys, it raises a value error with the amount missing.
                raise ValueError(f"Missing required keys: {missing_keys}")
            for (
                key
            ) in (
                required_keys
            ):  # iterates through each key and checks if they are null or empty.
                if entry[key] is None or entry[key] == "":
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
                    raise ValueError(f"Missing required keys: {missing_keys}")
                for key in required_keys:
                    # iterates through each key and checks if they are null or empty.
                    if row[key] is None or row[key] == "":
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
        return data

    def export_to_csv(self, file_path):
        conn = sqlite3.connect("databases/emissions.db")
        cursor = conn.cursor()
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "fuel_type", "fuel_used", "emissions"])
            for row in cursor.execute(
                "SELECT user_id, fuel_type, fuel_used, emissions FROM emissions"
            ):
                writer.writerow(row)
        conn.close()

    def export_to_json(self, file_path):
        conn = sqlite3.connect("databases/emissions.db")
        cursor = conn.cursor()
        with open(file_path, "w") as file:
            data = []
            for row in cursor.execute(
                "SELECT user_id, fuel_type, fuel_used, emissions FROM emissions"
            ):
                data.append(
                    {
                        "user_id": row[0],
                        "fuel_type": row[1],
                        "fuel_used": row[2],
                        "emissions": row[3],
                    }
                )
            json.dump(data, file, indent=4)
        conn.close()
