from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractSpinBox,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from ui.generated_python_ui import icons_rc  # noqa: F401


class Ui_GeneralWidget(object):
    def setupUi(self, GeneralWidget):
        if not GeneralWidget.objectName():
            GeneralWidget.setObjectName("GeneralWidget")
        GeneralWidget.setWindowModality(Qt.WindowModality.NonModal)
        GeneralWidget.resize(1179, 663)
        GeneralWidget.setAutoFillBackground(False)
        GeneralWidget.setStyleSheet("")
        self.horizontalLayout = QHBoxLayout(GeneralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftBar = QWidget(GeneralWidget)
        self.leftBar.setObjectName("leftBar")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftBar.sizePolicy().hasHeightForWidth())
        self.leftBar.setSizePolicy(sizePolicy)
        self.leftBar.setMaximumSize(QSize(16777215, 16777215))
        self.leftBar.setStyleSheet("")
        self.verticalLayout_2 = QVBoxLayout(self.leftBar)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.farmingVariablesWidget = QWidget(self.leftBar)
        self.farmingVariablesWidget.setObjectName("farmingVariablesWidget")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.farmingVariablesWidget.sizePolicy().hasHeightForWidth()
        )
        self.farmingVariablesWidget.setSizePolicy(sizePolicy1)
        self.farmingVariablesWidget.setMinimumSize(QSize(300, 0))
        self.farmingVariablesWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.DefaultContextMenu
        )
        self.verticalLayout_3 = QVBoxLayout(self.farmingVariablesWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.farmingVariablesLabel = QLabel(self.farmingVariablesWidget)
        self.farmingVariablesLabel.setObjectName("farmingVariablesLabel")
        sizePolicy.setHeightForWidth(
            self.farmingVariablesLabel.sizePolicy().hasHeightForWidth()
        )
        self.farmingVariablesLabel.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(12)
        font.setBold(True)
        self.farmingVariablesLabel.setFont(font)
        self.farmingVariablesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.farmingVariablesLabel)

        self.farmingTechniqueWidget = QWidget(self.farmingVariablesWidget)
        self.farmingTechniqueWidget.setObjectName("farmingTechniqueWidget")
        self.horizontalLayout_8 = QHBoxLayout(self.farmingTechniqueWidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.farmingTechniqueLabel = QLabel(self.farmingTechniqueWidget)
        self.farmingTechniqueLabel.setObjectName("farmingTechniqueLabel")

        self.horizontalLayout_8.addWidget(
            self.farmingTechniqueLabel, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.farmingTechniqueComboBox = QComboBox(self.farmingTechniqueWidget)
        self.farmingTechniqueComboBox.setObjectName("farmingTechniqueComboBox")
        self.farmingTechniqueComboBox.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )

        self.horizontalLayout_8.addWidget(
            self.farmingTechniqueComboBox, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.verticalLayout_3.addWidget(
            self.farmingTechniqueWidget, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.amountOfFuelUsedWidget = QWidget(self.farmingVariablesWidget)
        self.amountOfFuelUsedWidget.setObjectName("amountOfFuelUsedWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.amountOfFuelUsedWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.amountOfFuelUsedLabel = QLabel(self.amountOfFuelUsedWidget)
        self.amountOfFuelUsedLabel.setObjectName("amountOfFuelUsedLabel")
        sizePolicy.setHeightForWidth(
            self.amountOfFuelUsedLabel.sizePolicy().hasHeightForWidth()
        )
        self.amountOfFuelUsedLabel.setSizePolicy(sizePolicy)
        self.amountOfFuelUsedLabel.setMinimumSize(QSize(75, 0))
        self.amountOfFuelUsedLabel.setScaledContents(False)
        self.amountOfFuelUsedLabel.setIndent(4)

        self.horizontalLayout_4.addWidget(
            self.amountOfFuelUsedLabel, 0, Qt.AlignmentFlag.AlignRight
        )

        self.amountOfFuelUsedDoubleSpinBox = QDoubleSpinBox(self.amountOfFuelUsedWidget)
        self.amountOfFuelUsedDoubleSpinBox.setObjectName(
            "amountOfFuelUsedDoubleSpinBox"
        )
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.amountOfFuelUsedDoubleSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.amountOfFuelUsedDoubleSpinBox.setSizePolicy(sizePolicy2)
        self.amountOfFuelUsedDoubleSpinBox.setStyleSheet("")
        self.amountOfFuelUsedDoubleSpinBox.setAccelerated(True)
        self.amountOfFuelUsedDoubleSpinBox.setMinimum(-1000.000000000000000)
        self.amountOfFuelUsedDoubleSpinBox.setMaximum(1000.000000000000000)

        self.horizontalLayout_4.addWidget(
            self.amountOfFuelUsedDoubleSpinBox, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.fuelTypeComboBox = QComboBox(self.amountOfFuelUsedWidget)
        self.fuelTypeComboBox.setObjectName("fuelTypeComboBox")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.fuelTypeComboBox.sizePolicy().hasHeightForWidth()
        )
        self.fuelTypeComboBox.setSizePolicy(sizePolicy3)
        self.fuelTypeComboBox.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )

        self.horizontalLayout_4.addWidget(
            self.fuelTypeComboBox, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.fuelUnitOfMeasurementComboBox = QComboBox(self.amountOfFuelUsedWidget)
        self.fuelUnitOfMeasurementComboBox.setObjectName(
            "fuelUnitOfMeasurementComboBox"
        )
        self.fuelUnitOfMeasurementComboBox.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )

        self.horizontalLayout_4.addWidget(
            self.fuelUnitOfMeasurementComboBox, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.verticalLayout_3.addWidget(
            self.amountOfFuelUsedWidget, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.widget = QWidget(self.farmingVariablesWidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout_9 = QHBoxLayout(self.widget)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")

        self.horizontalLayout_9.addWidget(self.label, 0, Qt.AlignmentFlag.AlignLeft)

        self.temperatureDoubleSpinBox = QDoubleSpinBox(self.widget)
        self.temperatureDoubleSpinBox.setObjectName("temperatureDoubleSpinBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.temperatureDoubleSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.temperatureDoubleSpinBox.setSizePolicy(sizePolicy4)
        self.temperatureDoubleSpinBox.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.UpDownArrows
        )
        self.temperatureDoubleSpinBox.setAccelerated(True)
        self.temperatureDoubleSpinBox.setDecimals(1)
        self.temperatureDoubleSpinBox.setMinimum(-1000.000000000000000)
        self.temperatureDoubleSpinBox.setMaximum(1000.000000000000000)

        self.horizontalLayout_9.addWidget(
            self.temperatureDoubleSpinBox, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.temperatureTypesComboBox = QComboBox(self.widget)
        self.temperatureTypesComboBox.setObjectName("temperatureTypesComboBox")
        self.temperatureTypesComboBox.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )

        self.horizontalLayout_9.addWidget(
            self.temperatureTypesComboBox, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.verticalLayout_3.addWidget(self.widget, 0, Qt.AlignmentFlag.AlignLeft)

        self.userIDContainerWidget = QWidget(self.farmingVariablesWidget)
        self.userIDContainerWidget.setObjectName("userIDContainerWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.userIDContainerWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.userIDLabel = QLabel(self.userIDContainerWidget)
        self.userIDLabel.setObjectName("userIDLabel")

        self.horizontalLayout_5.addWidget(
            self.userIDLabel, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.userIDSpinBox = QSpinBox(self.userIDContainerWidget)
        self.userIDSpinBox.setObjectName("userIDSpinBox")

        self.horizontalLayout_5.addWidget(self.userIDSpinBox)

        self.verticalLayout_3.addWidget(
            self.userIDContainerWidget, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.verticalLayout_2.addWidget(self.farmingVariablesWidget)

        self.calculateContainerWidget = QWidget(self.leftBar)
        self.calculateContainerWidget.setObjectName("calculateContainerWidget")
        sizePolicy5 = QSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(
            self.calculateContainerWidget.sizePolicy().hasHeightForWidth()
        )
        self.calculateContainerWidget.setSizePolicy(sizePolicy5)
        self.horizontalLayout_6 = QHBoxLayout(self.calculateContainerWidget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.realTimeTemperaturesControlContainerWidget = QWidget(
            self.calculateContainerWidget
        )
        self.realTimeTemperaturesControlContainerWidget.setObjectName(
            "realTimeTemperaturesControlContainerWidget"
        )
        self.verticalLayout_7 = QVBoxLayout(
            self.realTimeTemperaturesControlContainerWidget
        )
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.realTimeTemperatureCheckBox = QCheckBox(
            self.realTimeTemperaturesControlContainerWidget
        )
        self.realTimeTemperatureCheckBox.setObjectName("realTimeTemperatureCheckBox")

        self.verticalLayout_7.addWidget(self.realTimeTemperatureCheckBox)

        self.horizontalLayout_6.addWidget(
            self.realTimeTemperaturesControlContainerWidget
        )

        self.calculateContainerPushButton = QPushButton(self.calculateContainerWidget)
        self.calculateContainerPushButton.setObjectName("calculateContainerPushButton")

        self.horizontalLayout_6.addWidget(self.calculateContainerPushButton)

        self.calculationUnitOfMeasurementComboBox = QComboBox(
            self.calculateContainerWidget
        )
        self.calculationUnitOfMeasurementComboBox.setObjectName(
            "calculationUnitOfMeasurementComboBox"
        )
        sizePolicy3.setHeightForWidth(
            self.calculationUnitOfMeasurementComboBox.sizePolicy().hasHeightForWidth()
        )
        self.calculationUnitOfMeasurementComboBox.setSizePolicy(sizePolicy3)
        self.calculationUnitOfMeasurementComboBox.setTabletTracking(False)
        self.calculationUnitOfMeasurementComboBox.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )

        self.horizontalLayout_6.addWidget(
            self.calculationUnitOfMeasurementComboBox,
            0,
            Qt.AlignmentFlag.AlignLeft,
        )

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
        self.editDatabasePushButton.setStyleSheet("")
        icon = QIcon()
        icon.addFile(
            ":/icons/svgs/solid/database.svg",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.editDatabasePushButton.setIcon(icon)

        self.verticalLayout_4.addWidget(self.editDatabasePushButton)

        self.importPushButton = QPushButton(self.moreWidget)
        self.importPushButton.setObjectName("importPushButton")
        icon1 = QIcon()
        icon1.addFile(
            ":/icons/svgs/solid/file-import.svg",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.importPushButton.setIcon(icon1)

        self.verticalLayout_4.addWidget(self.importPushButton)

        self.exportPushButton = QPushButton(self.moreWidget)
        self.exportPushButton.setObjectName("exportPushButton")
        icon2 = QIcon()
        icon2.addFile(
            ":/icons/svgs/solid/file-export.svg",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.exportPushButton.setIcon(icon2)

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
        self.mainBody.setSizeIncrement(QSize(10, 0))
        font1 = QFont()
        font1.setFamilies(["Segoe UI"])
        font1.setPointSize(10)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.mainBody.setFont(font1)
        self.verticalLayout_6 = QVBoxLayout(self.mainBody)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.mainBodyPlaceholderLabel = QLabel(self.mainBody)
        self.mainBodyPlaceholderLabel.setObjectName("mainBodyPlaceholderLabel")
        font2 = QFont()
        font2.setFamilies(["Segoe UI"])
        font2.setPointSize(10)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        font2.setKerning(False)
        self.mainBodyPlaceholderLabel.setFont(font2)
        self.mainBodyPlaceholderLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.mainBodyPlaceholderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.mainBodyPlaceholderLabel)

        self.madeByCreditsLabel = QLabel(self.mainBody)
        self.madeByCreditsLabel.setObjectName("madeByCreditsLabel")
        font3 = QFont()
        font3.setFamilies(["Segoe UI"])
        font3.setPointSize(9)
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
        self.horizontalLayout_3 = QHBoxLayout(self.recentTransactionsHeaderWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.recentTransactionsHeaderLabel = QLabel(self.recentTransactionsHeaderWidget)
        self.recentTransactionsHeaderLabel.setObjectName(
            "recentTransactionsHeaderLabel"
        )
        self.recentTransactionsHeaderLabel.setFont(font)
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
        sizePolicy6 = QSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding
        )
        sizePolicy6.setHorizontalStretch(199)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.sqlTableView.sizePolicy().hasHeightForWidth()
        )
        self.sqlTableView.setSizePolicy(sizePolicy6)
        self.sqlTableView.setMinimumSize(QSize(300, 0))
        self.sqlTableView.setMaximumSize(QSize(16777215, 900))
        self.sqlTableView.setSizeIncrement(QSize(0, 0))
        self.sqlTableView.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

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
        sizePolicy7 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy7)
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
            QCoreApplication.translate("GeneralWidget", "Farming Variables", None)
        )
        self.farmingTechniqueLabel.setText(
            QCoreApplication.translate("GeneralWidget", "Farming Technique:", None)
        )
        self.amountOfFuelUsedLabel.setText(
            QCoreApplication.translate("GeneralWidget", "Fuel Amount:", None)
        )
        self.label.setText(
            QCoreApplication.translate("GeneralWidget", "Temperature:", None)
        )
        self.temperatureDoubleSpinBox.setPrefix("")
        self.temperatureDoubleSpinBox.setSuffix(
            QCoreApplication.translate("GeneralWidget", "\u00b0", None)
        )
        self.userIDLabel.setText(
            QCoreApplication.translate("GeneralWidget", "User ID:", None)
        )
        self.realTimeTemperatureCheckBox.setText(
            QCoreApplication.translate("GeneralWidget", "Real-Time temperatures", None)
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
            QCoreApplication.translate("GeneralWidget", "Recent Transactions", None)
        )
        self.progressLabel.setText(
            QCoreApplication.translate("GeneralWidget", "nothing is happening", None)
        )

    # retranslateUi
