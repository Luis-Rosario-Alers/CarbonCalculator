import csv
import json
import logging
import os
import sqlite3

from data.database import databases_folder

logger = logging.getLogger("data")


class ExportManager:
    def __init__(self):
        self.db_path = os.path.join(databases_folder, "emissions.db")

    def fetch_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emissions")
        data = cursor.fetchall()
        conn.close()
        return data

    def export_to_json(self, output_path):
        data = self.fetch_data()

        # Convert data to a list of dictionaries
        data_dicts = [
            {
                "user_id": row[0],
                "fuel_type": row[1],
                "fuel_used": row[2],
                "emissions": row[3],
                "timestamp": row[4],
            }
            for row in data
        ]

        # Write data to JSON file
        with open(output_path, "w") as f:
            json.dump(data_dicts, f, indent=2)
        logger.info(f"Data exported to {output_path}")

    def export_to_csv(self, output_path):
        data = self.fetch_data()
        # Write data to CSV file
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["user_id", "fuel_type", "fuel_used", "emissions", "timestamp"]
            )
            writer.writerows(data)
        logger.info(f"Data exported to {output_path}")
