import logging

from PySide6.QtWidgets import QWidget

from ui.generated_python_ui.ui_helpTabWidget import Ui_helpTabWidget

logger = logging.getLogger("ui")


class HelpTabController:
    def __init__(self, model, view, application_controller):
        self.model = model
        self.view = view
        self.application_controller = application_controller


class HelpTabModel:
    def __init__(self, application_model):
        self.model = application_model


class HelpTabView(QWidget, Ui_helpTabWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class HelpTabWidget(QWidget):
    def __init__(self, application_model, application_controller) -> None:
        super().__init__()
        self.application_controller = application_controller
        self.application_model = application_model
        self.model = HelpTabModel(application_model)
        self.view = HelpTabView()
        self.controller = HelpTabController(
            self.model, self.view, self.application_controller
        )
