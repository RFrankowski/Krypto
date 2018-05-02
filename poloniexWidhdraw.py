import requests
# zwraca withdraw z poloniex np. dla waluty BTC 0.0005
def getPoloniexWithdrawFee(waluta):
    response = requests.get("https://poloniex.com/public?command=returnCurrencies")
    data = response.json()
    return float(data[waluta]['txFee'])
