# -*- coding: utf-8 -*-
#和风天气api

from sendemail import SendMail
import pandas as pd
import json
import requests
import time
import datetime

KEY = 'f54f4f3d93a948338dece4ca5fe27e94'
CITY = '无锡'
API_URL = 'https://free-api.heweather.com/s6/weather/forecast?'


def getweather(city=CITY):
    respone = requests.get(API_URL + 'key=%s&location=%s' % (KEY, city))
    data = json.loads(respone.text)
    df = pd.DataFrame(data['HeWeather6'][0]['daily_forecast'])
    df.index = df.date
    del df['date']
    weather = df.iloc[0, ]
    return weather


def weatherreport(h, m, delay,touser):
    while True:
        now = datetime.datetime.now()
        if (now.hour == h) and (now.minute == m):
            today = getweather()
            content = '''
                今天是%s,无锡天气白天%s,晚上%s,最高温度:%s摄氏度,最低温低:%s摄氏度,风向:%s,风力:%s级.
                ''' % (today.name, today.cond_txt_d, today.cond_txt_n, today.tmp_max, today.tmp_min, today.wind_dir,
                       today.wind_sc)
            SendMail(subject='天气预报', content=content, touser=touser)
        time.sleep(delay)


hour = int(input("please input hour:"))
min = int(input("please input minutes:"))
delay = int(input("please input delay:"))
touser = input("please input touser:")
print("engin start!")
print("next sending will be at %s:%s, delay %s senconds" % (hour,min,delay)) 
weatherreport(hour,min,delay,touser)
