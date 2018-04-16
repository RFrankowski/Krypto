#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from bitbay import get_bitbay_withdrawals

# waluty dostepne na bit bay: pozniez zamienic na zaczyt z api/parsowanie
waluty_bitbay = ['BTC', 'LTC', 'ETH']


# zwraca koszt wycofania dla danej waluty dla danych pobranych z giedly
def znajdz_koszt_wycofania(waluta, koszt_wycofania):
    for waluta_koszt in koszt_wycofania:
        if waluta_koszt[0] == waluta:
            return waluta_koszt[1]


# funkcja zwraca koszt wycofania w walucie2
def zwroc_koszt_wycofania(waluta, waluta2, koszt_wycofania_z_bitbay):
    time.sleep(1)
    response = requests.get("https://bitbay.net/API/Public/" + waluta + waluta2 + "/orderbook.json")
    data = response.json()
    # print data
    bids = data['bids']
    bid = []
    for item in bids:
        bid.append(item)
    # cena kupna jednej jednoski za walute2
    cena_kupna = bid[0][0]
    ilosc_w_ofercie = bid[0][1]

    # return ('pierwsza najtansza oferta: ', waluta, str(cena_kupna) + " " + waluta2, str(ilosc_w_ofercie) + " volume",
    #         znajdz_koszt_wycofania(waluta, koszt_wycofania_z_bitbay) * cena_kupna + "koszt wycofania z gieldy")
    return znajdz_koszt_wycofania(waluta, koszt_wycofania_z_bitbay) * cena_kupna


def main():
    koszt_wycofania_bitbay = get_bitbay_withdrawals()
    # sprawdzenie kosztu wycofrania w zlotowkach
    # dodac wszystko do listy lub slownika
    for waluta in waluty_bitbay:
        print waluta + " " + str(zwroc_koszt_wycofania(waluta, "PLN", koszt_wycofania_bitbay)) + "PLN"
    # sprawdzic opcje przewalutowania i wycofania z danej gieldy
        # np btc > game sprawdzic koszt (przewalutowania + wycofania)
        # czynnosc powtorzyc dla wszystkich par


if __name__ == '__main__':
    main()
