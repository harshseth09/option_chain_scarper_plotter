import pandas as pd 
import bs4 as bs
import requests

URL='https://www.nseindia.com/products-services/equity-derivatives-list-underlyings-information'
r=requests.get(URL)
print(r.content)