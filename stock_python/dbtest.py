# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 16:22:11 2021

@author: tony
"""

import requests
import pandas as pd
import xlwings as xw
import time
result = time.localtime()
datestr = f"{result.tm_year}{result.tm_mon}{result.tm_mday}" 
# 把csv檔抓下來
url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+ datestr + '&type=ALL'
res = requests.get(url)
data = res.text
# =============================================================================
#  抓台股
# =============================================================================
# 把爬下來的資料整理乾淨
cleaned_data = []
for da in data.split('\n'):
    if len(da.split('","')) == 16 and da.split('","')[0][0] != '=':
        cleaned_data.append([ele.replace('",\r','').replace('"','') 
                             for ele in da.split('","')])
 
# 輸出成表格並呈現在excel上
df = pd.DataFrame(cleaned_data, columns = cleaned_data[0])
df = df.set_index('證券代號')[1:]
# =============================================================================
# 抓取本益比
# =============================================================================
resu = df[pd.to_numeric(df['本益比'], errors='coerce') < 15]
xw.view(df)
# =============================================================================
# 
# =============================================================================
