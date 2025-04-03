from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMenu,
    QMenuBar,
    QStackedWidget,
    QStatusBar,
    QTabWidget,
    QWidget,
)

from ui.generated_python_ui import icons_rc  # noqa: F401


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(737, 507)
        MainWindow.setStyleSheet("")
        MainWindow.setIconSize(QSize(24, 24))
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setAutoFillBackground(False)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 737, 33))
        self.menuGeneral = QMenu(self.menubar)
        self.menuGeneral.setObjectName("menuGeneral")
        self.menuVisualization = QMenu(self.menubar)
        self.menuVisualization.setObjectName("menuVisualization")
        self.menuAI_chat = QMenu(self.menubar)
        self.menuAI_chat.setObjectName("menuAI_chat")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFeedback = QMenu(self.menubar)
        self.menuFeedback.setObjectName("menuFeedback")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuGeneral.menuAction())
        self.menubar.addAction(self.menuVisualization.menuAction())
        self.menubar.addAction(self.menuAI_chat.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuFeedback.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Carbon Calculator", None)
        )
        self.menuGeneral.setTitle(
            QCoreApplication.translate("MainWindow", "General", None)
        )
        self.menuVisualization.setTitle(
            QCoreApplication.translate("MainWindow", "Visualization", None)
        )
        self.menuAI_chat.setTitle(
            QCoreApplication.translate("MainWindow", "AI chat", None)
        )
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.menuFeedback.setTitle(
            QCoreApplication.translate("MainWindow", "Feedback", None)
        )

    # retranslateUi
