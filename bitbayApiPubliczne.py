#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from bitbay import get_bitbay_withdrawals

# waluty dostepne na bit bay: pozniez zamienic na zaczyt z api/parsowanie
waluty_bitbay = ['LTC', 'ETH']


# get info from public api



def znajdz_koszt_wycofania(waluta, koszt_wycofania):
    for waluta_koszt in koszt_wycofania:
        if waluta_koszt[0] == waluta:
            return waluta_koszt[1]


def wyswietl_koszt_wycofania_w_pln():
    koszt_wycofania_bitbay = get_bitbay_withdrawals()
    for waluta in waluty_bitbay:
        response = requests.get("https://bitbay.net/API/Public/" + waluta + "PLN" + "/orderbook.json")

        data = response.json()
        # print data
        bids = data['bids']
        bid = []
        for item in bids:
            bid.append(item)
        print('pierwsza: ', waluta, str(bid[0][0]) + " PLN", str(bid[0][1]) + " volum",
              znajdz_koszt_wycofania(waluta, koszt_wycofania_bitbay) * bid[0][0])
        time.sleep(1)

def wymina_na_inna_walute():
    koszt_wycofania_bitbay = get_bitbay_withdrawals()
    for waluta in waluty_bitbay:
        response = requests.get("https://bitbay.net/API/Public/" + waluta + "BTC" + "/orderbook.json")
        data = response.json()
        # print data
        bids = data['bids']
        bid = []
        for item in bids:
            bid.append(item)
        print('pierwsza: ', waluta, str(bid[0][0]) + " btc", str(bid[0][1]) + " volum")
        time.sleep(1)


wymina_na_inna_walute()



