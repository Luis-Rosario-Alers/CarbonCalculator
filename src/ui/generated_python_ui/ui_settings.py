from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ui.generated_python_ui import icons_rc  # noqa: F401


class Ui_settingsWidget(object):
    def setupUi(self, settingsWidget):
        if not settingsWidget.objectName():
            settingsWidget.setObjectName("settingsWidget")
        settingsWidget.resize(370, 636)
        self.horizontalLayout = QHBoxLayout(settingsWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftBar = QWidget(settingsWidget)
        self.leftBar.setObjectName("leftBar")
        self.leftBar.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(self.leftBar)
        self.verticalLayout.setObjectName("verticalLayout")
        self.leftBarMainWidget = QWidget(self.leftBar)
        self.leftBarMainWidget.setObjectName("leftBarMainWidget")
        self.leftBarMainWidget.setMaximumSize(QSize(400, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.leftBarMainWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pathsContainerWidget = QWidget(self.leftBarMainWidget)
        self.pathsContainerWidget.setObjectName("pathsContainerWidget")
        self.verticalLayout_5 = QVBoxLayout(self.pathsContainerWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pathsLabel = QLabel(self.pathsContainerWidget)
        self.pathsLabel.setObjectName("pathsLabel")
        self.pathsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.pathsLabel)

        self.verticalLayout_3.addWidget(
            self.pathsContainerWidget, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.emissionsModifiersPathContainer = QWidget(self.leftBarMainWidget)
        self.emissionsModifiersPathContainer.setObjectName(
            "emissionsModifiersPathContainer"
        )
        self.horizontalLayout_6 = QHBoxLayout(self.emissionsModifiersPathContainer)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.emissionsModifiersPathLabel = QLabel(self.emissionsModifiersPathContainer)
        self.emissionsModifiersPathLabel.setObjectName("emissionsModifiersPathLabel")

        self.horizontalLayout_6.addWidget(self.emissionsModifiersPathLabel)

        self.emissionsModifiersPathPushButton = QPushButton(
            self.emissionsModifiersPathContainer
        )
        self.emissionsModifiersPathPushButton.setObjectName(
            "emissionsModifiersPathPushButton"
        )

        self.horizontalLayout_6.addWidget(self.emissionsModifiersPathPushButton)

        self.verticalLayout_3.addWidget(
            self.emissionsModifiersPathContainer,
            0,
            Qt.AlignmentFlag.AlignHCenter,
        )

        self.apiKeysContainerWidget = QWidget(self.leftBarMainWidget)
        self.apiKeysContainerWidget.setObjectName("apiKeysContainerWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.apiKeysContainerWidget.sizePolicy().hasHeightForWidth()
        )
        self.apiKeysContainerWidget.setSizePolicy(sizePolicy)
        self.apiKeysContainerWidget.setMaximumSize(QSize(16777215, 16777215))
        self.apiKeysContainerWidget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.horizontalLayout_2 = QHBoxLayout(self.apiKeysContainerWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.apiKeysLabel = QLabel(self.apiKeysContainerWidget)
        self.apiKeysLabel.setObjectName("apiKeysLabel")
        self.apiKeysLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.apiKeysLabel)

        self.verticalLayout_3.addWidget(
            self.apiKeysContainerWidget, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.ipInfoAPIKeyWidget = QWidget(self.leftBarMainWidget)
        self.ipInfoAPIKeyWidget.setObjectName("ipInfoAPIKeyWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.ipInfoAPIKeyWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ipInfoAPIKeyLabel = QLabel(self.ipInfoAPIKeyWidget)
        self.ipInfoAPIKeyLabel.setObjectName("ipInfoAPIKeyLabel")

        self.horizontalLayout_4.addWidget(self.ipInfoAPIKeyLabel)

        self.ipInfoAPIKeyLineEdit = QLineEdit(self.ipInfoAPIKeyWidget)
        self.ipInfoAPIKeyLineEdit.setObjectName("ipInfoAPIKeyLineEdit")
        self.ipInfoAPIKeyLineEdit.setStyleSheet("")

        self.horizontalLayout_4.addWidget(self.ipInfoAPIKeyLineEdit)

        self.verticalLayout_3.addWidget(
            self.ipInfoAPIKeyWidget, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.openWeatherMapAPIKeyWidget = QWidget(self.leftBarMainWidget)
        self.openWeatherMapAPIKeyWidget.setObjectName("openWeatherMapAPIKeyWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.openWeatherMapAPIKeyWidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.openWeatherMapAPIKeyLabel = QLabel(self.openWeatherMapAPIKeyWidget)
        self.openWeatherMapAPIKeyLabel.setObjectName("openWeatherMapAPIKeyLabel")

        self.horizontalLayout_5.addWidget(
            self.openWeatherMapAPIKeyLabel, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.openWeatherMapAPIKeyLineEdit = QLineEdit(self.openWeatherMapAPIKeyWidget)
        self.openWeatherMapAPIKeyLineEdit.setObjectName("openWeatherMapAPIKeyLineEdit")
        self.openWeatherMapAPIKeyLineEdit.setStyleSheet(
            "* { lineedit-password-character: 9679 }"
        )
        self.openWeatherMapAPIKeyLineEdit.setFrame(True)
        self.openWeatherMapAPIKeyLineEdit.setClearButtonEnabled(False)

        self.horizontalLayout_5.addWidget(self.openWeatherMapAPIKeyLineEdit)

        self.verticalLayout_3.addWidget(
            self.openWeatherMapAPIKeyWidget, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.preferencesContainerWidget = QWidget(self.leftBarMainWidget)
        self.preferencesContainerWidget.setObjectName("preferencesContainerWidget")
        self.verticalLayout_4 = QVBoxLayout(self.preferencesContainerWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.preferencesLabel = QLabel(self.preferencesContainerWidget)
        self.preferencesLabel.setObjectName("preferencesLabel")
        self.preferencesLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.preferencesLabel.setLineWidth(1)
        self.preferencesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(
            self.preferencesLabel, 0, Qt.AlignmentFlag.AlignBottom
        )

        self.verticalLayout_3.addWidget(
            self.preferencesContainerWidget, 0, Qt.AlignmentFlag.AlignHCenter
        )

        self.preferredTemperatureMeasurementWidget = QWidget(self.leftBarMainWidget)
        self.preferredTemperatureMeasurementWidget.setObjectName(
            "preferredTemperatureMeasurementWidget"
        )
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.preferredTemperatureMeasurementWidget.sizePolicy().hasHeightForWidth()
        )
        self.preferredTemperatureMeasurementWidget.setSizePolicy(sizePolicy1)
        self.horizontalLayout_7 = QHBoxLayout(
            self.preferredTemperatureMeasurementWidget
        )
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.preferredTemperatureMeasurementLabel = QLabel(
            self.preferredTemperatureMeasurementWidget
        )
        self.preferredTemperatureMeasurementLabel.setObjectName(
            "preferredTemperatureMeasurementLabel"
        )

        self.horizontalLayout_7.addWidget(
            self.preferredTemperatureMeasurementLabel,
            0,
            Qt.AlignmentFlag.AlignHCenter,
        )

        self.preferredTemperatureMeasurementComboBox = QComboBox(
            self.preferredTemperatureMeasurementWidget
        )
        self.preferredTemperatureMeasurementComboBox.setObjectName(
            "preferredTemperatureMeasurementComboBox"
        )

        self.horizontalLayout_7.addWidget(self.preferredTemperatureMeasurementComboBox)

        self.verticalLayout_3.addWidget(
            self.preferredTemperatureMeasurementWidget,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
        )

        self.preferredUnitOfMeasurementWidget = QWidget(self.leftBarMainWidget)
        self.preferredUnitOfMeasurementWidget.setObjectName(
            "preferredUnitOfMeasurementWidget"
        )
        self.horizontalLayout_8 = QHBoxLayout(self.preferredUnitOfMeasurementWidget)
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
        self.preferredUnitOfMeasurementComboBox.setAutoFillBackground(False)

        self.horizontalLayout_8.addWidget(self.preferredUnitOfMeasurementComboBox)

        self.verticalLayout_3.addWidget(
            self.preferredUnitOfMeasurementWidget,
            0,
            Qt.AlignmentFlag.AlignRight,
        )

        self.languageContainerWidget = QWidget(self.leftBarMainWidget)
        self.languageContainerWidget.setObjectName("languageContainerWidget")
        self.horizontalLayout_9 = QHBoxLayout(self.languageContainerWidget)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.languageLabel = QLabel(self.languageContainerWidget)
        self.languageLabel.setObjectName("languageLabel")

        self.horizontalLayout_9.addWidget(
            self.languageLabel, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.languageComboBox = QComboBox(self.languageContainerWidget)
        self.languageComboBox.setObjectName("languageComboBox")

        self.horizontalLayout_9.addWidget(
            self.languageComboBox, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.verticalLayout_3.addWidget(
            self.languageContainerWidget, 0, Qt.AlignmentFlag.AlignRight
        )

        self.themeContainerWidget = QWidget(self.leftBarMainWidget)
        self.themeContainerWidget.setObjectName("themeContainerWidget")
        self.horizontalLayout_10 = QHBoxLayout(self.themeContainerWidget)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.themeLabel = QLabel(self.themeContainerWidget)
        self.themeLabel.setObjectName("themeLabel")

        self.horizontalLayout_10.addWidget(self.themeLabel)

        self.themeComboBox = QComboBox(self.themeContainerWidget)
        self.themeComboBox.setObjectName("themeComboBox")

        self.horizontalLayout_10.addWidget(self.themeComboBox)

        self.verticalLayout_3.addWidget(
            self.themeContainerWidget, 0, Qt.AlignmentFlag.AlignRight
        )

        self.preferredUserIDContainerWidget = QWidget(self.leftBarMainWidget)
        self.preferredUserIDContainerWidget.setObjectName(
            "preferredUserIDContainerWidget"
        )
        self.horizontalLayout_12 = QHBoxLayout(self.preferredUserIDContainerWidget)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.preferredUserIDLabel = QLabel(self.preferredUserIDContainerWidget)
        self.preferredUserIDLabel.setObjectName("preferredUserIDLabel")

        self.horizontalLayout_12.addWidget(self.preferredUserIDLabel)

        self.preferredUserIDSpinBox = QSpinBox(self.preferredUserIDContainerWidget)
        self.preferredUserIDSpinBox.setObjectName("preferredUserIDSpinBox")

        self.horizontalLayout_12.addWidget(self.preferredUserIDSpinBox)

        self.verticalLayout_3.addWidget(
            self.preferredUserIDContainerWidget, 0, Qt.AlignmentFlag.AlignRight
        )

        self.fetchLocalTemperaturesOnStartupContainerWIdget = QWidget(
            self.leftBarMainWidget
        )
        self.fetchLocalTemperaturesOnStartupContainerWIdget.setObjectName(
            "fetchLocalTemperaturesOnStartupContainerWIdget"
        )
        self.horizontalLayout_3 = QHBoxLayout(
            self.fetchLocalTemperaturesOnStartupContainerWIdget
        )
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fetchLocalTemperaturesOnStartupCheckBox = QCheckBox(
            self.fetchLocalTemperaturesOnStartupContainerWIdget
        )
        self.fetchLocalTemperaturesOnStartupCheckBox.setObjectName(
            "fetchLocalTemperaturesOnStartupCheckBox"
        )

        self.horizontalLayout_3.addWidget(
            self.fetchLocalTemperaturesOnStartupCheckBox,
            0,
            Qt.AlignmentFlag.AlignRight,
        )

        self.verticalLayout_3.addWidget(
            self.fetchLocalTemperaturesOnStartupContainerWIdget,
            0,
            Qt.AlignmentFlag.AlignRight,
        )

        self.temperatureUseContainerWidget = QWidget(self.leftBarMainWidget)
        self.temperatureUseContainerWidget.setObjectName(
            "temperatureUseContainerWidget"
        )
        self.horizontalLayout_11 = QHBoxLayout(self.temperatureUseContainerWidget)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.temperatureUseCheckBox = QCheckBox(self.temperatureUseContainerWidget)
        self.temperatureUseCheckBox.setObjectName("temperatureUseCheckBox")
        self.temperatureUseCheckBox.setChecked(False)

        self.horizontalLayout_11.addWidget(
            self.temperatureUseCheckBox, 0, Qt.AlignmentFlag.AlignRight
        )

        self.verticalLayout_3.addWidget(self.temperatureUseContainerWidget)

        self.verticalLayout.addWidget(
            self.leftBarMainWidget, 0, Qt.AlignmentFlag.AlignLeft
        )

        self.horizontalLayout.addWidget(self.leftBar)

        self.retranslateUi(settingsWidget)

        QMetaObject.connectSlotsByName(settingsWidget)

    # setupUi

    def retranslateUi(self, settingsWidget):
        settingsWidget.setWindowTitle(
            QCoreApplication.translate("settingsWidget", "Settings", None)
        )
        self.pathsLabel.setText(
            QCoreApplication.translate(
                "settingsWidget",
                '<html><head/><body><p><span style=" font-style:italic;">Paths</span></p></body></html>',
                None,
            )
        )
        self.emissionsModifiersPathLabel.setText(
            QCoreApplication.translate(
                "settingsWidget", "Emission modifiers path:", None
            )
        )
        self.emissionsModifiersPathPushButton.setText(
            QCoreApplication.translate("settingsWidget", "Set Path", None)
        )
        self.apiKeysLabel.setText(
            QCoreApplication.translate(
                "settingsWidget",
                '<html><head/><body><p><span style=" font-style:italic;">API Keys</span></p></body></html>',
                None,
            )
        )
        self.ipInfoAPIKeyLabel.setText(
            QCoreApplication.translate("settingsWidget", "IPinfo API key", None)
        )
        self.ipInfoAPIKeyLineEdit.setPlaceholderText(
            QCoreApplication.translate("settingsWidget", "add key here...", None)
        )
        self.openWeatherMapAPIKeyLabel.setText(
            QCoreApplication.translate("settingsWidget", "OpenWeatherAPI key:", None)
        )
        self.openWeatherMapAPIKeyLineEdit.setPlaceholderText(
            QCoreApplication.translate("settingsWidget", "add key here...", None)
        )
        self.preferencesLabel.setText(
            QCoreApplication.translate(
                "settingsWidget",
                '<html><head/><body><p><span style=" font-style:italic;">Preferences</span></p></body></html>',
                None,
            )
        )
        self.preferredTemperatureMeasurementLabel.setText(
            QCoreApplication.translate(
                "settingsWidget", "Preferred Temperature Measurement", None
            )
        )
        self.preferredUnitOfMeasurementLabel.setText(
            QCoreApplication.translate(
                "settingsWidget", "Preferred Unit of Measurement", None
            )
        )
        self.languageLabel.setText(
            QCoreApplication.translate("settingsWidget", "Language:", None)
        )
        self.themeLabel.setText(
            QCoreApplication.translate("settingsWidget", "Theme:", None)
        )
        self.preferredUserIDLabel.setText(
            QCoreApplication.translate("settingsWidget", "Preferred User ID", None)
        )
        self.fetchLocalTemperaturesOnStartupCheckBox.setText(
            QCoreApplication.translate(
                "settingsWidget", "Fetch local temperatures on startup", None
            )
        )
        self.temperatureUseCheckBox.setText(
            QCoreApplication.translate(
                "settingsWidget", "Use temperature in calculations", None
            )
        )

    # retranslateUi
