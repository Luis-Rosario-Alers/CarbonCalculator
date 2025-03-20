import logging
import os
from typing import Dict, List, Optional, Tuple

from PySide6.QtCore import QObject, Signal
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import QFileDialog, QTableView, QWidget

from data.database import databases_folder
from data.export_manager import ExportManager
from data.import_manager import ImportManager
from src.ui.generated_python_ui.ui_generalTabWidget import Ui_GeneralWidget
from src.ui.SettingsWidget import settingsWidget
from src.utils.gui_utilities import connect_threaded

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
        self.settingsWidget: settingsWidget = settingsWidget(
            self.application_controller, self.model, self, self.view
        )
        self.__connect_signals()

    def __connect_signals(self) -> None:
        logger.debug("Connecting signals in GeneralTabController")
        self.model.databases_model.databases_initialized.connect(
            self.handle_initialization_of_database_widget
        )
        self.model.databases_model.calculation_logged.connect(
            self.handle_database_widget_update
        )
        self.view.fuelUnitOfMeasurementComboBox.currentTextChanged.connect(
            self.handle_fuel_unit_changed
        )
        self.view.calculateContainerCheckBox.toggled.connect(
            self.handle_real_time_temperatures_check_box_changed
        )
        self.view.importPushButton.clicked.connect(
            self.handle_import_button_clicked
        )
        self.view.exportPushButton.clicked.connect(
            self.handle_export_button_clicked
        )
        self.view.settingsPushButton.clicked.connect(
            self.handle_settings_button_clicked
        )
        self.view.calculateContainerPushButton.clicked.connect(
            self.handle_calculate_button_clicked
        )

        connect_threaded(
            self.application_controller,
            "initialization",
            self.handle_real_time_temperatures_api_call,
        )
        connect_threaded(
            self.model.databases_model,
            "databases_initialized",
            self.handle_comboboxes_initialization,
        )
        connect_threaded(
            self.application_controller,
            "application_closed",
            self.handle_application_close,
        )

    def handle_real_time_temperatures_api_call(self) -> None:
        logger.debug("GeneralTabWidget: calling real-time temperature API")
        raise NotImplementedError("Real-time temperature API not implemented")
        # something like this?
        # user_location_service = UserLocationService()
        # user_location_service.get_user_location()

    def handle_import_button_clicked(self) -> None:
        logger.debug("GeneralTabWidget: import button clicked")
        input_path, file_type = self.view.get_import_file_path()
        if file_type:
            logger.debug(f"GeneralTabWidget: importing {file_type} file")
            if file_type == "json":
                import_manager = ImportManager(input_path)
                import_manager.import_from_json()
                self.view.update_database_table()
            elif file_type == "csv":
                import_manager = ImportManager(input_path)
                import_manager.import_from_csv()
                self.view.update_database_table()
            else:
                logger.error("GeneralTabWidget: Unsupported file type")

    def handle_export_button_clicked(self) -> None:
        logger.debug("GeneralTabWidget: export button clicked")
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
        combobox_data = {
            "fuel_types": self.model.databases_model.get_fuel_types(),
            "farming_techniques": self.model.databases_model.get_farming_techniques(),
            "fuel_type_units": ["Liters", "Cubic Meters", "Cubic Feet"],
            "calculation_units": [
                "Milligrams",
                "Grams",
                "Kilograms",
                "Metric Tons",
            ],
            "temperature_types": ["Celsius", "Fahrenheit", "Kelvin"],
        }
        self.combobox_information.emit(combobox_data)
        logger.debug("General Tab Controller: Emitted combobox_information.")
        self.view.initialize_combobox_values(
            combobox_data["fuel_types"],
            combobox_data["farming_techniques"],
            combobox_data["fuel_type_units"],
            combobox_data["temperature_types"],
            combobox_data["calculation_units"],
        )

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
        ) = self.view.get_calculation_info()
        self.model.calculation_model.calculate_emissions(
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

    def handle_real_time_temperatures_check_box_changed(
        self, checked: bool
    ) -> None:
        logger.debug(
            f"GeneralTabWidget: Real-Time temperature check box changed to {checked}"
        )
        if not checked:
            logger.debug("GeneralTabWidget: enabling temperature controls")
            self.view.temperatureDoubleSpinBox.setEnabled(True)
            self.view.temperatureTypesComboBox.setEnabled(True)
        else:
            logger.debug("GeneralTabWidget: disabling temperature controls")
            self.view.temperatureDoubleSpinBox.setEnabled(False)
            self.view.temperatureTypesComboBox.setEnabled(False)

    def handle_settings_button_clicked(self) -> None:
        logger.debug("GeneralTabWidget: settings button clicked")
        self.settingsWidget.view.show()


class GeneralTabModel:
    def __init__(self, application_model) -> None:
        self.application_model = application_model
        self.databases_model = self.application_model.databases_model
        self.calculation_model = self.application_model.calculation_model

    def load_database_table_content(self) -> None:
        pass


class GeneralTabView(QWidget, Ui_GeneralWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.database_loaded: bool = False
        self.db_connection = None
        self.sql_widget_model = None

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
        self,
    ) -> tuple[int, str, str, float, float, str, str, str] | None:
        fuel_type: str = self.fuelTypeComboBox.currentText()
        fuel_unit: str = self.fuelUnitOfMeasurementComboBox.currentText()
        amount_of_fuel_used: float = self.amountOfFuelUsedDoubleSpinBox.value()
        temperature_value: float = self.temperatureDoubleSpinBox.value()
        temperature_type: str = self.temperatureTypesComboBox.currentText()
        farming_technique: str = self.farmingTechniqueComboBox.currentText()
        calculation_unit: str = (
            self.calculationUnitOfMeasurementComboBox.currentText()
        )
        if self.calculateContainerCheckBox.isChecked():
            pass
            # TODO: implement real-time temperature collection for this
        else:
            return (
                1,
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

            logger.info(
                f"Table updated with {self.sql_widget_model.rowCount()} rows"
            )

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

        if (
            input_path.lower().endswith(".json")
            or "json" in selected_filter.lower()
        ):
            file_type = "json"
        elif (
            input_path.lower().endswith(".csv")
            or "csv" in selected_filter.lower()
        ):
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

        if (
            output_path.lower().endswith(".json")
            or "json" in selected_filter.lower()
        ):
            file_type = "json"
        elif (
            output_path.lower().endswith(".csv")
            or "csv" in selected_filter.lower()
        ):
            file_type = "csv"
        else:
            file_type = None

        return output_path, file_type


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
