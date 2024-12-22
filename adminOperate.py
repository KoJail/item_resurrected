import sqlite3

from PyQt5.QtWidgets import QWidget, QMessageBox

from adminW import Ui_adminWindow

class AdminWindow(QWidget):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_adminWindow()
        self.ui.setupUi(self)

        # 信号与槽
        self.ui.add_pushButton.clicked.connect(self.addTable)
        self.ui.delete_pushButton.clicked.connect(self.deleteTable)
        self.ui.back_pushButton.clicked.connect(self.back)

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
                    cur.execute(f"ALTER TABLE {tableName} INSERT COLUMN {attribute} TEXT BEFORE 联系人")
            QMessageBox.information(self, "消息对话框", "操作成功！", QMessageBox.Ok, QMessageBox.Ok)
            self.refreshSort()


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


    def back(self):
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

    def closeEvent(self, event):
        self.mw.show()
        event.accept()
        self.mw.refreshSort()

    def set_references(self, mw):
        self.mw = mw