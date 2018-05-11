# _*_ coding: utf-8 _*_
import pandas as pd
import numpy as np
import tushare as ts
from sqlalchemy import create_engine
import sendemail
import time
import datetime


ENGINE = create_engine("mysql://root:sj19851206@127.0.0.1/stocks?charset=utf8")
NOW = str(datetime.datetime.now()).split(' ')[0]
CLASSIFIED = {'industry_classified', 'concept_classified', 'area_classified', 'sme_classified', 'gem_classified', \
                  'st_classified', 'hs300s', 'sz50s', 'zz500s', 'terminated', 'suspended'}


def if_need_update(dataset):
    start = pd.read_sql_query('select max(date) from log where action = "%s"' % dataset, ENGINE).iloc[0][0]
    if start is None:
        start = '2015-01-01'
    elif start == NOW:
        print('%s is newest. Do not need to update!' % dataset)
        start = 0
    return start

def to_log(now_date,now_time,action,update_num):
    log = pd.DataFrame(
        {'date': [now_date], 'time': [now_time], 'action': [action], 'update_num': [update_num]})
    log.to_sql('log', ENGINE, if_exists='append', index=None)


#更新个股基础数据
def update_stock_basic():
    start = if_need_update('update_stock_basic')
    if start == 0:
        return
    df = ts.get_stock_basics().reset_index()
    df.to_sql('stock_basic', ENGINE, if_exists='replace', index=None)
    now_time = str(datetime.datetime.now()).split(' ')[1]
    num = df.shape[0]
    to_log(NOW, now_time, 'update_stock_basic', num)
    sendemail.SendMail(subject='更新股票基础资料成功', content='')

#更新个股历史数据
def update_stock_k():
    start = if_need_update('update_stock_k')
    if start == 0:
        return
    df = []
    codes = pd.read_sql_query('select code from stock_basic', ENGINE)
    for code in codes.code:
        data = ts.get_k_data(code, start=start)
        if data is None:
            continue
        if data.shape[0] == 0:
            continue
        df.append(data)
        print('%s is done' % code)
        #time.sleep(1)
    result = pd.concat(df)
    result = result.reset_index()
    result.to_sql('stock_k', ENGINE, if_exists='append', index=None)
    now_time = str(datetime.datetime.now()).split(' ')[1]
    num = result.shape[0]
    to_log(NOW, now_time, 'update_stock_k', num)
    title = '更新个股历史k线图成功,最后更新时间%s' % str(datetime.datetime.now())
    sendemail.SendMail(subject=title, content='')

'''
更新分类：
行业 industry_classified
概念 concept_classified
地域 area_classified
中小板 sme_classified
创业板 gem_classified
风险警示 st_classified
沪深300成分股及权重 hs300s
上证50成分股 sz50s
中证500成份股 zz500s
终止上市股票列表 terminated
暂停上市股票列表 suspended
'''
def update_classified(names=CLASSIFIED):
    for name in names:
        if name not in CLASSIFIED:
            print('%s is not a good key, try an other one please!' % name)
            continue
        function = 'ts.get_' + name + '()'
        action = 'update_' + name
        start = if_need_update(action)
        if start == 0:
            continue
        df = eval(function)
        df.to_sql(name, ENGINE, if_exists='replace', index=None)
        now_time = str(datetime.datetime.now()).split(' ')[1]
        num = df.shape[0]
        to_log(NOW, now_time, action, num)
        print('%s is done!' % action)



