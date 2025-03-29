import json
import logging
from pathlib import Path

import keyring
from keyring.errors import KeyringError, PasswordSetError
from PySide6.QtCore import QObject

from data.database_model import application_path

logger = logging.getLogger("data")


class SettingsModel(QObject):
    def __init__(self):
        super().__init__()
        self.application_controller = None
        self.settings_file = Path(
            application_path, "resources", "config", "settings.json"
        )
        self.settings_file.parent.mkdir(exist_ok=True)
        self.default_settings = (
            {  # TODO: Change these from string literals to actual json.
                "API Keys": {
                    "OpenWeatherMap API Key": "",
                    "IP Geolocation API Key": "",
                },
                "Paths": {"emissions_modifiers_path": ""},
                "Preferences": {
                    "Temperature Measurement Unit": "Celsius",
                    "Calculation Unit of Measurement": "Grams",
                    "Language": "English",
                    "Theme": "Light",
                    "Use Temperature": True,
                    "Fetch Local Temperatures On Startup": True,
                },
            }
        )
        self._load_settings()

    def set_controller(self, application_controller):
        """
        Sets the application controller for the settings model.
        :param application_controller: The application controller instance
        :return: Nothing
        """
        self.application_controller = application_controller

    def _load_settings(self):
        """
        loads settings from settings.json or default values
        :return: Nothing
        """
        if self.settings_file.exists():
            with open(self.settings_file, "r") as f:
                self.settings = json.load(f)
        else:
            self.settings = self.default_settings
            self._save_settings()

    def _save_settings(self):
        """
        Saves current settings to settings.json
        :return: Nothing
        """
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, setting_type, setting_name):
        """
        Get value for specified setting.
        :param setting_type: Domain in which the setting pertains to (Paths, Preferences, etc.)
        :param setting_name: Name of the specific setting whose value you want to retrieve
        :return: Specified setting's value or default value.
        """
        return self.settings.get(
            setting_type, self.default_settings.get(setting_type)
        ).get(setting_name)

    def get_all_settings(self):
        """
        :return: Dictionary of all settings defined in settings.json
        """
        return self.settings

    def update_settings(self, **kwargs):
        """
        Updates multiple settings at once.
        Expected format: {"Category": {"setting_name": value}}
        :param kwargs: Dictionary of settings to update
        :return: Nothing
        """
        for category, settings in kwargs.items():
            if category in self.settings and isinstance(settings, dict):
                self.settings[category].update(settings)
        self._save_settings()

    @staticmethod
    def save_api_key(service_name, key):
        """
        Saves the API key to the keyring on the user's OS.

        :param service_name: The Name of the service being saved
        :param key: password or sensitive information used to access the service.
        :returns: None
        :raises PasswordSetError: If the keyring fails to set the password.
        """
        try:
            keyring.set_password("Carbon Calculator", service_name, key)
        except PasswordSetError:
            logger.debug("SettingsModel: Failed to set password in keyring.")

    @staticmethod
    def get_api_key(service_name):
        """
        Gets the API key from the keyring on the user's OS.

        :param service_name: The name of the service being retrieved
        :returns: service password or sensitive information used to access the service.
        :raises KeyringError: If the keyring fails to retrieve the password.
        """
        try:
            return keyring.get_password("Carbon Calculator", service_name)
        except KeyringError:
            logger.debug("SettingsModel: Failed to get password from keyring.")
            return None
