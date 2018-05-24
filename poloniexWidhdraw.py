import requests


# zwraca withdraw z poloniex np. dla waluty BTC 0.0005
def getPoloniexWithdrawFee(waluta):
    response = requests.get("https://poloniex.com/public?command=returnCurrencies")
    data = response.json()
    return float(data[waluta]['txFee'])


def zwroc_lista_waluta_withdraw_poloniex():
    response = requests.get("https://poloniex.com/public?command=returnCurrencies")
    data = response.json()
    lista_waluta_withdraw = []
    for waluta in data:
        withdraw = data[waluta]['txFee']
        lista_waluta_withdraw.append([str(waluta), float(withdraw)])

    return lista_waluta_withdraw


# print zwroc_lista_waluta_withdraw()
