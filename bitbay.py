import urllib
import bs4 as bs
import lxml
import re
import requests
import time
from exceptions import Exception


def get_bitbay_withdrawals():
    sock = urllib.urlopen("https://bitbay.net/en/fees")
    htmlSource = sock.read()
    sock.close()
    soup = bs.BeautifulSoup(htmlSource, 'lxml')
    list_kursow = []
    lista_walut = []
    try:
        for item in soup.find_all('section', id='withdrawals'):
            for listItem in item.find_all('li'):
                if listItem.string is not None:
                    waluta_cena = re.search(r'([aA-zZ]{3,4}:\s[0-9](\.*[0-9]{0,8}))', str(listItem.text)).string
                    waluta, cena = waluta_cena.split(':')
                    # xx[waluta] = cena
                    if waluta not in lista_walut and waluta != "PLN":
                        lista_walut.append(waluta)
                        list_kursow.append([str(waluta), float(cena)])
    except Exception as e:
        print e.args
        print e.message
        print "blad w parsowaniu: https://bitbay.net/en/fees"

    return list_kursow


# print get_bitbay_withdrawals()


def zwroc_liste_walut_bitbay():
    lista_waluta_withdraw = get_bitbay_withdrawals()
    lista_walut = []

    for waluta_withdraw in lista_waluta_withdraw:
        lista_walut.append(waluta_withdraw[0])

    return lista_walut


# print zwroc_liste_walut_bitbay()





def get_specyfic_withdrawals_fee(waluta, koszt_wycofania):
    for waluta_koszt in koszt_wycofania:
        if waluta_koszt[0] == waluta:
            return waluta_koszt[1]


# funkcja zwraca koszt wycofania w walucie2
def zwroc_orderbook_bitbay(waluta, waluta2, kupno_sprzedaz, ilosc_do_przeslania):
    time.sleep(1)
    response = requests.get("https://bitbay.net/API/Public/" + waluta + waluta2 + "/orderbook.json")
    data = response.json()
    # print data
    asks_bids = data[kupno_sprzedaz]
    ask = []
    for item in asks_bids:
        ask.append(item)

    # suma = 0
    # ilosc_krypto = 0
    # flag = True
    # # potrzebuje zwrocic ilosc po przewalutowaniu
    # for cena, ilosc in ask:
    #
    #     if suma < ilosc_do_przeslania and flag:
    #         suma += cena * ilosc
    #         ilosc_krypto += ilosc
    #         print "ilosc kupionej" + str(ilosc_krypto)
    #         print "suma " + str(suma)
    #
    #     if suma > ilosc_do_przeslania:
    #         flag = False
    #         suma -= cena * ilosc
    #         ilosc_krypto -= ilosc
    #         print "ilosc kupionej" + str(ilosc_krypto)
    #         print "suma " + str(suma)
    #         ile_dokupic = ilosc_do_przeslania-suma
    #         ilosc_krypto += ile_dokupic/cena
    #         print "ilosc kupionej" + str(ilosc_krypto)
    #         print "suma " + str(suma)
    #
    #
    # print ile_dokupic
    # print suma
    # print ilosc_krypto

        # pass
    # cena kupna jednej jednoski za walute2
    # cena_kupna = ask[0][0]
    # ilosc_w_ofercie = ask[0][1]
    # zwraca pierwsza oferte sprzedazy
    return asks_bids


print zwroc_orderbook_bitbay("GAME", "BTC", "asks", 0.01)




# print zwrocListeWalut()
