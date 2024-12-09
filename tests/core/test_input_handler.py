import pytest
from src.core.input_handler import inputhandler
from src.data.data_validator import DataValidator


# Zero or negative user ID triggers error message and retry
def test_negative_user_id_retries(mocker):
    # Given
    mock_inputs = ["-5", "0", "10", "gas", "10.5"]
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=mock_inputs)
    mocker.patch(
        "src.data.data_validator.DataValidator.validate_fuel_type", return_value=True
    )

    # When
    result = inputhandler.get_user_input()

    # Then
    # 10.0 <- user_id, "gas" <- fuel_type, 10.5 <- fuel_used
    assert result == (10, "gas", 10.5)
    mock_print.assert_any_call("Invalid user ID. Please enter a numeric value.")
    mock_print.assert_any_call("Invalid user ID. Please enter a numeric value.")
    assert mock_print.call_count == 2


# test to check if tuple has valid input types
def test_input_validation_loops_until_valid_data(mocker):
    # Given
    mock_input = mocker.patch("builtins.input")
    mock_input.side_effect = ["-1", "abc", "123", "invalid", "diesel", "-10", "45.5"]
    mocker.patch(
        "src.data.data_validator.DataValidator.validate_fuel_type",
        side_effect=lambda x: x == "diesel",
    )

    # When
    result = inputhandler.get_user_input()

    # Then
    assert result == (123, "diesel", 45.5)
    assert isinstance(result[0], int)
    assert isinstance(result[1], str)
    assert isinstance(result[2], float)


# Test to make fuel_type_check doesnt return a NULL value
def test_no_null_emission_factor(mocker):
    # Given
    test_fuel = "diesel"
    mock_conn = mocker.patch("sqlite3.connect")
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [("diesel",), ("gasoline",)]

    # When
    result = DataValidator.validate_fuel_type(test_fuel)

    # Then
    assert result is not None
    mock_conn.assert_called_once_with("databases/fuel_type_conversions.db")
    mock_cursor.execute.assert_called_once_with("SELECT fuel_type FROM fuel_types")
