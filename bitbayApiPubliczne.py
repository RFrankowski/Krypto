#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from bitbay import get_bitbay_withdrawals
from poloniexAPI import *

# ================ bids - oferty kupna asks - oferty sprzedazy ===========================
# ================ "maker" i "taker"======================================================
# jak wystawiasz oferte to placisz 0.30% a jak bierzesz jakas oferte to cos kolo 0.40%
# ================ wystawiasz czyli maker, bierzesz - taker ==============================


# zwraca koszt wycofania dla danej waluty dla danych pobranych z giedly
def get_specyfic_withdrawals_fee(waluta, koszt_wycofania):
    for waluta_koszt in koszt_wycofania:
        if waluta_koszt[0] == waluta:
            return waluta_koszt[1]


# funkcja zwraca koszt wycofania w walucie2
def get_orderbook_first_offer(waluta, waluta2, kupno_sprzedaz):
    time.sleep(1)
    response = requests.get("https://bitbay.net/API/Public/" + waluta + waluta2 + "/orderbook.json")
    data = response.json()
    # print data
    asks_bids = data[kupno_sprzedaz]
    # ask = []
    # for item in asks_bids:
    #     ask.append(item)
    # cena kupna jednej jednoski za walute2
    # cena_kupna = ask[0][0]
    # ilosc_w_ofercie = ask[0][1]
    # zwraca pierwsza oferte sprzedazy
    return asks_bids[0]


def main():
    lista_kosztow_wycofania_bitbay = get_bitbay_withdrawals()
    # zalozenie przesylu
    # zakladam wyslanie z bitbay do poloniex
    waluta_do_przeslania = "BTC"
    ilosc_do_przeslania = 0.05  # BTC
    # sprawdzam koszt wyslania bez przewalutowania
    print str(get_specyfic_withdrawals_fee(waluta_do_przeslania,
                                           lista_kosztow_wycofania_bitbay)) + " to jest koszt transfer fee "

    print str((ilosc_do_przeslania - get_specyfic_withdrawals_fee(waluta_do_przeslania,
                                                                  lista_kosztow_wycofania_bitbay)) / ilosc_do_przeslania) + " tyle bedzie po przeslaniu bez przewalutowania"

    # waluty dla ktorych chce sprawdzic
    waluty_bitbay = ['GAME', 'LSK', 'LTC', 'ETH']
    for waluta in waluty_bitbay:
        print "____________Start_ " + waluta + "________________"

        # wzor na przesyl
        # (ilosc_do_przeslania - koszt_wycofania) / ilosc_do_przeslania

        # sprawdzenie cen waluty np game za btc na dwoch gieldach
        # wzor na ilosc Game
        # (ilosc_do_przeslania / cena_kryptowaluty)
        print "bitbay "
        print str(get_orderbook_first_offer(waluta, waluta_do_przeslania,
                                            "asks")) + "to jest odpowiednio cena " + waluta + " i ilosc w ofercie"
        ile_game = (ilosc_do_przeslania / get_orderbook_first_offer(waluta, "BTC", "asks")[0])
        # odejmuje koszt wycofania z bitbay
        ile_game -= get_specyfic_withdrawals_fee(waluta, lista_kosztow_wycofania_bitbay)
        print (str(ile_game) + " tyle kupie " + waluta + " na bitbay")
        # sprawdzam cene GAME na poloniex
        print "sprawdzam cene " + waluta + " na poloniex"
        polo = poloniex(APIKey, Secret)
        polo_cena_ilosc = polo.returnOrderBook(waluta_do_przeslania + "_" + waluta)['bids'][0]
        print str(polo_cena_ilosc) + "odpowiednio cena i ilosc "
        print "---------------wynik--------------"
        print (float(ile_game) * float(polo_cena_ilosc[0])) / ilosc_do_przeslania
        print "____________koniec_ " + waluta + "_______________"


if __name__ == '__main__':
    main()
