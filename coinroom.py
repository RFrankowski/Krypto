import bs4 as bs
import lxml
import re
import requests
from exceptions import Exception

# r = requests.get('https://www.kraken.com/help/fees')
r = requests.get('https://coinroom.com/tabela-oplat')
soup = bs.BeautifulSoup(r.text, 'lxml')

# if listItem.string is not None:
list_kursow = []

try:
    for rzecz in soup.find_all('tbody'):
        for rzeczlist in rzecz.find_all('tr'):
            kolumny = rzeczlist.find_all('td')
            if kolumny[1].text.find('fee') != -1:
                # print kolumny[1].text
                waluta = re.findall(r'([A-Z]{3,4})', str(kolumny[1].text))[0]
                kurs = re.findall(r'([0-9](\.*[0-9]{0,8}))', str(kolumny[1].text))[0]
                print kurs[0]
                list_kursow.append([str(waluta), float(kurs[0])])
except Exception as e:
    print e.args
    print e.message
    print "blad w parsowaniu: https://coinroom.com/tabela-oplat"

print list_kursow


