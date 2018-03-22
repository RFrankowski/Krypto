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
    for rzeczlist in rzecz.find_all('tr'):
        i=0
        for kolumny in rzeczlist.find_all('td'):
            if i == 1 or i == 3:
                print kolumny.text
            i += 1
    #print rzecz