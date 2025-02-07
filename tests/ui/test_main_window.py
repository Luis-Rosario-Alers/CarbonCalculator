import sys
import pytest
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QWidget

from src.ui.main_window import MainWindow


class TestMainWindow:
    @pytest.fixture
    def window(self, qtbot):
        window = MainWindow(internet_connection_status=True)
        qtbot.addWidget(window)
        return window

    def test_main_window_initialization(self, window):
        assert window.isEnabled()

    def test_main_window_geometry(self, window):
        assert window.geometry() == QRect(100, 100, 400, 300)

    def test_main_window_window_title(self, window):
        assert window.windowTitle() == "Carbon Calculator"

    def test_main_window_maximum_size(self, window):
        assert window.maximumSize() == QSize(400, 300)

    def test_main_window_tab_widget(self, window):
        assert window.tab_widget.count() == 2
        assert window.tab_widget.tabText(0) == "General"
        assert window.tab_widget.tabText(1) == "Settings"

    def test_main_window_internet_connection_status(self, window):
        # Assert
        assert window.windowTitle() == "Carbon Calculator"
        assert window.status_msg_box.text() == "Internet connection found."