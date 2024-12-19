import asyncio

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.emissions_calculator import EmissionsCalculator
from data.data_validator import DataValidator
from data.database import get_fuel_types
from data.export_manager import ExportManager
from data.import_manager import ImportManager


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

        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(self.fetch_fuel_data())
        self.loop.close()

        # Use QTimer to periodically check for the completion of the coroutine
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_fuel_types_loaded)
        self.timer.start(100)  # Check every 100 ms

    async def fetch_fuel_data(self):
        print("fetching")
        try:
            self.fuel_types = await get_fuel_types()
            print(f"Fetched fuel types: {self.fuel_types}")
        except Exception as e:
            print(f"Error fetching fuel types: {e}")
            self.fuel_types = []

    def check_fuel_types_loaded(self):
        if hasattr(self, "fuel_types"):
            print("found attr")
            self.fuel_type_entry.addItems(self.fuel_types)
            self.timer.stop()

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
        user_id = self.user_id_entry.text()
        fuel_type = self.fuel_type_entry.currentText()
        fuel_used = self.fuel_used_entry.text()
        user_id = int(user_id) if user_id else None
        fuel_used = float(fuel_used) if fuel_used else None
        data_validator = DataValidator()
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
                # Send the validated data to EmissionsCalculator
                emissions_calculator = EmissionsCalculator()
                emissions = emissions_calculator.calculate_emissions(
                    user_id, fuel_type, fuel_used
                )
                self.results = f"User ID: {user_id}, Fuel Type: {fuel_type}, Fuel Used: {fuel_used}, Emissions: {emissions[3]}"
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
                print(f"Importing data from: {file_path}")
                import_manager = ImportManager(file_path)
                if file_path.endswith(".csv"):
                    import_manager.import_from_csv()
                elif file_path.endswith(".json"):
                    import_manager.import_from_json()
                else:
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
                print(f"Exporting data to: {file_path}")
                export_manager = ExportManager("databases/emissions.db")
                if file_path.endswith(".csv"):
                    export_manager.export_to_csv(file_path)
                elif file_path.endswith(".json"):
                    export_manager.export_to_json(file_path)
                else:
                    QMessageBox.critical(self, "Error", "Unsupported file format")
