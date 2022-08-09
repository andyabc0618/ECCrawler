from datetime import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

import sys

from GUI import GUI
from Shopee import Shopee
from Ruten import Ruten
from Yahoo import Yahoo
import Function

class MainWindow( QMainWindow, GUI.Ui_MainWindow):
    def __init__(self):
        super().__init__() 
        self.setupUi(self) # Ui_MainWindow.setupUi()
        self.setComboBox()
        self.setMenu()

        # self.lineEdit_itemname.setText('三多葉黃素')

        self.pushButton_search.clicked.connect(self.search)


    def setComboBox(self):
        self.comboBox_website.addItems(['蝦皮','露天拍賣','Yahoo 奇摩拍賣'])
        self.comboBox_website.setCurrentIndex(0) # Default Display

    def setMenu(self):
        keyact   = self.menubar.addAction('關鍵字搜尋')
        shopeurl = self.menubar.addAction('蝦皮商品網址搜尋')
        keyact.triggered.connect(self.keyact_init)
        shopeurl.triggered.connect(self.shopeurl_init)

    def keyact_init(self):
        self.label.setText('產品名稱')
        self.comboBox_website.show()
        self.comboBox_website.clear()
        self.comboBox_website.addItems(['蝦皮','露天拍賣','Yahoo 奇摩拍賣'])
        self.comboBox_website.setCurrentIndex(0) # Default Display
        self.lineEdit_itemname.clear()
        self.tableWidget.setRowCount(0) 
        self.tableWidget.setColumnCount(0)

    def shopeurl_init(self):
        self.label.setText('商品網頁連結')
        self.comboBox_website.hide()
        self.lineEdit_itemname.clear()
        self.tableWidget.setRowCount(0) 
        self.tableWidget.setColumnCount(0)

    def closeEvent(self, event):
        # close all window
        sys.exit(0)
    
    def search(self):
        label_keyword = self.label.text()
        keyword = self.lineEdit_itemname.text() 
        if len(keyword) > 0 :
            if label_keyword == '產品名稱':
                website  = self.comboBox_website.currentText()
                website_choose = {
                    '蝦皮': Shopee.Shopee(),
                    '露天拍賣': Ruten.Ruten(),
                    'Yahoo 奇摩拍賣': Yahoo.Yahoo(),
                }
                web = website_choose.get( website, None)
                df  = web.search(keyword)
                Function.check_folder(website)
                web.data_to_csv( website+'_'+keyword, df)
                # Table 清空
                self.tableWidget.setRowCount(0) 
                web.show_table( self, df)
                if website == '蝦皮':
                    self.tableWidget.doubleClicked.connect(lambda:self.index( web, df))

            elif label_keyword == '商品網頁連結':
                Function.check_folder('蝦皮')
                shopee = Shopee.Shopee()
                shopee.url_search(keyword)
        

    def index( self, web, df):
        #selected cell index
        index = self.tableWidget.selectionModel().currentIndex()
        web.show_detail( self, index, df)
        

if __name__ == '__main__':
    # logging.basicConfig(filename='Error.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s [%(filename)s] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')
    # logger = logging.getLogger(__name__)
    # try:
        app = QtWidgets.QApplication(sys.argv) 
        window = MainWindow() 
        window.show()
        app.exec_() # GUI keep showing
    # except Exception as e:
    #     logger.exception(e)
    
        import time
        time.sleep(15)
