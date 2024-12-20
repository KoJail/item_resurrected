import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from login import LoginWindow, RegisterWindow
from mainW import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('resurrection of items')

        # 添加一些表格，默认课程要求的3中类型
        conn = sqlite3.connect('item.db')
        cur = conn.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS foods (  
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,  
                        名称 TEXT NOT NULL,
                        保质期 TEXT NOT NULL,
                        数量 TEXT NOT NULL,
                        描述 TEXT NOT NULL,
                        地址 TEXT NOT NULL,
                        手机 TEXT NOT NULL,
                        邮箱 TEXT
                    )  
                ''')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS books (  
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,  
                        名称 TEXT NOT NULL,
                        作者 TEXT NOT NULL,
                        出版社 TEXT NOT NULL,
                        描述 TEXT NOT NULL,
                        地址 TEXT NOT NULL,
                        手机 TEXT NOT NULL,
                        邮箱 TEXT
                    )  
                ''')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS tools (  
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,  
                        名称 TEXT NOT NULL,
                        描述 TEXT NOT NULL,
                        地址 TEXT NOT NULL,
                        手机 TEXT NOT NULL,
                        邮箱 TEXT
                    )  
                ''')
        conn.commit()
        conn.close()

        # 信号与槽
        self.ui.add_pushButton.clicked.connect(self.addItem)

    def addItem(self):
        return

if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    lw = LoginWindow()
    rw = RegisterWindow()
    mw = MainWindow()
    lw.setReferences(rw, mw)
    rw.set_references(lw)
    lw.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())