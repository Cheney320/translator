# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from train_models.language_detector import LanguageDetector


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(340, 390, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 50, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(650, 50, 60, 16))
        self.label_2.setObjectName("label_2")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(100, 120, 601, 251))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.textEdit_2 = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit_2.setObjectName("textEdit_2")
        self.horizontalLayout.addWidget(self.textEdit_2)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(100, 80, 601, 27))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.comboBox_2 = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBox_2.setMaximumSize(QtCore.QSize(300, 16777215))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox_2, 0, QtCore.Qt.AlignRight)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.text_edit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "translator"))
        self.pushButton.setText(_translate("MainWindow", "翻译"))
        self.label.setText(_translate("MainWindow", "检测语言"))
        self.label_2.setText(_translate("MainWindow", "目标语言"))
        self.label_3.setText(_translate("MainWindow", "语种状态栏"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "中文"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "英文"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "法语"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "德语"))
        self.comboBox_2.setItemText(4, _translate("MainWindow", "西班牙语"))
        self.comboBox_2.setItemText(5, _translate("MainWindow", "意大利语"))
        self.comboBox_2.setItemText(6, _translate("MainWindow", "荷兰语"))

    def text_edit(self):
        self.textEdit.textChanged.connect(self.show_language)

    def show_language(self):

        if self.textEdit.toPlainText() == '':
            self.label_3.setText('语种状态栏')
            return

        path = '../models/language_detector.model'
        detector = LanguageDetector()
        detector.load_model(path)
        label = detector.predict(self.textEdit.toPlainText())[0]
        d = {'ch':'中文', 'en':'英语', 'it':'意大利语', 'de':'德语',
             'es':'西班牙语', 'fr':'法语', 'nl':'荷兰语'}
        self.label_3.setText('检测到'+d[label])




