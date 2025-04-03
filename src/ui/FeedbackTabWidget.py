from PySide6.QtWidgets import QWidget

from ui.generated_python_ui.ui_feedbackTabWidget import Ui_feedbackTabWidget


class FeedbackTabController:
    def __init__(self, model, view, application_controller):
        self.model = model
        self.view = view
        self.application_controller = application_controller
        self.__connect_signals()

    def __connect_signals(self):
        pass


class FeedbackTabModel:
    def __init__(self, application_model) -> None:
        self.model = application_model


class FeedbackTabView(QWidget, Ui_feedbackTabWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class FeedbackTabWidget(QWidget):
    def __init__(self, application_model, application_controller) -> None:
        super().__init__()
        self.application_controller = application_controller
        self.application_model = application_model
        self.model = FeedbackTabModel(application_model)
        self.view = FeedbackTabView()
        self.controller = FeedbackTabController(
            self.model, self.view, self.application_controller
        )
