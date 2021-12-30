# -*- coding: UTF-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import csv
import sys

import RutenSearch
import GUI_Ruten


class MainWindow( QMainWindow, GUI_Ruten.Ui_MainWindow):
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
            id_list = RutenSearch.keyword_search(item_name)
            
            item_list = []
            for i in range( 0, len(id_list), 1):
                itemid = str(id_list[i])
                item_dict = RutenSearch.item_detail(itemid)
                if item_dict != None:
                    item_list.append(item_dict)
                # print('ItemID: '+str(itemid)+' ~ ItemDict: '+str(item_dict))
            
            RutenSearch.data_to_csv( item_name, item_list)

            # 初始化 Table 格式 (row)
            keys = list(item_list[0].keys())
            self.tableWidget_commodity.setColumnCount(len(keys))
            self.tableWidget_commodity.setRowCount(len(item_list)+1)
            # self.tableWidget_commodity.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.tableWidget_commodity.setHorizontalHeaderLabels(keys)

            self.tableWidget_commodity.setColumnWidth(0,300)
            self.tableWidget_commodity.setColumnWidth(1,200)
            self.tableWidget_commodity.setColumnWidth(2,800)
            self.tableWidget_commodity.setColumnWidth(3,60)
            self.tableWidget_commodity.setColumnWidth(4,80)
            self.tableWidget_commodity.setColumnWidth(5,400)

            # 表格中填入資料
            for i in range( 0, len(item_list), 1):
                for j in range( 0, len(keys), 1):
                    key_ = keys[j]
                    item = QTableWidgetItem()
                    item.setText(str(item_list[i][key_]))
                    self.tableWidget_commodity.setItem( i, j, item)



if __name__ == '__main__':
    # sys.argv 是一組命令行參數，可用來進行腳本控制
    # 建立 GUI 物件 (可以不用 sys.argv ,可以用 [] 代替)
    app = QtWidgets.QApplication(sys.argv) 
    window = MainWindow() # 創建 GUI 物件
    window.show() # GUI視窗顯示
    app.exec_() # 確保 GUI視窗保持開啟狀態，否則會顯示一下就關閉
    
