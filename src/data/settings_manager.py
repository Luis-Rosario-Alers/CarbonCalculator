import json
from pathlib import Path

from data.database import application_path


class SettingsManager:
    def __init__(self):
        self.settings_file = Path(
            application_path, "resources", "config", "settings.json"
        )
        self.settings_file.parent.mkdir(exist_ok=True)
        self.default_settings = {
            "ip_key": "",
            "weather_key": "",
            "emission_modifiers_path": "",
            "Preferred Temperature Measurement Unit": "",
            "Preferred Calculation Unit of Measurement": "",
        }
        self._load_settings()

    def _load_settings(self):
        if self.settings_file.exists():
            with open(self.settings_file, "r") as f:
                self.settings = json.load(f)
        else:
            self.settings = self.default_settings
            self._save_settings()

    def _save_settings(self):
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, key):
        return self.settings.get(key, self.default_settings.get(key))

    def update_settings(self, **kwargs):
        self.settings.update(kwargs)
        self._save_settings()
