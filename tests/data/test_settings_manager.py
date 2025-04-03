from pathlib import Path

import pytest

from src.data.settings_model import SettingsModel


class TestSettingsManager:
    @pytest.fixture
    def settings_manager(self) -> SettingsModel:
        return SettingsModel()

    # Successfully loads settings from JSON file
    def test_load_settings_loads_settings_from_json(self, mocker, settings_manager):
        # Arrange
        mock_settings_file = mocker.patch(
            "src.data.settings_manager.SettingsManager._load_settings"
        )
        mock_settings_file.return_value = "test/path/settings.json"

        # Act
        result = settings_manager._load_settings()

        # Assert
        assert result == "test/path/settings.json"

    # Unsuccessfully loads settings from JSON file
    def test_load_settings_raises_exception_when_file_not_found(
        self, mocker, settings_manager
    ):
        # Arrange
        settings_manager.settings_file_path = Path("test/path/settings.json")
        settings_manager.default_settings = {"test": "test"}
        mock_settings_file_exists = mocker.patch(
            "pathlib.Path.exists", return_value=False
        )
        mock_save_settings = mocker.patch(
            "src.data.settings_manager.SettingsManager._save_settings"
        )

        # Act
        settings_manager._load_settings()

        # Assert
        mock_settings_file_exists.assert_called_once()
        assert settings_manager.settings == {"test": "test"}
        mock_save_settings.assert_called_once()

    # Successfully saves settings to JSON file
    def test_save_settings_saves_settings_to_json(self, mocker, settings_manager):
        # Arrange
        mock_save_settings = mocker.patch(
            "src.data.settings_manager.SettingsManager._save_settings"
        )

        # Act
        settings_manager._save_settings()

        # Assert
        mock_save_settings.assert_called_once()

    # gets setting from settings
    def test_get_setting_gets_setting_from_settings(self, settings_manager):
        # Arrange
        settings_manager.settings = {"test": "test"}

        # Act
        result = settings_manager.get_setting("test")

        # Assert
        assert result == "test"

    # gets setting from default settings
    def test_get_setting_gets_setting_from_default_settings(
        self, mocker, settings_manager
    ):
        # Arrange
        mock_file = {"test": "default"}
        settings_manager.default_settings = mock_file
        mock_save_settings = mocker.patch(
            "src.data.settings_manager.SettingsManager._save_settings"
        )

        # Act
        result = settings_manager.get_setting("test")

        # Assert
        assert result == "default"
        mock_save_settings.assert_not_called()

    # updates settings
    def test_update_settings_updates_settings(self, mocker, settings_manager):
        # Arrange
        settings_manager.settings = {"test": "updated"}
        mock_save_settings = mocker.patch(
            "src.data.settings_manager.SettingsManager.update_settings"
        )

        # Act
        settings_manager.update_settings(test="updated")

        # Assert
        assert settings_manager.settings == {"test": "updated"}
        mock_save_settings.assert_called_once()
