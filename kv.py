import requests
import re
import os
import random
import time
import json
from bs4 import BeautifulSoup
from requests_html import HTMLSession

headers_file = open("user_agents.txt", "r")
headers = headers_file.readlines()
headers_file.close()

# This is how I'm going to extract more info for future development, that search url is going to give me all the necessary links
"""
url2 = "https://www.kv.ee/armas-privaatne-taiesti-omaette-sissepaasuga-korte-3059543.html"

page2 = requests.get(url2, headers=headers)
print()
y = open("output2.txt", "w")
y.write(page2.text)
y.close()
"""

session = HTMLSession()
page_number = 0
full_data = []
while True:
    url = f"https://www.kv.ee/search?orderby=ob&deal_type=2&county=12&parish=1063&limit=100&start={page_number}"
    page = requests.get(
        url, headers={"User-Agent": headers[random.randint(0, 1000)].strip()})

    soup = BeautifulSoup(page.content, "html.parser")
    if "Tulemusi ei leitud" in soup.text:
        print("END")
        break
    elif "KV.EE ikka ei avane?" in soup.text:
        print("ERROR")
        time.sleep(random.randint(10, 20))
        continue
    # elif "Turvakontroll" in soup.text:
    #     print("TURVAKONTROLL")
    #     time.sleep(random.randint(10, 20))
    #     continue

    try:
        elements = soup.find(
            "div", class_="results results-default").find_all("article")
    except AttributeError:
        with open("output.txt", "w") as file:
            file.write(soup.text)

    for e in elements:
        try:
            rooms = int(e.find("div", class_="rooms").contents[0].strip())
        except ValueError:
            rooms = None

        try:
            area = float(re.search(
                r'\d+', e.find("div", class_="area").contents[0].strip().split(r'"\d"')[0]).group())
        except ValueError:
            area = None

        obj = {
            "rooms": rooms,
            "price": int(e.find("div",
                                class_="price").contents[0].encode("ascii", "replace").decode('UTF-8').replace("?", "").strip()),
            "area": area,
            "permalink":  "https://www.kv.ee" + e['data-object-url']
        }
        full_data.append(obj)

    page_number += 100
    time.sleep(random.randint(1, 5))

session.close()
print(len(full_data))
json_object = json.dumps(full_data, indent=4)

os.remove("korteridKV.json")
with open("korteridKV.json", "w") as outfile:
    json.dump([], outfile)
    outfile.write(json_object)
