import json
import logging
import os
import shutil
from unittest.mock import patch

import aiosqlite
import pytest

from src.data.database_model import (
    create_fuel_type_database,
    database_initialization,
    determine_application_path,
    get_emissions_factor,
    get_fuel_types,
    initialize_emissions_database,
    initialize_fuel_type_database,
    initialize_user_data_database,
    insert_fuel_data,
    load_fuel_data,
    load_settings,
    log_calculation,
    setup_databases_folder,
)

# Handle a case when sys.frozen exists but sys._MEIPASS does not


class TestDatabase:
    def test_determine_path_with_frozen_but_no_meipass(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mock_sys_frozen = mocker.patch(  # noqa
            "sys.frozen", new=True, create=True  # noqa
        )  # noqa
        mock_dirname = mocker.patch("os.path.dirname")
        mock_dirname.return_value = "/tests/data"
        mock_join = mocker.patch("os.path.join")
        mock_join.return_value = "/tests/data/databases"

        # Act
        app_path, db_folder = determine_application_path()

        # Assert
        assert app_path == "/tests/data"
        assert db_folder == "/tests/data/databases"
        mock_dirname.assert_called_once()
        mock_join.assert_called_once_with("/tests/data", "databases")
        mock_logger.info.assert_any_call("Running as a script")
        mock_logger.info.assert_any_call(f"Application path set to: {app_path}")
        mock_logger.info.assert_any_call(f"Databases folder set to: {db_folder}")

    def test_determine_path_with_frozen_and_meipass(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mock_sys_frozen = mocker.patch(  # noqa
            "sys.frozen", new=True, create=True
        )  # noqa
        mock_sys_meipass = mocker.patch(  # noqa
            "sys._MEIPASS", new="/tests/data", create=True  # noqa
        )  # noqa
        mock_join = mocker.patch("os.path.join")
        mock_join.return_value = "/tests/data/databases"

        # Act
        app_path, db_folder = determine_application_path()

        # Assert
        assert app_path == "/tests/data"
        assert db_folder == "/tests/data/databases"
        mock_join.assert_called_once()
        mock_join.assert_called_once_with("/tests/data", "databases")
        mock_logger.info.assert_any_call("Running as a PyInstaller bundle")
        mock_logger.info.assert_any_call(f"Application path set to: {app_path}")
        mock_logger.info.assert_any_call(f"Databases folder set to: {db_folder}")

    # Handle a case when databases_folder path doesn't exist
    @pytest.mark.asyncio
    async def test_handles_nonexistent_database_folder(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mocker.patch("os.path.join", return_value="/nonexistent/path/emissions.db")

        # Act
        result = await initialize_emissions_database()

        # Assert
        assert result == 0
        mock_logger.error.assert_called_with("Emissions database not initialized")

    # Successfully creates emission table when a database doesn't exist
    @pytest.mark.asyncio
    async def test_creates_emissions_table_when_db_not_exists(self, mocker):
        # Arrange
        mock_db_path = "test_emissions.db"
        mocker.patch("os.path.join", return_value=mock_db_path)

        # Act
        await initialize_emissions_database()

        # Assert
        async with aiosqlite.connect(mock_db_path) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name='emissions'
                """
                )
                table_exists = await cursor.fetchone() is not None
                assert table_exists is True

        # Teardown
        try:
            os.remove(mock_db_path)
        except FileNotFoundError:
            pass

    # Successfully creates users' table when a database doesn't exist
    @pytest.mark.asyncio
    async def test_creates_users_table_when_db_not_exists(self, mocker, caplog):
        # Arrange
        caplog.set_level(logging.DEBUG)
        mock_db_path = "user_data.db"
        mocker.patch("os.path.join", return_value=mock_db_path)

        # Act
        await initialize_user_data_database()
        print(caplog.text)

        # Assert
        async with aiosqlite.connect(mock_db_path) as conn:
            async with await conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
                )
                table = await cursor.fetchone()
                assert table is not None
                assert table[0] == "users"

        # Teardown
        try:
            import os

            os.remove(mock_db_path)
        except FileNotFoundError:
            pass

    # Handle database connection errors gracefully
    @pytest.mark.asyncio
    async def test_database_connection_error(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mock_aiosqlite = mocker.patch("aiosqlite.connect")
        mock_aiosqlite.side_effect = aiosqlite.Error("Connection failed")

        # Act
        result = await initialize_user_data_database()

        # Assert
        assert result == 0

        # Assert that the logger is called with the correct message
        mock_logger.error.assert_called_with("User data database not initialized")

    # Database connection is established successfully and table is created
    @pytest.mark.asyncio
    async def test_successful_user_data_database_initialization(self, mocker):
        # Arrange
        mock_conn = mocker.AsyncMock()
        mock_cursor = mocker.AsyncMock()

        # Act
        with patch("aiosqlite.connect", return_value=mock_conn):
            mock_conn.__aenter__.return_value = mock_conn
            mock_conn.__aexit__.return_value = None
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.__aenter__.return_value = mock_cursor
            mock_cursor.__aexit__.return_value = None
            await initialize_user_data_database()

        # Assert | Be careful as this test can fail if the text of this assertion changes
        mock_cursor.execute.assert_called_once_with(
            """CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY, password TEXT)"""
        )
        mock_conn.commit.assert_called_once()

    # Handles invalid db_path parameter
    @pytest.mark.asyncio
    async def test_handles_invalid_db_path(self):
        # Arrange
        invalid_path = "/invalid/path/test1.db"

        # Act
        result = await create_fuel_type_database(invalid_path)

        # Assert
        assert result is None

    # Successfully creates a fuel type database without fuel_type data applied yet
    @pytest.mark.asyncio
    async def test_create_fuel_type_database(self, mocker):
        # Arrange
        mock_conn = mocker.AsyncMock()
        mock_cursor = mocker.AsyncMock()
        mock_aiosqlite = mocker.patch("aiosqlite.connect")
        mock_aiosqlite.return_value.__aenter__.return_value = mock_conn
        mock_conn.__aexit__.return_value = None
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
        mock_cursor.__aexit__.return_value = None

        # Act
        result = await create_fuel_type_database("test/path/emissions_variables.json")

        # Assert
        assert result is mock_conn
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    # Successfully creates and initializes a fuel type database with valid settings and data
    @pytest.mark.asyncio
    async def test_successful_fuel_type_database_initialization(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mock_setup = mocker.patch("src.data.database.setup_databases_folder")
        mock_setup.return_value = mocker.AsyncMock()
        mock_load_settings = mocker.patch("src.data.database.load_settings")
        mock_load_fuel = mocker.patch("src.data.database.load_fuel_data")
        mock_create_db = mocker.patch("src.data.database.create_fuel_type_database")
        mock_create_db.return_value = mocker.AsyncMock()
        mock_insert = mocker.patch("src.data.database.insert_fuel_data")
        mock_os_path_exists = mocker.patch("os.path.exists")
        mock_os_path_exists.return_value = True
        mock_os_remove = mocker.patch("os.remove")
        mock_os_remove.return_value = None

        # Act
        result = await initialize_fuel_type_database()

        # Assert
        assert result == 1
        mock_setup.assert_called_once()
        mock_load_settings.assert_called_once()
        mock_load_fuel.assert_called_once()
        mock_create_db.assert_called_once()
        mock_insert.assert_called_once()

        # Assert that the logger is called with the correct message
        mock_logger.info.assert_called_with(
            "Fuel type database initialized successfully"
        )

        # Assert that the logger is called with the correct message
        mock_logger.error.assert_not_called()

    # Unsuccessfully initializes a fuel type database when missing or invalid settings file
    @pytest.mark.asyncio
    async def test_unsuccessful_fuel_type_database_initialization_missing_settings(
        self, mocker
    ):
        # Arrange
        mock_setup = mocker.patch("src.data.database.setup_databases_folder")
        mock_load_settings = mocker.patch("src.data.database.load_settings")
        mock_load_settings.return_value = None
        mock_load_fuel = mocker.patch("src.data.database.load_fuel_data")
        mock_create_db = mocker.patch("src.data.database.create_fuel_type_database")
        mock_insert = mocker.patch("src.data.database.insert_fuel_data")

        # Act
        result = await initialize_fuel_type_database()

        # Assert
        assert result == 0
        mock_setup.assert_called_once()
        mock_load_settings.assert_called_once()
        mock_load_fuel.assert_not_called()
        mock_create_db.assert_not_called()
        mock_insert.assert_not_called()

    # Unsuccessfully initializes a fuel type database when load_fuel_data fails
    @pytest.mark.asyncio
    async def test_unsuccessful_fuel_type_database_initialization_load_fuel_data_fails(
        self, mocker
    ):
        # Arrange
        mock_setup = mocker.patch("src.data.database.setup_databases_folder")
        mock_load_settings = mocker.patch("src.data.database.load_settings")
        mock_load_settings.return_value = "test/path/settings.json"
        mock_load_fuel = mocker.patch("src.data.database.load_fuel_data")
        mock_load_fuel.return_value = None
        mock_create_db = mocker.patch("src.data.database.create_fuel_type_database")
        mock_insert = mocker.patch("src.data.database.insert_fuel_data")

        # Act
        result = await initialize_fuel_type_database()

        # Assert
        assert result == 0
        mock_setup.assert_called_once()
        mock_load_settings.assert_called_once()
        mock_load_fuel.assert_called_once()
        mock_create_db.assert_not_called()
        mock_insert.assert_not_called()

    # Unsuccessfully initializes a fuel type database when create_fuel_type_database fails
    @pytest.mark.asyncio
    async def test_unsuccessful_fuel_type_database_initialization_create_db_fails(
        self, mocker
    ):
        # Arrange
        mock_setup = mocker.patch("src.data.database.setup_databases_folder")
        mock_load_settings = mocker.patch("src.data.database.load_settings")
        mock_load_settings.return_value = "test/path/settings.json"
        mock_load_fuel = mocker.patch("src.data.database.load_fuel_data")
        mock_load_fuel.return_value = [
            {"fuel_type": "gasoline", "emissions_factor": 2.31}
        ]
        mock_create_db = mocker.patch("src.data.database.create_fuel_type_database")
        mock_create_db.return_value = None
        mock_insert = mocker.patch("src.data.database.insert_fuel_data")

        # Act
        result = await initialize_fuel_type_database()

        # Assert
        assert result == 0
        mock_setup.assert_called_once()
        mock_load_settings.assert_called_once()
        mock_load_fuel.assert_called_once()
        mock_create_db.assert_called_once()
        mock_insert.assert_not_called()

    # Unsuccessfully initializes a fuel type database when insert_fuel_data fails
    @pytest.mark.asyncio
    async def test_unsuccessful_fuel_type_database_initialization_insert_fails(
        self, mocker
    ):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mock_setup = mocker.patch("src.data.database.setup_databases_folder")
        mock_load_settings = mocker.patch("src.data.database.load_settings")
        mock_load_settings.return_value = Exception()

        # Act
        result = await initialize_fuel_type_database()

        # Assert
        assert result == 0
        mock_setup.assert_called_once()
        mock_load_settings.assert_called_once()
        mock_logger.error.assert_called_once()

    # Handle a care case when missing or invalid settings file
    @pytest.mark.asyncio
    async def test_missing_settings_file(self, mocker):
        # Arrange
        mock_setup = mocker.patch("src.data.database.setup_databases_folder")
        mock_load_settings = mocker.patch("src.data.database.load_settings")
        mock_load_settings.return_value = None
        mock_load_fuel = mocker.patch("src.data.database.load_fuel_data")
        mock_create_db = mocker.patch("src.data.database.create_fuel_type_database")
        mock_insert = mocker.patch("src.data.database.insert_fuel_data")

        # Act
        result = await initialize_fuel_type_database()

        # Assert
        assert result == 0
        mock_setup.assert_called_once()
        mock_load_settings.assert_called_once()
        mock_load_fuel.assert_not_called()
        mock_create_db.assert_not_called()
        mock_insert.assert_not_called()

    # Successfully reads settings.json and returns existing emission_modifiers_path
    @pytest.mark.asyncio
    async def test_load_settings_returns_existing_path(self, mocker):
        # Arrange
        mock_settings = {"emission_modifiers_path": "/test/path"}
        mock_file = mocker.AsyncMock()
        mock_file.read.return_value = json.dumps(mock_settings)

        mock_aiofiles = mocker.patch("aiofiles.open")
        mock_aiofiles.return_value.__aenter__.return_value = mock_file

        # Act
        result = await load_settings()

        # Assert
        assert result == "/test/path"
        mock_aiofiles.assert_called_once()

    # Handles missing settings.json file and returns None
    @pytest.mark.asyncio
    async def test_load_settings_handles_missing_file(self, mocker):
        # Arrange
        mock_aiofiles = mocker.patch("aiofiles.open")
        mock_aiofiles.side_effect = FileNotFoundError()

        # Act
        result = await load_settings()

        # Assert
        assert result is None
        mock_aiofiles.assert_called_once()

    @pytest.mark.asyncio
    async def test_load_settings_handles_invalid_json(self, mocker):
        # Arrange
        mock_file_path = "test/path/settings.json"
        mock_join = mocker.patch("os.path.join", return_value=mock_file_path)
        mock_file = mocker.AsyncMock()
        mock_file.read.return_value = '{"some_other_key": "value"}'  # json is valid but it doesn't contain the emissions_factors path key
        mock_aiofiles = mocker.patch("aiofiles.open")
        mock_aiofiles.return_value.__aenter__.return_value = mock_file

        # Act
        result = await load_settings()

        # Assert
        assert result is mock_file_path
        assert mock_join.call_count == 4

    # Successfully loads and parses valid JSON file containing fuel data
    @pytest.mark.asyncio
    async def test_load_valid_fuel_data(self, mocker):
        # Arrange
        mock_json_data = [
            {"fuel_type": "gasoline", "emissions_factor": 2.31},
            {"fuel_type": "diesel", "emissions_factor": 2.68},
        ]
        mock_file = mocker.AsyncMock()
        mock_file.read.return_value = json.dumps(mock_json_data)
        mock_aiofiles = mocker.patch("aiofiles.open")
        mock_aiofiles.return_value.__aenter__.return_value = mock_file

        # Act
        result = await load_fuel_data("test/path/emissions_variables.json")

        # Assert
        assert result == mock_json_data
        mock_aiofiles.assert_called_once_with("test/path/emissions_variables.json", "r")

    @pytest.mark.asyncio
    async def test_load_fuel_data_handles_invalid_fuel_data(self, mocker):
        # Arrange
        mock_invalid_fuel_data = [
            {"fuel_type": "gasoline"},  # Missing emissions_factor
            {"emissions_factor": 2.68},  # Missing fuel_type
            {"fuel_type": "diesel", "emissions_factor": 2.68},  # Valid entry
            {"something_else": "value"},  # Missing both required fields
        ]
        mock_file = mocker.AsyncMock()
        mock_file.read.return_value = json.dumps(mock_invalid_fuel_data)
        mock_aiofiles = mocker.patch("aiofiles.open")
        mock_aiofiles.return_value.__aenter__.return_value = mock_file
        # Act/Assert
        with pytest.raises(ValueError):
            await load_fuel_data("test/path/emissions_variables.json")

    # Returns None when JSON file is not found
    @pytest.mark.asyncio
    async def test_load_fuel_data_file_not_found(self, mocker):
        # Arrange
        mock_aiofiles = mocker.patch("aiofiles.open")
        mock_aiofiles.side_effect = FileNotFoundError()

        # Act
        result = await load_fuel_data("nonexistent/path/emissions_variables.json")

        # Assert
        assert result is None
        mock_aiofiles.assert_called_once_with(
            "nonexistent/path/emissions_variables.json", "r"
        )

    async def test_load_fuel_data_handles_invalid_json(self, mocker):
        # Arrange
        mock_file_path = "test/path/emissions_variables.json"
        mock_logger = mocker.patch("src.data.database.logger")
        mock_aiofiles = mocker.patch("aiofiles.open")
        mock_aiofiles.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)

        # Act
        result = await load_fuel_data(mock_file_path)

        # Assert
        assert result is None
        mock_logger.error.assert_called_with(
            f"Error loading fuel type data from {mock_file_path}"
        )

    # Returns list of fuel types from a database when a database exists and contains data
    @pytest.mark.asyncio
    async def test_get_fuel_types_returns_list(self, mocker):
        # Arrange
        mock_cursor = mocker.AsyncMock()
        mock_cursor.fetchall.return_value = [("gasoline",), ("diesel",)]

        mock_conn = mocker.AsyncMock()
        mock_conn.__aenter__.return_value = mock_conn
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        mocker.patch("aiosqlite.connect", return_value=mock_conn)

        # Act
        result = await get_fuel_types()

        # Assert
        assert result == ["gasoline", "diesel"]
        mock_cursor.execute.assert_called_once_with("SELECT fuel_type FROM fuel_types")

    # Handles case when a database file does not exist
    @pytest.mark.asyncio
    async def test_get_fuel_types_handles_missing_db(self, mocker):
        # Arrange
        mocker.patch(
            "aiosqlite.connect",
            side_effect=aiosqlite.OperationalError("database does not exist"),
        )

        # Act & Assert
        with pytest.raises(aiosqlite.OperationalError):
            await get_fuel_types()

    # Returns correct emissions factor for a valid fuel type
    @pytest.mark.asyncio
    async def test_returns_correct_factor_for_valid_fuel(self, mocker):
        # Arrange
        test_fuel = "diesel"
        expected_factor = 2.68

        mock_cursor = mocker.AsyncMock()
        mock_cursor.fetchone.return_value = (expected_factor,)

        mock_conn = mocker.AsyncMock()
        mock_conn.__aenter__.return_value = mock_conn
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        mocker.patch("aiosqlite.connect", return_value=mock_conn)

        # Act
        result = await get_emissions_factor(test_fuel)

        # Assert
        assert result == expected_factor
        mock_cursor.execute.assert_called_once_with(
            "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
            (test_fuel,),
        )

    # Handles a non-existent fuel type by raising ValueError
    @pytest.mark.asyncio
    async def test_raises_error_for_invalid_fuel(self, mocker):
        # Arrange
        test_fuel = "invalid_fuel"

        mock_cursor = mocker.AsyncMock()
        mock_cursor.fetchone.return_value = None

        mock_conn = mocker.AsyncMock()
        mock_conn.__aenter__.return_value = mock_conn
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        mocker.patch("aiosqlite.connect", return_value=mock_conn)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await get_emissions_factor(test_fuel)
        assert (
            str(exc_info.value)
            == f"No emissions factor found for fuel type: {test_fuel}"
        )

    # Successfully insert calculation data and return matching log entry
    @pytest.mark.asyncio
    async def test_successful_log_calculation(self, mocker):
        # Arrange
        user_id = 1
        fuel_type = "gasoline"
        fuel_used = 10.5
        emissions = 24.3
        expected_log = [(fuel_type, fuel_used, emissions)]

        mock_cursor = mocker.AsyncMock()
        mock_cursor.fetchall.return_value = expected_log

        mock_conn = mocker.AsyncMock()
        mock_conn.__aenter__.return_value = mock_conn
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

        mocker.patch("aiosqlite.connect", return_value=mock_conn)

        # Act
        result = await log_calculation(user_id, fuel_type, fuel_used, emissions)

        # Assert | Be careful as this test can fail if the text of this assertion changes
        assert result == expected_log
        mock_cursor.execute.assert_any_call(
            "SELECT fuel_type, fuel_used, emissions FROM emissions WHERE user_id = ? AND fuel_type = ? AND "
            "fuel_used = ? AND emissions = ?",
            (user_id, fuel_type, fuel_used, emissions),
        )

    # Handle ValueError when logging calculation
    @pytest.mark.asyncio
    async def test_log_calculation_handles_value_error(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mock_aiosqlite = mocker.patch("aiosqlite.connect")
        mock_aiosqlite.side_effect = ValueError("Error logging calculation")

        # Act
        result = await log_calculation(1, "gasoline", 10.5, 24.3)

        # Assert
        assert result is None
        mock_logger.error.assert_called_once_with(
            "Value error: Error logging calculation"
        )

    # Handle a non-existent database file path
    @pytest.mark.asyncio
    async def test_nonexistent_database_path(self, mocker):
        # Arrange
        user_id = 1
        fuel_type = "gasoline"
        fuel_used = 10.5
        emissions = 24.3

        mocker.patch(
            "aiosqlite.connect",
            side_effect=aiosqlite.Error("Database not found"),
        )

        # Act
        result = await log_calculation(user_id, fuel_type, fuel_used, emissions)

        # Assert
        assert result is None

    # When databases_folder exists, only fuel_type database is reinitialized
    @pytest.mark.asyncio
    async def test_existing_folder_reinitializes_fuel_type_only(self, mocker):
        # Arrange
        mocker.patch("os.path.exists", return_value=True)
        mock_initialize_fuel = mocker.patch(
            "src.data.database.initialize_fuel_type_database"
        )
        mock_initialize_emissions = mocker.patch(
            "src.data.database.initialize_emissions_database"
        )
        mock_initialize_user = mocker.patch(
            "src.data.database.initialize_user_data_database"
        )

        # Act
        await database_initialization()

        # Assert
        mock_initialize_fuel.assert_called_once()
        mock_initialize_emissions.assert_not_called()
        mock_initialize_user.assert_not_called()

    # Handle a case when databases_folder exists but is empty
    @pytest.mark.asyncio
    async def test_empty_existing_folder_reinitializes_fuel_type(self, mocker):
        # Arrange
        mock_db_folder = "databases"
        mocker.patch("src.data.database.databases_folder", str(mock_db_folder))
        mock_initialize_fuel = mocker.patch(
            "src.data.database.initialize_fuel_type_database"
        )
        mock_initialize_emissions = mocker.patch(
            "src.data.database.initialize_emissions_database"
        )
        mock_initialize_user = mocker.patch(
            "src.data.database.initialize_user_data_database"
        )
        mock_initialize_user.return_value = mocker.AsyncMock()
        mock_initialize_emissions.return_value = mocker.AsyncMock()
        mock_initialize_fuel.return_value = mocker.AsyncMock()

        # Act
        await database_initialization()

        # Assert
        mock_initialize_fuel.assert_called_once()
        assert os.path.exists(mock_db_folder)
        assert len(os.listdir(mock_db_folder)) == 0

        # Teardown
        try:
            shutil.rmtree(mock_db_folder)
        except FileNotFoundError:
            pass

    def test_setup_databases_folder_when_folder_exists(self, mocker):
        # Arrange
        mock_databases_folder_exists = mocker.patch("os.path.exists", return_value=True)

        # Act
        database_folder = setup_databases_folder()

        # Assert
        assert database_folder is None
        mock_databases_folder_exists.assert_called_once()

    def test_setup_databases_folder_when_folder_does_not_exist(self, mocker):
        # Arrange
        mock_databases_folder_exists = mocker.patch(
            "os.path.exists", return_value=False
        )
        mock_databases_folder_creation = mocker.patch("os.makedirs")

        # Act
        setup_databases_folder()

        # Assert
        mock_databases_folder_creation.assert_called_once()
        assert mock_databases_folder_exists.call_count == 2

    # Successfully inserts fuel data into the database
    @pytest.mark.asyncio
    async def test_insert_fuel_data(self, mocker):
        # Arrange
        mock_fuel_data = [{"fuel_type": "gasoline", "emissions_factor": 2.31}]
        mock_cursor = mocker.AsyncMock()
        mock_cursor.execute.return_value = None
        mock_conn = mocker.AsyncMock()
        mock_conn.__aenter__.return_value = mock_conn
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
        mocker.patch("aiosqlite.connect", return_value=mock_conn)

        # Act
        result = await insert_fuel_data(
            "test/path/emissions_variables.json", mock_fuel_data
        )

        # Assert
        assert result is None
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_insert_fuel_data_handles_error(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mock_fuel_data = [{"fuel_type": "gasoline", "emissions_factor": 2.31}]
        mock_cursor = mocker.AsyncMock()
        mock_cursor.execute.side_effect = Exception("Database error")
        mock_conn = mocker.AsyncMock()
        mock_conn.__aenter__.return_value = mock_conn
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
        mocker.patch("aiosqlite.connect", return_value=mock_conn)

        # Act
        result = await insert_fuel_data(
            "test/path/emissions_variables.json", mock_fuel_data
        )

        # Assert
        assert result is None
        mock_logger.error.assert_called_with(
            "Error inserting fuel data: Database error"
        )

    @pytest.mark.asyncio
    async def test_database_initialization_creates_databases_folder_if_doesnt_exist(
        self, mocker
    ):
        # Arrange
        mock_databases_folder_exists = mocker.patch(
            "os.path.exists", return_value=False
        )
        mock_setup_databases_folder = mocker.patch(
            "src.data.database.setup_databases_folder"
        )
        mocker.patch("src.data.database.initialize_fuel_type_database")
        mocker.patch("src.data.database.initialize_emissions_database")
        mocker.patch("src.data.database.initialize_user_data_database")
        mock_setup_databases_folder.return_value = None

        # Act
        await database_initialization()

        # Assert
        assert mock_setup_databases_folder.call_count == 1
        assert mock_databases_folder_exists.call_count == 2
