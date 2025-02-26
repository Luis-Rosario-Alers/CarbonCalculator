import logging
import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from data.database import application_path
from ui.input_forms import InputForms
from ui.settings_menu import SettingPage

logger = logging.getLogger("ui")


class MainWindow(QMainWindow):
    def __init__(self, internet_connection_status, parent=None):
        self.internet_connection_status = internet_connection_status
        super().__init__(parent)

        self.setWindowTitle("Carbon Calculator")
        self.setGeometry(100, 100, 400, 300)
        self.setMaximumSize(400, 300)
        if sys.platform == "darwin":
            self.setWindowIcon(
                QIcon(f"{application_path}/resources/assets/icon.icns")
            )
        elif sys.platform == "win32":
            self.setWindowIcon(
                QIcon(f"{application_path}/resources/assets/icon.ico")
            )
        else:
            self.setWindowIcon(
                QIcon(f"{application_path}/resources/assets/icon.png")
            )

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        loader = QUiLoader()
        ui_file_path = os.path.normpath(
            f"{application_path}/resources/assets/ui_files/help_widget.ui"
        )
        print(ui_file_path)
        self.help_widget = loader.load(ui_file_path, self)
        if self.help_widget is None:
            logger.error("Failed to load help widget UI file.")
            raise RuntimeError("Failed to load help widget UI file.")
        self.tab_widget = QTabWidget()

        self.tab_widget.addTab(InputForms(self), "General")
        self.tab_widget.addTab(SettingPage(self), "Settings")
        self.tab_widget.addTab(self.help_widget, "Help")

        layout.addWidget(self.tab_widget)

        self.display_internet_connection_status(
            self.internet_connection_status
        )

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            logging.getLogger("main").info("Exiting application")
            event.accept()
        else:
            event.ignore()

    def display_internet_connection_status(self, has_internet):
        """Display a message box with the internet connection status."""
        self.status_msg_box = QMessageBox(self)
        self.status_msg_box.setWindowTitle("Status")
        self.ok_button = QPushButton("Ok.")
        self.status_msg_box.addButton(self.ok_button, QMessageBox.AcceptRole)

        if has_internet:
            self.status_msg_box.setText("Internet connection found.")
        elif has_internet is False:
            self.status_msg_box.setText(
                "No internet connection found. Some features may not be available."
            )
        else:
            self.status_msg_box.setText(
                "There was an error checking the internet connection."
            )

        self.status_msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
