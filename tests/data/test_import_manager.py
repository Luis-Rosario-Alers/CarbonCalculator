import os
from datetime import datetime

import aiosqlite
import pytest

from src.data.database import (
    databases_folder,
    initialize_emissions_database,
    setup_databases_folder,
)
from src.data.import_manager import ImportManager


@pytest.fixture(autouse=True)
async def cleanup_database():
    # Create a fresh database folder if it doesn't exist
    setup_databases_folder()
    await initialize_emissions_database()
    yield
    db_path = os.path.join(databases_folder, "emissions.db")
    conn = await aiosqlite.connect(db_path)
    cursor = await conn.cursor()
    await cursor.execute("DELETE FROM emissions")
    await conn.commit()
    await conn.close()


# * Tests for import_json method
# Raises ValueError when JSON file is missing required headers
def test_import_json_with_missing_header(tmp_path):
    # Given
    json_content = '[{"user_id": 1, "fuel_type": "gas", "emissions": 25.3, "timestamp": "2023-01-01"}]'
    json_file = tmp_path / "test.json"
    json_file.write_text(json_content)
    import_manager = ImportManager(str(json_file))
    # When/Then
    with pytest.raises(ValueError) as exc_info:
        import_manager.import_from_json()
    assert "Missing required keys: {'fuel_used'}" in str(exc_info.value)


# Handles JSON file with extra columns beyond required ones
def test_import_json_with_extra_columns(tmp_path):
    # Given
    json_content = '[{"user_id": 123, "fuel_type": "gas", "fuel_used": 50, "emissions": 150, "timestamp": "2024-01-01", "extra_column": "extra_value"}]'
    json_file = tmp_path / "test.json"
    json_file.write_text(json_content)
    import_manager = ImportManager(str(json_file))
    # When
    imported_data = import_manager.import_from_json()
    # Then
    expected_data = [(123, "gas", 50, 150, "2024-01-01")]
    assert (
        imported_data == expected_data
    ), "Extra columns should be ignored in imported data"


# Checks that JSON values are of correct data types
def test_import_json_data_types(tmp_path):
    # Given
    json_content = '[{"user_id": 123, "fuel_type": "gas", "fuel_used": 50.5, "emissions": 150.3, "timestamp": "2024-01-01"}]'
    json_file = tmp_path / "test.json"
    json_file.write_text(json_content)
    import_manager = ImportManager(str(json_file))
    # When
    imported_data = import_manager.import_from_json()
    # Then
    row = imported_data[0]
    assert isinstance(row[0], int), "user_id should be integer"
    assert isinstance(row[1], str), "fuel_type should be string"
    assert isinstance(row[2], (int, float)), "fuel_used should be numeric"
    assert isinstance(row[3], (int, float)), "emissions should be numeric"
    try:
        datetime.strptime(row[4], "%Y-%m-%d")
    except ValueError:
        pytest.fail("timestamp should be in YYYY-MM-DD format")


# * Tests for import_csv method
# Raises ValueError when CSV file is missing required headers
def test_import_csv_with_missing_headers(tmp_path):
    # Given
    csv_content = (
        "user_id,fuel_type,emissions,timestamp\n1,gas,25.3,2023-01-01"
    )
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)
    import_manager = ImportManager(str(csv_file))
    # When/Then
    with pytest.raises(ValueError) as exc_info:
        import_manager.import_from_csv()
    assert "Missing required keys: {'fuel_used'}" in str(exc_info.value)


# Handles CSV file with extra columns beyond required ones
def test_import_csv_with_extra_columns(tmp_path):
    # Given
    csv_content = "user_id,fuel_type,fuel_used,emissions,timestamp,extra_column\n123,gas,50,150,2024-01-01,extra_value"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)
    import_manager = ImportManager(str(csv_file))

    # When
    imported_data = import_manager.import_from_csv()

    # Then
    expected_data = [("123", "gas", "50", "150", "2024-01-01")]
    assert (
        imported_data == expected_data
    ), "Extra columns should be ignored in imported data"


# Checks that CSV values are of correct data types
def test_import_csv_data_types(tmp_path):
    # Given
    csv_content = "user_id,fuel_type,fuel_used,emissions,timestamp\n123,gas,50.5,150.3,2024-01-01"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)
    import_manager = ImportManager(str(csv_file))

    # When
    imported_data = import_manager.import_from_csv()

    # Then
    row = imported_data[0]
    assert isinstance(int(row[0]), int), "user_id should be integer"
    assert isinstance(row[1], str), "fuel_type should be string"
    assert float(row[2]), "fuel_used should be numeric"
    assert float(row[3]), "emissions should be numeric"
    try:
        datetime.strptime(row[4], "%Y-%m-%d")
    except ValueError:
        pytest.fail("timestamp should be in YYYY-MM-DD format")
