import sys

from PyQt5.QtWidgets import QWidget, QApplication

from loginW import Ui_LoginWindow

class LoginWindow(QWidget):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        # 信号与槽
        self.ui.login_pushButton.clicked.connect((self.login()))
        self.ui.register_pushButton.clicked.connect((self.register()))

        self.show()

    def login(self):
        return

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