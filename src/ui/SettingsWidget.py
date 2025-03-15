from PySide6.QtWidgets import QWidget

from src.data.settings_manager import SettingsManager


class settingsController:
    def __init__(self, model, view, application_controller):
        self.application_controller = application_controller
        self.model = model
        self.view = view
        self.__connect_signals()

    def __connect_signals(self):
        pass

    def get_settings(self):
        self.model.settings_manager.get_setting()


class settingsModel:
    def __init__(self, settings_manager, application_model):
        self.settings_manager = settings_manager
        self.application_model = application_model

        def get_settings(self):
            pass


class settingsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def add_settings(
        self,
        calculation_units_of_measurement,
        fuel_units_of_measurement,
        temperature_measurements,
    ):
        self.preferredTemperatureMeasuremenComboBox.addItems()


class settingsWidget(QWidget):
    def __init__(self, application_controller, application_model):
        super().__init__()
        self.application_controller = application_controller
        self.application_model = application_model
        self.settings_manager = SettingsManager()
        self.model = settingsModel(
            self.settings_manager, self.application_model
        )
        self.view = settingsView()
        self.controller = settingsController(
            self.model, self.view, application_controller
        )
        self.view.show()
