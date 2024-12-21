import sqlite3
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QApplication, QHBoxLayout, QLabel, QMessageBox


class InputDialog(QDialog):
    def __init__(self, columns, table, mw):
        super().__init__()

        self.columns = columns
        self.table = table
        self.mw = mw
        self.initUI()

    def initUI(self):
        # 创建垂直布局
        layout = QVBoxLayout()
        self.columnNum = len(self.columns) - 1
        self.hboxs = []
        self.lineEdits = []

        # 创建多个输入框
        for i in range(self.columnNum):
            hbox = QHBoxLayout()
            label = QLabel(self.columns[i+1])
            lineEdit = QLineEdit()
            hbox.addWidget(label)
            hbox.addWidget(lineEdit)
            self.hboxs.append(hbox)
            self.lineEdits.append(lineEdit)
        for hbox in self.hboxs:
            layout.addLayout(hbox)

        # 创建按钮
        self.okButton = QPushButton('确定', self)
        self.cancelButton = QPushButton('取消', self)
        self.okButton.clicked.connect(self.okey)
        self.cancelButton.clicked.connect(self.quit)
        layout.addWidget(self.okButton)
        layout.addWidget(self.cancelButton)

        self.setLayout(layout)
        self.setWindowTitle('添加物品')
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

    def okey(self):
        data = ()
        isEmpty = False
        for lineEdit in self.lineEdits:
            data += (lineEdit.text(),)
        for da in data:
            if da == '':
                isEmpty = True
                QMessageBox.information(self, "消息对话框", "请输入完整信息", QMessageBox.Ok, QMessageBox.Ok)
                break
        if isEmpty == False:
            # 数据库操作
            conn = sqlite3.connect('item.db')
            cur = conn.cursor()
            self.columns.pop(0)
            # 构建插入语句
            columns_str = ', '.join(self.columns)
            placeholders_str = ', '.join(['?'] * self.columnNum)
            insert_sql = f"INSERT INTO {self.table} ({columns_str}) VALUES ({placeholders_str})"
            # 执行插入操作
            cur.execute(insert_sql, data)
            conn.commit()
            conn.close()
            QMessageBox.information(self, "消息对话框", "操作成功！即将为您跳转回主界面", QMessageBox.Ok, QMessageBox.Ok)
            self.quit()
            self.mw.displayItem()

    def quit(self):
        super().reject()

    def closeEvent(self, event):
        super().closeEvent(event)
