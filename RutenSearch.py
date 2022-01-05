# -*- coding: UTF-8 -*-
import requests
import urllib
from bs4 import BeautifulSoup
import json
import csv

def search_keyword(keyword):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Referer': f'https://www.ruten.com.tw/find/v3/?q={urllib.parse.quote(keyword)}',
    }

    base_url = 'https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod'
    query    = f'q={keyword}&type=direct&offset=1&limit=80'
    url      = base_url + '?' + query
    resp     = requests.get(url, headers=headers)

    if resp.status_code == requests.codes.ok:
        data = resp.json()
        data = data['Rows']

        return data
    else:
        return None


def search_item(itemid):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Referer': f'https://goods.ruten.com.tw/item/show?{itemid}',
    }

    base_url = 'https://goods.ruten.com.tw/item/show?'
    url      = base_url + itemid
    resp     = requests.get(url, headers=headers)

    if resp.status_code == requests.codes.ok:
        soup = BeautifulSoup(resp.text)
        data = json.loads(soup.findAll('script',{'type':'application/ld+json'})[0].text)
    
        return data

    else:
        return None