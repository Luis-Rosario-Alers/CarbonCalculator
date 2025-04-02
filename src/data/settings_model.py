import json
import logging
from pathlib import Path

import keyring
from keyring.errors import KeyringError, PasswordSetError
from PySide6.QtCore import QObject, Signal

from data.database_model import application_path

logger = logging.getLogger("data")


class SettingsModel(QObject):
    theme_changed = Signal(bool)  # True if light mode, False if dark mode.

    def __init__(self):
        super().__init__()
        self.application_controller = None
        self.settings_file_path = Path(
            application_path, "resources", "config", "settings.json"
        )
        self.settings_file_path.parent.mkdir(exist_ok=True)
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
        logger.debug(
            f"SettingsModel.__init__: Initializing with settings path: {self.settings_file_path}"
        )
        self._load_settings()

    def set_controller(self, application_controller):
        """
        Sets the application controller for the settings model.
        :param application_controller: The application controller instance
        :return: Nothing
        """
        self.application_controller = application_controller
        logger.debug("SettingsModel.set_controller: Application controller set")

    def _load_settings(self):
        """
        loads settings from settings.json or default values
        :return: Nothing
        """
        if self.settings_file_path.exists():
            logger.debug(
                "SettingsModel._load_settings: Settings file exists, loading from: {0}".format(
                    self.settings_file_path
                )
            )
            with open(self.settings_file_path, "r") as f:
                self.settings = json.load(f)
        else:
            logger.debug(
                "SettingsModel._load_settings: No settings file found, using defaults"
            )
            self.settings = self.default_settings
            self._save_settings()

    def _save_settings(self):
        """
        Saves current settings to settings.json
        :return: Nothing
        """
        logger.debug(
            f"SettingsModel._save_settings: Saving settings to: {self.settings_file_path}"
        )
        with open(self.settings_file_path, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, setting_type, setting_name):
        """
        Get value for specified setting.
        :param setting_type: Domain in which the setting pertains to (Paths, Preferences, etc.)
        :param setting_name: Name of the specific setting whose value you want to retrieve
        :return: Specified setting's value or default value.
        """
        value = self.settings.get(
            setting_type, self.default_settings.get(setting_type)
        ).get(setting_name)
        logger.debug(
            f"SettingsModel.get_setting: Retrieved setting [{setting_type}][{setting_name}] = {value}"
        )
        return value

    def get_all_settings(self):
        """
        :return: Dictionary of all settings defined in settings.json
        """
        logger.debug(
            "SettingsModel.get_all_settings: Returning all application settings"
        )
        return self.settings

    def update_settings(self, **kwargs):
        """
        Updates multiple settings at once.
        Expected format: {"Category": {"setting_name": value}}
        :param kwargs: Dictionary of settings to update
        :return: Nothing
        """
        logger.debug(f"SettingsModel.update_settings: Updating settings with: {kwargs}")
        for category, settings in kwargs.items():
            if category in self.settings and isinstance(settings, dict):
                self.settings[category].update(settings)
        self._save_settings()

    def update_theme(self, **kwargs):
        """
        Updates theme,
        Expected format: {"Category": {"setting_name": value}}
        :param kwargs: Dictionary of settings to update
        :return: Nothing
        """
        # yes, I know it's basically a copy of update_settings.
        # I just need separate functions so that I can emit signals properly
        # and keep separation of concerns
        logger.debug(f"SettingsModel.update_settings: Updating theme with: {kwargs}")
        for category, settings in kwargs.items():
            if category in self.settings and isinstance(settings, dict):
                if settings.get("Theme") == "Light":
                    self.settings[category].update(settings)
                    logger.debug(
                        f"SettingsModel.update_theme: theme_changed emitting: {True}"
                    )
                    self.theme_changed.emit(True)
                else:
                    self.settings[category].update(settings)
                    logger.debug(
                        f"SettingsModel.update_theme: theme_changed emitting: {False}"
                    )
                    self.theme_changed.emit(False)
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
        logger.debug(
            f"SettingsModel.save_api_key: Saving API key for service: {service_name}"
        )
        try:
            keyring.set_password("Carbon Calculator", service_name, key)
            logger.debug(
                f"SettingsModel.save_api_key: Successfully saved API key for: {service_name}"
            )
        except PasswordSetError:
            logger.error(
                f"SettingsModel.save_api_key: Failed to set password in keyring for: {service_name}"
            )

    @staticmethod
    def get_api_key(service_name):
        """
        Gets the API key from the keyring on the user's OS.

        :param service_name: The name of the service being retrieved
        :returns: service password or sensitive information used to access the service.
        :raises KeyringError: If the keyring fails to retrieve the password.
        """
        logger.debug(
            f"SettingsModel.get_api_key: Retrieving API key for service: {service_name}"
        )
        try:
            key = keyring.get_password("Carbon Calculator", service_name)
            logger.debug(
                f"SettingsModel.get_api_key: Successfully retrieved API key for: {service_name}"
            )
            return key
        except KeyringError:
            logger.error(
                f"SettingsModel.get_api_key: Failed to get password from keyring for: {service_name}"
            )
            return None
