import logging
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from data.database import application_path
from ui.input_forms import InputForms

logger = logging.getLogger("ui")


class MainWindow(QMainWindow):
    def __init__(self, internet_connection_status, parent=None):
        self.internet_connection_status = internet_connection_status
        super().__init__(parent)

        self.setWindowTitle("Carbon Calculator")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon(f"{application_path}/resources/assets/icon.png"))
        # TODO: find a way to change the icon on the taskbar

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.input_forms = InputForms(self)
        layout.addWidget(self.input_forms)

        self.display_internet_connection_status(self.internet_connection_status)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            logging.getLogger("main").info("Exiting application")
            event.accept()
        else:
            event.ignore()

    def display_internet_connection_status(self, has_internet):
        """Display a message box with the internet connection status."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Status")
        ok_button = QPushButton("Ok.")
        msg_box.addButton(ok_button, QMessageBox.AcceptRole)

        if has_internet:
            msg_box.setText("Internet connection found.")
        elif has_internet is False:
            msg_box.setText(
                "No internet connection found. Some features may not be available."
            )
        else:
            msg_box.setText("There was an error checking the internet connection.")

        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
