import logging

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from data.settings_manager import SettingsManager
from utils.logging import setup_logging

setup_logging()
logger = logging.getLogger("ui")


# SettingsMenu class
# This class is responsible for creating the settings menu
# It will be used to change the settings of the application


class SettingPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.settings_manager = SettingsManager()
        self.settings_manager._load_settings()

    def init_ui(self):
        self.setWindowTitle("Settings")
        self.ip_key_label = QLabel("IP Key")
        self.ip_key_input = QLineEdit()
        self.ip_key_input.setPlaceholderText("Enter IP Key")
        self.ip_key_input.setFixedSize(350, 25)

        self.weather_key_label = QLabel("Weather Key")
        self.weather_key_input = QLineEdit()
        self.weather_key_input.setPlaceholderText("Enter Weather Key")
        self.weather_key_input.setFixedSize(350, 25)

        self.change_emissions_factors_button = QPushButton(
            "Change Emissions Factors path"
        )
        self.change_emissions_factors_button.setFixedSize(175, 25)
        self.change_emissions_factors_button.setStyleSheet("text-align: left;")
        self.change_emissions_factors_button.clicked.connect(
            self.change_emissions_factors_path
        )

        self.change_emissions_factors_label = QLabel(
            "Note: changing settings requires a restart of the application"
        )
        self.change_emissions_factors_label.setStyleSheet(
            "font-style: italic; color: rgba(255, 255, 255, 0.5);"
        )

        self.set_settings_button = QPushButton("Set Settings")
        self.set_settings_button.setFixedSize(100, 25)

        self.set_settings_button.clicked.connect(self.set_settings_state)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.ip_key_label)
        self.layout().addWidget(self.ip_key_input)
        self.layout().addWidget(self.weather_key_label)
        self.layout().addWidget(self.weather_key_input)
        self.layout().addWidget(self.change_emissions_factors_button)
        self.layout().addSpacing(20)
        self.layout().addWidget(self.set_settings_button)
        self.layout().addWidget(self.change_emissions_factors_label)
        self.layout().addStretch(1)

    def set_settings_state(self):
        self.settings_manager.update_settings(
            ip_key=self.ip_key_input.text(),
            weather_key=self.weather_key_input.text(),
        )
        logger.info("Settings updated")
        logger.info(f"IP Key: {self.settings_manager.get_setting('ip_key')}")
        logger.info(
            f"Weather Key: {self.settings_manager.get_setting('weather_key')}"
        )

    def change_emissions_factors_path(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec():
            path = dialog.selectedFiles()[0]
        else:
            return
        self.settings_manager.update_settings(emissions_factors_path=path)
        logger.info(
            f"New Emissions Factors Path: {self.settings_manager.get_setting('emissions_factors_path')}"
        )
