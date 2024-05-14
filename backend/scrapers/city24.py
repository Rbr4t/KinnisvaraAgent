import requests
import os
import json
import random
import time
from bs4 import BeautifulSoup

# Accessing the API
url = "https://api.city24.ee/et_EE/search/realties?address%5Bcc%5D=1&address%5Bcity%5D%5B%5D=20411&tsType=rent&unitType=Apartment&adReach=1&itemsPerPage=50&page=1"
headers_file = open(
    "/home/rbr4t/KinnisvaraAgent/backend/scrapers/user_agents.txt", "r")
headers = headers_file.readlines()
headers_file.close()


def getDescriptionCity(url):
    page = requests.get(
        url, headers={"User-Agent": headers[random.randint(0, 1000)].strip()})
    soup = BeautifulSoup(page.content, "html.parser")
    description = soup.find(
        "div", class_="object-description__description").text
    return description


def queryAllCity():
    resp = requests.get(
        url, headers={"User-Agent": headers[random.randint(0, 1000)].strip()})
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
        full_data.append(obj)

    print(len(full_data))
    # json_object = json.dumps(full_data, indent=4)

    # os.remove("./../scraped_data/korteridCity.json")
    # time.sleep(1)
    # with open("./../scraped_data/korteridCity.json", "w") as outfile:
    #     outfile.write(json_object)
    return full_data
