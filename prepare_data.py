#!/usr/bin/env python
# coding: utf-8

# In[168]:


import pandas as pd
import json
from datetime import datetime
import re
import requests


# In[2]:


data_link = 'http://tgftp.nws.noaa.gov/data/observations/metar/decoded/'

airports = ['KTUS','ENSO','LRTZ','OERK','EETU','KTTS','MMLO','KBBF','KCCU','KPBF',
            'FTTC','KTKI','KPNA','KIMM','CWIS','UKON','FSIA','KESF','KNYG','KBEH',
            'KHAI','K5SM','CWSW','KLWV','GVAC','LIRZ','KPSM','EHDV','LFAT','CWJT']

temperature = -3
humidity = 75


# In[154]:


def extract_temperature(string):
    temperature_pattern = re.compile('Temperature: (-*\d+\.*\d*) F \((-*\d+\.*\d*) C\)')
    res = temperature_pattern.match(string)
    if res is not None:
        return res.group(2)
    else:
        return None


# In[81]:


def extract_humidity(string):
    humidity_pattern = re.compile('Relative Humidity: (\d+\.*\d*)%')
    res = humidity_pattern.match(string)
    if res is not None:
        return res.group(1)
    else:
        return None


# In[126]:


def extract_date(string):
    date_pattern = re.compile('.*(\d{4}.\d{2}.\d{2}).*')
    res = date_pattern.match(string)
    if res is not None:
        date = datetime.strptime(res.group(1), '%Y.%m.%d').strftime('%Y.%m.%d')
        return date
    else:
        return None


# In[116]:


def check_airport(data):
    date = None
    temp = None
    hum = None
    for line in data:
        date = extract_date(line) if date is None else date
        temp = extract_temperature(line) if temp is None else temp
        hum = extract_humidity(line) if hum is None else hum
    return [date, temp, hum]


# In[155]:


today = datetime.utcnow().strftime('%Y.%m.%d')
data_new = []

for el in airports:
    r = requests.get(data_link+el+'.TXT')
    if r.status_code == 200:
        content = r.content.decode("utf-8").split('\n')
        today_data = check_airport(content)
        today_data.append(el)
        if today_data[0] == today:
            data_new.append(today_data)
        else:
            print('No data available')
        print('\n')


# In[159]:


pd.DataFrame(data_new, columns=['date','temp','hum','name']).to_csv('data.txt', index=False)


# In[160]:


with open('history.json') as f:
    d = json.load(f)

for el in data_new:
    if el[3] in d:
        d[el[3]][el[0]] = {'Temperature': el[1], 'Humidity': el[2]}

r = json.dumps(d)
text_file = open("history.json", "w")
text_file.write(r)
text_file.close()

