# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginW.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(400, 300)
        self.register_pushButton = QtWidgets.QPushButton(LoginWindow)
        self.register_pushButton.setGeometry(QtCore.QRect(50, 200, 131, 28))
        self.register_pushButton.setObjectName("register_pushButton")
        self.login_pushButton = QtWidgets.QPushButton(LoginWindow)
        self.login_pushButton.setGeometry(QtCore.QRect(220, 200, 131, 28))
        self.login_pushButton.setObjectName("login_pushButton")
        self.userName_label = QtWidgets.QLabel(LoginWindow)
        self.userName_label.setGeometry(QtCore.QRect(50, 70, 72, 15))
        self.userName_label.setObjectName("userName_label")
        self.password_label = QtWidgets.QLabel(LoginWindow)
        self.password_label.setGeometry(QtCore.QRect(50, 130, 72, 15))
        self.password_label.setObjectName("password_label")
        self.userName_lineEdit = QtWidgets.QLineEdit(LoginWindow)
        self.userName_lineEdit.setGeometry(QtCore.QRect(120, 65, 231, 21))
        self.userName_lineEdit.setObjectName("userName_lineEdit")
        self.password_lineEdit = QtWidgets.QLineEdit(LoginWindow)
        self.password_lineEdit.setGeometry(QtCore.QRect(120, 125, 231, 21))
        self.password_lineEdit.setObjectName("password_lineEdit")

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Form"))
        self.register_pushButton.setText(_translate("LoginWindow", "注册"))
        self.login_pushButton.setText(_translate("LoginWindow", "登录"))
        self.userName_label.setText(_translate("LoginWindow", "用户名"))
        self.password_label.setText(_translate("LoginWindow", "密  码"))
