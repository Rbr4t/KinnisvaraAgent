from fastapi import APIRouter
from database import Session
from models import Flat
from datetime import datetime
from scrapers import kinnisvara24, kv, city24
import json
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
                        permalink=data["permalink"], published=datetime.fromisoformat(data["published"]))
            session.add(flat)
        session.commit()

    return {"status": 200}
