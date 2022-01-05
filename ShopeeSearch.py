import requests
import urllib
import json

# TODO: 資料筆數太多，需要翻頁!

def search_keyword(keyword):
        # Need to add headers to get complete return data
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'X-Requested-With': 'pc', 
            'Referer': f'https://shopee.tw/search?keyword={urllib.parse.quote(keyword)}',
        }    

        base_url = 'https://shopee.tw/api/v2/search_items/'
        query    = f"by=relevancy&keyword={keyword}&limit=100&newest=0&order=desc&page_type=search&version=2"
        # query    = f"by=relevancy&keyword={keyword}&limit=10&newest=0&order=desc&page_type=search&version=2"

        url      = base_url + '?' + query
        session  = requests.Session()
        request  = session.get(url, headers=headers)

        if request.status_code == requests.codes.ok:
            data = request.json()
            data = data['items']
            return data
        else:
            return None


def search_shopaccount( shopid, itemid, item_name):
    # Need to add headers to get complete return data
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'X-Requested-With': 'pc', 
        'Referer': f'https://shopee.tw/{urllib.parse.quote(item_name)}-i.{shopid}.{itemid}',
    }    

    base_url = 'https://shopee.tw/api/v4/product/get_shop_info'
    query    = f"shopid={shopid}"
    url      = base_url + '?' + query
    session  = requests.Session()
    request  = session.get(url, headers=headers)
    request  = request.text
    request  = json.loads(request)

    data         = request['data']
    shop_account = data['account']['username']
    shop_name    = data['name']

    return shop_account, shop_name


def search_shop( shopid):
    # Need to add headers to get complete return data
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'X-Requested-With': 'pc', 
        'Referer': f'https://shopee.tw/shop/{shopid}/search?shopCollection',
    }    

    base_url = 'https://shopee.tw/api/v2/search_items/'
    query    = f"by=pop&match_id={shopid}&limit=100&order=desc&page_type=shop&version=2" 
    url      = base_url + '?' + query
    session  = requests.Session()
    request  = session.get(url, headers=headers)

    if request.status_code == requests.codes.ok:
        data = request.json()
        data = data['items']
        return data
    else:
        return None


def search_comment( shopid, itemid, itemname):
    itemname = itemname.encode('utf-8').decode('latin1')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'X-Requested-With': 'pc', 
        'Referer': f'https://shopee.tw/{urllib.parse.quote(itemname)}-i.{shopid}.{itemid}',
    }  


    base_url = 'https://shopee.tw/api/v2/item/get_ratings'
    query    = f'shopid={shopid}&itemid={itemid}'
    query_c  = '&filter=3&type=0&limit=59&offset=0&flag=1'
    url      = base_url + '?' + query + query_c 
    session  = requests.Session()
    request  = session.get(url, headers=headers)


    if request.status_code == requests.codes.ok:
        data = request.json()
        data = data['data']['ratings']
        return data
    else:
        return None

