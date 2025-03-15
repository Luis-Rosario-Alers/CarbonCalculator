from pyqtgraph import PlotWidget
from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_visualizationTab(object):
    def setupUi(self, visualizationTab):
        if not visualizationTab.objectName():
            visualizationTab.setObjectName("visualizationTab")
        visualizationTab.resize(1123, 836)
        self.horizontalLayout = QHBoxLayout(visualizationTab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainBody = QWidget(visualizationTab)
        self.mainBody.setObjectName("mainBody")
        self.horizontalLayout_3 = QHBoxLayout(self.mainBody)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.chartPlotWidget = PlotWidget(self.mainBody)
        self.chartPlotWidget.setObjectName("chartPlotWidget")

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
        sizePolicy1.setHeightForWidth(
            self.label_6.sizePolicy().hasHeightForWidth()
        )
        self.label_6.setSizePolicy(sizePolicy1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(
            self.label_6, 0, Qt.AlignmentFlag.AlignTop
        )

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

        self.verticalLayout_6.addWidget(
            self.widget_2, 0, Qt.AlignmentFlag.AlignHCenter
        )

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

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(visualizationTab)

    # setupUi

    def retranslateUi(self, visualizationTab):
        visualizationTab.setWindowTitle(
            QCoreApplication.translate(
                "visualizationTab", "Visualization", None
            )
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "visualizationTab",
                '<html><head/><body><p><span style=" font-size:18pt;">Graph Menu</span></p></body></html>',
                None,
            )
        )
        self.exportGraphPushButton.setText(
            QCoreApplication.translate(
                "visualizationTab", "Export Graph", None
            )
        )
        self.Smthwithredline.setText(
            QCoreApplication.translate("visualizationTab", "Red Line", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate(
                "visualizationTab", "Filled in box", None
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.graphTypeTab),
            QCoreApplication.translate("visualizationTab", "Graph Type", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.dataFiltersTab),
            QCoreApplication.translate(
                "visualizationTab", "Data Filters", None
            ),
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
