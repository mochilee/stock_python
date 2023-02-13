# basic
import numpy as np
import pandas as pd

# get data
import pandas_datareader as pdr

# visual
import matplotlib.pyplot as plt
import mplfinance as mpf
from scipy.stats import linregress
import seaborn as sns

#time
import datetime as datetime
start = datetime.datetime(2021,8,1)
df_n = pdr.DataReader('2330.TW', 'yahoo', start=start)
df_n = df_n.reset_index()

stock_id = 2330
stock_name = "台積電"
reg_up = linregress(x = df_n.index,y = df_n.Close)
up_line = reg_up[1] + reg_up[0] * df_n.index
#.Close.plot()
#plt.plot(up_line)

df_uptemp = df_n[df_n["Close"] < up_line]
df_uptemp.head()
while len(df_uptemp) >= 2 :
    reg = linregress(x = df_uptemp.index,y = df_uptemp.Close)
    up_line = reg[1] + reg[0] * df_n.index
    df_uptemp = df_n[df_n["Close"] < up_line]
df_n["low_Trend"] = reg[1] + reg[0] * df_n.index    
df_downtemp = df_n[df_n["Close"] > up_line]
df_downtemp.head()
while len(df_downtemp) >= 2 :
    reg = linregress(x = df_downtemp.index,y = df_downtemp.Close)
    up_line = reg[1] + reg[0] * df_n.index
    df_downtemp = df_n[df_n["Close"] > up_line]
df_n["Up_Trend"] = reg[1] + reg[0] * df_n.index
df_n.Close.plot()
plt.plot(df_n.low_Trend,color=(255/255,100/255,100/255))
plt.plot(df_n.Up_Trend,color=(100/255,100/255,255/255))
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.title(f"{stock_id}  {stock_name}",fontsize=20)
plt.legend(['收盤價','上升趨勢線','下降趨勢線'])
plt.savefig("stock.png")