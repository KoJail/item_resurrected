import sqlite3
import sys

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QAbstractItemView, QMenu, QAction, \
    QMessageBox

from login import LoginWindow, RegisterWindow
from dialog import InputDialog
from adminOperate import AdminWindow
from mainW import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 更多的UI设置
        # QTableWidget设置整行选中
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # 表格右击事件的相关设置
        self.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu) # 设置自定义上下文菜单策略

        # 添加一些表格，默认课程要求的3中类型
        conn = sqlite3.connect('item.db')
        cur = conn.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS 食物 (  
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,  
                        名称 TEXT NOT NULL,
                        保质期 TEXT NOT NULL,
                        数量 TEXT NOT NULL,
                        联系人 TEXT NOT NULL,
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
                        联系人 TEXT NOT NULL,
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
                        联系人 TEXT NOT NULL,
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
        self.ui.findAll_pushButton.clicked.connect(self.displayItem)
        self.ui.findKeyWord_pushButton.clicked.connect(self.findItem)
        # 表格右击的信号与槽
        self.ui.tableWidget.customContextMenuRequested.connect(self.showContextMenu)
        # 更多操作的信号与槽
        self.ui.quitAction.triggered.connect(self.back2Login)
        self.ui.adminAction.triggered.connect(self.adminOperate)
        self.ui.helpAction.triggered.connect(self.helpMe)

        self.refreshSort()

    # 添加物品相关
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

    # 关键字查找相关
    def findItem(self):
        keyWord = self.ui.findKeyWord_lineEdit.text()
        tableName = self.ui.sort_comboBox.currentText()
        # 数据库操作
        conn = sqlite3.connect('item.db')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tableName} WHERE 名称 LIKE ? OR 描述 LIKE ?", ('%' + keyWord + '%', '%' + keyWord + '%',))
        results = cur.fetchall()
        cur.execute(f"PRAGMA table_info({tableName})")  # 查询表的列信息
        infos = cur.fetchall()  # 获取所有列的信息
        columns = [info[1] for info in infos]
        conn.close()
        # 表格中显示
        self.showItem(results, columns)

    def showItem(self, rows, columns):
        # 删除原有信息
        while self.ui.tableWidget.rowCount() > 0:
            self.ui.tableWidget.removeRow(0)
        # 添加查到的信息
        # 设置表格的行数和列数
        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.setColumnCount(len(columns))
        # 设置表头（可选）
        self.ui.tableWidget.setHorizontalHeaderLabels(columns)
        # 将列表数据填充到表格中
        for row, data in enumerate(rows):
            for column, value in enumerate(data):
                self.ui.tableWidget.setItem(row, column, QTableWidgetItem(str(value)))
        for i in range(len(columns) - 1):
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(i,QHeaderView.ResizeToContents)  # 设置第i列要根据内容使用宽度

    # 表格右击删除相关
    def showContextMenu(self, pos):
        # 获取当前选中的行
        indexes = self.ui.tableWidget.selectedIndexes()
        if not indexes:
            return  # 如果没有选中的行，则不显示菜单
        self.tableRow = indexes[0].row()
        # 创建菜单
        menu = QMenu(self)
        # 创建删除菜单项
        deleteAction = QAction("删除", self)
        menu.addAction(deleteAction)
        # 连接删除菜单项的触发信号
        deleteAction.triggered.connect(self.deleteItem)
        # 弹出菜单
        adjusted_pos = pos + QPoint(70, 250) # 目前是根据UI手工调的，应该会有更好的办法
        menu.exec_(self.mapToGlobal(adjusted_pos))

    def deleteItem(self):
        # 弹出提示框，删除是不可逆操作，建议给出提示
        reply = QMessageBox.information(self, "消息对话框", "删除是不可逆操作，您确认删除吗？", QMessageBox.Yes | QMessageBox.Cancel,  QMessageBox.Yes)
        if reply == 16384:
            # 数据库操作，需要先查找再删除
            tableName = self.ui.sort_comboBox.currentText()
            rowID = self.ui.tableWidget.item(self.tableRow, 0).text()
            conn = sqlite3.connect('item.db')
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {tableName} WHERE id = ?", (rowID,))  # 数据库索引和表格索引不同
            conn.commit()
            conn.close()
            # 表格中显式删除
            self.displayItem()

    # 刷新
    # 显示所有同一类的条目，需要和findItem的用到的showItem函数区分
    def displayItem(self):
        tableName = self.ui.sort_comboBox.currentText()
        # 数据库操作
        conn = sqlite3.connect('item.db')
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({tableName})")  # 查询表的列信息
        infos = cur.fetchall()  # 获取所有列的信息
        columns = [info[1] for info in infos]
        cur.execute(f"SELECT * FROM {tableName}")
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        # 表格显示
        self.showItem(rows, columns)

    # 注意，理论上会同时刷新表格
    def refreshSort(self):
        # 刷新下拉框中的物品类型
        # 需要先解绑，否则会程序崩溃
        self.ui.sort_comboBox.disconnect()
        self.ui.sort_comboBox.clear()
        # 数据库操作
        conn = sqlite3.connect('item.db')
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cur.fetchall()
        for table in tables:
            self.ui.sort_comboBox.addItem(table[0])
        conn.close()
        # 重新绑上
        self.ui.sort_comboBox.currentIndexChanged.connect(self.displayItem)
        self.displayItem()

    # 更多操作
    def adminOperate(self):
        self.aw.show()
        # 建议直接关闭主界面
        self.close()

    def back2Login(self):
        print(1)

    def helpMe(self):
        print(3)

    # 这个地方有希望改，写的比较烂
    def set_references(self, aw):
        self.aw = aw

# #主程序
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
    aw = AdminWindow()
    mw.set_references(aw)
    aw.set_references(mw)
    mw.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())