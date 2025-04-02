from PySide6.QtCore import QCoreApplication, QMetaObject, Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ui.generated_python_ui import icons_rc  # noqa: F401


class Ui_feedbackTabWidget(object):
    def setupUi(self, feedbackTabWidget):
        if not feedbackTabWidget.objectName():
            feedbackTabWidget.setObjectName("feedbackTabWidget")
        feedbackTabWidget.resize(892, 684)
        self.verticalLayout = QVBoxLayout(feedbackTabWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QWidget(feedbackTabWidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName("label")
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignJustify | Qt.AlignmentFlag.AlignVCenter
        )
        self.label.setWordWrap(True)

        self.horizontalLayout.addWidget(self.label)

        self.verticalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(feedbackTabWidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_3 = QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_4.addWidget(
            self.label_2,
            0,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
        )

        self.horizontalLayout_2.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_2)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout_3.addWidget(
            self.label_3,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
        )

        self.horizontalLayout_2.addWidget(self.widget_4, 0, Qt.AlignmentFlag.AlignRight)

        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(feedbackTabWidget)

        QMetaObject.connectSlotsByName(feedbackTabWidget)

    # setupUi

    def retranslateUi(self, feedbackTabWidget):
        feedbackTabWidget.setWindowTitle(
            QCoreApplication.translate("feedbackTabWidget", "feedback", None)
        )
        self.label.setText(
            QCoreApplication.translate(
                "feedbackTabWidget",
                '<html><head/><body><p align="center"><span style=" font-size:36pt; font-weight:700; font-style:italic;">For sending feedback concerning this application please contact Luis or Cameron.</span></p><p align="center"><br/></p></body></html>',
                None,
            )
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "feedbackTabWidget",
                '<html><head/><body><p><a href="luisrosarioalers@gmail.com"><span style=" font-size:36pt; text-decoration: underline; color:#24a1f4;">Luis\' Email</span></a></p></body></html>',
                None,
            )
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "feedbackTabWidget",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "hr { height: 1px; border-width: 0; }\n"
                'li.unchecked::marker { content: "\\2610"; }\n'
                'li.checked::marker { content: "\\2612"; }\n'
                "</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><a href="cam3r0n.m0rgan@gmail.com"><span style=" font-size:36pt; text-decoration: underline; color:#24a1f4;">Cameron\'s Email</span></a></p></body></html>',
                None,
            )
        )

    # retranslateUi
