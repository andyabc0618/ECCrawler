# -*- coding: UTF-8 -*-
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


from . import RutenSearch

class Ruten:
    def search( self, keyword):
        data = RutenSearch.search_keyword(keyword)
        if data!= None:
            attributes={'seller-name':'店家名稱','itemid':'商品ID','itemname':'商品名稱','priceCurrency':'幣別','price':'價格','url':'網址'}
            df = self.data_to_dataframe( data, attributes)
            return df
        else:
            return None



    def data_to_dataframe( self, data, attributes):
        dict_          = {}
        attributes_key = list(attributes.keys())
        for i in range( 0, len(data), 1):
            itemid = data[i]['Id']
            item_detail = RutenSearch.search_item(str(itemid))
            item_name = item_detail['name']
            if '三多' in item_name:
                price_currency = item_detail['offers']['priceCurrency']
                price          = item_detail['offers']['price']
                shop_name      = item_detail['offers']['seller']['name']

                for j in range( 0, len(attributes), 1):
                    key      = attributes_key[j]
                    key_name = attributes[key]
                    if key == 'seller-name':
                        value = shop_name
                    elif key == 'itemid':
                        value = itemid
                    elif key == 'itemname':
                        value = item_name
                    elif key == 'priceCurrency':
                        value = price_currency
                    elif key == 'price':
                        value = price
                    elif key == 'url':
                        value = 'https://goods.ruten.com.tw/item/show?'+itemid
                    
                    if key_name not in dict_:
                        dict_[key_name] = []
                    dict_[key_name].append(value)

        # Create DataFrame
        df = pd.DataFrame(dict_)

        return df


    def data_to_csv( self, csvname, df):
        df.to_csv('./露天拍賣/'+csvname+'.csv', encoding='utf-8-sig', index=False)


    def show_table( self, gui, df):
        keys  = list(df)
        table = gui.tableWidget
        table.setColumnCount(len(keys))
        table.setRowCount(len(df[keys[0]])+1)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setHorizontalHeaderLabels(keys)

        df_array = df.values
        for i in range( 0, df.shape[0], 1):
            for j in range( 0, df.shape[1], 1):
                item = QTableWidgetItem(str(df_array[i,j]))
                
                table.setItem( i, j, item)