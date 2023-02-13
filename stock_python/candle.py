# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 07:38:21 2021

@author: tony
"""
import numpy as np
import pandas as pd
from io import StringIO
import datetime
import xlstest as xls
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import mplfinance as mpf
from scipy.stats import linregress
import seaborn as sns

def stock_data(stock_id,start,end = 0): # 抓股票 變數 股票id 開始時間 結束時間
    
    start_time = datetime.datetime.strptime( str(start) , '%Y%m%d' )  
    stock = f'{stock_id}.TW'
    try:
        if (end == 0):
            #df_n = pdr.DataReader("2230.TWO", 'yahoo', start=start_time)
            df_n = pdr.DataReader(stock, 'yahoo', start=start_time)
            df_n = df_n.reset_index()                
        else :
            end_time = datetime.datetime.strptime( str(end) , '%Y%m%d' )
            df_n = pdr.DataReader(stock, 'yahoo', start=start_time,end=end_time)
            df_n = df_n.reset_index()
    except:
        print("fail")
    return df_n

def candle(df,stockid): # 畫蠟燭圖 變數 股票dataframe 股票id
   	
    df.index  = pd.DatetimeIndex(df.Date)
    df = df.drop(["Adj Close"],axis = 1) 
    #print(df)	
    #mpf.plot(df,type='candle')
    stock_name = xls.stock_search(stockid)
    stock = f'{stockid} {stock_name}'
    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    kwargs = dict(type='candle', mav=(5,10), volume=True, figratio=(20,15), figscale=1.2,title = stockid, style=s)
    #mpf.plot(df, **kwargs)
    mpf.plot(df, **kwargs,savefig='test_plot1.png')
    return stock
    #return mpf.plot(df, **kwargs,savefig='test_plot1.png')
    
if __name__ == "__main__":
    df_n = stock_data('2330',"20211001")
    temp = candle(df_n,'2330')
    print(temp)