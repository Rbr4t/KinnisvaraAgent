import requests
import os
import json
import random
import time
from bs4 import BeautifulSoup
from . import proxy
# Accessing the API
url = "https://api.city24.ee/et_EE/search/realties?address%5Bcc%5D=1&address%5Bcity%5D%5B%5D=20411&tsType=rent&unitType=Apartment&order[datePublished]=desc&adReach=1&itemsPerPage=50&page=1"
headers_file = open(
    "./scrapers/user_agents.txt", "r")
headers = headers_file.readlines()
headers_file.close()

proxy = proxy.getProxy()


def getDescriptionCity(url):
    page = requests.get(
        url, headers={"User-Agent": headers[random.randint(0, 1000)].strip()}, proxies=proxy)
    soup = BeautifulSoup(page.content, "html.parser")
    description = soup.find(
        "div", class_="object-description__description").text
    return description


def queryAllCity():
    resp = requests.get(
        url, headers={"User-Agent": headers[random.randint(0, 1000)].strip()}, proxies=proxy)
    full_data = []
    for d in resp.json():
        if d["booked"]:
            continue

        # More info can be extracted with more attributes
        obj = {
            "price": float(d["price"]),
            "area": d["property_size"],
            "rooms": d["room_count"],
            "permalink": "https://www.city24.ee/real-estate/" + d["friendly_id"],
            "published": d["date_published"]
        }

        # Check if that permalink is already in the DB, if it is, then stop the search

        full_data.append(obj)

    print(len(full_data))

    return full_data
