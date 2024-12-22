import sys

import sqlite3
from PyQt5.QtWidgets import QWidget, QMessageBox

from loginW import Ui_LoginWindow
from registerW import Ui_RegisterWindow

class LoginWindow(QWidget):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('login_page')

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
        self.ui.login_pushButton.clicked.connect(self.login)
        self.ui.register_pushButton.clicked.connect(self.register)

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

            if admin_pas is None:
                if users_pas is None:
                    QMessageBox.information(self, "消息对话框", "用户名或密码错误！", QMessageBox.Ok, QMessageBox.Ok)
                elif password == users_pas[0]:  # 普通用户登录
                    self.goToMain(False)
                else:
                    QMessageBox.information(self, "消息对话框", "用户名或密码错误！", QMessageBox.Ok, QMessageBox.Ok)
            elif password == admin_pas[0]: # 管理员登录
                self.goToMain(True)
            else:
                QMessageBox.information(self, "消息对话框", "用户名或密码错误！", QMessageBox.Ok, QMessageBox.Ok)

            conn.close()

    def clearText(self):
        self.ui.userName_lineEdit.clear()
        self.ui.password_lineEdit.clear()

    def register(self):
        self.rw.show()
        self.close()

    def goToMain(self, isAdmin):
        self.mw.ISAdmin(isAdmin)
        self.mw.show()
        self.close()

    def setReferences(self, rw, mw):
        self.rw = rw
        self.mw = mw

class RegisterWindow(QWidget):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('register_page')

        # 信号与槽
        self.ui.confirm_pushButton.clicked.connect(self.register)
        self.ui.cancel_pushButton.clicked.connect(self.quit)

    def register(self):
        registerdone = False
        name = self.ui.userName_lineEdit.text()
        password = self.ui.password_lineEdit.text()
        repassword = self.ui.repassword_lineEdit.text()
        address = self.ui.adress_lineEdit.text()
        phone = self.ui.phone_lineEdit.text()
        aduserName = self.ui.aduserName_lineEdit.text()
        adpassword = self.ui.adpassword_lineEdit.text()

        if name == '' or password == '' or repassword == '' or phone == '':
            QMessageBox.information(self, "消息对话框", "请输入完整的信息", QMessageBox.Ok, QMessageBox.Ok)
        elif adpassword == '' or aduserName == '':
            QMessageBox.information(self, "消息对话框", "请输入管理员用户名与密码", QMessageBox.Ok, QMessageBox.Ok)
        elif password != repassword:
            QMessageBox.information(self, "消息对话框", "两次输入密码不一致！", QMessageBox.Ok, QMessageBox.Ok)
        else: # 判断是否可以成功注册
            conn = sqlite3.connect('user.db')
            cur = conn.cursor()
            cur.execute("SELECT password FROM admin WHERE admin_name=?", (aduserName,))
            admin_pas = cur.fetchone()
            if admin_pas is None or admin_pas[0] != adpassword:
                QMessageBox.information(self, "消息对话框", "管理员账号或密码错误", QMessageBox.Ok, QMessageBox.Ok)
            else:
                cur.execute("SELECT password FROM users WHERE user_name=?", (name,))
                user_pas = cur.fetchone()
                cur.execute("SELECT password FROM admin WHERE admin_name=?", (name,))
                ad_pas = cur.fetchone()
                if user_pas is not None or ad_pas is not None:
                    QMessageBox.information(self, "消息对话框", "用户名重复！", QMessageBox.Ok, QMessageBox.Ok)
                else:
                    cur.execute("INSERT INTO users (user_name,password,address,phone) VALUES (?,?,?,?)", (name,password,address,phone))
                    registerdone = True
                    QMessageBox.information(self, "消息对话框", "注册成功，即将为您跳转至登陆界面", QMessageBox.Ok, QMessageBox.Ok)
            conn.commit()
            conn.close()

        if registerdone == True:
            self.quit()

    def quit(self):
        self.lw.clearText()
        self.lw.show()
        self.close()

    def closeEvent(self, event):
        self.lw.clearText()
        self.lw.show()
        event.accept()

    def setReferences(self, lw):
        self.lw = lw

# if __name__ == '__main__':
#     # 只有直接运行这个脚本，才会往下执行
#     # 别的脚本文件执行，不会调用这个条件句
#
#     # 实例化，传参
#     app = QApplication(sys.argv)
#
#     # 创建对象，这个地方一定是可以改进的，不然会导致所有窗体都在内存中
#     lw = LoginWindow()
#     rw = RegisterWindow()
#     lw.show()
#
#     # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
#     sys.exit(app.exec_())