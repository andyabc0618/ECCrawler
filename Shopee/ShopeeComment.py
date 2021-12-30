# -*- coding: UTF-8 -*-
import requests
import urllib
import csv
from datetime import datetime
import emoji
import json


def comment_get( shopid, itemid, item_name):

    item_name = item_name.encode('utf-8').decode('latin1')
    # 需要加入 Headers 才能得到完整回傳資料
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'X-Requested-With': 'pc', 
        'Referer': f'https://shopee.tw/{urllib.parse.quote(item_name)}-i.{shopid}.{itemid}',
    }  

    # print(headers['Referer'])

    s   = requests.Session()

    base_url = 'https://shopee.tw/api/v2/item/get_ratings'
    query    = f'shopid={shopid}&itemid={itemid}'
    query_c  = '&filter=3&type=0&limit=59&offset=0&flag=1'
    url      = base_url + '?' + query + query_c 
    # print(url)
    r        = s.get(url, headers=headers)


    if r.status_code == requests.codes.ok:
        data = r.json()
        # with open('shopee_comment.json', 'w', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)
        
        return data
    else:
        return None


def data_to_csv( itemid, data):
    attributes_dict={'userid':'買家ID','author_username':'買家名稱','author_shopid':'買家賣場','ctime':'評論時間','rating_star':'評分','comment':'評論','images':'圖片'}
    attributes_key    = list(attributes_dict.keys())
    attributes_values = list(attributes_dict.values())
    data_rating       = data['data']['ratings']

    with open(itemid+'.csv','w+', newline='', encoding="utf_8_sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(attributes_values)
        
        max_imgnum = 0
        table = []
        for i in range( 0, len(data_rating), 1):
            item       = data_rating[i]
            detail     = []
            table_dict = {}
            for j in range( 0, len(attributes_key), 1):
                key = attributes_key[j]
                if key == 'ctime':
                    date_time = datetime.fromtimestamp(item[key])
                    value     = date_time.strftime("%m/%d/%Y")
                elif key == 'images':
                    img_str = ''
                    if len(item[key])> max_imgnum:
                        max_imgnum  = len(item[key])
                    for k in range( 0, len(item[key])):
                        if k > 0:
                            img_str = img_str + '-'
                        img_str = img_str + item[key][k]
                    value = img_str
                else:
                    value = item[key]

                detail.append(value)
                table_dict[attributes_values[j]] = value
            
            writer.writerow(detail)
            table.append(table_dict)
        
        if len(table) > 0:
            return table, max_imgnum
        else:
            None, None






# shopid = '38499635'
# itemid = '1408729655'
# item_name = '[活動限時促銷] 三多 葉黃素複方軟膠囊100粒/盒 金盞花萃取物'
# data = comment_get( shopid, itemid, item_name)
# if data != None:
#     data_to_csv( shopid, itemid, data)
