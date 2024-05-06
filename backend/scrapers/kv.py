import requests
import re
import os
import random
import time
import json
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from datetime import datetime

headers_file = open("user_agents.txt", "r")
headers = headers_file.readlines()
headers_file.close()

flag = True

# This is how I'm going to extract more info for future development, that search url is going to give me all the necessary links


def get_descriptionKV(url):

    page = requests.get(
        url, headers={"User-Agent": headers[random.randint(0, 1000)].strip()})
    print(page.content)
    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find("p", class_="description-content")
    return content.text


def queryAllKV():
    global flag
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
            continue

        try:
            elements = soup.find(
                "div", class_="results results-default").find_all("article")
        except AttributeError:
            time.sleep(random.randint(1, 5))
            continue

        for e in elements:
            if "BRONEERITUD" in e.text:
                continue
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
                "permalink":  "https://www.kv.ee/" + e['data-object-id'],
                "published": datetime.now().isoformat()
            }
            print(obj["permalink"])
            full_data.append(obj)

        page_number += 100
        time.sleep(random.randint(1, 5))

    session.close()
    print(len(full_data))
    json_object = json.dumps(full_data, indent=4)

    os.remove("./scraped_data/korteridKV.json")
    time.sleep(1)
    with open("./scraped_data/korteridKV.json", "w") as outfile:
        outfile.write(json_object)


queryAllKV()
