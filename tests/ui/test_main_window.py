import sys

import pytest
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton

from src.ui.main_window import MainWindow


class TestMainWindow:
    @pytest.fixture(scope="function")
    def app(self, monkeypatch):
        # Set up headless mode
        monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
        app = QApplication
        if app is None:
            app = QApplication(sys.argv)
        return app

    @pytest.fixture
    def window(self, app, qtbot):
        window = MainWindow(internet_connection_status=True)
        qtbot.addWidget(window)
        # Wait for window to be ready
        qtbot.waitExposed(window)
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

    def test_main_window_has_right_widgets(self, qtbot, window):
        # Wait for the internet connection message box
        msg_box = None

        def check_msg_box():
            nonlocal msg_box
            msg_box = window.findChild(QMessageBox)
            return msg_box is not None

        qtbot.waitUntil(check_msg_box)
        assert msg_box is not None
        ok_button = msg_box.findChild(QPushButton, "Ok.")
        qtbot.mouseClick(ok_button, Qt.LeftButton)

        # Wait for and handle the exit window
        exit_msg_box = None

        def check_exit_msg_box():
            nonlocal exit_msg_box
            exit_msg_box = window.findChild(QMessageBox)
            return exit_msg_box is not None

        qtbot.waitUntil(check_exit_msg_box)
        assert exit_msg_box is not None
        yes_button = exit_msg_box.findChild(QPushButton, "Yes")
        qtbot.mouseClick(yes_button, Qt.LeftButton)

        # Verify tab widgets
        assert window.tab_widget.widget(0) is not None
        assert window.tab_widget.widget(1) is not None

    def test_internet_connection_message(self, app, qtbot):
        window = MainWindow(internet_connection_status=True)
        qtbot.addWidget(window)
        qtbot.waitForWindowShown(window)

        try:
            # Wait for message box to appear
            msg_box = qtbot.waitUntil(lambda: window.findChild(QMessageBox))
            assert msg_box is not None
            assert msg_box.windowTitle() == "Status"

            # Close message box
            qtbot.mouseClick(
                msg_box.findChild(QPushButton, "Ok."), Qt.LeftButton
            )

        finally:
            window.close()
            qtbot.wait(100)  # Give time for cleanup
            app.processEvents()
