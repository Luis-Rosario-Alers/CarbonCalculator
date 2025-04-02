import aiohttp
import pytest

from src.services.user_internet_connection_service import user_internet_connection_check


class TestInternetConnectionService:
    # Successful connection returns True when Google responds with status 200
    @pytest.mark.asyncio
    async def test_successful_connection_returns_true(self, mocker):
        # Arrange
        mock_response = mocker.AsyncMock()
        mock_response.status = 200
        mock_session = mocker.AsyncMock()
        mock_session.__aenter__.return_value = mock_response
        mock_session.get.return_value.__aenter__.return_value = mock_response
        mock_client = mocker.AsyncMock()
        mock_client.__aenter__.return_value = mock_session
        mocker.patch("aiohttp.ClientSession", return_value=mock_client)

        # Act
        result = await user_internet_connection_check()

        # Assert
        assert result is True

    # Connection timeout returns False and logs appropriate messages
    @pytest.mark.asyncio
    async def test_connection_timeout_returns_false(self, mocker):
        # Arrange
        mock_logger = mocker.patch(
            "src.services.user_internet_connection_service.logger"
        )
        mock_session = mocker.AsyncMock()
        mock_session.__aenter__.side_effect = aiohttp.ClientError()
        mocker.patch("aiohttp.ClientSession", return_value=mock_session)

        # Act
        result = await user_internet_connection_check()

        # Assert
        mock_logger.info.assert_called_with("Note: Some features may not be available.")
        assert result is False
