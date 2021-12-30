# -*- coding: UTF-8 -*-
import requests
import csv
from datetime import datetime
import emoji

import ShopeeShopDetail


def shop_search(shopid):
    # 需要加入 Headers 才能得到完整回傳資料
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'X-Requested-With': 'pc', 
        'Referer': f'https://shopee.tw/shop/{shopid}/search?shopCollection',
    }    

    s   = requests.Session()
    base_url = 'https://shopee.tw/api/v2/search_items/'
    query    = f"by=pop&match_id={shopid}&limit=100&order=desc&page_type=shop&version=2" 
    url      = base_url + '?' + query
    r        = s.get(url, headers=headers)

    if r.status_code == requests.codes.ok:
        data = r.json()
        # 產生 Json 檔案
        # with open('shop.json', 'w', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)
        return data
    else:
        return None

def data_to_csv( keyword, data):
    # attributes_dict={'shopid':'賣家ID', 'itemid':'商品ID', 'name':'商品名稱', 'shop_location':'賣場位置', 'ctime':'上架時間', 'historical_sold':'已售出數量', 'stock':'庫存', 'liked_count':'喜歡數', 'view_count':'瀏覽數', 'currency':'貨幣', 'price_before_discount':'原價', 'discount':'折扣', 'price':'實際價格', 'price_min_before_discount':'	折扣前價格範圍(最低)', 'price_max_before_discount':'折扣前價格範圍(最高)', 'is_official_shop': '是否為官方商城?', }
    attributes_dict={'itemid':'商品ID', 'name':'商品名稱', 'shop_location':'賣場位置', 'ctime':'上架時間', 'historical_sold':'已售出數量', 'stock':'庫存', 'liked_count':'喜歡數', 'view_count':'瀏覽數', 'price':'實際價格'}

    attributes_key    = list(attributes_dict.keys())
    attributes_values = list(attributes_dict.values())
    attributes_values.append('網址')
    data_item = data['items']

    with open(keyword+'.csv','w+', newline='', encoding="utf_8_sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(attributes_values)
        
        table = []
        for i in range( 0, len(data_item), 1):
            item       = data_item[i]
            detail     = []
            table_dict = {}
            bool_save  = False
            for j in range( 0, len(attributes_key), 1):
                key = attributes_key[j]
                if key == 'name':
                    str_ = item[key]
                    value = emoji.get_emoji_regexp().sub(u'', str_)
                    if '三多' in value:
                        bool_save = True

                elif key == 'shopacc':
                    shopid = item[attributes_key[attributes_key.index('shopid')]]
                    itemid = item[attributes_key[attributes_key.index('itemid')]]
                    item_name = item[attributes_key[attributes_key.index('name')]]

                    shop_account, shop_name = ShopeeShopDetail.shop_account(shopid,itemid,item_name)

                    detail.append(shop_account)
                    detail.append(shop_name)
                    table_dict['shopacc'] = shop_account
                    table_dict['shopname'] = shop_name
                    j = j+1
                    continue

                elif key == 'ctime':
                    date_time = datetime.fromtimestamp(item[key])
                    value = date_time.strftime("%m/%d/%Y")
                elif key== 'price_before_discount' or key== 'price' or key== 'price_min_before_discount' or key== 'price_max_before_discount':
                    if item[key] > 0:
                        value = int(item[key]/100000)
                    else:
                        value = item[key]
                else:
                    value = item[key]

                detail.append(value)
                table_dict[attributes_values[j]] = value
            
            # 商品網址 https://shopee.tw/product/{賣場ID}/{商品ID}
            url = 'https://shopee.tw/product/'+str(item['shopid'])+'/'+str(item['itemid'])
            detail.append(url)
            table_dict['網址'] = url

            if bool_save == True:
                writer.writerow(detail)
                table.append(table_dict)

        if len(table) > 0:
            return table



# shopid= '605103581'

# # keyword = '三多葉黃素'
# data = shop_search(shopid= shopid)
# if data != None:
#     data_to_csv( shopid, data)

