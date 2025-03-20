import json
import logging
from pathlib import Path

from data.database import application_path

logger = logging.getLogger("data")


class SettingsManager:
    def __init__(self):
        self.settings_file = Path(
            application_path, "resources", "config", "settings.json"
        )
        self.settings_file.parent.mkdir(exist_ok=True)
        self.default_settings = {
            "API Keys": {
                "OpenWeatherMap API Key": "",
                "IP Geolocation API Key": "",
            },
            "Paths": {"emissions_modifiers_path": ""},
            "Preferences": {
                "Temperature Measurement Unit": "Celsius",
                "Calculation Unit of Measurement": "Metric",
                "Language": "English",
                "Theme": "Light",
            },
        }
        self._load_settings()

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
