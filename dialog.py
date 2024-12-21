import sys

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QApplication

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建多个输入框
        self.lineEdit1 = QLineEdit(self)
        self.lineEdit2 = QLineEdit(self)
        self.lineEdit3 = QLineEdit(self)

        # 创建确定按钮
        okButton = QPushButton('OK', self)
        okButton.clicked.connect(self.on_ok)

        # 将输入框和按钮添加到布局中
        layout.addWidget(self.lineEdit1)
        layout.addWidget(self.lineEdit2)
        layout.addWidget(self.lineEdit3)
        layout.addWidget(okButton)

        # 设置布局
        self.setLayout(layout)
        self.setWindowTitle('Multi Input Dialog')

    def on_ok(self):
        # 获取输入框的内容
        input1 = self.lineEdit1.text()
        input2 = self.lineEdit2.text()
        input3 = self.lineEdit3.text()

        # 可以在这里处理输入的内容
        print(f"Input 1: {input1}, Input 2: {input2}, Input 3: {input3}")

        # 关闭对话框
        self.close()

# 仅用于内部测试
if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    appWindow = InputDialog()
    appWindow.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())