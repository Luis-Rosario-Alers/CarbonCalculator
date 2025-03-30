import csv
import json
import logging
import os
import sqlite3

from data.database_model import databases_folder

logger = logging.getLogger("data")


class ExportManager:
    def __init__(self):
        self.db_path = os.path.join(databases_folder, "emissions.db")
        self.config_path = os.path.join(
            os.path.dirname(__file__),
            "resources",
            "config",
            "conversion_factors",
            "emissions_variables.json",
        )
        logger.debug(
            f"ExportManager.__init__: Initialized with database path: {self.db_path}"
        )

    def fetch_data(self):
        logger.info(
            "ExportManager.fetch_data: Retrieving emissions data from database"
        )
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT user_id, fuel_type, fuel_used, emissions, emissions_unit, temperature, farming_technique, timestamp FROM emissions"
        )
        data = cursor.fetchall()
        conn.close()
        logger.debug(
            f"ExportManager.fetch_data: Retrieved {len(data)} records"
        )
        return data

    def export_to_json(self, output_path):
        logger.info(
            f"ExportManager.export_to_json: Starting export to {output_path}"
        )
        data = self.fetch_data()

        # Convert data to a list of dictionaries
        data_dicts = [
            {
                "user_id": row[0],
                "fuel_type": row[1],
                "fuel_used": row[2],
                "emissions": row[3],
                "emissions_unit": row[4],
                "temperature": row[5],
                "farming_technique": row[6],
                "timestamp": row[7],
            }
            for row in data
        ]

        # Write data to JSON file
        with open(output_path, "w") as f:
            json.dump(data_dicts, f, indent=2)
        logger.info(
            f"ExportManager.export_to_json: Data exported to {output_path}"
        )
        logger.debug(
            f"ExportManager.export_to_json: Exported {len(data_dicts)} records"
        )

    def export_to_csv(self, output_path):
        logger.info(
            f"ExportManager.export_to_csv: Starting export to {output_path}"
        )
        data = self.fetch_data()

        # Write data to CSV file
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "user_id",
                    "fuel_type",
                    "fuel_used",
                    "emissions",
                    "emissions_unit",
                    "temperature",
                    "farming_technique",
                    "timestamp",
                ]
            )
            writer.writerows(data)
        logger.info(
            f"ExportManager.export_to_csv: Data exported to {output_path}"
        )
        logger.debug(
            f"ExportManager.export_to_csv: Exported {len(data)} records"
        )
