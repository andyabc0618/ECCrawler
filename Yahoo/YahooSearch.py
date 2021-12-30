# -*- coding: UTF-8 -*-
import requests
import urllib
from bs4 import BeautifulSoup
import json
import csv
import emoji
from datetime import datetime


def keyword_search(keyword):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    }

    base_url = 'https://tw.bid.yahoo.com/search/auction/product'
    query    = f'p={urllib.parse.quote(keyword)}'
    url      = base_url + '?' + query
    resp     = requests.get(url, headers=headers)

    if resp.status_code == requests.codes.ok:
        data = resp.text
        soup = BeautifulSoup(data, 'html.parser')
        # print(soup.prettify())
        
        # 取得關鍵字搜尋結果
        res = soup.find('div', id='isoredux-data')['data-state']
        res = json.loads(res)
        res = res['search']['ecsearch']['hits']

        return res
    else:
        return None


def data_to_csv( keyword, data):
    attributes_dict={'seller':'商家帳號','ec_storename':'商家名稱','ec_productid':'商品編號','ec_title':'商品名稱','ec_listprice':'商品價格','ec_buy_count':'已售出數量','ec_starttime':'商品上架時間','ec_location':'商家位置','ec_item_url':'商品連結','ec_seller_url':'商家連結'}

    attributes_key    = list(attributes_dict.keys())
    attributes_values = list(attributes_dict.values())
    with open(keyword+'.csv','w+', newline='', encoding="utf_8_sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(attributes_values)

        table = []
        for i in range( 0, len(data), 1):
            item = data[i]
            detail = []
            table_dict = {}
            bool_save = False
            for j in range( 0, len(attributes_key), 1):
                key = attributes_key[j]
                if key == 'ec_title':
                    str_ = item[key]
                    value = emoji.get_emoji_regexp().sub(u'',str_)
                    if '三多' in value:
                        bool_save = True
                elif key == 'ec_listprice':
                    value = str(int(float(item[key])))
                
                elif key == 'ec_starttime':
                    date_time = datetime.fromtimestamp(int(item[key]))
                    value = date_time.strftime("%m/%d/%Y")

                elif key == 'seller':
                    value = item['i13nModel'][key]
                else:
                    value = item[key]
                
                detail.append(value)
                table_dict[attributes_values[j]] = value
            
            if bool_save == True:
                writer.writerow(detail)
                table.append(table_dict)

        if len(table) > 0:
            return table
        else:
            return None