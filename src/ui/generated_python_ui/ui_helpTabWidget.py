from PySide6.QtCore import QCoreApplication, QMetaObject, QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ui.generated_python_ui import icons_rc  # noqa: F401




class Ui_helpTabWidget(object):
    def setupUi(self, helpTabWidget):
        if not helpTabWidget.objectName():
            helpTabWidget.setObjectName("helpTabWidget")
        helpTabWidget.resize(875, 762)
        self.horizontalLayout = QHBoxLayout(helpTabWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.helpTabContainerWidget = QWidget(helpTabWidget)
        self.helpTabContainerWidget.setObjectName("helpTabContainerWidget")
        self.verticalLayout = QVBoxLayout(self.helpTabContainerWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.githubLogoContainerWidget = QWidget(self.helpTabContainerWidget)
        self.githubLogoContainerWidget.setObjectName("githubLogoContainerWidget")
        self.verticalLayout_2 = QVBoxLayout(self.githubLogoContainerWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.githubLogoLabel = QLabel(self.githubLogoContainerWidget)
        self.githubLogoLabel.setObjectName("githubLogoLabel")
        self.githubLogoLabel.setMinimumSize(QSize(200, 450))
        self.githubLogoLabel.setFrameShape(QFrame.Shape.NoFrame)
        self.githubLogoLabel.setPixmap(QPixmap(":/icons/svgs/brands/square-github.svg"))
        self.githubLogoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(
            self.githubLogoLabel, 0, Qt.AlignmentFlag.AlignTop
        )

        self.verticalLayout.addWidget(self.githubLogoContainerWidget)

        self.helpTextContainerWidget = QWidget(self.helpTabContainerWidget)
        self.helpTextContainerWidget.setObjectName("helpTextContainerWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.helpTextContainerWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.helpTextLabel = QLabel(self.helpTextContainerWidget)
        self.helpTextLabel.setObjectName("helpTextLabel")
        self.helpTextLabel.setMaximumSize(QSize(100000, 16777215))
        self.helpTextLabel.setFrameShape(QFrame.Shape.StyledPanel)
        self.helpTextLabel.setTextFormat(Qt.TextFormat.RichText)
        self.helpTextLabel.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )

        self.horizontalLayout_2.addWidget(self.helpTextLabel)

        self.verticalLayout.addWidget(self.helpTextContainerWidget)

        self.horizontalLayout.addWidget(self.helpTabContainerWidget)

        self.retranslateUi(helpTabWidget)

        QMetaObject.connectSlotsByName(helpTabWidget)

    # setupUi

    def retranslateUi(self, helpTabWidget):
        helpTabWidget.setWindowTitle(
            QCoreApplication.translate("helpTabWidget", "Form", None)
        )
        self.githubLogoLabel.setText("")
        self.helpTextLabel.setText(
            QCoreApplication.translate(
                "helpTabWidget",
                '<html><head/><body><p align="center"><span style=" font-size:36pt;">For more information go </span></p><p align="center"><span style=" font-size:36pt;">to our </span><a href="https://github.com/Luis-Rosario-Alers/CarbonCalculator/issues"><span style=" font-size:36pt; text-decoration: underline; color:#6295f4;">github repository </span></a></p><p align="center"><span style=" font-size:36pt;">and make an issue.</span></p></body></html>',
                None,
            )
        )

    # retranslateUi
