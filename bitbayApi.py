from exceptions import Exception
from datetime import datetime
import csv
import bs4 as bs
import lxml
import re
import requests
import json

r = requests.get("https://bitbay.net/API/Public/BTCPLN/orderbook.json")

print json.dumps( r.json())

bids = json.dumps(r.json()['bids'])
print bids



# asks = json.dumps(r.json()['asks'])
# print asks

# transactions = json.dumps(r.json()['transactions'])
# print transactions

