import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView

from login import LoginWindow, RegisterWindow
from dialog import InputDialog
from mainW import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # QTableWidget设置整行选中
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # 添加一些表格，默认课程要求的3中类型
        conn = sqlite3.connect('item.db')
        cur = conn.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS 食物 (  
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,  
                        名称 TEXT NOT NULL,
                        保质期 TEXT NOT NULL,
                        数量 TEXT NOT NULL,
                        地址 TEXT NOT NULL,
                        手机 TEXT NOT NULL,
                        邮箱 TEXT NOT NULL,
                        描述 TEXT NOT NULL
                    )  
                ''')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS 书籍 (  
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,  
                        名称 TEXT NOT NULL,
                        作者 TEXT NOT NULL,
                        出版社 TEXT NOT NULL,
                        地址 TEXT NOT NULL,
                        手机 TEXT NOT NULL,
                        邮箱 TEXT NOT NULL,
                        描述 TEXT NOT NULL
                    )  
                ''')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS 工具 (  
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,  
                        名称 TEXT NOT NULL,
                        地址 TEXT NOT NULL,
                        手机 TEXT NOT NULL,
                        邮箱 TEXT NOT NULL,
                        描述 TEXT NOT NULL
                    )  
                ''')
        conn.commit()
        conn.close()

        # 信号与槽
        self.ui.add_pushButton.clicked.connect(self.addItem)
        self.ui.sort_comboBox.currentIndexChanged.connect(self.displayItem)

        self.refreshSort()

    def addItem(self):
        tableName = self.ui.sort_comboBox.currentText()
        # 数据库操作
        conn = sqlite3.connect('item.db')
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({tableName})") # 查询表的列信息
        infos = cur.fetchall() # 获取所有列的信息
        columns = [info[1] for info in infos]
        conn.commit()
        conn.close()
        # 弹出多信息输入窗口
        self.ipw = InputDialog(columns, tableName, self)
        self.ipw.show()

    # 刷新
    def displayItem(self):
        # 删除原有信息
        while self.ui.tableWidget.rowCount() > 0:
            self.ui.tableWidget.removeRow(0)
        # 数据库操作
        tableName = self.ui.sort_comboBox.currentText()
        conn = sqlite3.connect('item.db')
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({tableName})")  # 查询表的列信息
        infos = cur.fetchall()  # 获取所有列的信息
        columns = [info[1] for info in infos]
        cur.execute(f"SELECT * FROM {tableName}")
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        # 添加所有信息
        # 设置表格的行数和列数
        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.setColumnCount(len(columns))
        # 设置表头（可选）
        self.ui.tableWidget.setHorizontalHeaderLabels(columns)
        # 将列表数据填充到表格中
        for row, data in enumerate(rows):
            for column, value in enumerate(data):
                self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(value)))
        for i in range(len(columns)-1):
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)  # 设置第i列要根据内容使用宽度


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

# if __name__ == '__main__':
#     # 只有直接运行这个脚本，才会往下执行
#     # 别的脚本文件执行，不会调用这个条件句
#
#     # 实例化，传参
#     app = QApplication(sys.argv)
#
#     # 创建对象
#     lw = LoginWindow()
#     rw = RegisterWindow()
#     mw = MainWindow()
#     lw.setReferences(rw, mw)
#     rw.set_references(lw)
#     lw.show()
#
#     # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
#     sys.exit(app.exec_())

# 单独测试主窗口
if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    mw = MainWindow()
    mw.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())