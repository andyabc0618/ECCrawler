# -*- coding: UTF-8 -*-
import requests
from requests import status_codes
import pandas as pd
import emoji
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QImage, QPixmap, QColor

import ShopeeSearch
import GUI_Shop
import GUI_Comment
import Function

class Shopee:
    def search(self, keyword):
        data = ShopeeSearch.search_keyword(keyword)
        if data != None:
            # attributes={'shopid':'賣家ID', 'itemid':'商品ID', 'name':'商品名稱', 'shop_location':'賣場位置', 'ctime':'上架時間', 'historical_sold':'已售出數量', 'stock':'庫存', 'liked_count':'喜歡數', 'view_count':'瀏覽數', 'currency':'貨幣', 'price_before_discount':'原價', 'discount':'折扣', 'price':'實際價格', 'price_min_before_discount':'	折扣前價格範圍(最低)', 'price_max_before_discount':'折扣前價格範圍(最高)', 'is_official_shop': '是否為官方商城?', }
            attributes={'shopid':'賣家ID','shopacc':'賣家帳號','shopname':'賣家名稱', 'itemid':'商品ID', 'name':'商品名稱', 'shop_location':'賣場位置', 'ctime':'上架時間', 'historical_sold':'已售出數量', 'stock':'庫存', 'liked_count':'喜歡數', 'view_count':'瀏覽數', 'price':'實際價格','url':'網址'}
            df = self.data_to_dataframe( data, attributes)
            return df
        else:
            return None


    def data_to_dataframe( self, data, attributes):
        dict_          = {}
        attributes_key = list(attributes.keys())
        for i in range( 0, len(data), 1):
            item      = data[i]
            if '三多' in item['name']:
                for j in range( 0, len(attributes_key), 1):
                    key = attributes_key[j]
                    key_name = attributes[key]
                    if 'shopacc' in key or 'shopname' in key:
                        shopid    = item['shopid']
                        itemid    = item['itemid']
                        item_name = item['name']
                        shop_account, shop_name = ShopeeSearch.search_shopaccount( shopid, itemid, item_name)

                    if key == 'name':
                        str_  = item[key]
                        value = emoji.get_emoji_regexp().sub(u'', str_)
                    elif key == 'shopacc':
                        value = shop_account
                    elif key == 'shopname':
                        value = shop_name
                    elif key == 'ctime':
                        date_time = datetime.fromtimestamp(item[key])
                        value = date_time.strftime("%m/%d/%Y")
                    elif key == 'price_before_discount' and item[key] > 0:
                        value = int(item[key]/100000)
                    elif key == 'price' and item[key] > 0:
                        value = int(item[key]/100000)
                    elif key == 'price_min_before_discount' and item[key] > 0:
                        value = int(item[key]/100000)
                    elif key == 'price_max_before_discount' and item[key] > 0:
                        value = int(item[key]/100000)
                    elif key == 'url':
                        value = 'https://shopee.tw/product/'+str(item['shopid'])+'/'+str(item['itemid'])
                    else:
                        value = item[key]
                    
                    if key_name not in dict_:
                        dict_[key_name] = []
                    dict_[key_name].append(value)

        # Create DataFrame
        df = pd.DataFrame(dict_)


        return df                


    def data_to_dataframe_comment( self, data, attributes):
        # check max image num
        max_imgnum = 0
        for i in range( 0, len(data), 1):
            num = len(data[i]['images'])
            max_imgnum = max( num, max_imgnum)
        for i in range( 0, max_imgnum, 1):
            attributes['image'+str(i)] = '圖片'+str(i)
        dict_ = {}
        attributes_key = list(attributes.keys())
        for i in range( 0, len(data), 1):
            item = data[i]
            for j in range( 0, len(attributes_key), 1):
                key = attributes_key[j]
                key_name = attributes[key]
                if key == 'ctime':
                    date_time = datetime.fromtimestamp(item[key])
                    value     = date_time.strftime("%m/%d/%Y")
                elif 'image' in key:
                    img_range = len(item['images'])
                    img_index = int(key.replace('image',''))
                    if img_index >= img_range:
                        value = ''
                    else:
                        value = item['images'][img_index]
                else:
                    value = item[key]

                if key_name not in dict_:
                    dict_[key_name] = []
                dict_[key_name].append(value)

        # Create DataFrame
        df = pd.DataFrame(dict_)

        return df


    def data_to_csv( self, csvname, df):
        # df_key = list(df)
        # df_array = df.values
        # with open(csvname+'.csv','w+', newline='', encoding="utf_8_sig") as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(df_key)
        #     for i in range( 0, len(df), 1):
        #        detail = []
        #        for j in range( 0, len(df_key), 1):
        #             detail.append(df_array[i][j]) 
        #     writer.writerow(detail)
        csvname = Function.check_csvname(csvname)
        df.to_csv('./蝦皮/'+csvname+'.csv', encoding='utf-8-sig', index=False)


    def show_table( self, gui, df):
        keys  = list(df)
        table = gui.tableWidget_commodity
        table.setColumnCount(len(keys))
        table.setRowCount(len(df[keys[0]])+1)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setHorizontalHeaderLabels(keys)

        df_array = df.values
        for i in range( 0, df.shape[0], 1):
            for j in range( 0, df.shape[1], 1):
                item = QTableWidgetItem(str(df_array[i,j]))
                if keys[j] == '賣家ID' or keys[j] == '商品ID':
                    item.setForeground(QBrush(QColor(0,0,255)))
                
                table.setItem( i, j, item)

    
    def show_detail( self, gui, index, df):
        keys     = list(df)
        column   = index.column()
        row      = index.row()
        shopid   = str(df['賣家ID'][row])
        shopname = str(df['賣家名稱'][row])
        itemid   = str(df['商品ID'][row])
        itemname = str(df['商品名稱'][row])

        if keys[column] == '賣家ID':
            self.show_shop( gui, shopid, shopname)

        elif keys[column] == '商品ID':
            self.show_comment( gui, shopid, shopname, itemid, itemname)

    
    def show_shop( self, gui, shopid, shopname):
        data = ShopeeSearch.search_shop(shopid)
        attributes = {'itemid':'商品ID', 'name':'商品名稱', 'shop_location':'賣場位置', 'ctime':'上架時間', 'historical_sold':'已售出數量', 'stock':'庫存', 'liked_count':'喜歡數', 'view_count':'瀏覽數', 'price':'實際價格'}
        df = self.data_to_dataframe( data, attributes)
        
        if df.empty:
            QMessageBox.information(None, '訊息', '此店家過多商品!(功能尚在開發中)')
        else:
            keys = list(df)
            self.data_to_csv( '蝦皮'+'_'+shopname, df)

            gui.shop_window = ShopWindow()
            gui.shop_window.show()
            gui.shop_window.label.setText(shopname)
            
            gui.shop_window.tableWidget.setColumnCount(len(keys))
            gui.shop_window.tableWidget.setRowCount(len(df[keys[0]])+1)

            gui.shop_window.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            gui.shop_window.tableWidget.setHorizontalHeaderLabels(keys)

            df_array = df.values
            for i in range( 0, df.shape[0], 1):
                for j in range( 0, df.shape[1], 1):
                    gui.shop_window.tableWidget.setItem( i, j, QTableWidgetItem(str(df_array[i,j])))
        

    def show_comment( self, gui, shopid, shopname, itemid, itemname):
        data = ShopeeSearch.search_comment( shopid, itemid, itemname)
        if data == None:
            QMessageBox.information(None, '訊息', '此商品尚無任何評論!')
        else:
            attributes = {'userid':'買家ID','author_username':'買家名稱','author_shopid':'買家賣場','ctime':'評論時間','rating_star':'評分','comment':'評論'}
            df = self.data_to_dataframe_comment( data, attributes)
            if df.empty:
                QMessageBox.information(None, '訊息', '此商品尚無任何圖片評論!')
            else:
                keys = list(df)
                self.data_to_csv( shopname+'_'+itemname, df)

                gui.comment_window = CommentWindow()
                gui.comment_window.show()
                gui.comment_window.label_shopid.setText(shopname)
                gui.comment_window.label_itemname.setText(itemname)

                gui.comment_window.tableWidget.setColumnCount(len(keys))
                gui.comment_window.tableWidget.setRowCount(len(df[keys[0]])+1)
                gui.comment_window.tableWidget.setHorizontalHeaderLabels(keys)


                gui.comment_window.tableWidget.setColumnWidth(0,130)
                gui.comment_window.tableWidget.setColumnWidth(1,120)
                gui.comment_window.tableWidget.setColumnWidth(2,130)
                gui.comment_window.tableWidget.setColumnWidth(3,130)
                gui.comment_window.tableWidget.setColumnWidth(4,50)
                gui.comment_window.tableWidget.setColumnWidth(5,600)
                for i in range( 6, len(keys), 1):
                    gui.comment_window.tableWidget.setColumnWidth(i,400)
                
                # TODO: 要加入圖片的例外狀況，因為要發請求，取得圖片! 
                df_key = list(df)
                df_array = df.values
                for i in range( 0, df.shape[0], 1):
                    gui.comment_window.tableWidget.setRowHeight(i, 400)
                    for j in range( 0, df.shape[1], 1):
                        key_ = df_key[j]
                        if '圖片' in key_ and df_array[i,j] != '':
                            img_url = 'https://cf.shopee.tw/file/'+df_array[i,j]
                            request = requests.get( img_url, stream=True)
                            assert request,status_codes == 200
                            img_o = QImage()
                            assert img_o.loadFromData(request.content)
                            img_p = QPixmap.fromImage(img_o)
                            img_p = img_p.scaled(350,350)
                            w = QLabel()
                            w.setPixmap(img_p)
                            gui.comment_window.tableWidget.setCellWidget( i, j, w)
                        else:
                            gui.comment_window.tableWidget.setItem( i, j, QTableWidgetItem(str(df_array[i,j])))



class ShopWindow( QMainWindow, GUI_Shop.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class CommentWindow( QMainWindow, GUI_Comment.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)