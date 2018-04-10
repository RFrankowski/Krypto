from exceptions import Exception
from datetime import datetime
import csv
import bs4 as bs
import lxml

import re
import requests

r = requests.get("https://exchangebit.info/binance")
soup = bs.BeautifulSoup(r.text, 'lxml')
list_kursow = []
# print soup

try:
    tbody = soup.find('tbody')
    for wiersz in tbody.find_all('tr'):
        i = 0
        para_waluta_kurs = []
        for kolumna in wiersz.find_all('td'):
            if i == 1:
                # print kolumny.text
                para_waluta_kurs.append(str(kolumna.text))
            if i == 3:
                para_waluta_kurs.append(float(kolumna.text))
            i += 1
        list_kursow.append(para_waluta_kurs)
    print list_kursow

    # print rzecz
except Exception as e:
    print e.args
    print e.message
    print "blad w parsowaniu: https://exchangebit.info/binance"




# for waluta_cena in list_kursow:
with open('binance.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for waluta_cena in list_kursow:
        writer.writerow([waluta_cena[0], waluta_cena[1], datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
