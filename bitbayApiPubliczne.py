import requests
crypto = "BTCPLN"
# get info from public api
response = requests.get("https://bitbay.net/API/Public/"+crypto+"/orderbook.json")
data = response.json()
print(response)
bid = []
ask = []
bids = data['bids']

for item in bids:
    bid.append(item)
    print(item)

print('pierwsza: ', bid[0])