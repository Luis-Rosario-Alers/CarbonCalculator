import aiohttp
import pytest

from src.services.weather_service import TemperatureConverter, WeatherService


class TestWeatherService:
    # Returns None when API response code is not 200
    @pytest.mark.asyncio
    async def test_get_weather_returns_none_on_error_response(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.services.weather_service.logger")
        mock_response = {"cod": 401, "message": "Invalid API key"}
        mock_session = mocker.AsyncMock()
        mock_session.get.return_value.__aenter__.return_value.json.return_value = (
            mock_response
        )
        mocker.patch("aiohttp.ClientSession", return_value=mock_session)

        weather_service = WeatherService("your_weather_api_key_here")
        # Act
        result = await weather_service.get_weather(latitude=51.5074, longitude=-0.1278)
        # Assert
        assert result is None
        mock_logger.error.assert_called_with("Weather data not retrieved")

    @pytest.mark.asyncio
    async def test_get_weather_returns_none_on_aiohttp_error_(self, mocker):
        # Arrange
        mock_logger = mocker.patch("src.services.weather_service.logger")
        mock_session = mocker.patch("aiohttp.ClientSession")
        mock_session.side_effect = aiohttp.ClientError

        weather_service = WeatherService("your_weather_api_key_here")
        # Act
        result = await weather_service.get_weather(latitude=51.5074, longitude=-0.1278)
        # Assert
        assert result is None
        mock_logger.error.assert_called()

    # Successfully retrieves weather data and returns tuple of temperatures when valid coordinates provided
    @pytest.mark.asyncio
    async def test_get_weather_returns_temperatures_for_valid_coordinates(self, mocker):
        # Arrange
        api_key = "test_key"
        mock_logger = mocker.patch("src.services.weather_service.logger")
        weather_service = WeatherService(api_key)
        mock_response = mocker.AsyncMock()
        mock_response.json.return_value = {
            "cod": 200,
            "main": {"temp": 293.15},
        }
        mock_session = mocker.AsyncMock()
        mock_session.get.return_value = mock_response
        mock_client_session = mocker.patch("aiohttp.ClientSession")
        mock_client_session.return_value.__aenter__.return_value = mock_session

        # Act
        result = await weather_service.get_weather(latitude=51.5074, longitude=-0.1278)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert result[0] == pytest.approx(20.0)  # Celsius
        assert result[1] == pytest.approx(68.0)  # Fahrenheit
        assert result[2] == pytest.approx(293.15)  # Kelvin
        mock_logger.info.assert_called_with(
            "Temperature in Celsius: 20.0, Fahrenheit: 68.0, Kelvin: 293.15"
        )

    # Convert Kelvin temperature to Celsius with positive input
    def test_convert_positive_kelvin_to_celsius(self):
        # Arrange
        kelvin_temp = 300.0
        converter = TemperatureConverter(kelvin_temp)

        # Act
        celsius = converter.kelvin_to_celsius()

        # Assert
        assert celsius == pytest.approx(26.85)

    # Convert Kelvin temperature to Fahrenheit with positive input
    def test_convert_positive_kelvin_to_fahrenheit(self):
        # Arrange
        kelvin_temp = 300.0
        converter = TemperatureConverter(kelvin_temp)

        # Act
        fahrenheit = converter.kelvin_to_fahrenheit()

        # Assert
        assert fahrenheit == pytest.approx(80.33)

    # Handle negative Kelvin temperatures (physically impossible)
    def test_convert_negative_kelvin_to_celsius(self):
        # Arrange
        kelvin_temp = -10.0
        converter = TemperatureConverter(kelvin_temp)

        # Act
        celsius = converter.kelvin_to_celsius()

        # Assert
        assert celsius < -273.15
