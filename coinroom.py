# import urllib
import bs4 as bs
import lxml
import re
import  requests

# r = requests.get('https://www.kraken.com/help/fees')
r = requests.get('https://coinroom.com/tabela-oplat')
soup = bs.BeautifulSoup(r.text, 'lxml')
for tabele in soup.find_all('table', 'payment-table'):
    # print tabele.text
    for row in tabele.tr:
        print row





