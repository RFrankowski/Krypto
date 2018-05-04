import urllib
import bs4 as bs
import lxml
import re
import requests

r = requests.get("https://www.coinegg.com/fee.html")
soup = bs.BeautifulSoup(r.text, 'lxml')

print r.text
