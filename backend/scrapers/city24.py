import requests
import os
import json
import random
import re
from bs4 import BeautifulSoup
from . import proxy
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

proxy = proxy.getProxy()

# Accessing the API

headers_file = open(
    "./scrapers/user_agents.txt", "r")
headers = headers_file.readlines()
headers_file.close()


def getDescriptionCity(url):
    errors = 0
    while True:

        page = requests.get(
            url, headers={"User-Agent": headers[random.randint(0, 999)].strip()}, proxies=proxy)
        soup = BeautifulSoup(page.content, "html.parser")

        try:
            description = soup.find(
                "div", class_="object-description__description").text
            break
        except AttributeError as e:
            print(e)
            errors += 1
            if errors == 10:
                return ""
            pass
    return description


def query(permalinks=[]):
    url = "https://api.city24.ee/et_EE/search/realties?address[cc]=1&tsType=rent&unitType=Apartment&order[datePublished]=desc&adReach=1&itemsPerPage=1000&page=1"

    full_data = []
    RUN = True
    while RUN:
        while True:
            try:
                resp = requests.get(
                    url, headers={"User-Agent": headers[random.randint(0, 999)].strip()}, proxies=proxy)
                break
            except:
                pass
        if len(resp.json()) == 0:
            RUN = False
        for d in resp.json():

            if d["booked"]:
                continue
            if datetime.fromisoformat(d["date_published"].replace("Z", "")).date() < (date.today() - relativedelta(months=1)):

                RUN = False
                break

            # Check if that permalink is already in the DB, if it is, then stop the search
            if "https://www.city24.ee/real-estate/" + d["friendly_id"] in permalinks:
                break

            # More info can be extracted with more attributes
            obj = {
                "address": f"{d['address']['county_name']}, {d['address']['parish_name']}, {d['address']['city_name']}, {d['address']['district_name']}, {d['address']['street_name']}, {d['address']['house_number']}".replace(", None", ""),
                "price": float(d["price"]) if d.get("price") is not None else None,
                "area": d["property_size"],
                "rooms": d["room_count"],
                "permalink": "https://www.city24.ee/real-estate/" + d["friendly_id"],
                "published": d["date_published"]
            }

            full_data.append(obj)
        pattern = re.compile(r'(&page=)(\d+)')

        def increment(match):

            # Extract the current page number
            current_page = int(match.group(2))
            print(current_page)

            # Increment the page number
            incremented_page = current_page + 1
            # Return the replacement string with the incremented page number
            return f"{match.group(1)}{incremented_page}"

        # Use re.sub to replace the matched pattern with the incremented page number
        url = re.sub(pattern, increment, url)

    print(len(full_data))

    return full_data
