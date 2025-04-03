import pytest

from src.core.emissions_calculator import calculate_emissions

# ! BEWARE THAT RUNNING THESE TESTS WILL DELETE THE DATABASES FOLDER AND ALL ITS CONTENTS.
# ! MAKE SURE TO BACK UP ANY IMPORTANT DATA BEFORE RUNNING THESE TESTS.
# ! RUNNING THESE TEST CONCURRENTLY WILL NOT WORK. IDK why.


class TestCalculator:
    @pytest.mark.asyncio
    async def test_calculate_emissions_without_temperature_data(self, mocker):
        # Arrange
        mock_emissions_factor = mocker.patch(
            "src.core.emissions_calculator.get_emissions_factor",
            return_value=2.5,
        )

        # Act
        fuel_type, fuel_used, emissions = await calculate_emissions(1, "gasoline", 10.0)

        # Assert
        assert emissions == 25.0
        mock_emissions_factor.assert_called_once_with("gasoline")

    @pytest.mark.asyncio
    async def test_calculate_emissions_with_temperature_data(self, mocker):
        # Arrange
        test_cases = [
            # (fuel_used, temperature, temperature_type, baseline_temp)
            (10.0, 20.0, 0, 20.0),  # Celsius baseline
            (10.0, 68.0, 1, 68.0),  # Fahrenheit baseline
            (10.0, 293.15, 2, 293.15),  # Kelvin baseline
            (10.0, 25.0, 0, 20.0),  # Above Celsius baseline
            (10.0, 78.0, 1, 68.0),  # Above Fahrenheit baseline
            (10.0, 303.15, 2, 293.15),  # Above Kelvin baseline
            (10.0, 15.0, 0, 20.0),  # Below Celsius baseline
            (10.0, 58.0, 1, 68.0),  # Below Fahrenheit baseline
            (10.0, 283.15, 2, 293.15),  # Below Kelvin baseline
        ]

        emission_factor = 2.5
        mocker.patch(
            "src.core.emissions_calculator.get_emissions_factor",
            return_value=emission_factor,
        )

        for fuel_used, temperature, temp_type, baseline in test_cases:
            # Calculate expected emissions using the formula from emissions_calculator.py:
            # temp_deviation = (temperature - baseline) / baseline
            # adjusted_factor = emissions_factor * (1 + temp_deviation^2)
            # emissions = fuel_used * adjusted_factor

            temp_deviation = (temperature - baseline) / baseline
            adjusted_factor = emission_factor * (1 + temp_deviation**2)
            expected_emissions = fuel_used * adjusted_factor

            # Act
            fuel_type, actual_fuel_used, actual_emissions = await calculate_emissions(
                1, "gasoline", fuel_used, temperature, temp_type
            )

            # Assert
            assert (
                abs(actual_emissions - expected_emissions) < 0.01
            ), f"Failed for {temperature}° (type {temp_type}): expected {expected_emissions:.2f}, got {actual_emissions:.2f}"

    @pytest.mark.asyncio
    async def test_calculate_emissions_with_invalid_temperature_type(self, mocker):
        # Arrange
        mock_db_path = "fuel_type_conversions.db"
        mocker.patch("os.path.join", return_value=mock_db_path)

        # Act/Assert
        with pytest.raises(ValueError):
            await calculate_emissions(1, "gasoline", 10.0, 25.0, 3)

    @pytest.mark.asyncio
    async def test_calculate_emissions_with_invalid_temperature(self, mocker):
        # Arrange
        mock_db_path = "fuel_type_conversions.db"
        mocker.patch("os.path.join", return_value=mock_db_path)

        invalid_temperatures = [
            -273.16,  # Below absolute zero in Celsius
            -459.68,  # Below absolute zero in Fahrenheit
            -0.1,  # Below absolute zero in Kelvin
        ]

        # Act/Assert
        for temp_type, temperature in enumerate(invalid_temperatures):
            with pytest.raises(ValueError):
                await calculate_emissions(1, "gasoline", 10.0, temperature, temp_type)

    @pytest.mark.asyncio
    async def test_calculate_emissions_uses_data_validator_validate_emissions_with_no_temperature_data(
        self, mocker
    ):
        # Arrange
        mock_data_validator = mocker.patch(
            "src.core.emissions_calculator.DataValidator.validate_emissions_result"
        )
        mock_data_validator.return_value = False
        mock_emissions_factor = mocker.patch(
            "src.core.emissions_calculator.get_emissions_factor"
        )
        mock_emissions_factor.return_value = 2.5

        # Act/Assert
        with pytest.raises(ValueError):
            await calculate_emissions(1, "gasoline", 10.0)

    @pytest.mark.asyncio
    async def test_calculate_emissions_uses_data_validator_validate_emissions_with_temperature_data(
        self, mocker
    ):
        # Arrange
        mock_data_validator = mocker.patch(
            "src.core.emissions_calculator.DataValidator.validate_emissions_result"
        )
        mock_data_validator.return_value = False
        mock_emissions_factor = mocker.patch(
            "src.core.emissions_calculator.get_emissions_factor"
        )
        mock_emissions_factor.return_value = 2.5

        # Assert/Act
        with pytest.raises(ValueError):
            await calculate_emissions(1, "gasoline", 10.0, 25.0, 0)
