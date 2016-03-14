# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1092, 813)
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 50, 1091, 761))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabIlluminance = QtGui.QWidget()
        self.tabIlluminance.setObjectName(_fromUtf8("tabIlluminance"))
        self.verticalLayoutWidget = QtGui.QWidget(self.tabIlluminance)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(180, 0, 901, 731))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.layoutIlluminance = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.layoutIlluminance.setObjectName(_fromUtf8("layoutIlluminance"))
        self.calDateTimeIllum = QtGui.QDateTimeEdit(self.tabIlluminance)
        self.calDateTimeIllum.setGeometry(QtCore.QRect(70, 10, 91, 22))
        self.calDateTimeIllum.setToolTip(_fromUtf8(""))
        self.calDateTimeIllum.setWrapping(True)
        self.calDateTimeIllum.setAlignment(QtCore.Qt.AlignCenter)
        self.calDateTimeIllum.setDate(QtCore.QDate(2015, 1, 1))
        self.calDateTimeIllum.setTime(QtCore.QTime(0, 0, 0))
        self.calDateTimeIllum.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(2015, 12, 31), QtCore.QTime(23, 59, 59)))
        self.calDateTimeIllum.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2015, 1, 1), QtCore.QTime(0, 0, 0)))
        self.calDateTimeIllum.setMinimumDate(QtCore.QDate(2015, 1, 1))
        self.calDateTimeIllum.setCalendarPopup(True)
        self.calDateTimeIllum.setObjectName(_fromUtf8("calDateTimeIllum"))
        self.cmbTimeIllum = QtGui.QComboBox(self.tabIlluminance)
        self.cmbTimeIllum.setGeometry(QtCore.QRect(70, 40, 91, 22))
        self.cmbTimeIllum.setObjectName(_fromUtf8("cmbTimeIllum"))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.cmbTimeIllum.addItem(_fromUtf8(""))
        self.lblDate = QtGui.QLabel(self.tabIlluminance)
        self.lblDate.setGeometry(QtCore.QRect(10, 10, 46, 13))
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.lblTime = QtGui.QLabel(self.tabIlluminance)
        self.lblTime.setGeometry(QtCore.QRect(10, 40, 46, 21))
        self.lblTime.setObjectName(_fromUtf8("lblTime"))
        self.tabWidget.addTab(self.tabIlluminance, _fromUtf8(""))
        self.tabThermal = QtGui.QWidget()
        self.tabThermal.setObjectName(_fromUtf8("tabThermal"))
        self.tabWidget.addTab(self.tabThermal, _fromUtf8(""))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(-10, -10, 1101, 61))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.btnOpenJson = QtGui.QPushButton(self.groupBox)
        self.btnOpenJson.setGeometry(QtCore.QRect(10, 10, 101, 23))
        self.btnOpenJson.setObjectName(_fromUtf8("btnOpenJson"))
        self.txtJsonPath = QtGui.QLineEdit(self.groupBox)
        self.txtJsonPath.setEnabled(False)
        self.txtJsonPath.setGeometry(QtCore.QRect(130, 10, 931, 20))
        self.txtJsonPath.setReadOnly(False)
        self.txtJsonPath.setObjectName(_fromUtf8("txtJsonPath"))
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(10, 40, 69, 16))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.cmbTimeIllum.setCurrentIndex(8)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.calDateTimeIllum.setDisplayFormat(_translate("Form", "MMMM/d", None))
        self.cmbTimeIllum.setItemText(0, _translate("Form", "1", None))
        self.cmbTimeIllum.setItemText(1, _translate("Form", "2", None))
        self.cmbTimeIllum.setItemText(2, _translate("Form", "3", None))
        self.cmbTimeIllum.setItemText(3, _translate("Form", "4", None))
        self.cmbTimeIllum.setItemText(4, _translate("Form", "5", None))
        self.cmbTimeIllum.setItemText(5, _translate("Form", "6", None))
        self.cmbTimeIllum.setItemText(6, _translate("Form", "7", None))
        self.cmbTimeIllum.setItemText(7, _translate("Form", "8", None))
        self.cmbTimeIllum.setItemText(8, _translate("Form", "9", None))
        self.cmbTimeIllum.setItemText(9, _translate("Form", "10", None))
        self.cmbTimeIllum.setItemText(10, _translate("Form", "11", None))
        self.cmbTimeIllum.setItemText(11, _translate("Form", "12", None))
        self.cmbTimeIllum.setItemText(12, _translate("Form", "13", None))
        self.cmbTimeIllum.setItemText(13, _translate("Form", "14", None))
        self.cmbTimeIllum.setItemText(14, _translate("Form", "15", None))
        self.cmbTimeIllum.setItemText(15, _translate("Form", "16", None))
        self.cmbTimeIllum.setItemText(16, _translate("Form", "17", None))
        self.cmbTimeIllum.setItemText(17, _translate("Form", "18", None))
        self.cmbTimeIllum.setItemText(18, _translate("Form", "19", None))
        self.cmbTimeIllum.setItemText(19, _translate("Form", "20", None))
        self.cmbTimeIllum.setItemText(20, _translate("Form", "21", None))
        self.cmbTimeIllum.setItemText(21, _translate("Form", "22", None))
        self.cmbTimeIllum.setItemText(22, _translate("Form", "23", None))
        self.cmbTimeIllum.setItemText(23, _translate("Form", "24", None))
        self.lblDate.setText(_translate("Form", "Date", None))
        self.lblTime.setText(_translate("Form", "Time", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIlluminance), _translate("Form", "Illuminance", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabThermal), _translate("Form", "Thermal Plots", None))
        self.groupBox.setTitle(_translate("Form", "GroupBox", None))
        self.btnOpenJson.setText(_translate("Form", "Open Json File", None))

