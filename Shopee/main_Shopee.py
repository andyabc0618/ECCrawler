from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap
import requests
from requests import status_codes
import sys
import requests


import ShopeeSearch
import ShopeeShop
import ShopeeComment
import ShopeeShopDetail

import GUI_shopee as ui
import GUI_shop
import GUI_comment

class MainWindow( QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        # 初始化 QtWidgets.QMainWindow() & Ui_MainWindow()
        super().__init__() 
        self.setupUi(self) # Ui_MainWindow.setupUi()

        self.lineEdit_itemname.setText('三多葉黃素')

        ''' 設定 GUI 事件 '''
        self.pushButton_search.clicked.connect(self.search)

    def closeEvent(self, event):
        sys.exit(0)

    def search(self):
        item_name = self.lineEdit_itemname.text() 
        if len(item_name) > 0:
            data = ShopeeSearch.commodity_search(item_name)
            if data != None:
                tables = ShopeeSearch.data_to_csv( item_name, data)
                self.show_table(tables)
                # QMessageBox.information(None, '搜尋完成', item_name+' 已完成搜尋!')

                # self.lineEdit_itemname.clear()

    def show_table(self, tables):
        # 初始化 Table 格式 (row)
        keys = list(tables[0].keys())
        self.tableWidget_commodity.setColumnCount(len(keys))
        self.tableWidget_commodity.setRowCount(len(tables)+1)
        self.tableWidget_commodity.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget_commodity.setHorizontalHeaderLabels(keys)

        # 表格中填入資料
        for i in range( 0, len(tables), 1):
            for j in range( 0, len(keys), 1):
                key_ = keys[j]
                item = QTableWidgetItem()
                item.setText(str(tables[i][key_]))
                self.tableWidget_commodity.setItem( i, j, item)
        
        # 表格點擊
        self.tables = tables
        self.tableWidget_commodity.doubleClicked.connect(self.show_detail)

    def show_detail(self, item):
        keys     = list(self.tables[0].keys())
        index_c  = item.column()
        index_r  = item.row()
        shopid   = str(self.tables[index_r][keys[0]])
        itemid   = str(self.tables[index_r][keys[3]])
        itemname = self.tables[index_r][keys[4]]
        shop_account, shop_name = ShopeeShopDetail.shop_account(shopid, itemid, itemname)
        if index_c == 0:
            try:
                shop_data = ShopeeShop.shop_search(shopid)
                shop_table = ShopeeShop.data_to_csv( shopid, shop_data)
                shop_keys = list(shop_table[0].keys())

                self.shop_window = ShopWindow()
                self.shop_window.show()
                self.shop_window.label.setText(shop_name)

                subtalbe = self.shop_window.tableWidget
                subtalbe.setColumnCount(len(shop_keys))
                subtalbe.setRowCount(len(shop_table)+1)
                subtalbe.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                subtalbe.setHorizontalHeaderLabels(shop_keys)

                # 表格中填入資料
                for i in range( 0, len(shop_table), 1):
                    for j in range( 0, len(shop_keys), 1):
                        key_ = shop_keys[j]
                        item = QTableWidgetItem()
                        item.setText(str(shop_table[i][key_]))
                        subtalbe.setItem( i, j, item)
            except Exception as e: 
                print(e)

        elif index_c == 3:
            try:
                comment_data = ShopeeComment.comment_get( shopid, itemid, itemname)
                comment_table, max_imgnum = ShopeeComment.data_to_csv( itemid, comment_data)
                
                if comment_table == None:
                    QMessageBox.information(None, '訊息', '此商品尚無任何評論!')
                else:
                    self.comment_window = CommentWindow()
                    self.comment_window.show()
                    self.comment_window.label_shopid.setText(shop_name)
                    self.comment_window.label_itemname.setText(itemname)

                    comment_keys = list(comment_table[0].keys())
                    subtalbe     = self.comment_window.tableWidget_commodity
                    subtalbe.setColumnCount(len(comment_keys)+max_imgnum-1)
                    subtalbe.setRowCount(len(comment_table)+1)
                    # subtalbe.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) # 自動調整
                    subtalbe.setColumnWidth(0,130)
                    subtalbe.setColumnWidth(1,120)
                    subtalbe.setColumnWidth(2,130)
                    subtalbe.setColumnWidth(3,130)
                    subtalbe.setColumnWidth(4,50)
                    subtalbe.setColumnWidth(5,600)

                    header_list = comment_keys.copy()
                    header_list.remove('圖片')
                    for i in range( 0, max_imgnum, 1):
                        header_list.append('圖片'+str(i+1))
                    subtalbe.setHorizontalHeaderLabels(header_list)

                    # 表格中填入資料
                    for i in range( 0, len(comment_table), 1):
                        subtalbe.setRowHeight(i, 400)
                        for j in range( 0, len(comment_keys), 1):
                            key_ = comment_keys[j]
                            if key_ == '圖片':
                                img_str = comment_table[i][key_]
                                img_list = img_str.split('-')
                                for k in range( 0, len(img_list), 1):
                                    img_url = 'https://cf.shopee.tw/file/'+img_list[k]
                                    r = requests.get( img_url, stream=True)
                                    assert r,status_codes == 200
                                    img_o = QImage()
                                    assert img_o.loadFromData(r.content)
                                    img_p = QPixmap.fromImage(img_o)
                                    img_p = img_p.scaled(350,350)
                                    w = QLabel()
                                    w.setPixmap(img_p)
                                    subtalbe.setColumnWidth(j+k,400)
                                    subtalbe.setCellWidget( i, j+k,w)

                            else:
                                item = QTableWidgetItem()
                                item.setText(str(comment_table[i][key_]))
                                subtalbe.setItem( i, j, item)

            except Exception as e: 
                print(e)


class ShopWindow( QMainWindow, GUI_shop.Ui_SubWindow):
    def __init__(self):
        # 初始化 QtWidgets.QMainWindow() & Ui_SubWindow()
        super().__init__() 
        self.setupUi(self) # Ui_SubWindow.setupUi()


class CommentWindow( QMainWindow, GUI_comment.Ui_SubWindow):
    def __init__(self):
        # 初始化 QtWidgets.QMainWindow() & Ui_SubWindow()
        super().__init__() 
        self.setupUi(self) # Ui_SubWindow.setupUi()



if __name__ == '__main__':
    # sys.argv 是一組命令行參數，可用來進行腳本控制
    # 建立 GUI 物件 (可以不用 sys.argv ,可以用 [] 代替)
    app = QtWidgets.QApplication(sys.argv) 
    window = MainWindow() # 創建 GUI 物件
    window.show() # GUI視窗顯示
    app.exec_() # 確保 GUI視窗保持開啟狀態，否則會顯示一下就關閉
    