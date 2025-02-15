import csv
import json
import logging
import os
import sqlite3
from typing import List

import chardet

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
            if len(missing_keys) > 0:
                logger.error(f"Missing required keys: {missing_keys}")
                raise ValueError(f"Missing required keys: {missing_keys}")
            for key in required_keys:
                if key not in entry or entry[key] is None or entry[key] == "":
                    logger.error(f"Missing value for key: {key}")
                    raise ValueError(f"Missing value for key: {key}")

        # Convert data to a list of tuples
        data = [
            (
                int(entry["user_id"]),
                entry["fuel_type"],
                float(entry["fuel_used"]),
                float(entry["emissions"]),
                entry["timestamp"],
            )
            for entry in data_dicts
        ]

        self.insert_data(data)
        logger.info(f"Data imported successfully from {self.input_path}")
        return data

    def import_from_csv(self) -> List[tuple]:
        # Initialize encoding to None before detection attempt
        encoding = None

        # Detect the file encoding
        try:
            with open(self.input_path, "rb") as file:
                raw_data = file.read()
                detected = chardet.detect(raw_data)
                encoding = detected["encoding"]
                confidence = detected["confidence"]
                logger.info(
                    f"Detected encoding: {encoding} with confidence: {confidence:.2%}"
                )

                if confidence < 0.6:
                    logger.warning(
                        f"Low confidence in encoding detection: {confidence:.2%}"
                    )
        except Exception as e:
            logger.error(f"Error detecting file encoding: {str(e)}")
            encoding = None

        # Fallback encodings to try if detection fails
        encodings_to_try = [
            enc
            for enc in [encoding, "utf-8", "utf-16", "iso-8859-1"]
            if enc is not None
        ]

        for enc in encodings_to_try:
            try:  # Tries to read with detected encoding, fall back to common encodings if it fails
                with open(
                    self.input_path, mode="r", encoding=enc, newline=""
                ) as csv_file:
                    reader = csv.DictReader(csv_file)
                    data_dicts = [row for row in reader]
                    logger.info(f"Successfully read file with encoding: {enc}")

                    required_keys = {
                        "user_id",
                        "fuel_type",
                        "fuel_used",
                        "emissions",
                        "timestamp",
                    }

                    for row in data_dicts:
                        missing_keys = required_keys - row.keys()
                        if len(missing_keys) > 0:
                            logger.error(
                                f"Missing required keys: {missing_keys}"
                            )
                            raise ValueError(
                                f"Missing required keys: {missing_keys}"
                            )
                        for key in required_keys:
                            if (
                                key not in row
                                or row[key] is None
                                or row[key] == ""
                            ):
                                logger.error(f"Missing value for key: {key}")
                                raise ValueError(
                                    f"Missing value for key: {key}"
                                )

                    # Convert data to a list of tuples
                    data = [
                        (
                            int(row["user_id"]),
                            row["fuel_type"],
                            float(row["fuel_used"]),
                            float(row["emissions"]),
                            row["timestamp"],
                        )
                        for row in data_dicts
                    ]

                    self.insert_data(data)
                    logger.info(
                        f"Data imported successfully from {self.input_path}"
                    )
                    return data

            except UnicodeDecodeError:
                logger.warning(f"Failed to read with encoding: {enc}")
                continue

        raise ValueError(
            f"Could not read file with any of the attempted encodings: {encodings_to_try}"
        )
