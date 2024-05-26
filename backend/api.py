from fastapi import APIRouter
from database import Session
from models import Flat, Search
from datetime import datetime
from scrapers import kinnisvara24, kv, city24
import json
from pydantic import BaseModel
from difflib import ndiff
from typing import Optional
from thefuzz import fuzz
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from curl_cffi import requests
import random
from scrapers import proxy


API = APIRouter()

API.get("/")


def index():
    return {"status": 200}


def check_all_entries():
    headers_file = open(
        "./scrapers/user_agents.txt", "r")

    headers = headers_file.readlines()
    headers_file.close()

    proxy = proxy.getProxy()

    removed_flats = 0
    with Session() as session:
        flats = session.query(Flat).all()

        for flat in flats:
            errors = 0
            try:
                resp = requests.get(flat.permalink, headers={
                                    "User-Agent": headers[random.randint(0, 999)].strip()}, impersonate="safari", proxies=proxy)
                if resp.status_code != 200:
                    session.query(Flat).filter(Flat.id == flat.id).delete()
                    removed_flats += 1

            except Exception:
                errors += 1
                if errors > 10:
                    session.query(Flat).filter(Flat.id == flat.id).delete()
                pass
    return {"removed_flats": removed_flats}


@API.get("/regular_query")
def regular_query():
    descriptions = []
    kinnisvara = []

    with Session() as session:
        permalinks = session.query(Flat).all()
        searches_db = session.query(Search).all()

    permalinks = [p.permalink for p in permalinks]
    searches = set([p.location for p in searches_db])
    print(searches)
    max_price = max(filter(lambda x: x is not None,
                    [p.price for p in searches_db])) + 100
    min_area = min(filter(lambda x: x is not None,
                   [p.area for p in searches_db])) - 5

    print(permalinks)

    req = kinnisvara24.query(permalinks)
    data1 = req[0]
    url_dict = req[1]
    for d in data1:
        for x in searches:
            if x.split(", ")[0] not in d["address"]:
                continue
            elif x.split(", ")[1] not in d["address"]:
                continue
            elif fuzz.ratio(x, d["address"]) < 60:
                continue
            elif None in [d["area"], d["price"]]:
                pass
            elif d in kinnisvara:
                continue
            elif d["area"] < min_area:
                continue
            elif d["price"] > max_price:
                continue
            elif d["permalink"] in permalinks:
                continue
            descriptions.append(
                kinnisvara24.getDescriptionKinnisvara(d["permalink"], url_dict))
            kinnisvara.append(d)
    print(len(kinnisvara))
    print("33%")

    data2 = city24.query(permalinks)
    print(len(data2))
    i = 0
    for d in data2:
        for x in searches:
            if x.split(", ")[0] not in d["address"]:
                continue
            elif x.split(", ")[1] not in d["address"]:
                continue
            elif fuzz.ratio(x, d["address"]) < 60:
                continue
            elif d in kinnisvara:
                continue
            elif None in [d["area"], d["price"]]:
                pass
            elif d["area"] < min_area:
                continue
            elif d["price"] > max_price:
                continue
            elif d["permalink"] in permalinks:
                continue
            elif not city24.getDescriptionCity(d["permalink"]) in descriptions:
                kinnisvara.append(d)
                descriptions.append(city24.getDescriptionCity(
                    d["permalink"]))
            print(i)
        i += 1
    print(len(kinnisvara))
    print("66%")
    data3 = kv.query(permalinks)

    i = 0

    for d in data3:
        print(i)
        for x in searches:
            if x.split(", ")[0] not in d["address"]:
                continue
            elif x.split(", ")[1] not in d["address"]:
                continue
            elif fuzz.ratio(x, d["address"]) < 60:
                continue
            elif d in kinnisvara:
                continue
            elif None in [d["area"], d["price"]]:
                pass
            elif d["area"] < min_area:
                continue
            elif d["price"] > max_price:
                continue
            elif d["permalink"] in permalinks:
                continue
            elif not kv.getDescriptionKV(d["permalink"]) in descriptions:
                kinnisvara.append(d)

        i += 1
    print(len(kinnisvara))

    print("100%")

    with open("output3.json", "w") as outfile:
        outfile.write(json.dumps(kinnisvara, indent=4))

    with Session() as session:
        for data in kinnisvara:

            if "kv.ee" in data["permalink"]:

                flat = Flat(rooms=data["rooms"], price=data["price"], area=data["area"],
                            permalink=data["permalink"], published=datetime.fromisoformat(data["published"].rsplit(".", 1)[0]), location=data["address"])
            else:
                flat = Flat(rooms=data["rooms"], price=data["price"], area=data["area"],
                            permalink=data["permalink"], published=datetime.fromisoformat(data["published"].replace("Z", "")), location=data["address"])

            session.add(flat)
        session.commit()

    return {"status": 200, "url_dict": url_dict}


class ParamsFlats(BaseModel):
    location: str
    rooms: Optional[int] = 0
    area: Optional[float] = 0.0
    price: Optional[float] = 0.0


def compute_similarity(input_string, reference_strings):
    similarity = [0]
    for reference_string in reference_strings:
        diff = ndiff(input_string, reference_string)
        diff_count = 0
        for line in diff:
            if line.startswith("-"):
                diff_count += 1
        similarity.append(1 - (diff_count / len(input_string)
                          if len(input_string) > 0 else -1))
    return max(similarity)


@API.post("/get_flats")
def get_flats(model: ParamsFlats):
    url_dict = regular_query()["url_dict"]

    with Session() as session:
        if model.rooms is None and model.area is None and model.price is None:
            res = session.query(Flat).filter(
                Flat.published > (date.today() - relativedelta(months=1)), Flat.location.like('%'.join(model.location.split(', '))+"%")).all()
        elif model.rooms is None and model.area is None:
            res = session.query(Flat).filter(
                Flat.price <= model.price, Flat.published > (date.today() - relativedelta(months=1)), Flat.location.like('%'.join(model.location.split(', '))+"%")).all()
        elif model.rooms is None:
            res = session.query(Flat).filter(Flat.area >= model.area,
                                             Flat.price <= model.price, Flat.published > (date.today() - relativedelta(months=1)), Flat.location.like('%'.join(model.location.split(', '))+"%")).all()
        elif model.area is None:
            res = session.query(Flat).filter(Flat.rooms >= model.rooms,
                                             Flat.price <= model.price, Flat.published > (
                                                 date.today() - relativedelta(months=1)), Flat.location.like('%'.join(model.location.split(', '))+"%")).all()
        elif model.price is None:
            res = session.query(Flat).filter(Flat.rooms >= model.rooms,
                                             Flat.area >= model.area, Flat.published > (
                                                 date.today() - relativedelta(months=1)), Flat.location.like('%'.join(model.location.split(', '))+"%")).all()
        else:
            res = session.query(Flat).filter(Flat.rooms >= model.rooms, Flat.price <= model.price,
                                             Flat.area >= model.area, Flat.published > (
                                                 date.today() - relativedelta(months=1)), Flat.location.like('%'.join(model.location.split(', '))+"%")).all()
        # Get all the descriptions of flats
        descriptions = {"kv": [], "city24": [], "kinnisvara24": []}

        with open("url_dicts.json", "r") as file:
            url_dict = json.load(file)

        print(len(res))
        flats = []
        res.sort(key=lambda r: r.published, reverse=True)

        for i, o in enumerate(res):
            if len(flats) == 20:
                break
            print(str(round(len(flats)/len(res), 2)*100) + "%")
            if "kv" in o.permalink:
                description = kv.getDescriptionKV(o.permalink)
                if compute_similarity(description, [*descriptions["city24"], *descriptions["kinnisvara24"]]) < 0.7:
                    flats.append(o)
                    descriptions["kv"].append(description)
            elif "city24" in o.permalink:
                description = city24.getDescriptionCity(o.permalink)
                if compute_similarity(description, [*descriptions["kv"], *descriptions["kinnisvara24"]]) < 0.7:
                    flats.append(o)
                    descriptions["city24"].append(description)

            elif "kinnisvara24" in o.permalink:
                description = kinnisvara24.getDescriptionKinnisvara(
                    o.permalink, url_dict)
                if compute_similarity(description, [*descriptions["city24"], *descriptions["kv"]]) < 0.7:
                    flats.append(o)
                    descriptions["kinnisvara24"].append(
                        description)
        return {"flats": flats}


@ API.post("/add_search")
def add_search(obj: ParamsFlats):

    with Session() as session:
        search = Search(location=obj.location, price=obj.price,
                        area=obj.area, rooms=obj.rooms)
        session.add(search)
        session.commit()
    resp = get_flats(obj)
    return resp
