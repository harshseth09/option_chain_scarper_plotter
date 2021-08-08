import requests
import json
import pandas as pd
from pymongo import MongoClient
import datetime
from bs4 import BeautifulSoup
import requests
from json.decoder import JSONDecodeError
import time 

def get_symbols():
    URL='https://www.nseindia.com/products-services/equity-derivatives-list-underlyings-information'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    r=requests.get(URL,headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    table=soup.find_all('tr')
    symbols=[]
    stocks=[]
    indices=['NIFTY','BANKNIFTY']
    for t in table:
        x=t.find_all('a',target='_blank')
        for i in x:
            symbols.append(i.text)
    for i in range(7,len(symbols),2):
        stocks.append(symbols[i])
    return stocks,indices


def fetch_oi_indices(expiry_dt):
    ce_values = [data['CE'] for data in dajs['records']['data'] if "CE" in data and data['expiryDate'] == expiry_dt]
    pe_values = [data['PE'] for data in dajs['records']['data'] if "PE" in data and data['expiryDate'] == expiry_dt]
    ce_dt = pd.DataFrame(ce_values).sort_values(['strikePrice'])
    pe_dt = pd.DataFrame(pe_values).sort_values(['strikePrice'])  
    ce_dt=ce_dt.drop(columns=['identifier','pchangeinOpenInterest'])
    pe_dt=pe_dt.drop(columns=['identifier','pchangeinOpenInterest'])
    ce_dt['date']=datetime.datetime.now()
    pe_dt['date']=datetime.datetime.now()
    return ce_dt,pe_dt
    
def insertion_indices(expiry_dt,symbol):
    ce,pe=fetch_oi_indices(expiry_dt)
    expiry_dt_ce=expiry_dt+'_ce'
    expiry_dt_pe=expiry_dt+'_pe'
    cluster = MongoClient('mongodb+srv://harshseth09:messis@cluster0.hfphg.mongodb.net/options?retryWrites=true&w=majority')
    cluster_name=symbol+'options'
    db=cluster[cluster_name]
    dataframe_ce =  ce.to_dict(orient='records')
    collection=db[expiry_dt_ce]
    collection.insert_many(dataframe_ce)
    dataframe_pe =  pe.to_dict(orient='records')
    collection=db[expiry_dt_pe]
    collection.insert_many(dataframe_pe)

while True:
    expiry_dt_lst=['12-Aug-2021','18-Aug-2021','26-Aug-2021']
    stocks,indices=get_symbols()
    for i in indices:
        new_url = 'https://www.nseindia.com/api/option-chain-indices?symbol='+i
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8',
            'accept-encoding': 'gzip, deflate, br'}
        page = requests.get(new_url,headers=headers)
        p=0
        while('<!DOCTYPE html>' in page.text):
            p+=1
            print('error '+str(p))
            page=requests.get(new_url,headers=headers)
        dajs = json.loads(page.text)
        for j in expiry_dt_lst:
            insertion_indices(j,i)
            print(i+' '+j)
    print('sleeping for 120 seconds')
    time.sleep(120)





