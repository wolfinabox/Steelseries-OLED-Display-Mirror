# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(262, 141)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)

        self.oled_device_box = QComboBox(self.centralwidget)
        self.oled_device_box.setObjectName(u"oled_device_box")

        self.gridLayout_2.addWidget(self.oled_device_box, 1, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.width_text = QLineEdit(self.centralwidget)
        self.width_text.setObjectName(u"width_text")

        self.horizontalLayout.addWidget(self.width_text)

        self.height_text = QLineEdit(self.centralwidget)
        self.height_text.setObjectName(u"height_text")

        self.horizontalLayout.addWidget(self.height_text)


        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")

        self.gridLayout_2.addWidget(self.start_button, 2, 0, 1, 1)

        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")

        self.gridLayout_2.addWidget(self.stop_button, 2, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 262, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Steelseries OLED Screen Mirror", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Monitor Resolution", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Steelseries OLED Device", None))
#if QT_CONFIG(statustip)
        self.oled_device_box.setStatusTip(QCoreApplication.translate("MainWindow", u"The Steelseries device to display on", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.width_text.setStatusTip(QCoreApplication.translate("MainWindow", u"Monitor width", None))
#endif // QT_CONFIG(statustip)
        self.width_text.setPlaceholderText(QCoreApplication.translate("MainWindow", u"width", None))
#if QT_CONFIG(statustip)
        self.height_text.setStatusTip(QCoreApplication.translate("MainWindow", u"Monitor height", None))
#endif // QT_CONFIG(statustip)
        self.height_text.setInputMask("")
        self.height_text.setPlaceholderText(QCoreApplication.translate("MainWindow", u"height", None))
#if QT_CONFIG(tooltip)
        self.start_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.start_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Start the mirroring", None))
#endif // QT_CONFIG(statustip)
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(tooltip)
        self.stop_button.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.stop_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Stop the mirroring", None))
#endif // QT_CONFIG(statustip)
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
    # retranslateUi

