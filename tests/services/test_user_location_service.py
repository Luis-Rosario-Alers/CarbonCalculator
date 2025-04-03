import pytest

from src.services.user_location_service import UserLocationService


class TestUserLocationService:
    # Returns tuple of latitude and longitude when ipinfo API call succeeds
    @pytest.mark.asyncio
    async def test_get_user_location_returns_coordinates_on_success(self, mocker):
        # Arrange
        mock_details = mocker.Mock()
        mock_details.latitude = 51.5074
        mock_details.longitude = -0.1278
        mock_handler = mocker.AsyncMock()
        mock_handler.getDetails.return_value = mock_details
        mock_get_handler = mocker.patch("ipinfo.getHandlerAsync")
        mock_get_handler.return_value = mock_handler
        service = UserLocationService("test_token")

        # Act
        result = await service.get_user_location()

        # Assert
        assert result == (51.5074, -0.1278)
        mock_get_handler.assert_called_once_with("test_token")
        mock_handler.getDetails.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_location_returns_none_on_error(self, mocker):
        # Arrange
        mock_handler = mocker.AsyncMock()
        mock_handler.getDetails.side_effect = Exception("API Error")
        mock_get_handler = mocker.patch("ipinfo.getHandlerAsync")
        mock_get_handler.return_value = mock_handler
        service = UserLocationService("test_token")

        # Act
        result = await service.get_user_location()

        # Assert
        assert result is None
        mock_get_handler.assert_called_once_with("test_token")
        mock_handler.getDetails.assert_called_once()
