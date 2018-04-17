#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from bitbay import get_bitbay_withdrawals


# ================ bids - oferty kupna asks - oferty sprzedazy ===========================
# ================ "maker" i "taker"======================================================
# jak wystawiasz oferte to placisz 0.30% a jak bierzesz jakas oferte to cos kolo 0.40%
# ================ wystawiasz czyli maker, bierzesz - taker ==============================



# zwraca koszt wycofania dla danej waluty dla danych pobranych z giedly
def calculate_withdrawals(waluta, koszt_wycofania, cena_sprzedazy):
    for waluta_koszt in koszt_wycofania:
        if waluta_koszt[0] == waluta:
            return waluta_koszt[1] * cena_sprzedazy


# funkcja zwraca koszt wycofania w walucie2
def get_orderbook_first_offer(waluta, waluta2, kupno_sprzedaz):
    time.sleep(1)
    response = requests.get("https://bitbay.net/API/Public/" + waluta + waluta2 + "/orderbook.json")
    data = response.json()
    # print data
    asks = data[kupno_sprzedaz]
    # ask = []
    # for item in asks:
    #     ask.append(item)
    # cena kupna jednej jednoski za walute2
    # cena_kupna = ask[0][0]
    # ilosc_w_ofercie = ask[0][1]
    # zwraca pierwsza oferte sprzedazy
    return asks[0]


def main():
    # pozniej dodac zaczyt z bitbay
    waluty_bitbay = ['LSK', 'LTC', 'ETH']

    koszt_wycofania_bitbay = get_bitbay_withdrawals()

    # sprawdzenie kosztu wycofrania w zlotowkach dla wszystkich walut
    for waluta in waluty_bitbay:
        cena_ilosc = get_orderbook_first_offer(waluta, "PLN", "bids")
        cena = cena_ilosc[0]
        print waluta + " " + str(calculate_withdrawals(waluta, koszt_wycofania_bitbay, cena)) + "pln"

    # przewalutowanie
    for waluta in waluty_bitbay:
        cena_ilosc = get_orderbook_first_offer(waluta, "BTC", "asks")
        cena = cena_ilosc[0]
        print cena_ilosc


        # sprawdzic opcje przewalutowania i wycofania z danej gieldy
        # np btc > game sprawdzic koszt (przewalutowania + wycofania)
        # czynnosc powtorzyc dla wszystkich par


if __name__ == '__main__':
    main()
