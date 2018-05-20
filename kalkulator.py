#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bitbay import *
from poloniexAPI import *
from poloniexWidhdraw import zwroc_lista_waluta_withdraw_poloniex
import re
import time
import requests


# ================ bids - oferty kupna asks - oferty sprzedazy ===========================
# ================ "maker" i "taker"======================================================
# jak wystawiasz oferte to placisz 0.30% a jak bierzesz jakas oferte to cos kolo 0.40%
# ================ wystawiasz czyli maker, bierzesz - taker ==============================
def znajdz_withdraw(waluta, lista_waluta_withdraw):
    for waluta_koszt in lista_waluta_withdraw:
        if waluta_koszt[0] == waluta:
            return waluta_koszt[1]


# Kalkulator wysylki BTC
class Kalkulator:
    def __init__(self):
        self.ilosc_do_przeslania = self.walidacja_inputu('wprowadz ilość BTC do przesłania:  ')
        self.gielda_bazowa = self.walidacja_wyboru_gieldy(
            'wybierz gielde bazowa 1 - bitbay, 2 - poloniex:  ')
        self.gielda_docelowa = self.walidacja_wyboru_gieldy(
            'wybierz gielde docelowa 1 - bitbay, 2 - poloniex:  ')

        # to waluty dostepne na danej gieldzie [['XVC'], ['SRCC']]
        self.lista_walut_gielda_bazowa = []
        self.lista_walut_gielda_docelowa = []
        # to lista kosztow wycofania z gieldy bazowej np. [['XVC', 0.01], ['SRCC', 0.01]]
        self.lista_waluta_withdraws = []
        self.pobierz_liste_walut()

        self.lista_waluta_ilosc_po_przewalutowaniu_bazowa = []
        self.lista_uzywa_waluta_ilosc_docelowa = []
        pass

    @staticmethod
    def walidacja_inputu(promt):
        while True:
            inp = raw_input(promt)
            num_format = re.compile("^[0-9](\.*[0-9]{0,8})$")
            isnumber = re.match(num_format, inp)
            if isnumber:
                return float(inp)
            else:
                print 'nieprawidłowy format!'

    @staticmethod
    def walidacja_wyboru_gieldy(promt):
        while True:
            inp = raw_input(promt)
            num_format = re.compile("^[0-2]$")
            isnumber = re.match(num_format, inp)
            if isnumber:
                return float(inp)
            else:
                print 'nieprawidłowy format!'

    def pobierz_liste_walut(self):
        # dla gieldy bazowej zwracam  self.lista_waluta_withdraws= [['XVC', 0.01], ['SRCC', 0.01]] kosztow wycofania
        # lista_walut_gielda_bazowa = [['XVC'], ['SRCC']]
        # gielda Bazowa
        # bitbay
        if self.gielda_bazowa == 1:
            self.lista_waluta_withdraws = get_bitbay_withdrawals()
            # dla gieldy bazowej zwracam liste [['XVC', 0.01], ['SRCC', 0.01]] kosztow wycofania
            self.lista_walut_gielda_bazowa = zwroc_liste_walut_bitbay()
        # poloniex
        if self.gielda_bazowa == 2:
            polo = poloniex(ApiKey, secret)
            for para_walutowa in polo.returnOrderBook("all"):
                if para_walutowa[0:3] == "BTC":
                    # print para_walutowa
                    a, waluta = para_walutowa.split("_")
                    self.lista_walut_gielda_bazowa.append(str(waluta))
                    # dla gieldy bazowej zwracam liste [['XVC', 0.01], ['SRCC', 0.01]] kosztow wycofania
            self.lista_waluta_withdraws = zwroc_lista_waluta_withdraw_poloniex()

        # gielda Docelowa
        if self.gielda_docelowa == 1:
            self.lista_walut_gielda_docelowa = zwroc_liste_walut_bitbay()
        if self.gielda_docelowa == 2:
            polo = poloniex(ApiKey, secret)
            for para_walutowa in polo.returnOrderBook("all"):
                if para_walutowa[0:3] == "BTC":
                    # print para_walutowa
                    a, waluta = para_walutowa.split("_")
                    self.lista_walut_gielda_docelowa.append(str(waluta))

    def licz_wysylka_bez_przewalutowania(self):
        print "ilość BTC bez przewalutowania"
        print self.ilosc_do_przeslania - znajdz_withdraw("BTC", self.lista_waluta_withdraws)

    def zwroc_orderbook(self, waluta1, waluta2, kupno_sprzedaz):
        # zwracam najbardziej korzystna cene danej kryptowaluty
        # na razie zwracam pierwsza oferte pozniej będę sumował oferty tak aby suma równa była ilości do przesłania
        if self.gielda_bazowa == 1:
            return zwroc_orderbook_bitbay(waluta2, waluta1, kupno_sprzedaz)[0][0]

        if self.gielda_bazowa == 2:
            time.sleep(0.3)
            p = poloniex(ApiKey, secret)
            data = p.returnOrderBook(waluta1 + "_" + waluta2)
            # zwraca cena i ilosc [u'0.01644212', 6.16528876]

            data = data[kupno_sprzedaz]
            # zwracam cene danej kryptowaluty
            return float(data[0][0])

    def zwroc_orderbook_bids(self, waluta1, waluta2):
        # zwracam najbardziej korzystna cene danej kryptowaluty
        # na razie zwracam pierwsza oferte pozniej będę sumował oferty tak aby suma równa była ilości do przesłania
        if self.gielda_docelowa == 1:
            return zwroc_orderbook_bitbay(waluta2, waluta1, "bids")[0][0]

        if self.gielda_docelowa == 2:
            time.sleep(0.2)
            p = poloniex(ApiKey, secret)
            data = p.returnOrderBook(waluta1 + "_" + waluta2)
            # zwraca cena i ilosc [u'0.01644212', 6.16528876]
            data = data["bids"]
            # zwracam cene danej kryptowaluty
            return float(data[0][0])

    def licz_z_przewalutowaniem(self):
        # wzor na przesyl
        # ilosc_do_przeslania - koszt_wycofania
        # wzor na ilosc kupowanej kryptowaluty np game
        # ilosc = (ilosc_do_przeslania / cena_kryptowaluty)
        # po drugiej stronie  ilosc * bids

        print "pobieranie danych... to może potrwać chwilę"
        for waluta in self.lista_walut_gielda_bazowa:
            if waluta in self.lista_walut_gielda_docelowa and waluta != "BTC":
                ilosc_po_przewalutowaniu = self.ilosc_do_przeslania / self.zwroc_orderbook("BTC", waluta, "asks")
                ilosc_po_przewalutowaniu -= get_specyfic_withdrawals_fee(waluta, self.lista_waluta_withdraws)
                self.lista_waluta_ilosc_po_przewalutowaniu_bazowa.append([waluta, ilosc_po_przewalutowaniu])

        for waluta, ilosc in self.lista_waluta_ilosc_po_przewalutowaniu_bazowa:
            ilosc_btc = ilosc * self.zwroc_orderbook_bids("BTC", waluta)
            self.lista_uzywa_waluta_ilosc_docelowa.append([waluta, ilosc_btc])
            pass

        print self.lista_uzywa_waluta_ilosc_docelowa


if __name__ == '__main__':
    ApiKey = "-"
    secret = "-"

    k = Kalkulator()
    k.licz_wysylka_bez_przewalutowania()
    k.licz_z_przewalutowaniem()
