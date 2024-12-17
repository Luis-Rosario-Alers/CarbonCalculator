import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from ui.input_forms import InputForms


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Agricultural Carbon Calculator")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon("resources/assets/icon.png"))
        # TODO: find a way to change the icon on the taskbar

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.input_forms = InputForms(self)
        layout.addWidget(self.input_forms)

    def run(self):
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
