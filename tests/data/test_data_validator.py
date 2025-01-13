from unittest import mock

import pytest

from data.data_validator import DataValidator


@pytest.fixture
def data_validator():
    return DataValidator()


def test_validate_fuel_type_valid(data_validator):
    with mock.patch("sqlite3.connect") as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock.Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("diesel",), ("petrol",)]

        assert data_validator.validate_fuel_type("diesel") is True


def test_validate_fuel_type_invalid(data_validator):
    with mock.patch("sqlite3.connect") as mock_connect:
        mock_conn = mock.Mock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock.Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("diesel",), ("petrol",)]

        assert data_validator.validate_fuel_type("electric") is False


def test_validate_fuel_used_valid(data_validator):
    assert data_validator.validate_fuel_used(10) is True
    assert data_validator.validate_fuel_used(10.5) is True


def test_validate_fuel_used_invalid(data_validator):
    assert data_validator.validate_fuel_used(-1) is False
    assert data_validator.validate_fuel_used("ten") is False
    assert data_validator.validate_fuel_used(0) is False


def test_validate_user_id_valid(data_validator):
    assert data_validator.validate_user_id(1) is True


def test_validate_user_id_invalid(data_validator):
    assert data_validator.validate_user_id(-1) is False
    assert data_validator.validate_user_id("one") is False
    assert data_validator.validate_user_id(0) is False


def test_validate_emissions_valid(data_validator):
    assert data_validator.validate_emissions(0) is True
    assert data_validator.validate_emissions(10.5) is True


def test_validate_emissions_invalid(data_validator):
    assert data_validator.validate_emissions(-1) is False
    assert data_validator.validate_emissions("ten") is False


def test_validate_integer_valid(data_validator):
    assert data_validator.validate_integer(0) is True
    assert data_validator.validate_integer(123456) is True
    assert data_validator.validate_integer(-123456) is True
    assert data_validator.validate_integer(9223372036854775807) is True
    assert data_validator.validate_integer(-9223372036854775808) is True


def test_validate_integer_invalid(data_validator):
    with pytest.raises(ValueError):
        data_validator.validate_integer(9223372036854775808)
    with pytest.raises(ValueError):
        data_validator.validate_integer(-9223372036854775809)
