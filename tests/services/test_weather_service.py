import pytest

from src.services.weather_service import WeatherService


# Returns None when API response code is not 200
@pytest.mark.asyncio
async def test_get_weather_returns_none_on_error_response(mocker):
    # Given
    mock_response = {"cod": 401, "message": "Invalid API key"}
    mock_session = mocker.AsyncMock()
    mock_session.get.return_value.__aenter__.return_value.json.return_value = (
        mock_response
    )
    mocker.patch("aiohttp.ClientSession", return_value=mock_session)

    weather_service = WeatherService("your_weather_api_key_here")
    # When
    result = await weather_service.get_weather(
        latitude=51.5074, longitude=-0.1278
    )
    # Then
    assert result is None
