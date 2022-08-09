# -*- coding: UTF-8 -*-
import requests
import urllib
from bs4 import BeautifulSoup
import json

def search_keyword(keyword):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    }

    base_url = 'https://tw.bid.yahoo.com/search/auction/product'
    query    = f'p={urllib.parse.quote(keyword)}'
    url      = base_url + '?' + query
    resp     = requests.get(url, headers=headers)

    if resp.status_code == requests.codes.ok:
        data = resp.text
        data = BeautifulSoup(data, 'html.parser')
        data = data.find('div', id='isoredux-data')['data-state']
        data = json.loads(data)
        data = data['search']['ecsearch']['hits']

        return data
    else:
        return None