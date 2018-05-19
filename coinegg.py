import urllib
import bs4 as bs
import lxml
import re
import requests

r = requests.get("https://www.coinegg.com/fee.html")
soup = bs.BeautifulSoup(r.text, 'lxml')





for ul in soup.find_all('ul', class_='noticeListHeadBody clearfix' ):
    print(ul.text)
