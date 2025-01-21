import asyncio
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.emissions_calculator import calculate_emissions
from data.data_validator import DataValidator
from data.database import get_fuel_types
from data.export_manager import ExportManager
from data.import_manager import ImportManager

logger = logging.getLogger("ui")


# this inherits from QWidget and DataValidator (this is to used to validate the data from user)
class InputForms(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        widget_size = (350, 25)

        self.user_id_label = QLabel("User ID:")
        self.user_id_entry = QLineEdit()
        self.user_id_entry.setFixedSize(*widget_size)

        self.fuel_type_label = QLabel("Fuel Type:")
        self.fuel_type_entry = QComboBox()
        self.fuel_type_entry.setFixedSize(*widget_size)

        self.fuel_used_label = QLabel("Fuel Used:")
        self.fuel_used_entry = QLineEdit()
        self.fuel_used_entry.setFixedSize(*widget_size)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(*widget_size)
        self.submit_button.clicked.connect(self.submit)

        self.results = None

        layout = QVBoxLayout()
        layout.addWidget(self.user_id_label)
        layout.addWidget(self.user_id_entry)
        layout.addWidget(self.fuel_type_label)
        layout.addWidget(self.fuel_type_entry)
        layout.addWidget(self.fuel_used_label)
        layout.addWidget(self.fuel_used_entry)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        asyncio.ensure_future(self.populate_fuel_types())

    async def populate_fuel_types(self):
        try:
            logger.info("Populating fuel types")
            fuel_types = await get_fuel_types()
            self.fuel_type_entry.addItems(fuel_types)
            logger.info("Fuel types populated")
        except Exception as e:
            logger.error(f"Error populating fuel types: {e}")
            QMessageBox.critical(
                self, "Error", str(f"{e}: Error populating fuel types")
            )

    def submit(self):
        """
        Submits the user input, validates it, and calculates emissions.
        This method retrieves the user ID, fuel type, and fuel used from the input fields.
        It validates each input using the DataValidator class. If any input is invalid,
        an error message is displayed using QMessageBox. If all inputs are valid, it prints
        the input values, calculates the emissions using EmissionsCalculator, and prints
        the calculated emissions.
        Raises:
            QMessageBox: If any input is invalid, an error message is displayed.
        """
        logger.info("Submit button clicked")
        user_id = self.user_id_entry.text()
        fuel_type = self.fuel_type_entry.currentText()
        fuel_used = self.fuel_used_entry.text()
        data_validator = DataValidator()
        try:
            user_id = int(user_id)
        except ValueError:
            logger.error("Invalid user ID")
            user_id = None
        try:
            fuel_used = float(fuel_used)
        except ValueError:
            logger.error("Invalid fuel used value")
            fuel_used = None
        try:
            # user_id, fuel_type and fuel_used are NOT valid, it will raise a ValueError and QMessageBox will show
            # the error message
            if not data_validator.validate_user_id(
                user_id
            ) or not data_validator.validate_fuel_used(fuel_used):
                error = ValueError("Invalid input")
                QMessageBox.critical(self, "Error", str(error))
                return
            # checking if the user_id, fuel_type and fuel_used are valid
            elif data_validator.validate_user_id(
                user_id
            ) and data_validator.validate_fuel_used(fuel_used):
                logger.info("Valid input: sending data to EmissionsCalculator")
                # Send the validated data to EmissionsCalculator
                from main import user_local_temps

                logger.info(f"User Local Temps: {user_local_temps}")

                if user_local_temps is None:
                    logger.info("Temperature data not available")
                    future = asyncio.ensure_future(
                        calculate_emissions(
                            user_id,
                            fuel_type,
                            fuel_used,
                        )
                    )
                    future.add_done_callback(
                        lambda f: self.display_results(*f.result())
                    )
                elif user_local_temps is not None:
                    logger.info("Temperature data available")
                    temperature_type = self.temperature_type()
                    future = asyncio.ensure_future(
                        calculate_emissions(
                            user_id,
                            fuel_type,
                            fuel_used,
                            user_local_temps[temperature_type],
                            temperature_type,
                        )
                    )
                    future.add_done_callback(
                        lambda f: self.display_results(*f.result())
                    )

        except ValueError as e:
            logger.error(f"Error submitting data: {e}")
            logger.info(f"user_id type: {type(user_id)}, value: {user_id}")
            logger.info(
                f"fuel_type type: {type(fuel_type)}, value: {fuel_type}"
            )
            logger.info(
                f"fuel_used type: {type(fuel_used)}, value: {fuel_used}"
            )
            QMessageBox.critical(self, "Error", str(e))

    def import_export_data(self):
        # Create a custom message box for import/export options
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Import/Export Data")
        msg_box.setText("Would you like to import or export data?")
        import_button = QPushButton("Import Data")
        export_button = QPushButton("Export Data")
        cancel_button = QPushButton("Cancel")
        msg_box.addButton(import_button, QMessageBox.AcceptRole)
        msg_box.addButton(export_button, QMessageBox.AcceptRole)
        msg_box.addButton(cancel_button, QMessageBox.RejectRole)
        msg_box.exec_()

        if msg_box.clickedButton() == import_button:
            # Open file dialog to import data
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Import Data",
                "",
                "CSV Files (*.csv);;JSON Files (*.json);;All Files (*)",
            )
            if file_path:
                import_manager = ImportManager(file_path)
                if file_path.endswith(".csv"):
                    import_manager.import_from_csv()
                elif file_path.endswith(".json"):
                    import_manager.import_from_json()
                else:
                    logger.error("Unsupported file format")
                    QMessageBox.critical(
                        self, "Error", "Unsupported file format"
                    )
        elif msg_box.clickedButton() == export_button:
            # Open file dialog to export data
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Data",
                "",
                "CSV Files (*.csv);;JSON Files (*.json);;All Files (*)",
            )
            if file_path:
                export_manager = ExportManager()
                if file_path.endswith(".csv"):
                    export_manager.export_to_csv(file_path)
                elif file_path.endswith(".json"):
                    export_manager.export_to_json(file_path)
                else:
                    logger.error("Unsupported file format")
                    QMessageBox.critical(
                        self, "Error", "Unsupported file format"
                    )

    def temperature_type(self):
        temperature_dialogue = QMessageBox(self)
        temperature_dialogue.setWindowTitle("Temperature Type")
        temperature_dialogue.setText(
            "Which temperature type would you like to use?"
        )
        celsius_button = QPushButton("Celsius")
        fahrenheit_button = QPushButton("Fahrenheit")
        kelvin_button = QPushButton("Kelvin")
        temperature_dialogue.addButton(celsius_button, QMessageBox.AcceptRole)
        temperature_dialogue.addButton(
            fahrenheit_button, QMessageBox.AcceptRole
        )
        temperature_dialogue.addButton(kelvin_button, QMessageBox.AcceptRole)
        temperature_dialogue.exec_()
        if temperature_dialogue.clickedButton() == celsius_button:
            logger.info("Celsius temperature type selected")
            temperature_type = 0
            return temperature_type
        elif temperature_dialogue.clickedButton() == fahrenheit_button:
            logger.info("Fahrenheit temperature type selected")
            temperature_type = 1
            return temperature_type
        elif temperature_dialogue.clickedButton() == kelvin_button:
            logger.info("Kelvin temperature type selected")
            temperature_type = 2
            return temperature_type

    def display_results(self, fuel_type, fuel_used, emissions):
        logger.info("Future callback: displaying results")
        results = QMessageBox(self)
        results.setWindowTitle("Results")
        results.setTextFormat(Qt.TextFormat.RichText)
        results.setText(
            f"<b>Fuel Type:</b> {fuel_type} <b>Fuel Used:</b> {fuel_used} <b>Emissions:</b> {emissions}"
        )
        ok_button = QPushButton("Ok")
        results.addButton(ok_button, QMessageBox.AcceptRole)
        logger.info("Emissions calculation results displayed")
        results.exec_()
        selected_button = results.clickedButton()
        if selected_button is ok_button:
            logger.info("Ok button clicked")
            self.import_export_data()
