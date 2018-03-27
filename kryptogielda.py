from exceptions import Exception

import bs4 as bs
import lxml
import re
import requests

r = requests.get("https://exchangebit.info/binance")
soup = bs.BeautifulSoup(r.text, 'lxml')
list_kursow = []
# print soup

try:
    for rzecz in soup.find_all('tbody'):
        for rzeczlist in rzecz.find_all('tr'):
            i = 0
            para_waluta_kurs = []
            for kolumny in rzeczlist.find_all('td'):
                if i == 1:
                    # print kolumny.text
                    para_waluta_kurs.append(str(kolumny.text))
                if i == 3:
                    para_waluta_kurs.append(float(kolumny.text))
                i += 1
            list_kursow.append(para_waluta_kurs)
    print list_kursow

    # print rzecz
except Exception as e:
    print e.args
    print e.message
    print "blad w parsowaniu: https://exchangebit.info/binance"
