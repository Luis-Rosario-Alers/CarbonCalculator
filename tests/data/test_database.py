import json
import logging
import os
import shutil
from unittest.mock import patch

import aiosqlite
import pytest

from src.data.database import (
    create_fuel_type_database,
    database_initialization,
    determine_application_path,
    get_emissions_factor,
    get_fuel_types,
    initialize_emissions_database,
    initialize_fuel_type_database,
    initialize_user_data_database,
    load_fuel_data,
    load_settings,
    log_calculation,
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
        mock_logger.info.assert_any_call(
            f"Application path set to: {app_path}"
        )
        mock_logger.info.assert_any_call(
            f"Databases folder set to: {db_folder}"
        )

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
        mock_logger.info.assert_any_call(
            f"Application path set to: {app_path}"
        )
        mock_logger.info.assert_any_call(
            f"Databases folder set to: {db_folder}"
        )

    # Handle a case when databases_folder path doesn't exist
    @pytest.mark.asyncio
    async def test_handles_nonexistent_database_folder(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mocker.patch(
            "os.path.join", return_value="/nonexistent/path/emissions.db"
        )

        # Act
        result = await initialize_emissions_database()

        # Assert
        assert result == 0
        mock_logger.error.assert_called_with(
            "Emissions database not initialized"
        )

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
    async def test_creates_users_table_when_db_not_exists(
        self, mocker, caplog
    ):
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
        mock_logger.error.assert_called_with(
            "User data database not initialized"
        )

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

    # Successfully creates and initializes a fuel type database with valid settings and data
    @pytest.mark.asyncio
    async def test_successful_fuel_type_database_initialization(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.data.database.logger")
        mock_setup = mocker.patch("src.data.database.setup_databases_folder")
        mock_setup.return_value = mocker.AsyncMock()
        mock_load_settings = mocker.patch("src.data.database.load_settings")
        mock_load_fuel = mocker.patch("src.data.database.load_fuel_data")
        mock_create_db = mocker.patch(
            "src.data.database.create_fuel_type_database"
        )
        mock_create_db.return_value = mocker.AsyncMock()
        mock_insert = mocker.patch("src.data.database.insert_fuel_data")

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

    # Handle a care case when missing or invalid settings file
    @pytest.mark.asyncio
    async def test_missing_settings_file(self, mocker):
        # Arrange
        mock_setup = mocker.patch("src.data.database.setup_databases_folder")
        mock_load_settings = mocker.patch("src.data.database.load_settings")
        mock_load_settings.return_value = None
        mock_load_fuel = mocker.patch("src.data.database.load_fuel_data")
        mock_create_db = mocker.patch(
            "src.data.database.create_fuel_type_database"
        )
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

    # Successfully reads settings.json and returns existing emissions_factors_path
    @pytest.mark.asyncio
    async def test_load_settings_returns_existing_path(self, mocker):
        # Arrange
        mock_settings = {"emissions_factors_path": "/test/path"}
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
        result = await load_fuel_data("test/path/fuel_types.json")

        # Assert
        assert result == mock_json_data
        mock_aiofiles.assert_called_once_with("test/path/fuel_types.json", "r")

    # Returns None when JSON file is not found
    @pytest.mark.asyncio
    async def test_load_fuel_data_file_not_found(self, mocker):
        # Arrange
        mock_aiofiles = mocker.patch("aiofiles.open")
        mock_aiofiles.side_effect = FileNotFoundError()

        # Act
        result = await load_fuel_data("nonexistent/path/fuel_types.json")

        # Assert
        assert result is None
        mock_aiofiles.assert_called_once_with(
            "nonexistent/path/fuel_types.json", "r"
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
        mock_cursor.execute.assert_called_once_with(
            "SELECT fuel_type FROM fuel_types"
        )

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
        result = await log_calculation(
            user_id, fuel_type, fuel_used, emissions
        )

        # Assert | Be careful as this test can fail if the text of this assertion changes
        assert result == expected_log
        mock_cursor.execute.assert_any_call(
            "SELECT fuel_type, fuel_used, emissions FROM emissions WHERE user_id = ? AND fuel_type = ? AND "
            "fuel_used = ? AND emissions = ?",
            (user_id, fuel_type, fuel_used, emissions),
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
        result = await log_calculation(
            user_id, fuel_type, fuel_used, emissions
        )

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
