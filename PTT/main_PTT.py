# -*- coding: UTF-8 -*-
import PTT

import datetime as dt


if __name__ == '__main__':
    URL = 'https://www.ptt.cc/bbs/Lifeismoney/index.html'
    KEYWORD = '序號'

    try:
        PTT.ptt_alert(URL, KEYWORD) # 開始執行
            
    except Exception as e:
        print('[%s] 執行期間錯誤：%s' %(dt.datetime.now(), e))