import json
import logging
import os
import sqlite3
import sys

from PySide6.QtCore import QObject, Signal

from src.utils.gui_utilities import connect_threaded

logger = logging.getLogger("data")


def determine_application_path():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        logger.info("Running as a PyInstaller bundle")
        application_path = sys._MEIPASS
        databases_folder = os.path.join(application_path, "databases")
        logger.info(f"Application path set to: {application_path}")
        logger.info(f"Databases folder set to: {databases_folder}")
    else:
        logger.info("Running as a script")
        application_path = os.path.dirname(__file__)
        databases_folder = os.path.join(application_path, "databases")
        logger.info(f"Application path set to: {application_path}")
        logger.info(f"Databases folder set to: {databases_folder}")
    return application_path, databases_folder


application_path, databases_folder = determine_application_path()


# function to bundle initialization of all databases
class databasesModel(QObject):
    databases_initialized = Signal()
    calculation_logged = Signal()

    def __init__(self):
        super().__init__()
        self.main_window_controller = None

    def set_controller(self, controller):
        self.main_window_controller = controller
        self.__connect_signals()

    def __connect_signals(self):
        logger.info("Connecting signals.")
        connect_threaded(
            self.main_window_controller,
            "initialization",
            self.database_initialization,
        )

    @staticmethod
    def setup_databases_folder():
        if not os.path.exists(databases_folder):
            os.makedirs(databases_folder, exist_ok=True)

    # function creates an emission's database during initialization of the program
    @staticmethod
    def initialize_emissions_database():
        try:
            db_path = os.path.join(databases_folder, "emissions.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS emissions
                (user_id INTEGER, fuel_type TEXT, fuel_used REAL,
                emissions REAL, farming_technique TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(username))"""
            )
            conn.commit()
            conn.close()
            return 1
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            logger.error("Emissions database not initialized")
            return 0

    @staticmethod
    def initialize_user_data_database():
        try:
            db_path = os.path.join(databases_folder, "user_data.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users
                (username TEXT PRIMARY KEY, password TEXT)"""
            )
            conn.commit()
            conn.close()
            return 1
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            logger.error("User data database not initialized")
            return 0

    @staticmethod
    def load_settings():
        settings_dir = os.path.join(application_path, "resources", "config")
        settings_path = os.path.join(settings_dir, "settings.json")
        default_factors_path = os.path.join(
            application_path, "resources", "config", "conversion_factors"
        )
        try:
            with open(settings_path, "r") as file:
                settings = json.load(file)
                json_path = settings.get("emissions_factors_path")
                if not json_path:
                    json_path = os.path.join(
                        default_factors_path, "fuel_types.json"
                    )
                    settings["emissions_factors_path"] = json_path
                    with open(settings_path, "w") as settings_file:
                        settings_file.write(json.dumps(settings, indent=4))
                return json_path
        except (json.JSONDecodeError, FileNotFoundError):
            logger.error("Error loading settings file")
            return None

    @staticmethod
    def load_emissions_variables(json_path):
        try:
            with open(json_path, "r") as file:
                fuel_data = json.load(file)
                if not all(
                    "fuel_type" in fuel and "emissions_factor" in fuel
                    for fuel in fuel_data
                ):
                    raise ValueError("Invalid fuel data")
                return fuel_data
        except json.JSONDecodeError:
            logger.error(f"Error loading fuel type data from {json_path}")
            return None
        except FileNotFoundError:
            logger.error(f"File not found: {json_path}")
            return None

    @staticmethod
    def create_emissions_variables_database(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS
                fuel_types (fuel_type TEXT PRIMARY KEY, emissions_factor REAL)"""
            )
            conn.commit()
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return None

    @staticmethod
    def insert_fuel_data(db_path, fuel_data):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            for fuel in fuel_data:
                cursor.execute(
                    "INSERT OR IGNORE INTO fuel_types VALUES (?, ?)",
                    (fuel["fuel_type"], fuel["emissions_factor"]),
                )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error inserting fuel data: {e}")

    def initialize_emissions_variables_database(self):
        try:
            self.setup_databases_folder()
            db_path = os.path.join(databases_folder, "emissions_variables.db")
            if os.path.exists(db_path):
                os.remove(db_path)
            json_path = self.load_settings()
            if not json_path:
                return 0
            logger.debug(f"Loaded json path: {json_path}")

            fuel_data = self.load_emissions_variables(json_path)
            if not fuel_data:
                return 0
            logger.debug(f"Loaded fuel data: {fuel_data}")

            conn = self.create_emissions_variables_database(db_path)
            if not conn:
                return 0
            logger.debug("Database initialized")

            self.insert_fuel_data(db_path, fuel_data)
            logger.info("Fuel type database initialized successfully")
            conn.close()
            return 1

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return 0

    @staticmethod
    def get_fuel_types():
        db_path = os.path.join(databases_folder, "fuel_type_conversions.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT fuel_type FROM fuel_types")
        fuel_types = cursor.fetchall()
        conn.close()
        return [fuel_type[0] for fuel_type in fuel_types]

    @staticmethod
    def get_emissions_factor(fuel_type: str) -> int:
        db_path = os.path.join(databases_folder, "fuel_type_conversions.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
            (fuel_type,),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        else:
            raise ValueError(
                f"No emissions factor found for fuel type: {fuel_type}"
            )

    def log_calculation(
        self, user_id, fuel_type, fuel_used, emissions, farming_technique
    ):
        try:
            logger.info("Logging calculation")
            logger.info(
                f"User ID: {user_id}, Fuel Type: {fuel_type}, Fuel Used: {fuel_used}, Emissions: {emissions}, Farming Technique: {farming_technique}"
            )
            db_path = os.path.join(databases_folder, "emissions.db")

            # connect to the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO emissions
                (user_id, fuel_type, fuel_used, emissions, farming_technique)
                VALUES (?, ?, ?, ?, ?)""",
                (user_id, fuel_type, fuel_used, emissions, farming_technique),
            )
            # Commit the transaction
            conn.commit()

            # Return the log for testing purposes
            cursor.execute(
                "SELECT fuel_type, fuel_used, emissions, farming_technique FROM emissions WHERE user_id = ? AND fuel_type = ? AND "
                "fuel_used = ? AND emissions = ? AND farming_technique = ?",
                (user_id, fuel_type, fuel_used, emissions, farming_technique),
            )
            log = cursor.fetchall()
            conn.close()
            self.calculation_logged.emit()
            return log
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            logger.error(e)
        except ValueError as e:
            logger.error(f"Value error: {e}")

    def database_initialization(self):
        logger.info("Received initialization signal, initializing databases")
        if os.path.exists(databases_folder):
            logger.info("restarting fuel_type database"),
            self.initialize_emissions_variables()
        else:
            self.setup_databases_folder()
            logger.info("Initializing databases"),
            self.initialize_emissions_database()
            self.initialize_user_data_database()
            self.initialize_emissions_variables_database()

        # Emit signal that databases are initialized
        self.databases_initialized.emit()
        logger.info("Databases initialized")

    # function to test initialization of all databases
    # database_initialization()
