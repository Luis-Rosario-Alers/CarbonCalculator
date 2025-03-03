import logging

from PySide6.QtWidgets import QFileDialog

logger = logging.getLogger("ui")


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
