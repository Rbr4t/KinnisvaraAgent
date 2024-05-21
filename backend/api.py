from fastapi import APIRouter
from database import Session
from models import Flat, Search
from datetime import datetime
from scrapers import kinnisvara24, kv, city24
import json
from pydantic import BaseModel
from difflib import ndiff
from typing import Optional

API = APIRouter()

API.get("/")


def index():
    return {"status": 200}


@API.get("/regular_query")
def regular_query():

    descriptions = []
    kinnisvara = []

    with Session() as session:
        permalinks = session.query(Flat).all()
    permalinks = [p.permalink for p in permalinks]
    # print(permalinks)

    req = kinnisvara24.queryRegularKinnisvara(permalinks)
    data1 = req[0]
    url_dict = req[1]
    for d in data1:
        descriptions.append(
            kinnisvara24.getDescriptionKinnisvara(d["permalink"], url_dict))
        kinnisvara.append(d)
    print("33%")

    data2 = city24.queryRegularCity(permalinks)
    print(len(data2))
    i = 0
    for d in data2:
        print(i)
        if not city24.getDescriptionCity(d["permalink"]) in descriptions:
            kinnisvara.append(d)
            descriptions.append(city24.getDescriptionCity(
                d["permalink"]))
        print(i)
        i += 1
    print("66%")
    data3 = kv.queryRegularKV(permalinks)

    i = 0

    for d in data3:
        print(i)
        if not kv.getDescriptionKV(d["permalink"]) in descriptions:
            kinnisvara.append(d)

        i += 1
    print("100%")
    with open("output2.json", "w") as outfile:
        outfile.write(json.dumps(kinnisvara, indent=4))

    with Session() as session:
        for data in kinnisvara:
            try:
                flat = Flat(rooms=data["rooms"], price=data["price"], area=data["area"],
                            permalink=data["permalink"], published=datetime.fromisoformat(data["published"].replace("Z", "")))
                session.add(flat)
            except:
                print(data)
        session.commit()

    return {"status": 200}


@API.get("/query_all")
def query_all():

    descriptions = []
    kinnisvara = []

    req = kinnisvara24.queryAllKinnisvara()
    data1 = req[0]
    url_dict = req[1]
    for d in data1:
        descriptions.append(
            kinnisvara24.getDescriptionKinnisvara(d["permalink"], url_dict))
        kinnisvara.append(d)
    print("33%")

    data2 = city24.queryAllCity()
    print(len(data2))
    i = 0
    for d in data2:
        print(i)
        if not city24.getDescriptionCity(d["permalink"]) in descriptions:
            kinnisvara.append(d)
            descriptions.append(city24.getDescriptionCity(
                d["permalink"]))
        print(i)
        i += 1
    print("66%")
    data3 = kv.queryAllKV()

    i = 0

    for d in data3:
        print(i)
        if not kv.getDescriptionKV(d["permalink"]) in descriptions:
            kinnisvara.append(d)

        i += 1
    print("100%")

    with Session() as session:
        for data in kinnisvara:
            flat = Flat(rooms=data["rooms"], price=data["price"], area=data["area"],
                        permalink=data["permalink"], published=datetime.fromisoformat(data["published"].replace("Z", "")))
            session.add(flat)
        session.commit()

    return {"status": 200}


class ParamsFlats(BaseModel):
    rooms: int
    area: float
    price: float


def compute_similarity(input_string, reference_strings):
    similarity = [0]
    for reference_string in reference_strings:
        diff = ndiff(input_string, reference_string)
        diff_count = 0
        for line in diff:
            if line.startswith("-"):
                diff_count += 1
        similarity.append(1 - (diff_count / len(input_string)))
    return max(similarity)


@API.post("/get_flats")
def get_flats(model: ParamsFlats):
    # return model
    with Session() as session:
        res = session.query(Flat).filter(Flat.area >= model.area,
                                         Flat.rooms >= model.rooms, Flat.price <= model.price).all()

        # Get all the descriptions of flats
        descriptions = []

        flats = []

        for o in res:
            if "kv" in o.permalink:
                if compute_similarity(kv.getDescriptionKV(o.permalink), descriptions) < 0.7:
                    flats.append(o)
                    descriptions.append(kv.getDescriptionKV(o.permalink))
            elif "city24" in o.permalink:
                if compute_similarity(city24.getDescriptionCity(o.permalink), descriptions) < 0.7:
                    flats.append(o)
                descriptions.append(city24.getDescriptionCity(o.permalink))

            elif "kinnisvara24" in o.permalink:
                if compute_similarity(kinnisvara24.getDescriptionKinnisvara(o.permalink), descriptions) < 0.7:
                    flats.append(o)
                    descriptions.append(
                        kinnisvara24.getDescriptionKinnisvara(o.permalink))
        return {"flats": flats}


class ParamsSearch(BaseModel):
    location: str
    rooms: Optional[int] = None
    area: Optional[float] = None
    price: Optional[float] = None


@API.post("/add_search")
def add_search(obj: ParamsSearch):
    with Session() as session:
        search = Search(location=obj.location, price=obj.price,
                        area=obj.area, rooms=obj.rooms)
        session.add(search)
        session.commit()
    return obj
