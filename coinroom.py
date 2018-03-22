# import urllib
import bs4 as bs
import lxml
import re
import  requests

# r = requests.get('https://www.kraken.com/help/fees')
r = requests.get('https://coinroom.com/tabela-oplat')
soup = bs.BeautifulSoup(r.text, 'lxml')
tabela = soup.find_all('table', 'payment-table')
for tr in tabela.find_all('tbody'):
    print tr






