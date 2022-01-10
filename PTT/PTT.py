# -*- coding: UTF-8 -*-
import requests
from requests_html import HTML

import datetime as dt

def ptt_alert(url, keyword):
    url          = url # 網址
    resp         = fetch(url) # 取得網頁內容
    post_entries = parse_article_entries(resp.text) # 取得各列標題
    print('[%s] 連線成功，開始搜尋目標「%s」\n' %(dt.datetime.now(), keyword))


    for entry in post_entries:
        meta = parse_article_meta(entry)
        # 如果找到關鍵字，而且還沒截止，寄信通知我
        # 記得先試著轉小寫，否則大小寫視作不同
        if keyword in meta['title'].lower() :
            print(meta['title'])

def fetch(url):
    # 傳入網址，向 PTT 回答已經滿 18 歲，回傳網頁內容
    response = requests.get(url, cookies={'over18':'1'})
    return response


def parse_article_entries(doc):
    # 傳入網頁內容，利用 requests_html 取出 div.r-ent 的元素內容並回傳'
    html = HTML( html = doc )
    post_entries = html.find('div.r-ent')
    return post_entries


def parse_article_meta(entry):
    # 將 r-ent 元素的內容格式化成 dict 再回傳'
    meta = {
        'title': entry.find('div.title', first=True).text,
        'push' : entry.find('div.nrec', first=True).text,
        'date' : entry.find('div.date', first=True).text
    }
    try:
        # 正常的文章可以取得作者和連結
        meta['author'] = entry.find('div.author', first=True).text
        meta['link'] = entry.find('div.title > a', first=True).attrs['href']
    except AttributeError:
        # 被刪除的文章我們就不要了
        meta['author'] = '[Deleted]'
        meta['link'] = '[Deleted]'
    return meta




