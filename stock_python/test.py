import datetime
import time
import requests
from io import StringIO
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import plotly.graph_objects
import plotly.subplots
from plotly.offline import plot

data = {}
n_days = 9
date = datetime.datetime.now()
fail_count = 0
allow_continuous_fail_count = 5

def KValue(rsv):
    global K
    K = (2/3) * K + (1/3) * rsv
    return K
def DValue(k):
    global D
    D = (2/3) * D + (1/3) * k
    return D
def crawl_price(date):
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                        for i in r.text.split('\n') 
                                        if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    ret = ret.set_index('證券代號')
    ret['成交金額'] = ret['成交金額'].str.replace(',','')
    ret['成交股數'] = ret['成交股數'].str.replace(',','')
    return ret

while len(data) < n_days:

    print('parsing', date)
    # 使用 crawPrice 爬資料
    try:
        # 抓資料
        data[date.date()] = crawl_price(date)
        print('success!')
        fail_count = 0
    except:
        # 假日爬不到
        print('fail! check the date is holiday')
        fail_count += 1
        if fail_count == allow_continuous_fail_count:
            raise
            break
    
    # 減一天
    date -= datetime.timedelta(days=1)
    time.sleep(random.randint(2,5))
    
open = pd.DataFrame({k:d['開盤價'] for k,d in data.items()}).transpose()
open.index = pd.to_datetime(open.index)


high = pd.DataFrame({k:d['最高價'] for k,d in data.items()}).transpose()
high.index = pd.to_datetime(high.index)
close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()}).transpose()
close.index = pd.to_datetime(close.index)
low = pd.DataFrame({k:d['最低價'] for k,d in data.items()}).transpose()
low.index = pd.to_datetime(low.index)
volume = pd.DataFrame({k:d['成交股數'] for k,d in data.items()}).transpose()
volume.index = pd.to_datetime(volume.index)

tar_stock = {
    'close':close['2330']['2021'].dropna().astype(float),
    'open':open['2330']['2021'].dropna().astype(float),
    'high':high['2330']['2021'].dropna().astype(float),
    'low':low['2330']['2021'].dropna().astype(float),
    'volume': volume['2330']['2021'].dropna().astype(float),
}
tar_stock['close'].plot()
# =============================================================================
# kd
# =============================================================================
tar_stock['9DAYMAX'] = 0
tar_stock['9DAYMAX'] = tar_stock['high'].rolling('9D').max()
# 計算 9 日內最高成交價
tar_stock['9DAYMIN'] = 0
tar_stock['9DAYMIN'] = tar_stock['low'].rolling('9D').min()
# 計算 9 日內最低成交價
# 計算每日 RSV 值
tar_stock['RSV'] = 0
tar_stock['RSV'] = 100 * (tar_stock['close'] - tar_stock['9DAYMIN']) / (tar_stock['9DAYMAX'] - tar_stock['9DAYMIN'])
# 計算 K 值
K = 0
tar_stock['K'] = 0
tar_stock['K'] = tar_stock['RSV'].apply(KValue)
# 計算 D 值
D = 0
tar_stock['D'] = 0
tar_stock['D'] = tar_stock['K'].apply(DValue)
figure = plotly.graph_objects.Figure(
    data=[
        # K
        plotly.graph_objects.Scatter(
            x=(tar_stock['K'] != 0).index,
            y=tar_stock['K'],
            name='K',
            mode='lines',
            line=plotly.graph_objects.scatter.Line(
                color='#6B99E5'
            )
        ),
        # D
        plotly.graph_objects.Scatter(
            x=(tar_stock['D'] != 0).index,
            y=tar_stock['D'],
            name='D',
            mode='lines',
            line=plotly.graph_objects.scatter.Line(
                color='#E58B6B'
            )
        )
        ],
    # 設定 XY 顯示格式
        layout=plotly.graph_objects.Layout(
            xaxis=plotly.graph_objects.layout.XAxis(
                tickformat='%Y-%m-%d'
            ),
            yaxis=plotly.graph_objects.layout.YAxis(
                tickformat='.2f'
            )
        )
)
plot(figure, filename='basic-heatmap.html')
