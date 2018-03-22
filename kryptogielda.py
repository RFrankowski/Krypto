import urllib
import bs4 as bs
import lxml
import re
import numpy as  np
import requests

r = requests.get("https://exchangebit.info/binance")
soup = bs.BeautifulSoup(r.text,'lxml')
#print soup

for rzecz in soup.find_all('tbody'):
    for rzeczlist in rzecz.find_all('td'):
        print rzeczlist
    #print rzecz