import aiosqlite
import pytest

from src.core.emissions_calculator import calculate_emissions
from src.data.database import initialize_fuel_type_database, log_calculation

# ! BEWARE THAT RUNNING THESE TESTS WILL DELETE THE DATABASES FOLDER AND ALL ITS CONTENTS.
# ! MAKE SURE TO BACK UP ANY IMPORTANT DATA BEFORE RUNNING THESE TESTS.
# ! RUNNING THESE TEST CONCURRENTLY WILL NOT WORK. IDK why.


# * If this test fails, check the calculate_emissions module for logic changes such as math operator changing
@pytest.mark.asyncio
async def test_calculate_emissions(
    mocker, fuel_type="gasoline", fuel_used: float = 10.0
):
    # Arrange
    mock_db_path = "fuel_type_conversions.db"
    mocker.patch("os.path.join", return_value=mock_db_path)

    mock_databases_folder = mocker.patch(
        "src.data.database.setup_databases_folder"
    )
    mock_databases_folder.return_value = mocker.AsyncMock()

    mock_cursor = mocker.AsyncMock()
    mock_cursor.fetchone.return_value = [2.5]  # Mocked emission factor

    mock_conn = mocker.AsyncMock()
    mock_conn.__aenter__.return_value = mock_conn
    mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor

    mocker.patch("aiosqlite.connect", return_value=mock_conn)

    await initialize_fuel_type_database()

    # Act | if this test is failing, PLEASE check emission factor values for changes
    async with aiosqlite.connect(mock_db_path) as conn:
        async with await conn.cursor() as cursor:
            await cursor.execute(
                "SELECT emissions_factor FROM fuel_types WHERE fuel_type = ?",
                (fuel_type,),
            )
            emissions_factor = (await cursor.fetchone())[0]
            expected_emissions = fuel_used * emissions_factor
            fuel_type, fuel_used, emissions = await calculate_emissions(
                1, fuel_type, fuel_used
            )

    # Assert
    assert expected_emissions == emissions


@pytest.mark.asyncio
async def test_log_calculation(mocker):
    # Arrange
    mock_db_path = "emissions.db"
    mocker.patch("os.path.join", return_value=mock_db_path)

    mock_databases_folder = mocker.patch(
        "src.data.database.setup_databases_folder"
    )
    mock_databases_folder.return_value = mocker.AsyncMock()

    mock_cursor = mocker.AsyncMock()
    mock_cursor.fetchall.return_value = [(1, "gasoline", 10.0, 25.0)]

    mock_conn = mocker.AsyncMock()
    mock_conn.__aenter__.return_value = mock_conn
    mock_conn.__aexit__.return_value = None
    mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
    mock_conn.cursor.return_value.__aexit__.return_value = None

    mocker.patch("aiosqlite.connect", return_value=mock_conn)

    # Act
    result = await log_calculation(1, "gasoline", 10.0, 25.0)

    # Assert
    assert result == [(1, "gasoline", 10.0, 25.0)]
