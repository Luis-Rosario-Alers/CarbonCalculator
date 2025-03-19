from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_settingsWidget(object):
    def setupUi(self, settingsWidget):
        if not settingsWidget.objectName():
            settingsWidget.setObjectName("settingsWidget")
        settingsWidget.resize(789, 613)
        self.horizontalLayout = QHBoxLayout(settingsWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftBar = QWidget(settingsWidget)
        self.leftBar.setObjectName("leftBar")
        self.verticalLayout = QVBoxLayout(self.leftBar)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leftBarMainWidget = QWidget(self.leftBar)
        self.leftBarMainWidget.setObjectName("leftBarMainWidget")
        self.verticalLayout_3 = QVBoxLayout(self.leftBarMainWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.emissionsModifiersPathContainer = QWidget(self.leftBarMainWidget)
        self.emissionsModifiersPathContainer.setObjectName(
            "emissionsModifiersPathContainer"
        )
        self.horizontalLayout_6 = QHBoxLayout(
            self.emissionsModifiersPathContainer
        )
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.emissionsModifiersPathLabel = QLabel(
            self.emissionsModifiersPathContainer
        )
        self.emissionsModifiersPathLabel.setObjectName(
            "emissionsModifiersPathLabel"
        )

        self.horizontalLayout_6.addWidget(self.emissionsModifiersPathLabel)

        self.emissionsModifiersPathPushButton = QPushButton(
            self.emissionsModifiersPathContainer
        )
        self.emissionsModifiersPathPushButton.setObjectName(
            "emissionsModifiersPathPushButton"
        )

        self.horizontalLayout_6.addWidget(
            self.emissionsModifiersPathPushButton
        )

        self.verticalLayout_3.addWidget(self.emissionsModifiersPathContainer)

        self.apiKeyInputContainer = QWidget(self.leftBarMainWidget)
        self.apiKeyInputContainer.setObjectName("apiKeyInputContainer")
        self.verticalLayout_4 = QVBoxLayout(self.apiKeyInputContainer)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.openWeatherMapAPIKeyWidget = QWidget(self.apiKeyInputContainer)
        self.openWeatherMapAPIKeyWidget.setObjectName(
            "openWeatherMapAPIKeyWidget"
        )
        self.horizontalLayout_5 = QHBoxLayout(self.openWeatherMapAPIKeyWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.openWeatherMapAPIKeyLabel = QLabel(
            self.openWeatherMapAPIKeyWidget
        )
        self.openWeatherMapAPIKeyLabel.setObjectName(
            "openWeatherMapAPIKeyLabel"
        )

        self.horizontalLayout_5.addWidget(self.openWeatherMapAPIKeyLabel)

        self.openWeatherMapAPIKeyLineEdit = QLineEdit(
            self.openWeatherMapAPIKeyWidget
        )
        self.openWeatherMapAPIKeyLineEdit.setObjectName(
            "openWeatherMapAPIKeyLineEdit"
        )

        self.horizontalLayout_5.addWidget(self.openWeatherMapAPIKeyLineEdit)

        self.verticalLayout_4.addWidget(
            self.openWeatherMapAPIKeyWidget, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.ipInfoAPIKeyWidget = QWidget(self.apiKeyInputContainer)
        self.ipInfoAPIKeyWidget.setObjectName("ipInfoAPIKeyWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.ipInfoAPIKeyWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ipInfoAPIKeyLabel = QLabel(self.ipInfoAPIKeyWidget)
        self.ipInfoAPIKeyLabel.setObjectName("ipInfoAPIKeyLabel")

        self.horizontalLayout_4.addWidget(self.ipInfoAPIKeyLabel)

        self.ipInfoAPIKeyLineEdit = QLineEdit(self.ipInfoAPIKeyWidget)
        self.ipInfoAPIKeyLineEdit.setObjectName("ipInfoAPIKeyLineEdit")

        self.horizontalLayout_4.addWidget(self.ipInfoAPIKeyLineEdit)

        self.verticalLayout_4.addWidget(
            self.ipInfoAPIKeyWidget, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.verticalLayout_3.addWidget(
            self.apiKeyInputContainer, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.preferredTemperatureMeasurementWidget = QWidget(
            self.leftBarMainWidget
        )
        self.preferredTemperatureMeasurementWidget.setObjectName(
            "preferredTemperatureMeasurementWidget"
        )
        self.horizontalLayout_7 = QHBoxLayout(
            self.preferredTemperatureMeasurementWidget
        )
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.preferredTemperatureMeasuremenLabel = QLabel(
            self.preferredTemperatureMeasurementWidget
        )
        self.preferredTemperatureMeasuremenLabel.setObjectName(
            "preferredTemperatureMeasuremenLabel"
        )

        self.horizontalLayout_7.addWidget(
            self.preferredTemperatureMeasuremenLabel
        )

        self.preferredTemperatureMeasuremenComboBox = QComboBox(
            self.preferredTemperatureMeasurementWidget
        )
        self.preferredTemperatureMeasuremenComboBox.setObjectName(
            "preferredTemperatureMeasuremenComboBox"
        )

        self.horizontalLayout_7.addWidget(
            self.preferredTemperatureMeasuremenComboBox
        )

        self.verticalLayout_3.addWidget(
            self.preferredTemperatureMeasurementWidget,
            0,
            Qt.AlignmentFlag.AlignLeft,
        )

        self.preferredUnitOfMeasurementWidget = QWidget(self.leftBarMainWidget)
        self.preferredUnitOfMeasurementWidget.setObjectName(
            "preferredUnitOfMeasurementWidget"
        )
        self.horizontalLayout_8 = QHBoxLayout(
            self.preferredUnitOfMeasurementWidget
        )
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.preferredUnitOfMeasurementLabel = QLabel(
            self.preferredUnitOfMeasurementWidget
        )
        self.preferredUnitOfMeasurementLabel.setObjectName(
            "preferredUnitOfMeasurementLabel"
        )

        self.horizontalLayout_8.addWidget(
            self.preferredUnitOfMeasurementLabel, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.preferredUnitOfMeasurementComboBox = QComboBox(
            self.preferredUnitOfMeasurementWidget
        )
        self.preferredUnitOfMeasurementComboBox.setObjectName(
            "preferredUnitOfMeasurementComboBox"
        )

        self.horizontalLayout_8.addWidget(
            self.preferredUnitOfMeasurementComboBox
        )

        self.verticalLayout_3.addWidget(
            self.preferredUnitOfMeasurementWidget,
            0,
            Qt.AlignmentFlag.AlignLeft,
        )

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.verticalLayout.addWidget(self.leftBarMainWidget)

        self.horizontalLayout.addWidget(self.leftBar)

        self.rightBar = QWidget(settingsWidget)
        self.rightBar.setObjectName("rightBar")
        self.verticalLayout_2 = QVBoxLayout(self.rightBar)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.returnWidget = QWidget(self.rightBar)
        self.returnWidget.setObjectName("returnWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.returnWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.returnPushButton = QPushButton(self.returnWidget)
        self.returnPushButton.setObjectName("returnPushButton")

        self.horizontalLayout_3.addWidget(
            self.returnPushButton, 0, Qt.AlignmentFlag.AlignTop
        )

        self.verticalLayout_2.addWidget(
            self.returnWidget,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
        )

        self.horizontalLayout.addWidget(self.rightBar)

        self.retranslateUi(settingsWidget)

        QMetaObject.connectSlotsByName(settingsWidget)

    # setupUi

    def retranslateUi(self, settingsWidget):
        settingsWidget.setWindowTitle(
            QCoreApplication.translate("settingsWidget", "Settings", None)
        )
        self.emissionsModifiersPathLabel.setText(
            QCoreApplication.translate(
                "settingsWidget", "Emission modifiers path:", None
            )
        )
        self.emissionsModifiersPathPushButton.setText(
            QCoreApplication.translate("settingsWidget", "Set Path", None)
        )
        self.openWeatherMapAPIKeyLabel.setText(
            QCoreApplication.translate(
                "settingsWidget", "OpenWeatherAPI key:", None
            )
        )
        self.ipInfoAPIKeyLabel.setText(
            QCoreApplication.translate(
                "settingsWidget", "IPinfo API key", None
            )
        )
        self.preferredTemperatureMeasuremenLabel.setText(
            QCoreApplication.translate(
                "settingsWidget", "Preferred Temperature Measurement", None
            )
        )
        self.preferredUnitOfMeasurementLabel.setText(
            QCoreApplication.translate(
                "settingsWidget", "Preferred Unit of Measurement", None
            )
        )
        self.returnPushButton.setText(
            QCoreApplication.translate("settingsWidget", "Return", None)
        )

    # retranslateUi
