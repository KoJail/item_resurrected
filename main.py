import os
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QAbstractItemView, QTableWidgetItem, QMessageBox

from window import Ui_MainWindow

import json

class AppWindow(QMainWindow):
    def __init__(self):
        # UI建立
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('resurrection of items')
        # 设置物品列表
        # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格头的伸缩模式
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 将表格变为禁止编辑
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格整行选中
        self.ui.tableWidget.horizontalHeader().resizeSection(0, 100)
        self.ui.tableWidget.horizontalHeader().resizeSection(1, 140)
        self.ui.tableWidget.horizontalHeader().resizeSection(2, 350)
        self.ui.tableWidget.horizontalHeader().resizeSection(3, 400)

        # 亿些常量
        self.dataPath = 'data.json'
        self.itemList = []

        # 信号与槽
        self.ui.add_pushButton.clicked.connect(self.addItem)
        self.ui.findAll_pushButton.clicked.connect(self.displayItem)
        self.ui.findName_pushButton.clicked.connect(self.findItem)
        self.ui.delele_pushButton.clicked.connect(self.delteItem)

        # 显示数据
        self.loadAllInfos()

        self.show()

    def loadAllInfos(self):
        # 检查是否存在json，若无则新建
        if not os.path.exists(self.dataPath):
            with open(self.dataPath, 'w') as file:
                json.dump([], file, indent=4)

        # 获取数据，更新列表
        with open(self.dataPath, 'r') as file:
            self.data = json.load(file)
            self.dataLen = len(self.data)
            if self.dataLen == 0:
                self.id = 0
            else:
                self.id = self.data[self.dataLen-1]['ID']
            self.updateData()

    def addItem(self):
        name = self.ui.addName_lineEdit.text()
        description = self.ui.addDesc_textEdit.toPlainText()
        information = self.ui.addInfo_textEdit.toPlainText()
        if name == '' or description == '' or information == '':
            reply = QMessageBox.information(self, "消息对话框", "请完善信息", QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.id += 1
            newDict = {'ID': self.id, 'name': name, 'desc': description, 'info': information}
            self.data.append(newDict)
            self.dataLen += 1
            self.updateData()
            self.ui.addName_lineEdit.clear()
            self.ui.addDesc_textEdit.clear()
            self.ui.addInfo_textEdit.clear()


    def delteItem(self):
        id = self.ui.delID_lineEdit.text()
        item = self.ui.delName_comboBox.currentText()
        # 无物品
        if item == '无物品':
            reply = QMessageBox.information(self, "消息对话框", "目前没有物品，请添加物品。", QMessageBox.Ok, QMessageBox.Ok)
        # 有物品且仅输入id
        elif item == '(请选择)':
            if id == '':
                reply = QMessageBox.information(self, "消息对话框", "请输入ID或选择有效的物品。", QMessageBox.Ok, QMessageBox.Ok)
            else:
                if id.isdigit():
                    # 删除指定ID
                    idInt = int(id)
                    for i in range(self.dataLen):
                        if self.data[i]['ID'] == idInt:
                            self.data.pop(i)
                            self.dataLen -= 1
                            self.updateData()
                            self.ui.delID_lineEdit.clear()
                            break
                else:
                    reply = QMessageBox.information(self, "消息对话框", "请输入合法ID或选择有效的物品。", QMessageBox.Ok, QMessageBox.Ok)
                    self.ui.delID_lineEdit.clear()
        # 有物品且仅选择物品
        else:
            if id != '':
                reply = QMessageBox.information(self, "消息对话框", "请不要同时输入ID与选择物品。", QMessageBox.Ok,  QMessageBox.Ok)
            else:
                # 删除所有指定物品，注意应该倒序删除
                reply = QMessageBox.information(self, "消息对话框", "该操作可能会删除多条信息，您确认吗？", QMessageBox.Yes | QMessageBox.Cancel,  QMessageBox.Yes)
                if reply == 16384:
                    for i in range(self.dataLen-1, -1, -1):
                        if self.data[i]['name'] == item:
                            self.data.pop(i)
                            self.dataLen -= 1
                    self.updateData()

    # 显示所有物品信息
    def displayItem(self):
        # 删除原有信息
        while self.ui.tableWidget.rowCount() > 0:
            self.ui.tableWidget.removeRow(0)
        # 添加所有信息
        for i in range(self.dataLen):
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(self.data[i]['ID'])))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(self.data[i]['name']))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(self.data[i]['desc']))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(self.data[i]['info']))

    def findItem(self):
        item = self.ui.findName_comboBox.currentText()
        if item == '无物品':
            reply = QMessageBox.information(self, "消息对话框", "目前没有物品，请添加物品。", QMessageBox.Ok, QMessageBox.Ok)
        elif item == '(请选择)':
            reply = QMessageBox.information(self, "消息对话框", "请选择有效的物品。", QMessageBox.Ok, QMessageBox.Ok)
        else:
            # 删除原有信息
            while self.ui.tableWidget.rowCount() > 0:
                self.ui.tableWidget.removeRow(0)
            # 添加查到的信息
            for i in range(self.dataLen):
                if self.data[i]['name'] == item:
                    row = self.ui.tableWidget.rowCount()
                    self.ui.tableWidget.insertRow(row)
                    self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(str(self.data[i]['ID'])))
                    self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(self.data[i]['name']))
                    self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(self.data[i]['desc']))
                    self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(self.data[i]['info']))

    # 用于在程序关闭时把剩下的记录存入文件中
    def saveAllInfos(self):
        with open(self.dataPath, 'w')as file:
            json.dump(self.data, file, indent=4)

    def closeEvent(self, event):
        self.saveAllInfos()
        event.accept()

    def updateData(self):
        self.displayItem()
        # 更新两个下拉列表
        self.ui.delName_comboBox.clear()
        self.ui.findName_comboBox.clear()
        if self.dataLen == 0:
            self.ui.delName_comboBox.addItem('无物品')
            self.ui.findName_comboBox.addItem('无物品')
        else:
            self.ui.delName_comboBox.addItem('(请选择)')
            self.ui.findName_comboBox.addItem('(请选择)')
            for i in range(self.dataLen):
                name = self.data[i]['name']
                if not(name in self.itemList):
                    self.itemList.append(name)
            for i in range(len(self.itemList)):
                self.ui.delName_comboBox.addItem(self.itemList[i])
                self.ui.findName_comboBox.addItem(self.itemList[i])

if __name__ == '__main__':
    # 只有直接运行这个脚本，才会往下执行
    # 别的脚本文件执行，不会调用这个条件句

    # 实例化，传参
    app = QApplication(sys.argv)

    # 创建对象
    appWindow = AppWindow()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
