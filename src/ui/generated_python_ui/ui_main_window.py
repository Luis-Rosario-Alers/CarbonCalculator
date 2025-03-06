# -*- coding: utf-8 -*-
# flake8: noqa
################################################################################
## Form generated from reading UI file 'main_windowSHdQrd.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QStackedWidget,
    QStatusBar,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1222, 755)
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
        self.menubar.setGeometry(QRect(0, 0, 1222, 30))
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
            QCoreApplication.translate("MainWindow", "MainWindow", None)
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
        self.menuHelp.setTitle(
            QCoreApplication.translate("MainWindow", "Help", None)
        )
        self.menuFeedback.setTitle(
            QCoreApplication.translate("MainWindow", "Feedback", None)
        )

    # retranslateUi
