from models import Flat
from datetime import datetime
from database import Base, engine
import os
from fastapi import FastAPI
from difflib import ndiff
from scrapers import kinnisvara24, kv, city24


if not os.path.isfile("./test.db"):
    Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test")
def test():
    v = kinnisvara24.queryAllKinnisvara()
    k = kinnisvara24.getDescriptionKinnisvara(
        "https://kinnisvara24.ee/240777010")
    print(k)


def manageFlats():
    pass


def compute_similarity(input_string, reference_string):
    # The ndiff method returns a list of strings representing the differences between the two input strings.
    diff = ndiff(input_string, reference_string)
    diff_count = 0
    for line in diff:
        # a "-", indicating that it is a deleted character from the input string.
        if line.startswith("-"):
            diff_count += 1
    # calculates the similarity by subtracting the ratio of the number of deleted characters to the length of the input string from 1
    return 1 - (diff_count / len(input_string))


@app.get("/test2")
def test2():
    descriptions = []
    kinnisvara = []

    data1 = kinnisvara24.queryAllKinnisvara()
    for d in data1:
        descriptions += kinnisvara24.getDescriptionKinnisvara(d.permalink)
        kinnisvara += d
    print("33%")

    data2 = city24.queryAllCity()
    for d in data2:
        for desc in descriptions:
            if compute_similarity(city24.getDescriptionCity(d.permalink), desc) > 0.8:
                print(d.permalink)
                break

    print("66%")
    data3 = kv.queryAllKV()
    print("99%")

    return {"data": data1}


@app.get("/add")
def add():
    from database import Session

    with Session() as session:
        flat = Flat(rooms=2, price=420.2, area=50.5,
                    permalink="abs.kkdsajflk", published=datetime.now())
        session.add(flat)
        session.commit()
