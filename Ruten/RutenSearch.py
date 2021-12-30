# -*- coding: UTF-8 -*-
import requests
import urllib
from bs4 import BeautifulSoup
import json
import csv

def keyword_search(keyword):
    headers = {
        'Referer': f'https://www.ruten.com.tw/find/v3/?q={urllib.parse.quote(keyword)}',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    }

    base_url = 'https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod'
    query    = f'q={keyword}&type=direct&offset=1&limit=80'
    url      = base_url + '?' + query
    resp     = requests.get(url, headers=headers)

    id_list = []
    if resp.status_code == requests.codes.ok:
        data = resp.json()
        rows = data['Rows']
        for i in range( 0, len(rows), 1):
            id_list.append(rows[i]['Id'])

    return id_list

def item_detail(itemid):
    headers = {
        'Referer': f'https://goods.ruten.com.tw/item/show?{itemid}',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    }

    base_url = 'https://goods.ruten.com.tw/item/show?'
    url      = base_url + itemid
    resp     = requests.get(url, headers=headers)
    if resp.status_code == requests.codes.ok:
        soup = BeautifulSoup(resp.text)

        data1 = json.loads(soup.findAll('script',{'type':'application/ld+json'})[0].text)
        
        
        item_name = data1['name']
        if '三多' in item_name:
            price_currency = data1['offers']['priceCurrency']
            price = data1['offers']['price']
            shop_name = data1['offers']['seller']['name']

            item_dict = {'店家名稱':shop_name, '商品ID':itemid, '商品名稱':item_name, '幣別':price_currency, '價格':price,'網址':url}
            

            return item_dict
        else:
            return None

def data_to_csv( keyword, item_list):
    item_key = list(item_list[0].keys())
    with open(keyword+'.csv','w+', newline='', encoding="utf_8_sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(item_key)

        for i in range( 0, len(item_list), 1):
            item_value = list(item_list[i].values())
            writer.writerow(item_value)

    