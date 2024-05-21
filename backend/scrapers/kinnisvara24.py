import requests
import os
import json
import random
import time
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from . import proxy

proxy = proxy.getProxy()


def remove_slug_from_url(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    # Assuming that the slug is the last part of the path
    path_segments.pop(len(path_segments)-2)
    new_path = '/'.join(path_segments)
    new_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, new_path, '', '', ''))
    return new_url


headers_file = open(
    "./scrapers/user_agents.txt", "r")
headers = headers_file.readlines()
headers_file.close()

url = "https://kinnisvara24.ee/search"

url_dict = {}


def getDescriptionKinnisvara(url, url_dict):
    return url_dict.get(url, None)


def queryRegularKinnisvara(permalinks):
    RUN = True
    search_obj = {
        "hash": None,
        "addresses": [
        ],
        "area_min": None,
        "area_max": None,
        "land_area_min": None,
        "land_area_max": None,
        "around_point": None,
        "bounds": [],
        "broker_id": None,
        "bureau_id": None,
        "build_year_min": None,
        "build_year_max": None,
        "client_day_date_max": None,
        "client_day_date_min": None,
        "comforts": [],
        "commercial_types": [],
        "deal_types": ["rent"],
        "developments_only": False,
        "energy_classes": [],
        "exclusives": False,
        "uniques": False,
        "extras": [],
        "floor_min": None,
        "floor_max": None,
        "from_owner": False,
        "with_detail_planning_only": False,
        "with_building_permit_only": False,
        "with_360_tour_only": False,
        "with_video_only": False,
        "intended_uses": [],
        "keywords": [],
        "materials": [],
        "object_types": ["apartment"],
        "price_max": None,
        "price_min": None,
        "price_per_m2_max": None,
        "price_per_m2_min": None,
        "land_price_per_m2_max": None,
        "land_price_per_m2_min": None,
        "water_supplies": [],
        "heating_types": [],
        "energy_sources": [],
        "rooms_max": None,
        "rooms_min": None,
        "sewage_types": [],
        "sort_by": "created_at",
        "sort_order": "desc",
        "page": 1,
        "utility_join_fees_paid": False,
        "has_repairs_canal": False,
        "is_development_lot": False,
        "is_top_floor": False,
        "has_water_border": False,
        "pets_allowed": False,
        "with_usage_permit": False,
        "has_client_day": False,
        "free": False,
        "amount": None,
        "rooms": None,
        "period": None,
        "has_furniture": None,
        "has_washing": False,
        "are_pets_allowed": False,
        "show_deactivated": False,
        "price_without_utilities": False,
        "has_kitchen": False,
        "has_job_possibility": False,
        "additional": [],
        "house_part_types": [],
        "conditions": [],
        "neighbours": [],
        "road_conditions": [],
        "address": [],
    }

    full_data = []
    while RUN:
        z = requests.post(url, json=search_obj, headers={
            "User-Agent": headers[random.randint(0, 999)].strip(), "Accept": "application/json"}, proxies=proxy)
        print(search_obj["page"])

        try:
            if len(z.json()["data"]) == 0:
                RUN = False
            for d in z.json()["data"]:
                if d["disabled_text"]:
                    continue
                # Check if that permalink is already in the DB, if it is, then stop the search
                if remove_slug_from_url(d["permalink"]) in permalinks:
                    RUN = False
                    break

                # More info can be extracted with more attributes
                full_data.append({
                    "address": d["address"],
                    "price": d["hind"],
                    "area": float(d["area"]),
                    "rooms": d["rooms"],
                    "permalink": remove_slug_from_url(d["permalink"]),
                    "published": d["created_at"]
                })

                soup = BeautifulSoup(d["lisainfo"], "lxml")
                url_dict[remove_slug_from_url(d["permalink"])] = soup.text

            search_obj["page"] += 1

        except json.decoder.JSONDecodeError:
            pass

    print(len(full_data))

    return full_data, url_dict


def queryAllKinnisvara():
    RUN = True
    search_obj = {
        "hash": None,
        "addresses": [],
        "area_min": None,
        "area_max": None,
        "land_area_min": None,
        "land_area_max": None,
        "around_point": None,
        "bounds": [],
        "broker_id": None,
        "bureau_id": None,
        "build_year_min": None,
        "build_year_max": None,
        "client_day_date_max": None,
        "client_day_date_min": None,
        "comforts": [],
        "commercial_types": [],
        "deal_types": ["rent"],
        "developments_only": False,
        "energy_classes": [],
        "exclusives": False,
        "uniques": False,
        "extras": [],
        "floor_min": None,
        "floor_max": None,
        "from_owner": False,
        "with_detail_planning_only": False,
        "with_building_permit_only": False,
        "with_360_tour_only": False,
        "with_video_only": False,
        "intended_uses": [],
        "keywords": [],
        "materials": [],
        "object_types": ["apartment"],
        "price_max": None,
        "price_min": None,
        "price_per_m2_max": None,
        "price_per_m2_min": None,
        "land_price_per_m2_max": None,
        "land_price_per_m2_min": None,
        "water_supplies": [],
        "heating_types": [],
        "energy_sources": [],
        "rooms_max": None,
        "rooms_min": None,
        "sewage_types": [],
        "sort_by": "created_at",
        "sort_order": "desc",
        "page": 1,
        "utility_join_fees_paid": False,
        "has_repairs_canal": False,
        "is_development_lot": False,
        "is_top_floor": False,
        "has_water_border": False,
        "pets_allowed": False,
        "with_usage_permit": False,
        "has_client_day": False,
        "free": False,
        "amount": None,
        "rooms": None,
        "period": None,
        "has_furniture": None,
        "has_washing": False,
        "are_pets_allowed": False,
        "show_deactivated": False,
        "price_without_utilities": False,
        "has_kitchen": False,
        "has_job_possibility": False,
        "additional": [],
        "house_part_types": [],
        "conditions": [],
        "neighbours": [],
        "road_conditions": [],
        "address": [],
    }

    full_data = []
    while RUN:
        z = requests.post(url, json=search_obj, headers={
            "User-Agent": headers[random.randint(0, 999)].strip(), "Accept": "application/json"}, proxies=proxy)
        print(search_obj["page"])

        try:
            if len(z.json()["data"]) == 0:
                RUN = False
            for d in z.json()["data"]:
                if d["disabled_text"]:
                    continue
                # More info can be extracted with more attributes

                full_data.append({
                    "address": d["address"],
                    "price": d["hind"],
                    "area": float(d["area"]) if d.get("area") is not None else None,
                    "rooms": d["rooms"],
                    "permalink": remove_slug_from_url(d["permalink"]),
                    "published": d["created_at"]
                })

                soup = BeautifulSoup(d["lisainfo"], "lxml")
                url_dict[remove_slug_from_url(d["permalink"])] = soup.text

            search_obj["page"] += 1

        except json.decoder.JSONDecodeError:
            pass

    print(len(full_data))

    return full_data, url_dict
