# -*- coding: UTF-8 -*-
import requests
import urllib
import json

from requests.models import requote_uri


def shop_account(shopid, itemid, item_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'X-Requested-With': 'pc', 
        'Referer': f'https://shopee.tw/{urllib.parse.quote(item_name)}-i.{shopid}.{itemid}',
    }    

    s        = requests.Session()
    base_url = 'https://shopee.tw/api/v4/product/get_shop_info'
    query    = f"shopid={shopid}"
    url      = base_url + '?' + query
    r        = s.get(url, headers=headers)
    r        = r.text
    r        = json.loads(r)

    data = r['data']
    user_account = data['account']['username']
    user_name = data['name']
    # print(str(user_account)+' = '+str(user_name))

    return user_account, user_name

# shopid = '1234987'
# itemid = '18853467'
# item_name = '【三多葉黃素100粒】三多金盞花萃取物(含葉黃素）複方軟膠囊100顆-雙11限量特價' 

# shop_account( shopid, itemid, item_name)