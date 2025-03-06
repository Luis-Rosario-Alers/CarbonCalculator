# -*- coding: utf-8 -*-
# flake8: noqa
################################################################################
## Form generated from reading UI file 'generalTabWidgetGedHjW.ui'
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
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class Ui_GeneralWidget(object):
    def setupUi(self, GeneralWidget):
        if not GeneralWidget.objectName():
            GeneralWidget.setObjectName("GeneralWidget")
        GeneralWidget.resize(877, 759)
        self.horizontalLayout = QHBoxLayout(GeneralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftBar = QWidget(GeneralWidget)
        self.leftBar.setObjectName("leftBar")
        self.leftBar.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.leftBar)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.farmingVariablesWidget = QWidget(self.leftBar)
        self.farmingVariablesWidget.setObjectName("farmingVariablesWidget")
        self.verticalLayout_3 = QVBoxLayout(self.farmingVariablesWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.farmingVariablesLabel = QLabel(self.farmingVariablesWidget)
        self.farmingVariablesLabel.setObjectName("farmingVariablesLabel")
        font = QFont()
        font.setPointSize(10)
        self.farmingVariablesLabel.setFont(font)
        self.farmingVariablesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.farmingVariablesLabel)

        self.farmingTechniqueWidget = QWidget(self.farmingVariablesWidget)
        self.farmingTechniqueWidget.setObjectName("farmingTechniqueWidget")
        self.horizontalLayout_8 = QHBoxLayout(self.farmingTechniqueWidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.farmingTechniqueLabel = QLabel(self.farmingTechniqueWidget)
        self.farmingTechniqueLabel.setObjectName("farmingTechniqueLabel")

        self.horizontalLayout_8.addWidget(self.farmingTechniqueLabel)

        self.farmingTechniqueComboBox = QComboBox(self.farmingTechniqueWidget)
        self.farmingTechniqueComboBox.setObjectName("farmingTechniqueComboBox")

        self.horizontalLayout_8.addWidget(self.farmingTechniqueComboBox)

        self.verticalLayout_3.addWidget(
            self.farmingTechniqueWidget, 0, Qt.AlignmentFlag.AlignRight
        )

        self.unitOfMeasurementWidget = QWidget(self.farmingVariablesWidget)
        self.unitOfMeasurementWidget.setObjectName("unitOfMeasurementWidget")
        self.horizontalLayout_7 = QHBoxLayout(self.unitOfMeasurementWidget)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.unitOfMeasurementLabel = QLabel(self.unitOfMeasurementWidget)
        self.unitOfMeasurementLabel.setObjectName("unitOfMeasurementLabel")

        self.horizontalLayout_7.addWidget(self.unitOfMeasurementLabel)

        self.unitOfMeasurementComboBox = QComboBox(
            self.unitOfMeasurementWidget
        )
        self.unitOfMeasurementComboBox.setObjectName(
            "unitOfMeasurementComboBox"
        )

        self.horizontalLayout_7.addWidget(self.unitOfMeasurementComboBox)

        self.verticalLayout_3.addWidget(
            self.unitOfMeasurementWidget, 0, Qt.AlignmentFlag.AlignRight
        )

        self.fuelTypeWidget = QWidget(self.farmingVariablesWidget)
        self.fuelTypeWidget.setObjectName("fuelTypeWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.fuelTypeWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.fuelTypeLabel = QLabel(self.fuelTypeWidget)
        self.fuelTypeLabel.setObjectName("fuelTypeLabel")

        self.horizontalLayout_5.addWidget(
            self.fuelTypeLabel, 0, Qt.AlignmentFlag.AlignRight
        )

        self.fuelTypeComboBox = QComboBox(self.fuelTypeWidget)
        self.fuelTypeComboBox.setObjectName("fuelTypeComboBox")

        self.horizontalLayout_5.addWidget(
            self.fuelTypeComboBox, 0, Qt.AlignmentFlag.AlignRight
        )

        self.verticalLayout_3.addWidget(
            self.fuelTypeWidget, 0, Qt.AlignmentFlag.AlignRight
        )

        self.amountOfFuelUsedWidget = QWidget(self.farmingVariablesWidget)
        self.amountOfFuelUsedWidget.setObjectName("amountOfFuelUsedWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.amountOfFuelUsedWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.amountOfFuelUsedLabel = QLabel(self.amountOfFuelUsedWidget)
        self.amountOfFuelUsedLabel.setObjectName("amountOfFuelUsedLabel")

        self.horizontalLayout_4.addWidget(
            self.amountOfFuelUsedLabel, 0, Qt.AlignmentFlag.AlignRight
        )

        self.amountOfFuelUsedDoubleSpinBox = QDoubleSpinBox(
            self.amountOfFuelUsedWidget
        )
        self.amountOfFuelUsedDoubleSpinBox.setObjectName(
            "amountOfFuelUsedDoubleSpinBox"
        )

        self.horizontalLayout_4.addWidget(
            self.amountOfFuelUsedDoubleSpinBox, 0, Qt.AlignmentFlag.AlignRight
        )

        self.verticalLayout_3.addWidget(
            self.amountOfFuelUsedWidget, 0, Qt.AlignmentFlag.AlignRight
        )

        self.verticalLayout_2.addWidget(self.farmingVariablesWidget)

        self.calculateContainerWidget = QWidget(self.leftBar)
        self.calculateContainerWidget.setObjectName("calculateContainerWidget")
        self.horizontalLayout_6 = QHBoxLayout(self.calculateContainerWidget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.calculateContainerCheckBox = QCheckBox(
            self.calculateContainerWidget
        )
        self.calculateContainerCheckBox.setObjectName(
            "calculateContainerCheckBox"
        )

        self.horizontalLayout_6.addWidget(self.calculateContainerCheckBox)

        self.calculateContainerPushButton = QPushButton(
            self.calculateContainerWidget
        )
        self.calculateContainerPushButton.setObjectName(
            "calculateContainerPushButton"
        )

        self.horizontalLayout_6.addWidget(self.calculateContainerPushButton)

        self.verticalLayout_2.addWidget(
            self.calculateContainerWidget, 0, Qt.AlignmentFlag.AlignTop
        )

        self.moreContainerWidget = QWidget(self.leftBar)
        self.moreContainerWidget.setObjectName("moreContainerWidget")
        self.verticalLayout_5 = QVBoxLayout(self.moreContainerWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.moreWidget = QWidget(self.moreContainerWidget)
        self.moreWidget.setObjectName("moreWidget")
        self.verticalLayout_4 = QVBoxLayout(self.moreWidget)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.editDatabasePushButton = QPushButton(self.moreWidget)
        self.editDatabasePushButton.setObjectName("editDatabasePushButton")

        self.verticalLayout_4.addWidget(self.editDatabasePushButton)

        self.importPushButton = QPushButton(self.moreWidget)
        self.importPushButton.setObjectName("importPushButton")

        self.verticalLayout_4.addWidget(self.importPushButton)

        self.exportPushButton = QPushButton(self.moreWidget)
        self.exportPushButton.setObjectName("exportPushButton")

        self.verticalLayout_4.addWidget(self.exportPushButton)

        self.settingsPushButton = QPushButton(self.moreWidget)
        self.settingsPushButton.setObjectName("settingsPushButton")

        self.verticalLayout_4.addWidget(self.settingsPushButton)

        self.verticalLayout_5.addWidget(
            self.moreWidget,
            0,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom,
        )

        self.verticalLayout_2.addWidget(
            self.moreContainerWidget, 0, Qt.AlignmentFlag.AlignBottom
        )

        self.horizontalLayout.addWidget(self.leftBar)

        self.mainBody = QWidget(GeneralWidget)
        self.mainBody.setObjectName("mainBody")
        font1 = QFont()
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.mainBody.setFont(font1)
        self.verticalLayout_6 = QVBoxLayout(self.mainBody)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.mainBodyPlaceholderLabel = QLabel(self.mainBody)
        self.mainBodyPlaceholderLabel.setObjectName("mainBodyPlaceholderLabel")
        font2 = QFont()
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        font2.setKerning(False)
        self.mainBodyPlaceholderLabel.setFont(font2)
        self.mainBodyPlaceholderLabel.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.verticalLayout_6.addWidget(self.mainBodyPlaceholderLabel)

        self.madeByCreditsLabel = QLabel(self.mainBody)
        self.madeByCreditsLabel.setObjectName("madeByCreditsLabel")
        font3 = QFont()
        font3.setBold(True)
        font3.setItalic(True)
        font3.setUnderline(False)
        font3.setStrikeOut(False)
        self.madeByCreditsLabel.setFont(font3)
        self.madeByCreditsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(
            self.madeByCreditsLabel, 0, Qt.AlignmentFlag.AlignBottom
        )

        self.horizontalLayout.addWidget(self.mainBody)

        self.rightBar = QWidget(GeneralWidget)
        self.rightBar.setObjectName("rightBar")
        self.verticalLayout = QVBoxLayout(self.rightBar)
        self.verticalLayout.setObjectName("verticalLayout")
        self.recentTransactionsHeaderWidget = QWidget(self.rightBar)
        self.recentTransactionsHeaderWidget.setObjectName(
            "recentTransactionsHeaderWidget"
        )
        self.horizontalLayout_3 = QHBoxLayout(
            self.recentTransactionsHeaderWidget
        )
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.recentTransactionsHeaderLabel = QLabel(
            self.recentTransactionsHeaderWidget
        )
        self.recentTransactionsHeaderLabel.setObjectName(
            "recentTransactionsHeaderLabel"
        )
        font4 = QFont()
        font4.setPointSize(15)
        self.recentTransactionsHeaderLabel.setFont(font4)
        self.recentTransactionsHeaderLabel.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter
        )

        self.horizontalLayout_3.addWidget(
            self.recentTransactionsHeaderLabel, 0, Qt.AlignmentFlag.AlignTop
        )

        self.verticalLayout.addWidget(
            self.recentTransactionsHeaderWidget, 0, Qt.AlignmentFlag.AlignTop
        )

        self.sqlTableView = QTableView(self.rightBar)
        self.sqlTableView.setObjectName("sqlTableView")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.sqlTableView.sizePolicy().hasHeightForWidth()
        )
        self.sqlTableView.setSizePolicy(sizePolicy)
        self.sqlTableView.setMinimumSize(QSize(300, 0))
        self.sqlTableView.setMaximumSize(QSize(16777215, 900))
        self.sqlTableView.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )

        self.verticalLayout.addWidget(self.sqlTableView)

        self.progressContainerWidget = QWidget(self.rightBar)
        self.progressContainerWidget.setObjectName("progressContainerWidget")
        self.progressContainerWidget.setMinimumSize(QSize(39, 0))
        self.horizontalLayout_2 = QHBoxLayout(self.progressContainerWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressLabel = QLabel(self.progressContainerWidget)
        self.progressLabel.setObjectName("progressLabel")

        self.horizontalLayout_2.addWidget(
            self.progressLabel, 0, Qt.AlignmentFlag.AlignVCenter
        )

        self.progressBar = QProgressBar(self.progressContainerWidget)
        self.progressBar.setObjectName("progressBar")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.progressBar.sizePolicy().hasHeightForWidth()
        )
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setValue(0)

        self.horizontalLayout_2.addWidget(
            self.progressBar,
            0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
        )

        self.verticalLayout.addWidget(
            self.progressContainerWidget,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom,
        )

        self.horizontalLayout.addWidget(self.rightBar)

        self.retranslateUi(GeneralWidget)

        QMetaObject.connectSlotsByName(GeneralWidget)

    # setupUi

    def retranslateUi(self, GeneralWidget):
        GeneralWidget.setWindowTitle(
            QCoreApplication.translate("GeneralWidget", "General", None)
        )
        self.farmingVariablesLabel.setText(
            QCoreApplication.translate(
                "GeneralWidget", "Farming Variables", None
            )
        )
        self.farmingTechniqueLabel.setText(
            QCoreApplication.translate(
                "GeneralWidget", "Farming Technique:", None
            )
        )
        self.unitOfMeasurementLabel.setText(
            QCoreApplication.translate(
                "GeneralWidget", "Unit of Measurement:", None
            )
        )
        self.fuelTypeLabel.setText(
            QCoreApplication.translate("GeneralWidget", "Fuel Type:", None)
        )
        self.amountOfFuelUsedLabel.setText(
            QCoreApplication.translate(
                "GeneralWidget", "Amount of fuel used:", None
            )
        )
        self.calculateContainerCheckBox.setText(
            QCoreApplication.translate(
                "GeneralWidget", "Local Temperatures", None
            )
        )
        self.calculateContainerPushButton.setText(
            QCoreApplication.translate("GeneralWidget", "Calculate", None)
        )
        self.editDatabasePushButton.setText(
            QCoreApplication.translate("GeneralWidget", "Edit Database", None)
        )
        self.importPushButton.setText(
            QCoreApplication.translate("GeneralWidget", "Import", None)
        )
        self.exportPushButton.setText(
            QCoreApplication.translate("GeneralWidget", "Export", None)
        )
        self.settingsPushButton.setText(
            QCoreApplication.translate("GeneralWidget", "Settings", None)
        )
        self.mainBodyPlaceholderLabel.setText(
            QCoreApplication.translate("GeneralWidget", "main body", None)
        )
        self.madeByCreditsLabel.setText(
            QCoreApplication.translate(
                "GeneralWidget",
                "Made by Luis Rosario and Cameron Morgan",
                None,
            )
        )
        self.recentTransactionsHeaderLabel.setText(
            QCoreApplication.translate(
                "GeneralWidget", "Recent Transactions", None
            )
        )
        self.progressLabel.setText(
            QCoreApplication.translate(
                "GeneralWidget", "nothing is happening", None
            )
        )

    # retranslateUi
