from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import sys

import YahooSearch
import GUI_Yahoo


class MainWindow( QMainWindow, GUI_Yahoo.Ui_MainWindow):
    def __init__(self):
        # 初始化 QtWidgets.QMainWindow() & Ui_MainWindow()
        super().__init__() 
        self.setupUi(self) # Ui_MainWindow.setupUi()

        self.lineEdit_itemname.setText('三多葉黃素')

        ''' 設定 GUI 事件 '''
        self.pushButton_search.clicked.connect(self.search)

    def search(self):
        item_name = self.lineEdit_itemname.text() 
        if len(item_name) > 0:
            data = YahooSearch.keyword_search(item_name)
            if data != None:
                tables = YahooSearch.data_to_csv( item_name, data)
                self.show_table(tables)
                # QMessageBox.information(None, '搜尋完成', item_name+' 已完成搜尋!')

                # self.lineEdit_itemname.clear()

    def show_table(self, tables):
        # 初始化 Table 格式 (row)
        keys = list(tables[0].keys())
        self.tableWidget_commodity.setColumnCount(len(keys))
        self.tableWidget_commodity.setRowCount(len(tables)+1)
        # self.tableWidget_commodity.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget_commodity.setHorizontalHeaderLabels(keys)

        self.tableWidget_commodity.setColumnWidth(0,150)
        self.tableWidget_commodity.setColumnWidth(1,250)
        self.tableWidget_commodity.setColumnWidth(2,150)
        self.tableWidget_commodity.setColumnWidth(3,500)
        self.tableWidget_commodity.setColumnWidth(4,100)
        self.tableWidget_commodity.setColumnWidth(5,140)
        self.tableWidget_commodity.setColumnWidth(6,150)
        self.tableWidget_commodity.setColumnWidth(7,120)
        self.tableWidget_commodity.setColumnWidth(8,150)
        self.tableWidget_commodity.setColumnWidth(9,150)




        # 表格中填入資料
        for i in range( 0, len(tables), 1):
            for j in range( 0, len(keys), 1):
                key_ = keys[j]
                item = QTableWidgetItem()
                item.setText(str(tables[i][key_]))
                self.tableWidget_commodity.setItem( i, j, item)


if __name__ == '__main__':
    # sys.argv 是一組命令行參數，可用來進行腳本控制
    # 建立 GUI 物件 (可以不用 sys.argv ,可以用 [] 代替)
    app = QtWidgets.QApplication(sys.argv) 
    window = MainWindow() # 創建 GUI 物件
    window.show() # GUI視窗顯示
    app.exec_() # 確保 GUI視窗保持開啟狀態，否則會顯示一下就關閉


    # keyword = '三多葉黃素'
    # result = YahooSearch.keyword_search(keyword)

    # if result != None:
    #     table = YahooSearch.data_to_csv( keyword, result)