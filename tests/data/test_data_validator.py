from unittest.mock import AsyncMock, Mock, patch
import pytest

from data.data_validator import DataValidator


@pytest.fixture
def data_validator():
    return DataValidator()

@pytest.mark.asyncio
async def test_validate_fuel_type_valid(data_validator):
    with patch("aiosqlite.connect", new=AsyncMock()) as mock_connect:
        mock_conn = AsyncMock()
        mock_cursor = AsyncMock()
        mock_connect = AsyncMock()
        mock_connect.return_value = mock_conn
        mock_conn.__aenter__.return_value = mock_conn
        mock_conn.__aexit__.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("diesel",), ("petrol",)]

        with patch('aiosqlite.connect', return_value=mock_conn):
            result = await data_validator.validate_fuel_type("electric")
            assert result is False

@pytest.mark.asyncio
async def test_validate_fuel_type_invalid(data_validator):
    with patch("aiosqlite.connect", new=AsyncMock()) as mock_connect:
        mock_conn = AsyncMock()
        mock_cursor = AsyncMock()
        mock_connect = AsyncMock()
        mock_connect.return_value = mock_conn
        mock_conn.__aenter__.return_value = mock_conn
        mock_conn.__aexit__.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("diesel",), ("petrol",)]

        with patch('aiosqlite.connect', return_value=mock_conn):
            result = await data_validator.validate_fuel_type("gasoline")
            assert result is True


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
