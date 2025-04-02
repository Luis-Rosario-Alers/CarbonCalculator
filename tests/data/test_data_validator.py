from unittest.mock import AsyncMock, patch

import pytest

from src.data.data_validator import DataValidator


class TestDataValidator:
    @pytest.fixture
    def data_validator(self) -> DataValidator:
        """Fixture to provide a DataValidator instance."""
        return DataValidator()

    @pytest.mark.asyncio
    async def test_validate_fuel_type_valid(self, data_validator: DataValidator):
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
    async def test_validate_fuel_type_invalid(self, data_validator: DataValidator):
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

    def test_validate_fuel_used_valid(self, data_validator: DataValidator):
        """Test validate_fuel_used with valid inputs."""
        assert data_validator.validate_fuel_used(10) is True
        assert data_validator.validate_fuel_used(10.5) is True

    def test_validate_fuel_used_invalid(self, data_validator: DataValidator):
        """Test validate_fuel_used with invalid inputs."""
        assert data_validator.validate_fuel_used(-1) is False
        assert data_validator.validate_fuel_used("ten") is False
        assert data_validator.validate_fuel_used(0) is False

    def test_validate_fuel_used_validate_integer(
        self, mocker, data_validator: DataValidator
    ):
        mock_validate_integer = mocker.patch(
            "src.data.data_validator.DataValidator.validate_integer"
        )
        mock_validate_integer.return_value = False
        """Test validate_fuel_used with an integer input."""
        assert data_validator.validate_fuel_used(10 * 10**10) is False
        assert mock_validate_integer.call_count == 1
        assert mock_validate_integer.call_args[0][0] == 10 * 10**10

    def test_validate_user_id_valid(self, data_validator: DataValidator):
        """Test validate_user_id with a valid input."""
        assert data_validator.validate_user_id(1) is True

    def test_validate_user_id_invalid(self, data_validator: DataValidator):
        """Test validate_user_id with invalid inputs."""
        assert data_validator.validate_user_id(-1) is False
        assert data_validator.validate_user_id("one") is False
        assert data_validator.validate_user_id(0) is False

    def test_validate_user_id_validate_integer(
        self, mocker, data_validator: DataValidator
    ):
        mock_validate_integer = mocker.patch(
            "src.data.data_validator.DataValidator.validate_integer"
        )
        mock_validate_integer.return_value = False
        """Test validate_user_id with an integer input."""
        assert data_validator.validate_user_id(10 * 10**10) is False
        assert mock_validate_integer.call_count == 1
        assert mock_validate_integer.call_args[0][0] == 10 * 10**10

    def test_validate_emissions_valid(self, data_validator: DataValidator):
        """Test validate_emissions_result with valid inputs."""
        assert data_validator.validate_emissions_result(0) is True
        assert data_validator.validate_emissions_result(10.5) is True

    def test_validate_emissions_invalid(self, data_validator: DataValidator):
        """Test validate_emissions_result with invalid inputs."""
        assert data_validator.validate_emissions_result(-1) is False
        assert data_validator.validate_emissions_result("ten") is False

    def test_validate_integer_valid(self, data_validator: DataValidator):
        """Test validate_integer with valid inputs."""
        assert data_validator.validate_integer(0) is True
        assert data_validator.validate_integer(123456) is True
        assert data_validator.validate_integer(-123456) is True
        assert data_validator.validate_integer(9223372036854775807) is True
        assert data_validator.validate_integer(-9223372036854775808) is True

    def test_validate_integer_invalid(self, data_validator: DataValidator):
        """Test validate_integer with invalid inputs that raise ValueError."""
        with pytest.raises(ValueError):
            data_validator.validate_integer(9223372036854775808)
        with pytest.raises(ValueError):
            data_validator.validate_integer(-9223372036854775809)

    def test_validate_temperature_valid(self, data_validator: DataValidator):
        """Test validate_temperature with valid inputs."""
        assert data_validator.validate_temperature(0, 0) is True  # Celsius
        assert data_validator.validate_temperature(100, 1) is True  # Fahrenheit
        assert data_validator.validate_temperature(273.15, 2) is True  # Kelvin

    def test_validate_temperature_invalid(self, data_validator: DataValidator):
        """Test validate_temperature with invalid inputs."""
        with pytest.raises(ValueError):
            data_validator.validate_temperature(-273.16, 0)  # Celsius
        with pytest.raises(ValueError):
            data_validator.validate_temperature(str(True), 1)  # boolean temperature
        with pytest.raises(ValueError):
            data_validator.validate_temperature(
                bool(1 + 1 == 2), 2
            )  # string temperature
        with pytest.raises(ValueError):
            data_validator.validate_temperature(-459.68, 0)  # Fahrenheit
        with pytest.raises(ValueError):
            data_validator.validate_temperature(0, 2)  # Kelvin
