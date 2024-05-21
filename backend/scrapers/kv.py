from curl_cffi import requests

import re
import os
import random
import time
from bs4 import BeautifulSoup
from datetime import datetime
from . import proxy

headers_file = open(
    "./scrapers/user_agents.txt", "r")
headers = headers_file.readlines()
headers_file.close()

flag = True

# This is how I'm going to extract more info for future development, that search url is going to give me all the necessary links


proxy = proxy.getProxy()


def getDescriptionKV(url):
    errors = 0
    while True:
        page = requests.get(
            url, headers={"User-Agent": headers[random.randint(0, 999)].strip()}, impersonate="chrome101", proxies=proxy)
        soup = BeautifulSoup(page.content, "html.parser")
        print(page)
        try:
            description = soup.find("p", class_="description-content").text
            break
        except AttributeError as e:
            print(e)
            errors += 1
            if errors == 10:
                return ""
            pass
    return description


def queryRegularKV(permalinks):
    global flag
    page_number = 0
    full_data = []
    RUN = True
    while RUN:
        print(page_number)
        url = f"https://www.kv.ee/search?orderby=ob&deal_type=2&limit=100&start={page_number}&orderby=cdwl"
        page = requests.get(
            url, headers={"User-Agent": headers[random.randint(0, 1000)].strip()}, proxies=proxy)

        soup = BeautifulSoup(page.content, "html.parser")
        if "Tulemusi ei leitud" in soup.text:
            print("END")
            break
        elif "KV.EE ikka ei avane?" in soup.text:
            print("ERROR")
            time.sleep(random.randint(0, 5))

            continue

        try:
            elements = soup.find(
                "div", class_="results results-default").find_all("article")
        except AttributeError:
            print("CANT FIND")
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

            # try:
            address = e.find("div", class_="description").find("h2")[
                1].contents
            print(address)

            obj = {
                "rooms": rooms,
                "price": int(e.find("div",
                                    class_="price").contents[0].encode("ascii", "replace").decode('UTF-8').replace("?", "").strip()),
                "area": area,
                "permalink":  "https://www.kv.ee/" + e['data-object-id'],
                "published": datetime.now().isoformat()
            }

            # Check if that permalink is already in the DB, if it is, then stop the search
            if "Tasemeteenus muudab Sinu kuulutuse rohkem nähtavamaks tõstes selle KV.EE otsingutes ettepoole." not in e.text:
                if "https://www.kv.ee/" + e['data-object-id'] in permalinks:
                    RUN = False
                    break

            full_data.append(obj)

        page_number += 100

    print(len(full_data))

    return full_data


def queryAllKV():

    global flag
    page_number = 0
    full_data = []
    RUN = True
    while RUN:
        print(page_number)

        cookies = {
            'INTRESS_PERCENT_EST': '6.1',
            'LVO': '3629551',
            'PHPSESSID': 'j5rta7bcj73ib4rdiahe9rviv172gnq1',
            '__cf_bm': 'KmjOqor86I0Y5B9akZSuER7gQ7vEn2Ponwcuy5jzdlU-1716289933-1.0.1.1-6yKQMg0bB8blL.cK3.iVzxXTAunlKkRMBPSeMqKIqWTGqeXDbFRP6pNSPQaHzcNn5aBGKfIU9xXZyJaO3.PmrA',
            'interest': '6.1',
            'list_view': 'default',
            'saved_searches': '2e4e74a12692ee7b2dff57022b1bf929',
        }
        url = f"https://www.kv.ee/search?orderby=ob&deal_type=2&limit=100&start={page_number}&orderby=cdwl"
        while True:
            try:

                page = requests.get(
                    url, cookies=cookies, headers={
                        "User-Agent": headers[random.randint(0, 1000)].strip(),
                        'Accept': 'application/json, text/javascript, */*; q=0.01'
                    }, proxies=proxy, impersonate="chrome101")
                elements = page.json()["objects"]
                soup = BeautifulSoup(page.json()["content"], "html.parser")
                addresses = list(soup.find(
                    "div", class_="results results-default").find_all("article"))
                break
            except:
                pass

        if page_number > page.json()["counts"]:
            RUN = False
        for index, e in enumerate(elements):
            try:
                address = addresses[index].find(
                    "div", class_="description").h2.find_all("a")[-1].text.strip()
            except IndexError:
                address = addresses[index].find(
                    "div", class_="description").h2.a.text.strip()

            try:
                rooms = int(addresses[index].find(
                    "div", class_="rooms").contents[0].strip())
            except ValueError:
                rooms = None

            try:
                area = float(re.search(
                    r'\d+', addresses[index].find("div", class_="area").contents[0].strip().split(r'"\d"')[0]).group())
            except:
                area = None

            obj = {
                "address": address,
                "rooms": rooms,
                "price": e["price_eur"],
                "area": area,
                "permalink":  "https://www.kv.ee/" + str(e['object_id']),
                "published": e["date_activated"]
            }

            full_data.append(obj)

        page_number += 100

    print(len(full_data))

    return full_data
