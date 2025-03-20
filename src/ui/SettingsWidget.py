import os

from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

from src.data.settings_manager import SettingsManager
from ui.generated_python_ui.ui_settings import Ui_settingsWidget


class settingsController:
    def __init__(
        self,
        model,
        view,
        application_controller,
        parent_controller,
        parent_view,
    ):
        self.parent_view = parent_view
        self.parent_controller = parent_controller
        self.application_controller = application_controller
        self.model = model
        self.view = view
        self.__connect_signals()

    def __connect_signals(self) -> None:
        self.parent_controller.combobox_information.connect(
            self.handle_initialization_of_settings
        )
        self.view.emissionsModifiersPathPushButton.clicked.connect(
            self.handle_emissions_path_setting_clicked
        )
        self.view.ipInfoAPIKeyLineEdit.returnPressed.connect(
            self.handle_ip_info_api_key_entered
        )
        self.view.openWeatherMapAPIKeyLineEdit.returnPressed.connect(
            self.handle_open_weather_map_api_key_entered
        )

        # Add connections for combo boxes
        self.view.preferredTemperatureMeasurementComboBox.currentTextChanged.connect(
            self.handle_temperature_unit_changed
        )
        self.view.preferredUnitOfMeasurementComboBox.currentTextChanged.connect(
            self.handle_unit_of_measurement_changed
        )
        self.view.languageComboBox.currentTextChanged.connect(
            self.handle_language_changed
        )
        self.view.themeComboBox.currentTextChanged.connect(
            self.handle_theme_changed
        )
        self.view.temperatureUseCheckBox.stateChanged.connect(
            self.handle_temperature_use_changed
        )

    def handle_initialization_of_settings(self, combobox_information) -> None:
        current_settings = {
            "current_temp_unit": self.model.settings_manager.get_setting(
                "Preferences", "Temperature Measurement Unit"
            ),
            "current_unit_of_measurement": self.model.settings_manager.get_setting(
                "Preferences", "Calculation Unit of Measurement"
            ),
            "current_language": self.model.settings_manager.get_setting(
                "Preferences", "Language"
            ),
            "current_theme": self.model.settings_manager.get_setting(
                "Preferences", "Theme"
            ),
        }
        self.view.initialize_settings(combobox_information, current_settings)

    def handle_emissions_path_setting_clicked(self):
        path = self.view.emissions_modifiers_path_button_clicked()
        self.model.settings_manager.update_settings(
            **{"Paths": {"emissions_modifiers_path": path}}
        )

    def handle_ip_info_api_key_entered(self):
        key = self.view.ipInfoAPIKeyLineEdit.text().strip()
        self.model.settings_manager.update_settings(
            **{"API Keys": {"IP Geolocation API Key": key}}
        )

    def handle_open_weather_map_api_key_entered(self):
        key = self.view.openWeatherMapAPIKeyLineEdit.text().strip()
        self.model.settings_manager.update_settings(
            **{"API Keys": {"OpenWeatherMap API Key": key}}
        )

    def handle_temperature_unit_changed(self, text):
        self.model.settings_manager.update_settings(
            **{"Preferences": {"Temperature Measurement Unit": text}}
        )

    def handle_unit_of_measurement_changed(self, text):
        self.model.settings_manager.update_settings(
            **{"Preferences": {"Calculation Unit of Measurement": text}}
        )

    def handle_language_changed(self, text):
        self.model.settings_manager.update_settings(
            **{"Preferences": {"Language": text}}
        )

    def handle_theme_changed(self, text):
        self.model.settings_manager.update_settings(
            **{"Preferences": {"Theme": text}}
        )

    def handle_temperature_use_changed(self, state):
        is_checked = bool(state)
        self.model.settings_manager.update_settings(
            **{"Preferences": {"Use Temperature": is_checked}}
        )


class settingsModel:
    def __init__(self, settings_manager, application_model):
        self.settings_manager = settings_manager
        self.application_model = application_model


class settingsView(QWidget, Ui_settingsWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def initialize_settings(
        self,
        combobox_information,
        current_settings,
        languages=None,
        themes=None,
    ) -> None:
        """
        Initializes settings ui for user.
        :param current_settings: Dictionary with the current user settings.
        :param combobox_information: Contains information like temp units, calculation units, etc.
        :param languages: supported languages for the application (English, Spanish, etc.)
        :param themes: supported themes for application (Light, Dark, etc.)
        :return: Nothing
        """
        if themes is None:
            themes = {"Dark"}
        if languages is None:
            languages = {"English"}
        current_temp_unit = current_settings["current_temp_unit"]
        current_unit_of_measurement = current_settings[
            "current_unit_of_measurement"
        ]
        current_language = current_settings["current_language"]
        current_theme = current_settings["current_theme"]

        self._insert_current_setting(
            self.preferredTemperatureMeasurementComboBox,
            current_temp_unit,
            combobox_information["temperature_types"],
        )
        self._insert_current_setting(
            self.preferredUnitOfMeasurementComboBox,
            current_unit_of_measurement,
            combobox_information["calculation_units"],
        )
        self._insert_current_setting(
            self.languageComboBox, current_language, languages
        )
        self._insert_current_setting(self.themeComboBox, current_theme, themes)

        self.temperatureUseCheckBox.setChecked(True)

    @staticmethod
    def _insert_current_setting(combo_box, current_setting, items):
        if current_setting in items:
            items.remove(current_setting)
        combo_box.addItem(current_setting)
        combo_box.addItems(items)

    def emissions_modifiers_path_button_clicked(self) -> str:
        input_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Select file",
            os.path.expanduser("~"),
            "JSON Files (*.json)",
        )

        if not input_path:
            return ""

        if (
            input_path.lower().endswith(".json")
            or "json" in selected_filter.lower()
        ):
            pass
        else:
            QMessageBox.critical(self, "Error", "Invalid file type")
            return ""

        return input_path


class settingsWidget(QWidget):
    def __init__(
        self,
        application_controller,
        application_model,
        parent_controller,
        parent_view,
    ):
        super().__init__()
        self.application_controller = application_controller
        self.application_model = application_model
        self.parent_controller = parent_controller
        self.parent_view = parent_view
        self.settings_manager = SettingsManager()
        self.model = settingsModel(
            self.settings_manager, self.application_model
        )
        self.view = settingsView()
        self.controller = settingsController(
            self.model,
            self.view,
            application_controller,
            parent_controller,
            parent_view,
        )
