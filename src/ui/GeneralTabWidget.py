import logging
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import QObject, Qt, QTimer, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QApplication, QFileDialog, QStyle, QTableView, QWidget

from data.database_model import databases_folder
from data.export_manager import ExportManager
from data.import_manager import ImportManager
from services.user_internet_connection_service import user_internet_connection_check
from services.user_location_service import UserLocationService
from services.weather_service import WeatherService
from ui.generated_python_ui.ui_generalTabWidget import Ui_GeneralWidget
from ui.SettingsWidget import SettingsWidget
from utils.gui_utilities import connect_threaded

logger = logging.getLogger("ui")


class GeneralTabController(QObject):
    calculation_requested = Signal(int, str, float, float, str, str)
    combobox_information = Signal(dict)

    def __init__(
        self,
        model: "GeneralTabModel",
        view: "GeneralTabView",
        application_controller,
    ) -> None:
        super().__init__()
        self.model: "GeneralTabModel" = model
        self.view: "GeneralTabView" = view
        self.application_controller = application_controller
        self.settingsWidget = None
        self.__connect_signals()

    def __connect_signals(self) -> None:
        logger.debug("GeneralTabController.__connect_signals: Connecting signals")
        self.model.databases_model.databases_initialized.connect(
            self.handle_initialization_of_database_widget
        )
        self.model.databases_model.calculation_logged.connect(
            self.handle_database_widget_update
        )
        self.view.fuelUnitOfMeasurementComboBox.currentTextChanged.connect(
            self.handle_fuel_unit_changed
        )
        self.view.realTimeTemperatureCheckBox.toggled.connect(
            self.handle_real_time_temperatures_check_box_changed
        )
        self.view.importPushButton.clicked.connect(self.handle_import_button_clicked)
        self.view.exportPushButton.clicked.connect(self.handle_export_button_clicked)
        self.view.settingsPushButton.clicked.connect(
            self.handle_settings_button_clicked
        )
        self.view.calculateContainerPushButton.clicked.connect(
            self.handle_calculate_button_clicked
        )
        # Handles progress bar updates.
        self.application_controller.progress_updated.connect(
            self.handle_progress_update
        )
        self.application_controller.progress_complete.connect(
            self.handle_progress_complete
        )

        self.model.databases_model.databases_initialized.connect(
            self.model.populate_combobox_dataclass
        )
        self.model.databases_model.databases_initialized.connect(
            self.handle_comboboxes_initialization
        )
        connect_threaded(
            self.application_controller,
            "initialization",
            self.handle_real_time_temperatures_api_call,
        )
        connect_threaded(
            self.application_controller,
            "application_closed",
            self.handle_application_close,
        )

    def handle_progress_update(self, percentage: int, message: str) -> None:
        self.view.update_progress_status(percentage, message)

    def handle_progress_complete(self) -> None:
        self.view.progressBar.setValue(100)

        # Hides progress bar and label after 3 seconds
        QTimer.singleShot(3000, lambda: self.view.progressBar.setVisible(False))
        QTimer.singleShot(3000, lambda: self.view.progressLabel.setVisible(False))

    def handle_real_time_temperatures_api_call(self) -> None:
        logger.debug(
            "GeneralTabController.handle_real_time_temperatures_api_call: Requesting temperature data"
        )
        if self.model.settings_model.get_setting(
            "Preferences", "Fetch Local Temperatures On Startup"
        ):
            self.model.load_real_time_temperature_data()
        else:
            logger.info("skipping temperature data fetch.")

    def handle_import_button_clicked(self) -> None:
        logger.debug(
            "GeneralTabController.handle_import_button_clicked: Import button clicked"
        )
        input_path, file_type = self.view.get_import_file_path()
        if file_type:
            logger.debug(f"GeneralTabWidget: importing {file_type} file")
            if file_type == "json":
                import_manager = ImportManager()
                import_manager.import_from_json(input_path)
                self.view.update_database_table()
            elif file_type == "csv":
                import_manager = ImportManager()
                import_manager.import_from_csv(input_path)
                self.view.update_database_table()
            else:
                logger.error("GeneralTabWidget: Unsupported file type")

    def handle_export_button_clicked(self) -> None:
        logger.debug(
            "GeneralTabController.handle_export_button_clicked: Export button clicked"
        )
        output_path, selected_filter = self.view.get_export_file_path()
        if output_path:
            logger.debug(f"GeneralTabWidget: exporting {selected_filter} file")
            if selected_filter == "json":
                export_manager = ExportManager()
                export_manager.export_to_json(output_path)
            elif selected_filter == "csv":
                export_manager = ExportManager()
                export_manager.export_to_csv(output_path)
            else:
                logger.error("GeneralTabWidget: Unsupported file type")

    def handle_initialization_of_database_widget(self) -> None:
        self.model.load_database_table_content()
        self.view.load_database_table()

    def handle_comboboxes_initialization(self) -> None:
        logger.debug(
            "GeneralTabController.handle_comboboxes_initialization: Initializing comboboxes"
        )
        combobox_data = self.model.combobox_data

        self.combobox_information.emit(
            {
                "fuel_types": combobox_data.fuel_types,
                "farming_techniques": combobox_data.farming_techniques,
                "fuel_type_units": combobox_data.fuel_type_units,
                "calculation_units": combobox_data.calculation_units,
                "temperature_types": combobox_data.temperature_types,
            }
        )
        logger.debug(
            "GeneralTabController.handle_comboboxes_initialization: Emitted combobox_information"
        )

        self.view.initialize_combobox_values(
            combobox_data.fuel_types,
            combobox_data.farming_techniques,
            combobox_data.fuel_type_units,
            combobox_data.temperature_types,
            combobox_data.calculation_units,
        )

        self.handle_apply_user_preferences()

    def handle_calculate_button_clicked(self) -> None:
        (
            user_id,
            fuel_type,
            fuel_unit,
            amount_of_fuel_used,
            temperature_value,
            temperature_type,
            farming_technique,
            calculation_unit,
        ) = self.view.get_calculation_info(self.model.real_time_temp_data)
        self.model.calculation_model.calculate_emissions(  # ? We could probably change this to a signal.
            user_id,
            fuel_type,
            fuel_unit,
            amount_of_fuel_used,
            temperature=temperature_value,
            temperature_type=temperature_type,
            farming_technique=farming_technique,
            calculation_unit=calculation_unit,
        )

    def handle_application_close(self) -> None:
        logger.debug("GeneralTabWidget: closing database connection")
        self.view.close_database_on_application_close()

    def handle_database_widget_update(self) -> None:
        logger.debug("GeneralTabWidget: updating database view")
        self.view.update_database_table()

    def handle_fuel_unit_changed(self, fuel_unit: str) -> None:
        logger.debug("GeneralTabWidget: fuel unit changed")
        self.view.fuel_unit_suffix_update(fuel_unit)

    def handle_real_time_temperatures_check_box_changed(self, checked: bool) -> None:
        logger.debug(
            f"GeneralTabWidget: Real-Time temperature check box changed to {checked}"
        )
        if not checked:
            logger.debug("GeneralTabWidget: enabling temperature controls")
            self.view.temperatureDoubleSpinBox.setEnabled(True)
        else:
            logger.debug("GeneralTabWidget: disabling temperature controls")
            self.view.temperatureDoubleSpinBox.setEnabled(False)

    def handle_settings_button_clicked(self) -> None:
        logger.debug("GeneralTabWidget: settings button clicked")
        # Create settings widget only once (lazy initialization)
        if not hasattr(self, "settingsWidget") or self.settingsWidget is None:
            self.settingsWidget = SettingsWidget(
                self.application_controller,
                self.model.application_model,
                self,
                self.view,
            )

            # Configure as proper dialog with correct parenting
            self.settingsWidget.view.setParent(self.view)
            self.settingsWidget.view.setWindowFlags(Qt.Dialog)
            self.settingsWidget.view.setWindowModality(Qt.WindowModal)

            combobox_data = self.model.combobox_data
            combobox_information = {
                "fuel_types": combobox_data.fuel_types,
                "farming_techniques": combobox_data.farming_techniques,
                "fuel_type_units": combobox_data.fuel_type_units,
                "calculation_units": combobox_data.calculation_units,
                "temperature_types": combobox_data.temperature_types,
            }
            self.settingsWidget.controller.handle_initialization_of_settings(
                combobox_information
            )

        # Position dialog centered on parent
        self.settingsWidget.view.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.settingsWidget.view.size(),
                self.view.geometry(),
            )
        )
        self.settingsWidget.view.show()

    def handle_apply_user_preferences(self):
        logger.debug("GeneralTabWidget: setting user preferences")

        preferred_temp_unit = self.model.settings_model.get_setting(
            "Preferences", "Temperature Measurement Unit"
        )
        preferred_calc_unit = self.model.settings_model.get_setting(
            "Preferences", "Calculation Unit of Measurement"
        )
        use_temperature = self.model.settings_model.get_setting(
            "Preferences", "Use Temperature"
        )
        preferred_user_id = self.model.settings_model.get_setting(
            "Preferences", "User ID"
        )

        self.view.apply_user_preferences(
            [
                preferred_temp_unit,
                preferred_calc_unit,
                use_temperature,
                preferred_user_id,
            ]
        )


class GeneralTabModel:
    @dataclass
    class ComboBoxData:
        fuel_types: List[str] = field(default_factory=list)
        farming_techniques: List[str] = field(default_factory=list)
        fuel_type_units: List[str] = field(
            default_factory=lambda: ["Liters", "Cubic Meters", "Cubic Feet"]
        )
        calculation_units: List[str] = field(
            default_factory=lambda: [
                "Milligrams",
                "Grams",
                "Kilograms",
                "Metric Tons",
            ]
        )
        temperature_types: List[str] = field(
            default_factory=lambda: ["Celsius", "Fahrenheit", "Kelvin"]
        )

    def __init__(self, application_model) -> None:
        self.application_model = application_model
        self.databases_model = self.application_model.databases_model
        self.calculation_model = self.application_model.calculation_model
        self.settings_model = self.application_model.settings_model
        self.real_time_temp_data = None
        self.combobox_data = self.ComboBoxData()

    def populate_combobox_dataclass(self):
        try:
            self.combobox_data.fuel_types = self.databases_model.get_fuel_types()
            self.combobox_data.farming_techniques = (
                self.databases_model.get_farming_techniques()
            )
        except Exception as e:
            logger.debug(f"GeneralTabModel.__init__: Could not load database data: {e}")

        logger.debug("GeneralTabModel.__init__: Model initialized with combobox data")

    def load_database_table_content(self) -> None:
        pass

    def load_real_time_temperature_data(self) -> None:
        ipinfo_user_key = self.settings_model.get_api_key("IP Geolocation API Key")
        open_weather_map_user_key = self.settings_model.get_api_key(
            "OpenWeatherMap API Key"
        )

        if open_weather_map_user_key is None:
            raise ValueError("User does not have necessary API keys set.")

        if user_internet_connection_check():
            latitude, longitude = UserLocationService(
                ipinfo_user_key
            ).get_user_location()
            temperature_data = WeatherService(
                open_weather_map_user_key
            ).get_weather_data(latitude, longitude)
            self.real_time_temp_data = temperature_data
        else:
            raise ConnectionError("Unable to find internet connection.")


class GeneralTabView(QWidget, Ui_GeneralWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.database_loaded: bool = False
        self.db_connection = None
        self.sql_widget_model = None

    def update_progress_status(self, percentage: int, message: str) -> None:
        self.progressBar.setValue(percentage)
        self.progressLabel.setText(message)

        self.progressBar.setVisible(True)
        self.progressLabel.setVisible(True)

        # Force update to ensure UI refreshes
        QApplication.processEvents()

    def load_database_table(self) -> None:
        if not self.database_loaded:
            logger.info("Loading database table")
            # Set up database connection
            self.db_connection = QSqlDatabase.addDatabase("QSQLITE")
            db_path = os.path.join(databases_folder, "emissions.db")
            self.db_connection.setDatabaseName(db_path)

            if not self.db_connection.open():
                logger.error(
                    f"Failed to open database: {self.db_connection.lastError().text()}"
                )
                return

            # Create and configure the model
            self.sql_widget_model = QSqlTableModel(self, self.db_connection)
            self.sql_widget_model.setTable("emissions")

            # Check if select() succeeded
            if not self.sql_widget_model.select():
                logger.error(
                    f"Failed to select data: {self.sql_widget_model.lastError().text()}"
                )
                return

            if hasattr(self, "sqlTableView"):
                self.sqlTableView.setEditTriggers(QTableView.NoEditTriggers)
                # Explicitly set the model after select() has completed
                self.sqlTableView.setModel(self.sql_widget_model)

                # Make sure columns are visible
                self.sqlTableView.horizontalHeader().setVisible(True)
                self.sqlTableView.resizeColumnsToContents()

                # Check row count for debugging
                row_count = self.sql_widget_model.rowCount()
                logger.info(f"Loaded {row_count} rows from emissions table")

            else:
                logger.error("sqlTableView not found in UI")
            self.database_loaded = True
        else:
            logger.debug("Database already loaded, skipping")

    def close_database_on_application_close(self) -> None:
        logger.info("closing database connection.")
        if self.db_connection and self.db_connection.isOpen():
            self.db_connection.close()

    def initialize_combobox_values(
        self,
        fuel_types: List[str],
        farming_techniques: List[str],
        fuel_type_units: List[str],
        temperature_types: List[str],
        calculation_units: List[str],
    ) -> None:
        self.farmingTechniqueComboBox.clear()
        self.farmingTechniqueComboBox.addItems(farming_techniques)
        self.temperatureTypesComboBox.clear()
        self.temperatureTypesComboBox.addItems(temperature_types)
        self.fuelTypeComboBox.clear()
        self.fuelTypeComboBox.addItems(fuel_types)
        self.fuelUnitOfMeasurementComboBox.addItems(fuel_type_units)
        self.calculationUnitOfMeasurementComboBox.addItems(calculation_units)

    def get_calculation_info(
        self, real_time_temp_data
    ) -> tuple[int, str, str, float, float, str, str, str] | None:
        """
        :param real_time_temp_data: contains real time data from openweathermap API.
        This data is located within the General Tab Model as an attribute.
        :returns: (user_id, fuel_type, fuel_unit, amount_of_fuel_used, temperature_value,
        temperature_type, farming_technique, calculation_unit)
        """
        user_id: int = self.userIDSpinBox.value()
        fuel_type: str = self.fuelTypeComboBox.currentText()
        fuel_unit: str = self.fuelUnitOfMeasurementComboBox.currentText()
        amount_of_fuel_used: float = self.amountOfFuelUsedDoubleSpinBox.value()
        temperature_value: float = self.temperatureDoubleSpinBox.value()
        temperature_type: str = self.temperatureTypesComboBox.currentText()
        farming_technique: str = self.farmingTechniqueComboBox.currentText()
        calculation_unit: str = self.calculationUnitOfMeasurementComboBox.currentText()
        num_of_temp_scales = 3
        # This checks for temp data validity.
        # Yes, I know we should probably
        # move that functionality to the data validator class, but it will happen later.
        if (
            self.realTimeTemperatureCheckBox.isChecked()
            and len(real_time_temp_data) == num_of_temp_scales
        ):
            temperature_value = real_time_temp_data[
                self.temperatureTypesComboBox.currentIndex()
            ]
        return (
            user_id,
            fuel_type,
            fuel_unit,
            amount_of_fuel_used,
            temperature_value,
            temperature_type,
            farming_technique,
            calculation_unit,
        )

    def update_database_table(self) -> None:
        if self.sql_widget_model:
            self.sql_widget_model.select()
            self.sqlTableView.resizeColumnsToContents()

            logger.info(f"Table updated with {self.sql_widget_model.rowCount()} rows")

    def fuel_unit_suffix_update(self, fuel_unit: str) -> None:
        fuel_unit_suffixes: Dict[str, str] = {
            "Liters": "L",
            "Cubic Meters": "m³",
            "Cubic Feet": "ft³",
        }
        suffix: str = fuel_unit_suffixes.get(fuel_unit, "")
        self.amountOfFuelUsedDoubleSpinBox.setSuffix(suffix)
        logger.debug(f"Updated fuel unit suffix to {suffix}")

    def get_import_file_path(self) -> Tuple[Optional[str], Optional[str]]:
        input_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Select file",
            os.path.expanduser("~"),
            "CSV Files (*.csv);;JSON Files (*.json)",
        )

        if not input_path:
            return None, None

        if input_path.lower().endswith(".json") or "json" in selected_filter.lower():
            file_type = "json"
        elif input_path.lower().endswith(".csv") or "csv" in selected_filter.lower():
            file_type = "csv"
        else:
            file_type = None

        return input_path, file_type

    def get_export_file_path(self) -> Tuple[Optional[str], Optional[str]]:
        output_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Select file",
            os.path.expanduser("~"),
            "CSV Files (*.csv);;JSON Files (*.json)",
        )

        if not output_path:
            return None, None

        if output_path.lower().endswith(".json") or "json" in selected_filter.lower():
            file_type = "json"
        elif output_path.lower().endswith(".csv") or "csv" in selected_filter.lower():
            file_type = "csv"
        else:
            file_type = None

        return output_path, file_type

    def apply_user_preferences(self, user_preferences: List):
        (
            preferred_temp_unit,
            preferred_calc_unit,
            use_temperature,
            preferred_user_id,
        ) = user_preferences
        self.temperatureTypesComboBox.setCurrentText(preferred_temp_unit)
        self.calculationUnitOfMeasurementComboBox.setCurrentText(preferred_calc_unit)
        self.userIDSpinBox.setValue(int(preferred_user_id))
        if use_temperature:
            pass
        else:
            self.realTimeTemperatureCheckBox.setChecked(False)
            self.temperatureDoubleSpinBox.setEnabled(True)
            self.temperatureTypesComboBox.setEnabled(True)


class GeneralTabWidget(QWidget):
    def __init__(
        self, application_model: QObject, application_controller: QObject
    ) -> None:
        super().__init__()
        self.application_model = application_model
        self.application_controller = application_controller
        self.model = GeneralTabModel(self.application_model)
        self.view = GeneralTabView()
        self.controller = GeneralTabController(
            self.model, self.view, self.application_controller
        )
