# _*_ coding: utf-8 _*_
import tushare as ts
import pandas as pd
import datetime
import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()


#data_today = ts.get_today_all()
#codes = data_today.code
engine = sqlalchemy.create_engine('mysql://root:melody@127.0.0.1/stocks?charset=utf8')
today = pd.read_sql_table('today',engine)
hist = pd.read_sql_query('select date,close,code from stock_k', engine, index_col='date', parse_dates = True)

'''如果今日收盘价高于20日均价则返回股票代码'''
def close_high_ma20():
    df1 = hist.pivot(columns = 'code')
    df2 = df1.rolling(window=20).mean().iloc[-1,].reset_index().iloc[:,1:].dropna()
    df2.columns = ['code','ma20']
    df3 = pd.merge(df2,today[['code','trade']])
    res = list(df3[df3.trade >= df3.ma20].code)
    return res

res = close_high_ma20()
print(len(res))


