from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

from src.data.database import application_path


class HelpWidget(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        ui_file_path = (
            f"{application_path}/resources/assets/ui_files/help_widget.ui"
        )
        self.ui = loader.load(ui_file_path, self)
        self.ui.show()
