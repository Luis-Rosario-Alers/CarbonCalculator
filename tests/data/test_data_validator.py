from unittest.mock import AsyncMock, patch

import pytest

from data.data_validator import DataValidator


@pytest.fixture
def data_validator() -> DataValidator:
    """Fixture to provide a DataValidator instance."""
    return DataValidator()


@pytest.mark.asyncio
async def test_validate_fuel_type_valid(data_validator: DataValidator):
    """Test validate_fuel_type with an invalid fuel type."""
    mock_cursor = AsyncMock()
    mock_cursor.fetchone.return_value = "gasoline"

    mock_conn = AsyncMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_conn.__aenter__.return_value = mock_conn
    mock_conn.__aexit__.return_value = None

    with patch("aiosqlite.connect", return_value=mock_conn):
        result = await data_validator.validate_fuel_type("gasoline")
        assert result is True

    # Verify that the mock cursor was used
    mock_cursor.fetchone.assert_called_once()

    # Verify that the fuel types were returned as expected
    assert mock_cursor.fetchone.return_value == "gasoline"


@pytest.mark.asyncio
async def test_validate_fuel_type_invalid(data_validator: DataValidator):
    """Test validate_fuel_type with a valid fuel type."""
    mock_cursor = AsyncMock()
    mock_cursor.fetchone.return_value = "biodiesel"

    mock_conn = AsyncMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_conn.__aenter__.return_value = mock_conn
    mock_conn.__aexit__.return_value = None

    with patch("aiosqlite.connect", return_value=mock_conn):
        result = await data_validator.validate_fuel_type("electric")
        assert result is False

    # Verify that the mock cursor was used
    mock_cursor.fetchone.assert_called_once()

    # Verify that the fuel types were returned as expected
    assert mock_cursor.fetchone.return_value == "biodiesel"


def test_validate_fuel_used_valid(data_validator: DataValidator):
    """Test validate_fuel_used with valid inputs."""
    assert data_validator.validate_fuel_used(10) is True
    assert data_validator.validate_fuel_used(10.5) is True


def test_validate_fuel_used_invalid(data_validator: DataValidator):
    """Test validate_fuel_used with invalid inputs."""
    assert data_validator.validate_fuel_used(-1) is False
    assert data_validator.validate_fuel_used("ten") is False
    assert data_validator.validate_fuel_used(0) is False


def test_validate_user_id_valid(data_validator: DataValidator):
    """Test validate_user_id with a valid input."""
    assert data_validator.validate_user_id(1) is True


def test_validate_user_id_invalid(data_validator: DataValidator):
    """Test validate_user_id with invalid inputs."""
    assert data_validator.validate_user_id(-1) is False
    assert data_validator.validate_user_id("one") is False
    assert data_validator.validate_user_id(0) is False


def test_validate_emissions_valid(data_validator: DataValidator):
    """Test validate_emissions with valid inputs."""
    assert data_validator.validate_emissions(0) is True
    assert data_validator.validate_emissions(10.5) is True


def test_validate_emissions_invalid(data_validator: DataValidator):
    """Test validate_emissions with invalid inputs."""
    assert data_validator.validate_emissions(-1) is False
    assert data_validator.validate_emissions("ten") is False


def test_validate_integer_valid(data_validator: DataValidator):
    """Test validate_integer with valid inputs."""
    assert data_validator.validate_integer(0) is True
    assert data_validator.validate_integer(123456) is True
    assert data_validator.validate_integer(-123456) is True
    assert data_validator.validate_integer(9223372036854775807) is True
    assert data_validator.validate_integer(-9223372036854775808) is True


def test_validate_integer_invalid(data_validator: DataValidator):
    """Test validate_integer with invalid inputs that raise ValueError."""
    with pytest.raises(ValueError):
        data_validator.validate_integer(9223372036854775808)
    with pytest.raises(ValueError):
        data_validator.validate_integer(-9223372036854775809)
