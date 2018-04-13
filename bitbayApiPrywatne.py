from exceptions import Exception
import requests
import hashlib
import hmac
import time
import urllib
import requests
import json

# r = requests.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json")

# print json.dumps(r.json())
#
# bids = json.dumps(r.json()['bids'])
# print bids
# asks = json.dumps(r.json()['asks'])
# print asks

# transactions = json.dumps(r.json()['transactions'])
# print transactions


#tu podaj klucz prywatny
secret = ""
#tu podaj klucz publiczny
apiKey = ""
bid = []
ask = []


def get_orderbook():
    timestamp = int(time.time())
    data = urllib.urlencode((
        ('method', 'orderbook'),
        ('order_currency', 'BTC'),
        ('payment_currency', 'PLN'),
        ('moment', timestamp)))
    apihash = hmac.new(secret, data.encode('utf-8'), hashlib.sha512).hexdigest()
    res = requests.post('https://bitbay.net/API/Trading/tradingApi.php',
                        headers={
                            'API-Key': apiKey,
                            'API-Hash': apihash,
                        },
                        data=data
                        )
    data = res.json()
    bids = data['bids']
    asks = data['asks']
    for item in bids:
        bid.append(item)
        # print(item)
    for item in asks:
        ask.append(item)
        # print(item)
    print('bids: ', bid[0], '\nasks: ', ask[0])



def main():
    while True:
        get_orderbook()
        time.sleep(2)  # na bitbay najlepiej co 1 sekunde


main()
