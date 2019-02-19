#!/usr/bin/python3

from decimal import *
from bs4 import BeautifulSoup
import urllib.request

beerurl = "https://demeter.dtek.se/wiki/Delta/Hllista"

class Beer:
    def __init__(self, name, type, country, perc, vol, price):
        self.name = name
        self.type = type
        self.country = country
        self.perc = perc
        self.vol = vol
        self.price = price
        self.apk = (vol * (perc / 100)) / price
        self.apk = self.apk.quantize(Decimal('.01'), rounding=ROUND_DOWN)

    def to_string(self):
        s = ","
        return str(self.name) + s + self.type + s + self.country + s + \
        str(self.perc) + "%" + s + str(self.vol) + "ml" + s + str(self.price) + "kr" + s + str(self.apk)

def item_to_beer(item):
    res = ""
    entry = item.find_all("td")
    if len(entry) < 7:
        return False

    name = entry[1].get_text()
    type = entry[2].get_text()
    country = entry[3].get_text()
    perc = Decimal(entry[4].get_text().replace("%", ""))
    vol = int(entry[5].get_text().replace("ml", ""))
    price = int(entry[6].get_text().replace("kr", ""))

    return Beer(name, type, country, perc, vol, price)


with urllib.request.urlopen(beerurl) as response:
    soup = BeautifulSoup(response, 'html.parser')
    table = soup.find("div", id="wikitext").find("table")

    beer_map = {}

    for item in table.find_all("tr"):
        beer = item_to_beer(item)
        if beer != False:
            beer_map[beer.name] = beer

    list = [(v) for k,v in beer_map.items()]
    list.sort(key=lambda b: b.apk, reverse=True)
    i = 1
    for beer in list:
            print(str(i) + "," + beer.to_string())
            i = i + 1

    print (len(list))
