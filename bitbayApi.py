from exceptions import Exception
from datetime import datetime
import csv
import bs4 as bs
import lxml
import re
import requests


r = requests.get("https://bitbay.net/API/Public/BTCPLN/ticker.json")

print r.json()


