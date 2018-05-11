# _*_ coding: utf-8 _*_
import tushare as ts
import pandas as pd
import datetime

data_today = ts.get_today_all()
codes = data_today.code
history = pd.read_sql_query('select data,ma20')

'''如果今日收盘价高于20日均价则返回股票代码'''
def close_high_ma20():
    res = []
    for code in codes:
        if data_today[data_today.code == code].trade >=