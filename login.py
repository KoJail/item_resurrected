import sys

import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit

from loginW import Ui_LoginWindow

class LoginWindow(QWidget):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.password_lineEdit.setEchoMode(QLineEdit.Password)

        # 数据库相关操作
        conn = sqlite3.connect('user.db')
        cur = conn.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS admin (  
                        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                        admin_name TEXT NOT NULL,  
                        password TEXT NOT NULL
                    )  
                ''')
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (  
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,  
                        user_name TEXT NOT NULL,  
                        password TEXT NOT NULL,
                        address TEXT,
                        phone TEXT NOT NULL
                    )  
                ''')
        cur.execute("SELECT * from admin")
        if cur.fetchall() == []:
            cur.execute("INSERT INTO admin (admin_name,password) VALUES ('root','root')")
        conn.commit()
        conn.close()

        # 信号与槽
        self.ui.login_pushButton.clicked.connect((self.login))
        self.ui.register_pushButton.clicked.connect((self.register))

        self.show()

    def login(self):
        userName = self.ui.userName_lineEdit.text()
        password = self.ui.password_lineEdit.text()
        if userName == '' or password == '':
            QMessageBox.information(self, "消息对话框", "请填写用户名和密码", QMessageBox.Ok, QMessageBox.Ok)
        else:
            conn = sqlite3.connect('user.db')
            cur = conn.cursor()

            cur.execute("SELECT password FROM admin WHERE admin_name=?", (userName,))
            admin_pas = cur.fetchone()
            cur.execute("SELECT password FROM users WHERE user_name=?", (userName,))
            users_pas = cur.fetchone()

            if password == admin_pas[0]: # 管理员登录
                print('admin sucess')
            elif password == users_pas[0]: # 普通用户登录
                print('user sucess')
            else:
                QMessageBox.information(self, "消息对话框", "密码错误！", QMessageBox.Ok, QMessageBox.Ok)

            conn.close()

    def register(self):
        return


if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    w = LoginWindow()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())