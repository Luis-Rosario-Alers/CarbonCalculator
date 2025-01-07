import csv
import json

import pytest

from data.export_manager import ExportManager


# Successfully exports data from SQLite to JSON file with correct structure
def test_export_to_json_writes_data_with_correct_structure(tmp_path, mocker):
    # Given
    test_data = [
        (1, "gasoline", 10.5, 24.3, "2023-01-01"),
        (2, "diesel", 8.2, 22.1, "2023-01-02"),
    ]
    mock_fetch = mocker.patch("data.export_manager.ExportManager.fetch_data")
    mock_fetch.return_value = test_data

    export_manager = ExportManager("dummy.db")
    output_file = tmp_path / "test_output.json"

    # When
    export_manager.export_to_json(output_file)

    # Then
    with open(output_file) as f:
        exported_data = json.load(f)

    assert len(exported_data) == 2
    assert exported_data[0] == {
        "user_id": 1,
        "fuel_type": "gasoline",
        "fuel_used": 10.5,
        "emissions": 24.3,
        "timestamp": "2023-01-01",
    }


# Handle empty result set from database
def test_export_to_json_handles_empty_dataset(tmp_path, mocker):
    # Given
    mock_fetch = mocker.patch("data.export_manager.ExportManager.fetch_data")
    mock_fetch.return_value = []

    export_manager = ExportManager("dummy.db")
    output_file = tmp_path / "empty_output.json"

    # When
    export_manager.export_to_json(output_file)

    # Then
    with open(output_file) as f:
        exported_data = json.load(f)

    assert isinstance(exported_data, list)
    assert len(exported_data) == 0


# Handle very large datasets efficiently
def test_export_to_json_handles_large_datasets(tmp_path, mocker):

    # Given
    large_test_data = [
        (i, "fuel_type", i * 1.1, i * 2.2, f"2023-01-{i % 30 + 1:02d}")
        for i in range(1000000)  # Simulate a large dataset
    ]
    mock_fetch = mocker.patch("data.export_manager.ExportManager.fetch_data")
    mock_fetch.return_value = large_test_data
    export_manager = ExportManager("dummy.db")
    output_file = tmp_path / "large_test_output.json"
    # When
    export_manager.export_to_json(output_file)
    # Then
    with open(output_file) as f:
        exported_data = json.load(f)
    assert len(exported_data) == 1000000
    assert exported_data[0] == {
        "user_id": 0,
        "fuel_type": "fuel_type",
        "fuel_used": 0.0,
        "emissions": 0.0,
        "timestamp": "2023-01-01",
    }


# Successfully exports data from SQLite to CSV file with correct structure
def test_export_to_csv_writes_data_with_correct_structure(tmp_path, mocker):
    # Given
    test_data = [
        (1, "gasoline", 10.5, 24.3, "2023-01-01"),
        (2, "diesel", 8.2, 22.1, "2023-01-02"),
    ]
    mock_fetch = mocker.patch("data.export_manager.ExportManager.fetch_data")
    mock_fetch.return_value = test_data
    export_manager = ExportManager("dummy.db")
    output_file = tmp_path / "test_output.csv"
    # When
    export_manager.export_to_csv(output_file)
    # Then
    with open(output_file, newline="") as f:
        reader = csv.DictReader(f)
        exported_data = list(reader)
    assert len(exported_data) == 2
    assert exported_data[0] == {
        "user_id": "1",
        "fuel_type": "gasoline",
        "fuel_used": "10.5",
        "emissions": "24.3",
        "timestamp": "2023-01-01",
    }


def test_export_to_csv_handles_empty_dataset(tmp_path, mocker):

    # Given
    mock_fetch = mocker.patch("data.export_manager.ExportManager.fetch_data")
    mock_fetch.return_value = []
    export_manager = ExportManager("dummy.db")
    output_file = tmp_path / "empty_output.csv"
    # When
    export_manager.export_to_csv(output_file)
    # Then
    with open(output_file, newline="") as f:
        reader = csv.DictReader(f)
        exported_data = list(reader)
    assert len(exported_data) == 0


def test_export_to_csv_handles_large_datasets(tmp_path, mocker):
    # Given
    large_test_data = [
        (i, "fuel_type", i * 1.1, i * 2.2, f"2023-01-{i % 30 + 1:02d}")
        for i in range(1000000)
    ]
    mock_fetch = mocker.patch("data.export_manager.ExportManager.fetch_data")
    mock_fetch.return_value = large_test_data
    export_manager = ExportManager("dummy.db")
    output_file = tmp_path / "large_test_output.csv"
    # When
    export_manager.export_to_csv(output_file)
    # Then
    with open(output_file, newline="") as f:
        reader = csv.DictReader(f)
        first_row = next(reader)
        row_count = sum(1 for _ in reader) + 1
    assert row_count == 1000000
    assert first_row == {
        "user_id": "0",
        "fuel_type": "fuel_type",
        "fuel_used": "0.0",
        "emissions": "0.0",
        "timestamp": "2023-01-01",
    }
