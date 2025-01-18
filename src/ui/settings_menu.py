import PySide6.QtCore
import PySide6.QtGui
import logging
import sys

from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel
from utils.logging import setup_logging
from data.database import application_path


setup_logging()
logger = logging.getLogger("ui")


# SettingsMenu class
# This class is responsible for creating the settings menu
# It will be used to change the settings of the application



class SettingPage(QTabWidget):
    def __init__(self, parent=None):
        self.tab_widget = QTabWidget()
        super().__init__(parent)
    
    
    def addTabs(self, title: str):
        title = QWidget()
        count = self.count()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Content of Tab {count}"))
        title.setLayout(layout)
        TabBar.addTab(count, title)

