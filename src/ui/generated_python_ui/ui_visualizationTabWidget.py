from pyqtgraph import PlotWidget
from PySide6.QtCore import QCoreApplication, QDate, QMetaObject, QSize, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ui.generated_python_ui import icons_rc  # noqa: F401


class Ui_visualizationTab(object):
    def setupUi(self, visualizationTab):
        if not visualizationTab.objectName():
            visualizationTab.setObjectName("visualizationTab")
        visualizationTab.resize(973, 836)
        self.horizontalLayout = QHBoxLayout(visualizationTab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainBody = QWidget(visualizationTab)
        self.mainBody.setObjectName("mainBody")
        self.horizontalLayout_3 = QHBoxLayout(self.mainBody)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.chartPlotWidget = PlotWidget(self.mainBody)
        self.chartPlotWidget.setObjectName("chartPlotWidget")
        self.chartPlotWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.chartPlotWidget.setFrameShadow(QFrame.Shadow.Plain)

        self.horizontalLayout_3.addWidget(self.chartPlotWidget)

        self.horizontalLayout.addWidget(self.mainBody)

        self.rightBar = QWidget(visualizationTab)
        self.rightBar.setObjectName("rightBar")
        self.rightBar.setMaximumSize(QSize(400, 16777215))
        self.verticalLayout = QVBoxLayout(self.rightBar)
        self.verticalLayout.setObjectName("verticalLayout")
        self.GraphMenuContainerWidget = QWidget(self.rightBar)
        self.GraphMenuContainerWidget.setObjectName("GraphMenuContainerWidget")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.GraphMenuContainerWidget.sizePolicy().hasHeightForWidth()
        )
        self.GraphMenuContainerWidget.setSizePolicy(sizePolicy)
        self.GraphMenuContainerWidget.setMinimumSize(QSize(0, 800))
        self.verticalLayout_3 = QVBoxLayout(self.GraphMenuContainerWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_9 = QWidget(self.GraphMenuContainerWidget)
        self.widget_9.setObjectName("widget_9")
        self.widget_9.setMinimumSize(QSize(0, 0))
        self.verticalLayout_5 = QVBoxLayout(self.widget_9)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget = QWidget(self.widget_9)
        self.widget.setObjectName("widget")
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_6, 0, Qt.AlignmentFlag.AlignTop)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.widget_2.setMinimumSize(QSize(220, 0))
        self.widget_2.setMaximumSize(QSize(99999, 9999))
        self.verticalLayout_7 = QVBoxLayout(self.widget_2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.exportGraphPushButton = QPushButton(self.widget_2)
        self.exportGraphPushButton.setObjectName("exportGraphPushButton")
        self.exportGraphPushButton.setMaximumSize(QSize(261, 31))

        self.verticalLayout_7.addWidget(self.exportGraphPushButton)

        self.verticalLayout_6.addWidget(self.widget_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Smthwithredline = QPushButton(self.widget_3)
        self.Smthwithredline.setObjectName("Smthwithredline")
        self.Smthwithredline.setMinimumSize(QSize(125, 0))
        self.Smthwithredline.setMaximumSize(QSize(111111, 16777215))

        self.horizontalLayout_2.addWidget(self.Smthwithredline)

        self.pushButton_2 = QPushButton(self.widget_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(125, 0))

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.verticalLayout_6.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tabWidget = QTabWidget(self.widget_4)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setMinimumSize(QSize(320, 400))
        self.graphTypeTab = QWidget()
        self.graphTypeTab.setObjectName("graphTypeTab")
        self.tabWidget.addTab(self.graphTypeTab, "")
        self.dataFiltersTab = QWidget()
        self.dataFiltersTab.setObjectName("dataFiltersTab")
        self.verticalLayout_2 = QVBoxLayout(self.dataFiltersTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dataFiltersContainerWidget = QWidget(self.dataFiltersTab)
        self.dataFiltersContainerWidget.setObjectName("dataFiltersContainerWidget")
        self.verticalLayout_4 = QVBoxLayout(self.dataFiltersContainerWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.emissionsUnitContainerWidget = QWidget(self.dataFiltersContainerWidget)
        self.emissionsUnitContainerWidget.setObjectName("emissionsUnitContainerWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.emissionsUnitContainerWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.emissionsUnitLabel = QLabel(self.emissionsUnitContainerWidget)
        self.emissionsUnitLabel.setObjectName("emissionsUnitLabel")

        self.horizontalLayout_4.addWidget(
            self.emissionsUnitLabel, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.emissionsUnitComboBox = QComboBox(self.emissionsUnitContainerWidget)
        self.emissionsUnitComboBox.setObjectName("emissionsUnitComboBox")

        self.horizontalLayout_4.addWidget(self.emissionsUnitComboBox)

        self.verticalLayout_4.addWidget(self.emissionsUnitContainerWidget)

        self.userIDContainerWidget = QWidget(self.dataFiltersContainerWidget)
        self.userIDContainerWidget.setObjectName("userIDContainerWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.userIDContainerWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.userIDContainerLabel = QLabel(self.userIDContainerWidget)
        self.userIDContainerLabel.setObjectName("userIDContainerLabel")

        self.horizontalLayout_5.addWidget(
            self.userIDContainerLabel, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.userIDLineEdit = QLineEdit(self.userIDContainerWidget)
        self.userIDLineEdit.setObjectName("userIDLineEdit")

        self.horizontalLayout_5.addWidget(
            self.userIDLineEdit, 0, Qt.AlignmentFlag.AlignRight
        )

        self.verticalLayout_4.addWidget(self.userIDContainerWidget)

        self.fuelTypeContainerWidget = QWidget(self.dataFiltersContainerWidget)
        self.fuelTypeContainerWidget.setObjectName("fuelTypeContainerWidget")
        self.horizontalLayout_7 = QHBoxLayout(self.fuelTypeContainerWidget)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.fuelTypeContainerLabel = QLabel(self.fuelTypeContainerWidget)
        self.fuelTypeContainerLabel.setObjectName("fuelTypeContainerLabel")

        self.horizontalLayout_7.addWidget(self.fuelTypeContainerLabel)

        self.fuelTypeComboBox = QComboBox(self.fuelTypeContainerWidget)
        self.fuelTypeComboBox.setObjectName("fuelTypeComboBox")

        self.horizontalLayout_7.addWidget(self.fuelTypeComboBox)

        self.verticalLayout_4.addWidget(self.fuelTypeContainerWidget)

        self.timeFrameContainerWidget = QWidget(self.dataFiltersContainerWidget)
        self.timeFrameContainerWidget.setObjectName("timeFrameContainerWidget")
        self.horizontalLayout_10 = QHBoxLayout(self.timeFrameContainerWidget)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.timeFrameLabel = QLabel(self.timeFrameContainerWidget)
        self.timeFrameLabel.setObjectName("timeFrameLabel")
        self.timeFrameLabel.setFrameShape(QFrame.Shape.WinPanel)
        self.timeFrameLabel.setFrameShadow(QFrame.Shadow.Raised)
        self.timeFrameLabel.setTextFormat(Qt.TextFormat.RichText)
        self.timeFrameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.timeFrameLabel)

        self.verticalLayout_4.addWidget(self.timeFrameContainerWidget)

        self.startTimeFrameContainerWidget = QWidget(self.dataFiltersContainerWidget)
        self.startTimeFrameContainerWidget.setObjectName(
            "startTimeFrameContainerWidget"
        )
        self.horizontalLayout_8 = QHBoxLayout(self.startTimeFrameContainerWidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.startTimeFramelLabel = QLabel(self.startTimeFrameContainerWidget)
        self.startTimeFramelLabel.setObjectName("startTimeFramelLabel")
        font = QFont()
        font.setFamilies(["Nirmala UI"])
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QFont.PreferDefault)
        self.startTimeFramelLabel.setFont(font)
        self.startTimeFramelLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.startTimeFramelLabel)

        self.startTimeFrameDataTimeEdit = QDateTimeEdit(
            self.startTimeFrameContainerWidget
        )
        self.startTimeFrameDataTimeEdit.setObjectName("startTimeFrameDataTimeEdit")
        self.startTimeFrameDataTimeEdit.setDate(QDate(2025, 1, 1))
        self.startTimeFrameDataTimeEdit.setTimeSpec(Qt.TimeSpec.LocalTime)

        self.horizontalLayout_8.addWidget(self.startTimeFrameDataTimeEdit)

        self.verticalLayout_4.addWidget(
            self.startTimeFrameContainerWidget,
            0,
            Qt.AlignmentFlag.AlignHCenter,
        )

        self.endTimeFrameContainerWidget = QWidget(self.dataFiltersContainerWidget)
        self.endTimeFrameContainerWidget.setObjectName("endTimeFrameContainerWidget")
        self.horizontalLayout_9 = QHBoxLayout(self.endTimeFrameContainerWidget)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.endTimeFrameLabel = QLabel(self.endTimeFrameContainerWidget)
        self.endTimeFrameLabel.setObjectName("endTimeFrameLabel")
        font1 = QFont()
        font1.setFamilies(["Nirmala UI"])
        font1.setPointSize(14)
        self.endTimeFrameLabel.setFont(font1)
        self.endTimeFrameLabel.setMouseTracking(True)
        self.endTimeFrameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_9.addWidget(self.endTimeFrameLabel)

        self.endTimeFrameDataTimeEdit = QDateTimeEdit(self.endTimeFrameContainerWidget)
        self.endTimeFrameDataTimeEdit.setObjectName("endTimeFrameDataTimeEdit")
        self.endTimeFrameDataTimeEdit.setDate(QDate(2025, 1, 1))

        self.horizontalLayout_9.addWidget(self.endTimeFrameDataTimeEdit)

        self.verticalLayout_4.addWidget(
            self.endTimeFrameContainerWidget, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.verticalLayout_2.addWidget(
            self.dataFiltersContainerWidget, 0, Qt.AlignmentFlag.AlignTop
        )

        self.tabWidget.addTab(self.dataFiltersTab, "")
        self.groupingTab = QWidget()
        self.groupingTab.setObjectName("groupingTab")
        self.tabWidget.addTab(self.groupingTab, "")
        self.appearanceTab = QWidget()
        self.appearanceTab.setObjectName("appearanceTab")
        self.tabWidget.addTab(self.appearanceTab, "")
        self.exportTab = QWidget()
        self.exportTab.setObjectName("exportTab")
        self.tabWidget.addTab(self.exportTab, "")

        self.horizontalLayout_6.addWidget(self.tabWidget)

        self.verticalLayout_6.addWidget(self.widget_4)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.verticalLayout_5.addWidget(self.widget)

        self.verticalLayout_3.addWidget(self.widget_9)

        self.verticalLayout.addWidget(self.GraphMenuContainerWidget)

        self.horizontalLayout.addWidget(self.rightBar)

        self.retranslateUi(visualizationTab)

        self.tabWidget.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(visualizationTab)

    # setupUi

    def retranslateUi(self, visualizationTab):
        visualizationTab.setWindowTitle(
            QCoreApplication.translate("visualizationTab", "Visualization", None)
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "visualizationTab",
                '<html><head/><body><p><span style=" font-size:18pt;">Graph Menu</span></p></body></html>',
                None,
            )
        )
        self.exportGraphPushButton.setText(
            QCoreApplication.translate("visualizationTab", "Export Graph", None)
        )
        self.Smthwithredline.setText(
            QCoreApplication.translate("visualizationTab", "Red Line", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate("visualizationTab", "Filled in box", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.graphTypeTab),
            QCoreApplication.translate("visualizationTab", "Graph Type", None),
        )
        self.emissionsUnitLabel.setText(
            QCoreApplication.translate("visualizationTab", "Emissions Unit", None)
        )
        self.userIDContainerLabel.setText(
            QCoreApplication.translate("visualizationTab", "User ID", None)
        )
        self.fuelTypeContainerLabel.setText(
            QCoreApplication.translate("visualizationTab", "Fuel Type", None)
        )
        self.timeFrameLabel.setText(
            QCoreApplication.translate(
                "visualizationTab",
                '<html><head/><body><p><span style=" font-size:12pt; font-weight:700;">Time Frame</span></p></body></html>',
                None,
            )
        )
        self.startTimeFramelLabel.setText(
            QCoreApplication.translate(
                "visualizationTab",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "hr { height: 1px; border-width: 0; }\n"
                'li.unchecked::marker { content: "\\2610"; }\n'
                'li.checked::marker { content: "\\2612"; }\n'
                "</style></head><body style=\" font-family:'Nirmala UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:14pt;">Start</span></p></body></html>',
                None,
            )
        )
        self.endTimeFrameLabel.setText(
            QCoreApplication.translate("visualizationTab", "End", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.dataFiltersTab),
            QCoreApplication.translate("visualizationTab", "Data Filters", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.groupingTab),
            QCoreApplication.translate("visualizationTab", "Grouping", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.appearanceTab),
            QCoreApplication.translate("visualizationTab", "Appearance", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.exportTab),
            QCoreApplication.translate("visualizationTab", "Export", None),
        )

    # retranslateUi
