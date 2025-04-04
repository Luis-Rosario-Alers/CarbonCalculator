import json
import logging
import os
import sqlite3
import sys

from PySide6.QtCore import QObject, Signal

from utils.gui_utilities import connect_threaded

logger = logging.getLogger("data")


def determine_application_path():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        logger.info("determine_application_path: Running as a PyInstaller bundle")
        application_path = sys._MEIPASS
        databases_folder = os.path.join(application_path, "databases")
        logger.info(
            f"determine_application_path: Application path set to: {application_path}"
        )
        logger.info(
            f"determine_application_path: Databases folder set to: {databases_folder}"
        )
    else:
        logger.info("determine_application_path: Running as a script")
        application_path = os.path.dirname(__file__)
        databases_folder = os.path.join(application_path, "databases")
        logger.info(
            f"determine_application_path: Application path set to: {application_path}"
        )
        logger.info(
            f"determine_application_path: Databases folder set to: {databases_folder}"
        )
    return application_path, databases_folder


application_path, databases_folder = determine_application_path()


class databasesModel(QObject):
    databases_initialized = Signal()
    calculation_logged = Signal()

    def __init__(self):
        super().__init__()
        self.main_window_controller = None
        logger.debug("databasesModel.__init__: Initialized databases model")

    def set_controller(self, controller):
        self.main_window_controller = controller
        logger.debug(
            "databasesModel.set_controller: Controller set, connecting signals"
        )
        self.__connect_signals()

    def __connect_signals(self):
        logger.info("databasesModel.__connect_signals: Connecting signals")
        connect_threaded(
            self.main_window_controller,
            "initialization",
            self.database_initialization,
        )

    @staticmethod
    def setup_databases_folder():
        logger.info(
            "databasesModel.setup_databases_folder: Setting up databases folder"
        )
        if not os.path.exists(databases_folder):
            os.makedirs(databases_folder, exist_ok=True)
            logger.debug(
                f"databasesModel.setup_databases_folder: Created folder at {databases_folder}"
            )

    # function creates an emission's database during initialization of the program
    @staticmethod
    def initialize_emissions_database():
        logger.info(
            "databasesModel.initialize_emissions_database: Creating emissions database"
        )
        try:
            db_path = os.path.join(databases_folder, "emissions.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS emissions
                (user_id INTEGER, fuel_type TEXT, fuel_used REAL,
                emissions REAL, emissions_unit TEXT, temperature REAL, farming_technique TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(username))"""
            )
            conn.commit()
            conn.close()
            logger.info(
                "databasesModel.initialize_emissions_database: Emissions database created successfully"
            )
            return 1
        except sqlite3.Error as e:
            logger.error(
                f"databasesModel.initialize_emissions_database: Database error: {e}"
            )
            logger.error(
                "databasesModel.initialize_emissions_database: Emissions database not initialized"
            )
            return 0

    @staticmethod
    def initialize_user_data_database():
        logger.info(
            "databasesModel.initialize_user_data_database: Creating user data database"
        )
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
            logger.info(
                "databasesModel.initialize_user_data_database: User data database created successfully"
            )
            return 1
        except sqlite3.Error as e:
            logger.error(
                f"databasesModel.initialize_user_data_database: Database error: {e}"
            )
            logger.error(
                "databasesModel.initialize_user_data_database: User data database not initialized"
            )
            return 0

    @staticmethod
    def load_settings():
        logger.info("databasesModel.load_settings: Loading application settings")
        settings_dir = os.path.join(application_path, "resources", "config")
        settings_path = os.path.join(settings_dir, "settings.json")
        default_factors_path = os.path.join(
            application_path, "resources", "config", "conversion_factors"
        )
        try:
            with open(settings_path, "r") as file:
                settings = json.load(file)
                paths = settings.get("Paths")
                json_path = paths.get("emissions_modifiers_path")
                if not json_path:
                    logger.debug(
                        "databasesModel.load_settings: Using default emissions modifiers path"
                    )
                    json_path = os.path.join(
                        default_factors_path, "emissions_variables.json"
                    )
                    settings["Paths"]["emissions_modifiers_path"] = json_path
                    with open(settings_path, "w") as settings_file:
                        settings_file.write(json.dumps(settings, indent=4))
                return json_path
        except (json.JSONDecodeError, FileNotFoundError):
            logger.error("databasesModel.load_settings: Error loading settings file")
            return None

    @staticmethod
    def load_emissions_variables(json_path):
        logger.info(
            f"databasesModel.load_emissions_variables: Loading emissions variables from {json_path}"
        )
        try:
            with open(json_path, "r") as file:
                data = json.load(file)
                # Validate fuel types
                if not all(
                    "fuel_type" in fuel and "emissions_modifier" in fuel
                    for fuel in data.get("fuel_types", [])
                ):
                    logger.error(
                        "databasesModel.load_emissions_variables: Invalid fuel data format"
                    )
                    raise ValueError("Invalid fuel data")
                # Validate farming techniques
                if not all(
                    "technique" in tech and "emissions_modifier" in tech
                    for tech in data.get("farming_techniques", [])
                ):
                    logger.error(
                        "databasesModel.load_emissions_variables: Invalid farming technique data format"
                    )
                    raise ValueError("Invalid farming technique data")
                logger.debug(
                    f"databasesModel.load_emissions_variables: Successfully loaded data with {len(data.get('fuel_types', []))} fuel types"
                )
                return data
        except json.JSONDecodeError:
            logger.error(
                f"databasesModel.load_emissions_variables: Error loading data from {json_path}"
            )
            return None
        except FileNotFoundError:
            logger.error(
                f"databasesModel.load_emissions_variables: File not found: {json_path}"
            )
            return None
        except Exception as e:
            logger.error(
                f"databasesModel.load_emissions_variables: Unexpected error loading emissions variables: {e}"
            )
            return None

    @staticmethod
    def create_emissions_variables_database(db_path):
        """Create the emissions' variables database with both fuel types and farming techniques tables"""
        logger.info(
            f"databasesModel.create_emissions_variables_database: Creating database at {db_path}"
        )
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Create fuel types table
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS
                fuel_types (fuel_type TEXT PRIMARY KEY, emissions_modifier REAL)"""
            )

            # Create farming techniques table in the same database
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS
                farming_techniques (technique TEXT PRIMARY KEY, emissions_modifier REAL, description TEXT)"""
            )

            conn.commit()
            logger.info(
                "databasesModel.create_emissions_variables_database: Tables created successfully"
            )
            return conn
        except sqlite3.Error as e:
            logger.error(
                f"databasesModel.create_emissions_variables_database: Database error: {e}"
            )
            return None

    @staticmethod
    def insert_fuel_data(conn, fuel_data):
        """Insert fuel data into the fuel_types table"""
        logger.info(
            f"databasesModel.insert_fuel_data: Inserting {len(fuel_data)} fuel types"
        )
        try:
            cursor = conn.cursor()
            for fuel in fuel_data:
                cursor.execute(
                    "INSERT OR REPLACE INTO fuel_types VALUES (?, ?)",
                    (fuel["fuel_type"], fuel["emissions_modifier"]),
                )
            conn.commit()
            logger.debug(
                "databasesModel.insert_fuel_data: Fuel data inserted successfully"
            )
        except Exception as e:
            logger.error(
                f"databasesModel.insert_fuel_data: Error inserting fuel data: {e}"
            )

    @staticmethod
    def insert_farming_techniques(conn, farming_techniques_data):
        """Insert farming techniques into the database"""
        logger.info(
            f"databasesModel.insert_farming_techniques: Inserting {len(farming_techniques_data)} farming techniques"
        )
        try:
            cursor = conn.cursor()
            for technique in farming_techniques_data:
                # Get the description if available, otherwise use empty string
                description = technique.get("description", "")
                cursor.execute(
                    "INSERT OR REPLACE INTO farming_techniques VALUES (?, ?, ?)",
                    (
                        technique["technique"],
                        technique["emissions_modifier"],
                        description,
                    ),
                )
            conn.commit()
            logger.info(
                "databasesModel.insert_farming_techniques: Farming techniques inserted successfully"
            )
        except Exception as e:
            logger.error(
                f"databasesModel.insert_farming_techniques: Error inserting farming techniques: {e}"
            )

    def initialize_emissions_variables_database(self):
        """Initialize the emissions' variables database with fuel types and farming techniques"""
        logger.info(
            "databasesModel.initialize_emissions_variables_database: Initializing emissions variables database"
        )
        try:
            self.setup_databases_folder()
            db_path = os.path.join(databases_folder, "emissions_variables.db")

            # Remove existing database if it exists
            if os.path.exists(db_path):
                os.remove(db_path)
                logger.debug(
                    f"databasesModel.initialize_emissions_variables_database: Removed existing database at {db_path}"
                )

            # Load configuration data
            json_path = self.load_settings()
            if not json_path:
                logger.error(
                    "databasesModel.initialize_emissions_variables_database: Failed to load settings"
                )
                return 0
            logger.debug(
                f"databasesModel.initialize_emissions_variables_database: Loaded json path: {json_path}"
            )

            data = self.load_emissions_variables(json_path)
            if not data:
                logger.error(
                    "databasesModel.initialize_emissions_variables_database: Failed to load emissions data"
                )
                return 0
            logger.debug(
                "databasesModel.initialize_emissions_variables_database: Loaded emissions data successfully"
            )

            # Create a database with both tables
            conn = self.create_emissions_variables_database(db_path)
            if not conn:
                logger.error(
                    "databasesModel.initialize_emissions_variables_database: Failed to create database"
                )
                return 0

            # Initialize fuel types
            fuel_data = data.get("fuel_types", [])
            self.insert_fuel_data(conn, fuel_data)
            logger.info(
                "databasesModel.initialize_emissions_variables_database: Fuel type data initialized successfully"
            )

            # Initialize farming techniques in the same database
            farming_techniques_data = data.get("farming_techniques", [])
            self.insert_farming_techniques(conn, farming_techniques_data)
            logger.info(
                "databasesModel.initialize_emissions_variables_database: Farming techniques initialized successfully"
            )

            # Close connection
            conn.close()
            logger.debug(
                "databasesModel.initialize_emissions_variables_database: Database connection closed"
            )

            return 1

        except Exception as e:
            logger.error(
                f"databasesModel.initialize_emissions_variables_database: Unexpected error: {e}"
            )
            return 0

    @staticmethod
    def get_fuel_types():
        """Get a list of all fuel types from the database"""
        logger.info("databasesModel.get_fuel_types: Retrieving all fuel types")
        db_path = os.path.join(databases_folder, "emissions_variables.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT fuel_type FROM fuel_types")
        fuel_types = cursor.fetchall()
        conn.close()
        logger.debug(
            f"databasesModel.get_fuel_types: Retrieved {len(fuel_types)} fuel types"
        )
        return [fuel_type[0] for fuel_type in fuel_types]

    @staticmethod
    def get_farming_techniques():
        """Get a list of all farming techniques from the database"""
        logger.info(
            "databasesModel.get_farming_techniques: Retrieving all farming techniques"
        )
        db_path = os.path.join(databases_folder, "emissions_variables.db")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT technique FROM farming_techniques")
            techniques = cursor.fetchall()
            conn.close()
            logger.debug(
                f"databasesModel.get_farming_techniques: Retrieved {len(techniques)} techniques"
            )
            return [technique[0] for technique in techniques]
        except sqlite3.Error as e:
            logger.error(
                f"databasesModel.get_farming_techniques: Error getting farming techniques: {e}"
            )
            return []

    @staticmethod
    def get_farming_technique_info(info, technique=None):
        """
        Get information about farming techniques
        """
        logger.info(
            f"databasesModel.get_farming_technique_info: Retrieving info '{info}' for technique: {technique if technique else 'all'}"
        )
        db_path = os.path.join(databases_folder, "emissions_variables.db")
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            if technique:
                cursor.execute(
                    "SELECT technique, emissions_modifier, description FROM farming_techniques WHERE technique = ?",
                    (technique,),
                )
                row = cursor.fetchone()
                conn.close()

                if row:
                    technique_information = {
                        "technique": row[0],
                        "emissions_modifier": row[1],
                        "description": row[2],
                    }
                    return technique_information.get(info, None)
                logger.debug(
                    f"databasesModel.get_farming_technique_info: No information found for technique: {technique}"
                )
                return None
            else:
                cursor.execute(
                    "SELECT technique, emissions_modifier, description FROM farming_techniques"
                )
                rows = cursor.fetchall()
                conn.close()

                technique_information = [
                    {
                        "technique": row[0],
                        "emissions_modifier": row[1],
                        "description": row[2],
                    }
                    for row in rows
                ]

                logger.debug(
                    f"databasesModel.get_farming_technique_info: Retrieved information for {len(rows)} techniques"
                )
                return technique_information[0].get(info, None)
        except sqlite3.Error as e:
            logger.error(
                f"databasesModel.get_farming_technique_info: Error getting farming technique info: {e}"
            )
            return [] if technique is None else None

    @staticmethod
    def get_fuel_type_emissions_modifier(fuel_type: str) -> int:
        """Get the emissions factor for a specific fuel type"""
        logger.info(
            f"databasesModel.get_fuel_type_emissions_modifier: Getting modifier for {fuel_type}"
        )
        db_path = os.path.join(databases_folder, "emissions_variables.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emissions_modifier FROM fuel_types WHERE fuel_type = ?",
            (fuel_type,),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            logger.debug(
                f"databasesModel.get_fuel_type_emissions_modifier: Found modifier: {row[0]}"
            )
            return row[0]
        else:
            logger.error(
                f"databasesModel.get_fuel_type_emissions_modifier: No emissions modifier found for {fuel_type}"
            )
            raise ValueError(f"No emissions modifier found for fuel type: {fuel_type}")

    def log_transaction(
        self,
        user_id,
        fuel_type,
        fuel_unit,
        fuel_used,
        emissions,
        temperature,
        temperature_type,
        farming_technique=None,
        emissions_unit=None,
    ):
        try:
            logger.info("databasesModel.log_transaction: Logging new calculation")
            logger.info(
                f"databasesModel.log_transaction: User ID: {user_id}, Fuel Type: {fuel_type}, Fuel Used: {fuel_used} {fuel_unit}, "
                f"Emissions: {emissions} {emissions_unit}, Temperature: {temperature}{temperature_type[:1]}°, Farming Technique: {farming_technique}"
            )
            db_path = os.path.join(databases_folder, "emissions.db")

            # connect to the database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO emissions
                (user_id, fuel_type, fuel_used, emissions, emissions_unit, temperature, farming_technique)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    user_id,
                    fuel_type,
                    f"{fuel_used} {fuel_unit}",
                    f"{emissions:.2f}",
                    f"{emissions_unit}",
                    f"{temperature}°{temperature_type[:1]}",
                    farming_technique,
                ),
            )
            # Commit the transaction
            conn.commit()
            logger.debug(
                "databasesModel.log_transaction: Transaction committed to database"
            )
            logger.debug("databasesModel.log_transaction: Database connection closed")
            conn.close()
            self.calculation_logged.emit()
        except sqlite3.Error as e:
            logger.error(f"databasesModel.log_transaction: Database error: {e}")
            logger.error(e)
        except ValueError as e:
            logger.error(f"databasesModel.log_transaction: Value error: {e}")

    @staticmethod
    def get_emissions_history(
        time_frame=None,
        user_id=None,
        fuel_type=None,
        emissions_unit=None,
    ):
        """
        Get Emissions' History with optional filtering
        :param emissions_unit: The unit of measurement for emissions (e.g., kg CO2e)
        :param user_id: The ID of the user whose emissions history is being queried
        :param fuel_type: The type of fuel used (e.g., diesel, gasoline)
        :param time_frame: The time frame for the emission history Ex. "1/1/2025 -- 1/1/2026." Start - End.
        :returns: Emissions History for filter parameters
        """
        logger.info(
            f"databasesModel.get_emissions_history: Retrieving history with filters - time_frame: {time_frame}, user_id: {user_id}, fuel_type: {fuel_type}"
        )
        try:
            db_path = os.path.join(databases_folder, "emissions.db")
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM emissions WHERE 1=1"
                params = []

                if time_frame is not None:
                    query += " AND timestamp BETWEEN datetime(?) AND datetime(?)"
                    params.append(time_frame[0])
                    params.append(time_frame[1])

                if isinstance(user_id, str):
                    query += " AND user_id = ?"
                    params.append(user_id)
                if isinstance(fuel_type, str):
                    query += " AND fuel_type = ?"
                    params.append(fuel_type)
                if isinstance(emissions_unit, str):
                    query += " AND emissions_unit = ?"
                    params.append(emissions_unit)

                logger.debug(
                    f"databasesModel.get_emissions_history: Executing query with params: {params}"
                )
                cursor.execute(query, params)
                results = cursor.fetchall()
                logger.info(
                    f"databasesModel.get_emissions_history: Retrieved {len(results)} emission records"
                )
                return results
        except sqlite3.Error as e:
            logger.error(
                f"databasesModel.get_emissions_history: Error getting emissions history: {e}"
            )
            return []

    @staticmethod
    def get_all_user_ids():
        """Get all unique user IDs from the database"""
        logger.info("databasesModel.get_all_user_ids: Retrieving all unique user IDs")
        db_path = os.path.join(databases_folder, "emissions.db")
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT user_id FROM emissions")
            user_ids = [str(row[0]) for row in cursor.fetchall()]
            logger.debug(
                f"databasesModel.get_all_user_ids: Found {len(user_ids)} unique user IDs"
            )
            return user_ids

    def database_initialization(self):
        logger.info(
            "databasesModel.database_initialization: Starting database initialization"
        )
        if os.path.exists(databases_folder):
            logger.info(
                "databasesModel.database_initialization: Restarting emissions variables database"
            )
            self.initialize_emissions_variables_database()
        else:
            self.setup_databases_folder()
            logger.info(
                "databasesModel.database_initialization: Initializing all databases"
            )
            self.initialize_emissions_database()
            self.initialize_user_data_database()
            self.initialize_emissions_variables_database()

        # Emit signal that databases are initialized
        self.databases_initialized.emit()
        logger.info("databasesModel.database_initialization: All databases initialized")

    # function to test initialization of all databases
    # database_initialization()
