import logging
import os
from typing import List

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QComboBox, QFileDialog, QMessageBox, QWidget

from ui.generated_python_ui.ui_settings import Ui_settingsWidget

logger = logging.getLogger("ui")


class SettingsController(QObject):
    def __init__(
        self,
        model,
        view,
        application_controller,
        parent_controller,
        parent_view,
    ):
        super().__init__()
        self.parent_view = parent_view
        self.parent_controller = parent_controller
        self.application_controller = application_controller
        self.model = model
        self.view = view
        self.__connect_signals()

    def __connect_signals(self) -> None:
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
        self.view.themeComboBox.currentTextChanged.connect(self.handle_theme_changed)
        self.view.temperatureUseCheckBox.stateChanged.connect(
            self.handle_temperature_use_changed
        )
        self.view.fetchLocalTemperaturesOnStartupCheckBox.stateChanged.connect(
            self.handle_fetch_local_temperatures_changed
        )
        self.view.preferredUserIDSpinBox.valueChanged.connect(
            self.handle_user_id_changed
        )

    def handle_initialization_of_settings(self, combobox_information) -> None:

        current_settings = self.model.settings_model.get_all_settings()

        self.view.initialize_settings(combobox_information, current_settings)

    def handle_emissions_path_setting_clicked(self):
        path = self.view.emissions_modifiers_path_button_clicked()
        self.model.settings_model.update_settings(
            **{"Paths": {"emissions_modifiers_path": path}}
        )

    def handle_ip_info_api_key_entered(self):
        key = self.view.ipInfoAPIKeyLineEdit.text().strip()
        if key:
            self.model.settings_model.save_api_key("IP Geolocation API Key", key)
            self.model.settings_model.update_settings(
                **{"API Keys": {"IP Geolocation API Key": "[STORED_SECURELY]"}}
            )
        else:
            QMessageBox.critical(
                self.view,
                "Error",
                "Please enter a valid ipinfo API key.",
            )
            self.view.openWeatherMapAPIKeyLineEdit.setText("")
            return

    def handle_open_weather_map_api_key_entered(self):
        key = self.view.openWeatherMapAPIKeyLineEdit.text().strip()
        if key:
            self.model.settings_model.save_api_key("OpenWeatherMap API Key", key)
            self.model.settings_model.update_settings(
                **{"API Keys": {"OpenWeatherMap API Key": "[STORED_SECURELY]"}}
            )
        else:
            QMessageBox.critical(
                self.view,
                "Error",
                "Please enter a valid OpenWeatherMap API key.",
            )
            self.view.openWeatherMapAPIKeyLineEdit.setText("")

    def handle_temperature_unit_changed(self, text):
        self.model.settings_model.update_settings(
            **{"Preferences": {"Temperature Measurement Unit": text}}
        )

    def handle_unit_of_measurement_changed(self, text):
        self.model.settings_model.update_settings(
            **{"Preferences": {"Calculation Unit of Measurement": text}}
        )

    def handle_language_changed(self, text):
        self.model.settings_model.update_settings(**{"Preferences": {"Language": text}})
        self.application_controller.set_application_language(text)

    def handle_theme_changed(self, text):
        self.model.settings_model.update_theme(**{"Preferences": {"Theme": text}})

    def handle_temperature_use_changed(self, state):
        is_checked = bool(state)
        self.model.settings_model.update_settings(
            **{"Preferences": {"Use Temperature": is_checked}}
        )

    def handle_fetch_local_temperatures_changed(self, state):
        is_checked = bool(state)
        self.model.settings_model.update_settings(
            **{"Preferences": {"Fetch Local Temperatures On Startup": is_checked}}
        )

    def handle_user_id_changed(self):
        value = str(self.view.preferredUserIDSpinBox.value())
        if int(value) >= 0:
            self.model.settings_model.update_settings(
                **{"Preferences": {"User ID": value}}
            )
        else:
            QMessageBox.critical(
                self.view, "Invalid User ID", "Please enter a valid user ID."
            )
            self.view.preferredUserIDSpinBox.setValue(0)


class SettingsModel:
    def __init__(self, application_model):
        self.application_model = application_model
        self.settings_model = application_model.settings_model


class SettingsView(QWidget, Ui_settingsWidget):
    def __init__(self, parent_view):
        super().__init__()
        self.setupUi(self)
        self.parent_view = parent_view

    def initialize_settings(
        self,
        combobox_information,
        current_settings,
    ) -> None:
        """
        Initializes settings ui for user.
        :param current_settings: Dictionary with the current user settings.
        :param combobox_information: Contains information like temp units, calculation units, etc.
        :return: Nothing
        """
        # Process settings by category
        preference_settings = current_settings.get("Preferences", {})
        api_keys = current_settings.get("API Keys", {})

        # Initialize preferences
        current_temp_unit = preference_settings.get(
            "Temperature Measurement Unit", "Celsius"
        )
        current_unit_of_measurement = preference_settings.get(
            "Calculation Unit of Measurement", "Grams"
        )
        current_language = preference_settings.get("Language", "English")
        current_theme = preference_settings.get("Theme", "Light")
        fetch_local_temps_on_startup = preference_settings.get(
            "Fetch Local Temperatures On Startup", True
        )
        use_temperature = preference_settings.get("Use Temperature", True)
        current_user_id = preference_settings.get("User ID", "1")

        # insert settings into comboboxes
        # Fixme: This function seems to over write the emissions_modifiers_path for the [[settings.json]] file
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
            self.languageComboBox, current_language, ["English", "Spanish"]
        )
        self._insert_current_setting(
            self.themeComboBox, current_theme, ["Light", "Dark"]
        )

        # Note: signals are blocked to avoid unnecessary slot activations.
        self.fetchLocalTemperaturesOnStartupCheckBox.blockSignals(True)
        self.temperatureUseCheckBox.blockSignals(True)
        self.preferredUserIDSpinBox.blockSignals(True)
        self.fetchLocalTemperaturesOnStartupCheckBox.setChecked(
            fetch_local_temps_on_startup
        )
        self.temperatureUseCheckBox.setChecked(use_temperature)
        self.fetchLocalTemperaturesOnStartupCheckBox.blockSignals(False)
        self.temperatureUseCheckBox.blockSignals(False)

        self.preferredUserIDSpinBox.setValue(int(current_user_id))
        self.preferredUserIDSpinBox.blockSignals(False)

        # Initialize API keys
        openweather_key = api_keys.get("OpenWeatherMap API Key", "")
        ipinfo_key = api_keys.get("IP Geolocation API Key", "")
        self.openWeatherMapAPIKeyLineEdit.setText(openweather_key)
        self.ipInfoAPIKeyLineEdit.setText(ipinfo_key)

    @staticmethod
    def _insert_current_setting(combo_box: QComboBox, current_setting, items: List):
        """
        Inserts the current settings into the combo box and then sets the current text as the current setting.
        :param combo_box: Combobox object
        :param current_setting: current setting state
        :param items: items that normally go into the combo box
        :return:
        """
        combo_box.blockSignals(True)
        combo_box.addItems(items)
        combo_box.setCurrentText(current_setting)
        combo_box.blockSignals(False)

    def emissions_modifiers_path_button_clicked(self) -> str:
        input_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Select file",
            os.path.expanduser("~"),
            "JSON Files (*.json)",
        )

        if not input_path:
            return ""

        if input_path.lower().endswith(".json") or "json" in selected_filter.lower():
            pass
        else:
            QMessageBox.critical(self, "Error", "Invalid file type")
            return ""

        return input_path


class SettingsWidget(QWidget):
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
        self.model = SettingsModel(self.application_model)
        self.view = SettingsView(self.parent_view)
        self.controller = SettingsController(
            self.model,
            self.view,
            application_controller,
            parent_controller,
            parent_view,
        )
