import asyncio
import logging

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
from qasync import QEventLoop

from core.emissions_calculator import EmissionsCalculator
from data.data_validator import DataValidator
from data.database import get_fuel_types
from data.export_manager import ExportManager
from data.import_manager import ImportManager

logger = logging.getLogger("ui")


# this inherits from QWidget and DataValidator (this is to used to validate the data from user)
class InputForms(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_id_label = QLabel("User ID:")
        self.user_id_entry = QLineEdit()

        self.fuel_type_label = QLabel("Fuel Type:")
        self.fuel_type_entry = QComboBox()

        self.fuel_used_label = QLabel("Fuel Used:")
        self.fuel_used_entry = QLineEdit()

        self.submit_button = QPushButton("Submit")
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

        loop = QEventLoop()
        asyncio.set_event_loop(loop)
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
            # user_id, fuel_type and fuel_used are NOT valid, it will raise a ValueError and QMessageBox will show the error message
            if (
                not data_validator.validate_user_id(user_id)
                or not data_validator.validate_fuel_type(fuel_type)
                or not data_validator.validate_fuel_used(fuel_used)
            ):
                error = ValueError("Invalid input")
                QMessageBox.critical(self, "Error", str(error))
                return
            # checking if the user_id, fuel_type and fuel_used are valid
            if (
                data_validator.validate_user_id(user_id)
                and data_validator.validate_fuel_type(fuel_type)
                and data_validator.validate_fuel_used(fuel_used)
            ):
                logger.info("Valid input: sending data to EmissionsCalculator")
                # Send the validated data to EmissionsCalculator
                emissions_calculator = EmissionsCalculator()
                emissions = emissions_calculator.calculate_emissions(
                    user_id, fuel_type, fuel_used
                )
                self.results = f"User ID: {user_id}, Fuel Type: {fuel_type}, Fuel Used: {fuel_used}, Emissions: {emissions}"
                QMessageBox.information(self, "Info", self.results)
                self.import_export_data()
        except ValueError as e:
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
                    QMessageBox.critical(self, "Error", "Unsupported file format")
        elif msg_box.clickedButton() == export_button:
            # Open file dialog to export data
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Data",
                "",
                "CSV Files (*.csv);;JSON Files (*.json);;All Files (*)",
            )
            if file_path:
                export_manager = ExportManager("databases/emissions.db")
                if file_path.endswith(".csv"):
                    export_manager.export_to_csv(file_path)
                elif file_path.endswith(".json"):
                    export_manager.export_to_json(file_path)
                else:
                    logger.error("Unsupported file format")
                    QMessageBox.critical(self, "Error", "Unsupported file format")
