# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 08:50:23 2021

@author: tony
"""
import pandas as pd

test = []
def stock_list():
    
    dft = pd.read_excel("StockTable.xlsx")

    dft = dft.reset_index() 
    for i in range(len(dft)):   #整理原始資料
        if dft.loc[i,'id'].replace(u'\xa0', '') != '上市' and dft.loc[i,'id'].replace(u'\xa0', '') != '上櫃':
            test.append({'id':dft.loc[i,'id'].replace(u'\xa0', ''),
                         'name':dft.loc[i,'name'].replace(u'\xa0', '')})
    for i in range(len(test)):
        if test[i]['name'] == "其祥-KY":
            TWO_range = i
        if test[i]['name'].endswith("＊"):
            test[i]['name'] = test[i]['name'].replace(u'＊', '')
        elif test[i]['name'].endswith("＃"):
            test[i]['name'] = test[i]['name'].replace(u'＃', '')
    return test

def stock_search(id):
    stock_list()
    for i in range(len(test)):
       if test[i]['id'] == str(id):
           result = test[i]['name']
    return result   
        
        
        
#if __name__ == "__main__":
    #print(stock_search(2230))