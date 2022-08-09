# -*- coding: UTF-8 -*-
import emoji
from datetime import datetime
import pandas as pd
from PyQt5.QtWidgets import *

from . import YahooSearch

class Yahoo:
    def search( self, keyword):
        data = YahooSearch.search_keyword(keyword)
        if data != None:
            attributes = {'seller':'商家帳號','ec_storename':'商家名稱','ec_productid':'商品編號','ec_title':'商品名稱','ec_listprice':'商品價格','ec_buy_count':'已售出數量','ec_starttime':'商品上架時間','ec_location':'商家位置','ec_item_url':'商品連結','ec_seller_url':'商家連結'}
            df = self.data_to_dataframe( data, attributes)
            return df
        else:
            return None


    def data_to_dataframe( self, data, attributes):
        dict_ = {}
        attributes_key = list(attributes.keys())
        for i in range( 0, len(data), 1):
            item = data[i]
            if '三多' in item['ec_title']:
                for j in range( 0, len(attributes_key), 1):
                    key = attributes_key[j]
                    key_name = attributes[key]
                    
                    if key == 'ec_title':
                        str_ = item[key]
                        value = emoji.get_emoji_regexp().sub(u'',str_)
                    elif key == 'ec_listprice':
                        value = str(int(float(item[key])))
                    elif key == 'ec_starttime':
                        date_time = datetime.fromtimestamp(int(item[key]))
                        value = date_time.strftime("%m/%d/%Y")
                    elif key == 'seller':
                        value = item['i13nModel'][key]
                    else:
                        value = item[key]
                    
                    if key_name not in dict_:
                        dict_[key_name] = []
                    dict_[key_name].append(value)

        # Create DataFrame
        df = pd.DataFrame(dict_)

        return df


    def data_to_csv( self, csvname, df):
        df.to_csv('./Yahoo 奇摩拍賣/'+csvname+'.csv', encoding='utf-8-sig', index=False)


    def show_table( self, gui, df):
        keys  = list(df)
        table = gui.tableWidget
        table.setColumnCount(len(keys))
        table.setRowCount(len(df[keys[0]])+1)
        # table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setHorizontalHeaderLabels(keys)
        table.setColumnWidth(0,150)
        table.setColumnWidth(1,250)
        table.setColumnWidth(2,150)
        table.setColumnWidth(3,500)
        table.setColumnWidth(4,100)
        table.setColumnWidth(5,140)
        table.setColumnWidth(6,150)
        table.setColumnWidth(7,120)
        table.setColumnWidth(8,150)
        table.setColumnWidth(9,150)


        df_array = df.values
        for i in range( 0, df.shape[0], 1):
            for j in range( 0, df.shape[1], 1):
                item = QTableWidgetItem(str(df_array[i,j]))
                
                table.setItem( i, j, item)