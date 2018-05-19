#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from bitbay import get_bitbay_withdrawals
from poloniexAPI import *
from poloniexWidhdraw import getPoloniexWithdrawFee
import re

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


def wprowadz_ile_chce_przeslac():
    while True:
        ilosc_do_przeslania = raw_input('wprowadz ilosc BTC do przeslania')
        num_format = re.compile("^[0-9](\.*[0-9]{0,8})$")
        isnumber = re.match(num_format, ilosc_do_przeslania)
        if isnumber:
            return float(ilosc_do_przeslania)
        else:
            print 'wprowadz liczbe a nie string!'


def wprowadz_wybierz_gielde_bazowa():
    while True:
        gielda = raw_input('wybierz gielde bazowa 1 - bitbay, 2 - poloniex, |3 - coinegg working in progress|')
        num_format = re.compile("^[0-9]{0,2}$")
        isnumber = re.match(num_format, gielda)
        if isnumber:
            return float(gielda)
        else:
            print 'wprowadz liczbe a nie string!'


def wprowadz_wybierz_gielde_docelowa():
    while True:
        gielda = raw_input('wybierz gielde docelowa 1 - bitbay, 2 - poloniex, |3 - coinegg working in progress|')
        num_format = re.compile("^[0-9]{0,2}$")
        isnumber = re.match(num_format, gielda)
        if isnumber:
            return float(gielda)
        else:
            print 'wprowadz liczbe a nie string!'


def get_orderbook_form_stock(gielda, waluta, waluta_do_przeslania, kupno_sprzedaz):
    # zwraca pierwsza oferte cene i ilosc[0.5687, 13583]
    if float(gielda) == 1:
        return get_orderbook_first_offer(waluta, waluta_do_przeslania, kupno_sprzedaz)
    elif float(gielda) == 2:
        return polo.returnOrderBook(waluta_do_przeslania + "_" + waluta)[kupno_sprzedaz][0]


polo = poloniex(ApiKey, secret)


def main():
    lista_kosztow_wycofania_bitbay = get_bitbay_withdrawals()
    # zalozenie przesylu
    # zakladam wyslanie z bitbay do poloniex
    waluta_do_przeslania = "BTC"

    ilosc_do_przeslania = wprowadz_ile_chce_przeslac()

    gielda_bazowa = wprowadz_wybierz_gielde_bazowa()
    gielda_docelowa = wprowadz_wybierz_gielde_docelowa()

    withdraw_fee = None

    if float(gielda_bazowa) == 1:
        withdraw_fee = get_specyfic_withdrawals_fee(waluta_do_przeslania, lista_kosztow_wycofania_bitbay)
    elif float(gielda_bazowa) == 2:
        withdraw_fee = getPoloniexWithdrawFee(waluta_do_przeslania)

    # sprawdzam koszt wyslania bez przewalutowania
    print str(withdraw_fee) + " to jest koszt transfer fee "

    print str(
        (ilosc_do_przeslania - withdraw_fee) ) + " tyle BTC bedzie po przeslaniu bez przewalutowania"

    # waluty dla ktorych chce sprawdzic
    waluty_do_sprawdzenia = ['GAME', 'LSK', 'LTC', 'ETH']
    for waluta in waluty_do_sprawdzenia:
        print "\n\n\n____________Start_ " + waluta + "________________"

        # wzor na przesyl
        # (ilosc_do_przeslania - koszt_wycofania) / ilosc_do_przeslania
        # wzor na ilosc Game
        # (ilosc_do_przeslania / cena_kryptowaluty)

        print "gielda Bazowa"
        print str(get_orderbook_form_stock(gielda_bazowa, waluta, waluta_do_przeslania,
                                           "asks")) + "to jest odpowiednio cena " + waluta + " i ilosc w ofercie"
        ile_krypto = (
            ilosc_do_przeslania / float(
                get_orderbook_form_stock(gielda_bazowa, waluta, waluta_do_przeslania, "asks")[0]))
        # odejmuje koszt wycofania z gieldy bazowej
        ile_krypto -= withdraw_fee
        print (str(ile_krypto) + " tyle kupie " + waluta + " na bitbay")


        print "gielda Docelowa \n sprawdzam cene " + waluta
        gielda_docelowa_cena_ilosc = get_orderbook_form_stock(gielda_docelowa, waluta, waluta_do_przeslania, 'bids')
        print str(gielda_docelowa_cena_ilosc) + "odpowiednio cena i ilosc "
        print "---------------wynik--------------"
        print (float(ile_krypto) * float(gielda_docelowa_cena_ilosc[0])) / ilosc_do_przeslania

        print "____________koniec_ " + waluta + "_______________\n\n\n"


if __name__ == '__main__':
    main()
