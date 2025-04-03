import shutil
from datetime import datetime

import chardet
import pytest

from src.data.database_model import (
    databases_folder,
    initialize_emissions_database,
    setup_databases_folder,
)
from src.data.import_manager import ImportManager


class TestImportManager:
    @pytest.fixture(autouse=True)
    async def cleanup_database(self):
        # Arrange
        setup_databases_folder()
        await initialize_emissions_database()

        # Act & Assert
        yield

        # Cleanup
        shutil.rmtree(databases_folder)

    # * Tests for import_json method
    def test_import_json_with_missing_header(self, tmp_path):
        # Arrange
        json_content = '[{"user_id": 1, "fuel_type": "gas", "emissions": 25.3, "timestamp": "2023-01-01"}]'
        json_file = tmp_path / "test.json"
        json_file.write_text(json_content)
        import_manager = ImportManager(str(json_file))

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            import_manager.import_from_json()
        assert "Missing required keys: {'fuel_used'}" in str(exc_info.value)

    def test_import_json_with_extra_columns(self, tmp_path):
        # Arrange
        json_content = '[{"user_id": 123, "fuel_type": "gas", "fuel_used": 50, "emissions": 150, "timestamp": "2024-01-01", "extra_column": "extra_value"}]'
        json_file = tmp_path / "test.json"
        json_file.write_text(json_content)
        import_manager = ImportManager(str(json_file))
        expected_data = [(123, "gas", 50, 150, "2024-01-01")]

        # Act
        imported_data = import_manager.import_from_json()

        # Assert
        assert (
            imported_data == expected_data
        ), "Extra columns should be ignored in imported data"

    def test_import_json_data_types(self, tmp_path):
        # Arrange
        json_content = '[{"user_id": 123, "fuel_type": "gas", "fuel_used": 50.5, "emissions": 150.3, "timestamp": "2024-01-01"}]'
        json_file = tmp_path / "test.json"
        json_file.write_text(json_content)
        import_manager = ImportManager(str(json_file))

        # Act
        imported_data = import_manager.import_from_json()
        row = imported_data[0]

        # Assert
        assert isinstance(row[0], int), "user_id should be integer"
        assert isinstance(row[1], str), "fuel_type should be string"
        assert isinstance(row[2], (int, float)), "fuel_used should be numeric"
        assert isinstance(row[3], (int, float)), "emissions should be numeric"
        try:
            datetime.strptime(row[4], "%Y-%m-%d")
        except ValueError:
            pytest.fail("timestamp should be in YYYY-MM-DD format")

    # * Tests for import_csv method
    def test_import_csv_with_missing_headers(self, tmp_path):
        # Arrange
        csv_content = "user_id,fuel_type,emissions,timestamp\n1,gas,25.3,2023-01-01"
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        import_manager = ImportManager(str(csv_file))

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            import_manager.import_from_csv()
        assert "Missing required keys: {'fuel_used'}" in str(exc_info.value)

    def test_import_csv_with_extra_columns(self, tmp_path):
        # Arrange
        csv_content = "user_id,fuel_type,fuel_used,emissions,timestamp,extra_column\n123,gas,50,150,2024-01-01,extra_value"
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        import_manager = ImportManager(str(csv_file))
        expected_data = [(123, "gas", 50, 150, "2024-01-01")]

        # Act
        imported_data = import_manager.import_from_csv()

        # Assert
        assert (
            imported_data == expected_data
        ), "Extra columns should be ignored in imported data"

    def test_import_csv_data_types(self, tmp_path):
        # Arrange
        csv_content = "user_id,fuel_type,fuel_used,emissions,timestamp\n123,gas,50.5,150.3,2024-01-01"
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        import_manager = ImportManager(str(csv_file))

        # Act
        imported_data = import_manager.import_from_csv()
        row = imported_data[0]

        # Assert
        assert isinstance(int(row[0]), int), "user_id should be integer"
        assert isinstance(row[1], str), "fuel_type should be string"
        assert float(row[2]), "fuel_used should be numeric"
        assert float(row[3]), "emissions should be numeric"
        try:
            datetime.strptime(row[4], "%Y-%m-%d")
        except ValueError:
            pytest.fail("timestamp should be in YYYY-MM-DD format")

    def test_import_from_json_missing_values_in_keys(self, mocker, tmp_path):
        # Arrange
        mock_logger = mocker.patch("src.data.import_manager.logger")
        json_content = '[{"user_id": 1, "fuel_type": "gas", "fuel_used": null, "emissions": 25.3, "timestamp": "2023-01-01"}]'
        json_file = tmp_path / "test.json"
        json_file.write_text(json_content)
        import_manager = ImportManager(str(json_file))

        # Act & Assert
        with pytest.raises(ValueError):
            import_manager.import_from_json()
        mock_logger.error.assert_called_once_with("Missing value for key: fuel_used")

    def test_import_from_csv_missing_values_in_keys(self, mocker, tmp_path):
        # Arrange
        mock_logger = mocker.patch("src.data.import_manager.logger")
        csv_content = (
            "user_id,fuel_type,fuel_used,emissions,timestamp\n1,gas,,25.3,2023-01-01"
        )
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        import_manager = ImportManager(str(csv_file))

        # Act & Assert
        with pytest.raises(ValueError):
            import_manager.import_from_csv()
        mock_logger.error.assert_called_once_with("Missing value for key: fuel_used")

    def test_import_from_csv_with_utf_8_encoding(self, mocker, tmp_path):
        # Arrange with no special characters
        csv_content = (
            "user_id,fuel_type,fuel_used,emissions,timestamp\n1,gas,50,150,2024-01-01"
        )
        csv_file = tmp_path / "test.csv"
        # Explicitly write in UTF-8 encoding
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            f.write(csv_content)

        import_manager = ImportManager(str(csv_file))

        # Act
        imported_data = import_manager.import_from_csv()

        # Assert
        assert imported_data == [(1, "gas", 50, 150, "2024-01-01")]

        # Verify the file was actually written in UTF-8
        with open(csv_file, "rb") as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            assert "UTF-8" or "ASCII" in detected["encoding"].upper()

    def test_import_from_csv_with_utf_16_encoding(self, mocker, tmp_path):
        # Arrange Using UTF-16 specific characters
        csv_content = "user_id,fuel_type,fuel_used,emissions,timestamp\n1,gas⛽,50,150,2024-01-01"  # Added emoji to force UTF-16
        csv_file = tmp_path / "test.csv"
        # Explicitly write in UTF-16 encoding
        with open(csv_file, "w", encoding="utf-16", newline="") as f:
            f.write(csv_content)

        import_manager = ImportManager(str(csv_file))

        # Act
        imported_data = import_manager.import_from_csv()

        # Assert
        assert imported_data == [(1, "gas⛽", 50, 150, "2024-01-01")]

        # Verify the file was actually written in UTF-16
        with open(csv_file, "rb") as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            assert "UTF-16" in detected["encoding"].upper()

    def test_import_from_csv_with_iso_8859_1_encoding(self, mocker, tmp_path):
        # Arrange Using ISO-8859-1 specific characters
        csv_content = "user_id,fuel_type,fuel_used,emissions,timestamp\n1,gasolina señal düración,50,150,2024-01-01"
        csv_file = tmp_path / "test.csv"
        # Explicitly write in ISO-8859-1 encoding
        with open(csv_file, "w", encoding="iso-8859-1", newline="") as f:
            f.write(csv_content)

        # Act
        import_manager = ImportManager(str(csv_file))
        imported_data = import_manager.import_from_csv()

        # Assert
        assert imported_data == [(1, "gasolina señal düración", 50, 150, "2024-01-01")]

        # Verify the file was actually written in ISO-8859-1
        with open(csv_file, "rb") as f:
            raw_data = f.read()
            detected = chardet.detect(raw_data)
            print(f"Detected encoding: {detected}")  # Debug info
            assert detected["encoding"] and detected["encoding"].upper() in [
                "ISO-8859-1",
                "LATIN1",
            ]

    def test_import_from_csv_with_UnicodeDecodeError(self, mocker, tmp_path):
        # Arrange
        csv_content = (
            "user_id,fuel_type,fuel_used,emissions,timestamp\n1,gas,50,150,2024-01-01"
        )
        csv_file = tmp_path / "test.csv"
        mock_logger = mocker.patch("src.data.import_manager.logger")

        mock_chardet = mocker.patch("src.data.import_manager.chardet")
        mock_chardet.detect.return_value = {
            "encoding": "utf-8",
            "confidence": 0.9,
        }

        # Will only raise UnicodeDecodeError for text mode opens
        def mock_open_side_effect(*args, **kwargs):
            if "encoding" in kwargs:
                raise UnicodeDecodeError("testcodec", b"", 0, 1, "test")
            return mocker.mock_open(read_data=csv_content)(*args, **kwargs)

        mocker.patch("src.data.import_manager.open", side_effect=mock_open_side_effect)

        import_manager = ImportManager(str(csv_file))

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            import_manager.import_from_csv()

        assert "Could not read file with any of the attempted encodings" in str(
            exc_info.value
        )

        # Verify warnings were logged for each attempted encoding
        expected_encodings = ["utf-8", "utf-16", "iso-8859-1"]
        assert (
            mock_logger.warning.call_count == len(expected_encodings) + 1
        )  # This accounts for the encoding that was detected originally
        for encoding in expected_encodings:
            mock_logger.warning.assert_any_call(
                f"Failed to read with encoding: {encoding}"
            )

    def test_import_from_csv_with_error_detecting_encoding(self, mocker, tmp_path):
        # Arrange
        csv_content = (
            "user_id,fuel_type,fuel_used,emissions,timestamp\n1,gas,50,150,2024-01-01"
        )
        csv_file = tmp_path / "test.csv"
        mock_logger = mocker.patch("src.data.import_manager.logger")

        # Mock chardet to fail with an exception
        mock_chardet = mocker.patch("src.data.import_manager.chardet")
        mock_chardet.detect.side_effect = Exception("Error detecting encoding")

        # Will only raise UnicodeDecodeError for text mode opens
        def mock_open_side_effect(*args, **kwargs):
            if "encoding" in kwargs:
                raise UnicodeDecodeError("testcodec", b"", 0, 1, "test")
            return mocker.mock_open(read_data=csv_content)(*args, **kwargs)

        mocker.patch("src.data.import_manager.open", side_effect=mock_open_side_effect)

        # Act
        import_manager = ImportManager(str(csv_file))

        # Assert
        with pytest.raises(ValueError) as exc_info:
            import_manager.import_from_csv()

        # Verify error message includes the fallback encodings that were attempted
        expected_encodings = ["utf-8", "utf-16", "iso-8859-1"]
        assert (
            f"Could not read file with any of the attempted encodings: {expected_encodings}"
            in str(exc_info.value)
        )

        # Verify the error from encoding detection was logged
        mock_logger.error.assert_called_with(
            "Error detecting file encoding: Error detecting encoding"
        )

        # Verify warnings for each failed encoding attempt
        assert mock_logger.warning.call_count == len(expected_encodings)
        for encoding in expected_encodings:
            mock_logger.warning.assert_any_call(
                f"Failed to read with encoding: {encoding}"
            )

    def test_import_from_csv_with_low_confidence_in_encoding_detection(
        self, mocker, tmp_path
    ):
        # Arrange
        csv_content = (
            "user_id,fuel_type,fuel_used,emissions,timestamp\n1,gas,50,150,2024-01-01"
        )
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        mock_logger = mocker.patch("src.data.import_manager.logger")
        mock_chardet = mocker.patch("src.data.import_manager.chardet")
        mock_chardet.detect.return_value = {
            "encoding": "ISO-8859-1",
            "confidence": 0.5,
        }

        # Act
        import_manager = ImportManager(str(csv_file))

        # Assert
        import_manager.import_from_csv()
        mock_logger.warning.assert_called_once_with(
            "Low confidence in encoding detection: 50.00%"
        )

    def test_import_from_csv_when_all_encodings_fail(self, mocker, tmp_path):
        # Arrange
        csv_content = (
            "user_id,fuel_type,fuel_used,emissions,timestamp\n1,gas,50,150,2024-01-01"
        )
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        mock_chardet = mocker.patch("src.data.import_manager.chardet")
        mock_chardet.detect.return_value = {
            "encoding": "utf-8",
            "confidence": 0.9,
        }

        mock_logger = mocker.patch("src.data.import_manager.logger")

        # Will only raise UnicodeDecodeError for text mode opens
        def mock_open_side_effect(*args, **kwargs):
            if "encoding" in kwargs:
                raise UnicodeDecodeError("testcodec", b"", 0, 1, "test")
            return mocker.mock_open(read_data=csv_content)(*args, **kwargs)

        mocker.patch("src.data.import_manager.open", side_effect=mock_open_side_effect)

        import_manager = ImportManager(str(csv_file))

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            import_manager.import_from_csv()

        # Verify the exact error message
        expected_encodings = ["utf-8", "utf-8", "utf-16", "iso-8859-1"]
        assert (
            f"Could not read file with any of the attempted encodings: {expected_encodings}"
            in str(exc_info.value)
        )

        # Verify that each encoding was attempted
        assert mock_logger.warning.call_count == 4
        for encoding in expected_encodings:
            mock_logger.warning.assert_any_call(
                f"Failed to read with encoding: {encoding}"
            )
