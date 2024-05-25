from curl_cffi import requests

import re
import os
import random
import time
from bs4 import BeautifulSoup
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from . import proxy

headers_file = open(
    "./scrapers/user_agents.txt", "r")
headers = headers_file.readlines()
headers_file.close()

proxy = proxy.getProxy()


def getDescriptionKV(url):
    errors = 0
    while True:
        page = requests.get(
            url, headers={"User-Agent": headers[random.randint(0, 999)].strip()}, impersonate="safari", proxies=proxy)
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


def query(permalinks=[]):

    page_number = 0
    full_data = []
    RUN = True
    while RUN:
        print(page_number)

        cookies = {
            "__cf_bm": "bAPfnIxANV2WBiXcADb9NBbREBhVu6wlSToYhQtVRrA-1716666599-1.0.1.1-ZogJHN1ZxFHNf0WuvpgBkNJ42WmScYQUjZ.D5bHx2mOSkwY7x7JEjSPx3yAXZxOcGtNDCwNayAsCeKsN0WvOjw",
            "eupubconsent-v2": "CP8y4wgP8y4wgAcABBENAvEsAP_gAAAAAChQJwtX_D5ebWtj8XJUIftkaYwf55izokQxBhaIke4FwIOG7BgGH2EwNAU4JiQCGBAEkiIBAQFlHABUAQAAAIgRiTCMYkGMgTNKJKBAgFMRa0NYCB5mmAFDWQCY5kosM3d5mTeAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABYAAADAkCsABAACwAKgAcAA8ACAAF8AMgA1AB4AEQAJgAVQA3gB-AEJAIgAiQBHACWAE0AMAAYYAywBsgD4gH2AfsA_wEAgIuAjABGoCRAJKAT8AqABcwDFAG0ANxAj0CRAE7AKHAUiAtgBcgC7wF5hABQADgASAEHAI4AX0BKwCZQFIALEAXkOALgAIgAcAB4AFwASAA_ACgAGgARwA5ACAAEHAIiARwAqAB0gErAJiATKApMBVQCxAF0AMEHQLwAFgAVAA4ACAAF8AMQA1AB4AEQAJgAVYAuAC6AGIAN4AfoBEAESAJYATQAwABhgDZgH2AfoA_4CLAIxAR0BJQCfgFzALyAYoA2gBuAD7AIvgR6BIgCZAE7AKHAUgAsUBbAC3QFyALtAXeAvMBfQE3gJwkABQACAAHgBoAHIARwAvoCkwFiALyAYIQgJAALABiADUAJgAVQAuABiADeAI4AYAA_wC5gGKANoAj0BYoC0QFyEoDAACAAFgAcABiADwAIgATAAqgBcADFAIgAiQBHADAAGyAPwAuYBigETAIvgR6BIgCxQFsALzAnCSAEAAXAIAAQcAjgBUAErAJiAUmUAIgAKAAuACQARwA5AB9gEAAIOAa8A7YB_wExAKkAXQAvIBggE4SkCUABYAFQAOAAggBiAGoAPAAiABMACqAGIAP0AiACJAGAANmAfgB-gEWAIxAR0BJQC5gF5AMUAbQA3AB9gETAIvgR6BIgCdgFDgKQAWKAtgBcgC7QF5gL6Am8WgCAA1AEcAMAA-xYAIAMsAjgCPQExAAAA.f_wAAAAAAAAA",
            "interest": "6.1",
            "INTRESS_PERCENT_EST": "6.1",
            "list_view": "default",
            "LVO": "3637515|3651150|3441766|3633065|3648750|2936897|3640519|3637126|3516688|3488676|2059222|3631740|3611791|3627892|3645560|3645457|3562524|3649730|3646552|3649098|3604728|3226815|3625574|3465537|3640138|3547936|2618735|3642640|3629551|3616702|3333545|3614622|1890877|3550464|3059543|3329422|3633471|3625272",
            "OptanonAlertBoxClosed": "2024-04-09T11:14:27.034Z",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Sat+May+25+2024+22:59:07+GMT+0300+(Eastern+European+Summer+Time)&version=202311.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5960c1e9-548d-4fef-85df-a3cce069a3ba&interactionCount=1&landingPath=NotLandingPage&groups=C0003:1,C0001:1,C0004:1,C0002:1,V2STACK42:1&geolocation=;&AwaitingReconsent=false",
            "other_objects_side": "narco",
            "PHPSESSID": "9qgseeanappmhkigcd0dvfsn6hore3ck",
            "saved_searches": "2e4e74a12692ee7b2dff57022b1bf929"
        }
        url = f"https://www.kv.ee/search?orderby=ob&deal_type=2&limit=100&start={page_number}&orderby=cdwl"
        while True:
            try:
                page = requests.get(
                    url, cookies=cookies, headers={
                        "User-Agent": headers[random.randint(0, 1000)].strip(),
                        'Accept': 'application/json, text/javascript, */*; q=0.01'
                    }, proxies=proxy, impersonate="safari")
                elements = page.json()["objects"]
                soup = BeautifulSoup(page.json()["content"], "html.parser")
                addresses = list(soup.find(
                    "div", class_="results results-default").find_all("article"))
                break
            except Exception as e:
                print(e)
                pass

        if page_number > page.json()["counts"]:
            RUN = False

        for index, e in enumerate(elements):
            if "https://www.kv.ee/" + str(e['object_id']) in permalinks:
                continue
            if datetime.fromisoformat(e["date_activated"].rsplit(".", 1)[0]).date() < (date.today() - relativedelta(months=1)):
                RUN = False
                break
            if e["price_eur"] < 100:
                continue
            if "BRONEERITUD" in addresses[index].text:
                continue

            try:
                address = addresses[index].find(
                    "div", class_="description").h2.find_all("a")[-1].text.strip().split(", ")
            except IndexError:
                address = addresses[index].find(
                    "div", class_="description").h2.a.text.strip().split(", ")

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
                "address": address[0].replace("maa", " maakond, ") + ", ".join(address[1:]),
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
