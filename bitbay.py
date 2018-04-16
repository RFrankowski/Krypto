import urllib
import bs4 as bs
import lxml
import re
from exceptions import Exception


def get_bitbay_withdrawals():

    sock = urllib.urlopen("https://bitbay.net/en/fees")
    htmlSource = sock.read()
    sock.close()
    soup = bs.BeautifulSoup(htmlSource, 'lxml')
    list_kursow = []
    try:
        for item in soup.find_all('section', id='withdrawals'):
            for listItem in item.find_all('li'):
                if listItem.string is not None:
                    waluta_cena = re.search(r'([aA-zZ]{3,4}:\s[0-9](\.*[0-9]{0,8}))', str(listItem.text)).string
                    waluta, cena = waluta_cena.split(':')
                    # xx[waluta] = cena
                    list_kursow.append([str(waluta), float(cena)])
    except Exception as e:
        print e.args
        print e.message
        print "blad w parsowaniu: https://bitbay.net/en/fees"

    return list_kursow


# print get_bitbay_withdrawals()



