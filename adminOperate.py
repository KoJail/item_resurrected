# -*- coding: utf-8 -*- #

# ------------------------------------------------------------------
# File Name:        adminOperate.py
# Author:           KoJail
# Version:          ver0_1
# Created:          2024/12/22
# Description:      定义了管理员操作界面类，主要功能是增加物品类型或增加属性、删除物品类型、删除普通用户
# Function List:
# History:
#       <author>        <version>       <time>      <desc>
#       KoJail          ver0_1          2024/12/22  xxx
# ------------------------------------------------------------------
import sqlite3

from PyQt5.QtWidgets import QWidget, QMessageBox

from adminW import Ui_adminWindow

class AdminWindow(QWidget):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_adminWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('管理员操作界面')

        # 信号与槽
        self.ui.add_pushButton.clicked.connect(self.addTable)
        self.ui.delete_pushButton.clicked.connect(self.deleteTable)
        self.ui.back_pushButton.clicked.connect(self.back)
        # 账号相关信号与槽
        self.ui.findUser_pushButton.clicked.connect(self.findUser)
        self.ui.deleteUser_pushButton.clicked.connect(self.deleteUser)

        self.refreshSort()

    # 添加表格，如果表格存在则添加列？
    def addTable(self):
        tableName = self.ui.name_lineEdit.text()
        attributeText = self.ui.attribute_lineEdit.text()
        if tableName == '':
            QMessageBox.information(self, "消息对话框", "请输入种类名称", QMessageBox.Ok, QMessageBox.Ok)
        else:
            attributeArray = attributeText.split()
            # 数据库操作
            conn = sqlite3.connect('item.db')
            cur = conn.cursor()
            cur.execute(f'''
                        CREATE TABLE IF NOT EXISTS {tableName} (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,  
                            名称 TEXT NOT NULL,
                            联系人 TEXT NOT NULL,
                            地址 TEXT NOT NULL,
                            手机 TEXT NOT NULL,
                            邮箱 TEXT NOT NULL,
                            描述 TEXT NOT NULL
                        )
                    ''')
            # 检查列是否存在，如果不存在则添加列
            cur.execute(f"PRAGMA table_info({tableName})")
            infos = cur.fetchall()  # 获取所有列的信息
            columns = [info[1] for info in infos]
            for attribute in attributeArray:
                if attribute not in columns:
                    cur.execute(f"ALTER TABLE {tableName} ADD COLUMN {attribute} TEXT")
            QMessageBox.information(self, "消息对话框", "操作成功！", QMessageBox.Ok, QMessageBox.Ok)
            conn.commit()
            conn.close()
            # 清空文本框
            self.clearText()
            # 刷新下拉框
            self.refreshSort()

    # 删除表格
    def deleteTable(self):
        # 弹出提示框，删除是不可逆操作，建议给出提示
        reply = QMessageBox.information(self, "消息对话框", "删除是不可逆操作，您确认删除吗？",
                                        QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Yes)
        if reply == 16384:
            tableName = self.ui.sort_comboBox.currentText()
            # 数据库操作
            conn = sqlite3.connect('item.db')
            cur = conn.cursor()
            cur.execute(f"DROP TABLE IF EXISTS {tableName}")
            conn.commit()
            conn.close()
            QMessageBox.information(self, "消息对话框", "删除成功", QMessageBox.Ok, QMessageBox.Ok)
            self.refreshSort()

    # 以下两个函数为账号相关
    def findUser(self):
        self.ui.userName_comboBox.clear()
        conn = sqlite3.connect('user.db')
        cur = conn.cursor()
        cur.execute("SELECT user_name FROM users")
        users = cur.fetchall()
        for user in users:
            self.ui.userName_comboBox.addItem(user[0])
        conn.close()

    def deleteUser(self):
        userName = self.ui.userName_comboBox.currentText()
        if userName == '':
            QMessageBox.information(self, "消息对话框", "请先查找用户名", QMessageBox.Ok, QMessageBox.Ok)
        else:
            reply = QMessageBox.information(self, "消息对话框", "删除是不可逆操作，您确认删除吗？",
                                            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == 16384:
                # 以下是删除操作
                conn = sqlite3.connect('user.db')
                cur = conn.cursor()
                cur.execute("DELETE FROM users WHERE user_name = ?", (userName,))
                conn.commit()
                conn.close()
                self.findUser()

    def back(self):
        self.clearText()
        self.close()
        self.mw.show()
        self.mw.refreshSort()

    def refreshSort(self):
        # 刷新下拉框中的物品类型
        self.ui.sort_comboBox.clear()
        conn = sqlite3.connect('item.db')
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cur.fetchall()
        for table in tables:
            self.ui.sort_comboBox.addItem(table[0])
        conn.close()

    def clearText(self):
        # 清空文本框
        self.ui.name_lineEdit.clear()
        self.ui.attribute_lineEdit.clear()

    def closeEvent(self, event):
        self.mw.show()
        self.clearText()
        event.accept()
        self.mw.refreshSort()

    def setReferences(self, mw):
        self.mw = mw