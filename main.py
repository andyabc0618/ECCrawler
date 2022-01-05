from datetime import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

import sys
import logging

import GUI
import Shopee
import Ruten
import Yahoo
import Function

class MainWindow( QMainWindow, GUI.Ui_MainWindow):
    def __init__(self):
        super().__init__() 
        self.setupUi(self) # Ui_MainWindow.setupUi()
        self.setComboBox()

        self.lineEdit_itemname.setText('三多葉黃素')

        self.pushButton_search.clicked.connect(self.search)

    def setComboBox(self):
        self.comboBox_website.addItems(['蝦皮','露天拍賣','Yahoo 奇摩拍賣'])
        self.comboBox_website.setCurrentIndex(0) # Default Display
    
    def closeEvent(self, event):
        # close all window
        sys.exit(0)
    
    def search(self):
        keyword = self.lineEdit_itemname.text() 
        if len(keyword) > 0:
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
            self.tableWidget_commodity.setRowCount(0) 
            web.show_table( self, df)
            if website == '蝦皮':
                self.tableWidget_commodity.doubleClicked.connect(lambda:self.index( web, df))

    def index( self, web, df):
        #selected cell index
        index = self.tableWidget_commodity.selectionModel().currentIndex()
        web.show_detail( self, index, df)
        

if __name__ == '__main__':
    logging.basicConfig(filename='Error.log', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s [%(filename)s] %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')
    logger = logging.getLogger(__name__)
    try:
        # sys.argv: contains all the command-line arguments passed to the script
        app = QtWidgets.QApplication(sys.argv) 
        window = MainWindow() 
        window.show()
        app.exec_() # GUI keep showing
    except Exception as e:
        logger.exception(e)
    
    