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


@app.get("/test3")
def manageFlats():
    print(kinnisvara24.getDescriptionKinnisvara(
        "https://kinnisvara24.ee/240755931"))
    # print(compute_similarity(city24.getDescriptionCity(
    #     "https://kinnisvara24.ee/240755931"), """Välja üürida avar(45, 2m²) rõdu ja parkimiskohaga möbleeritud kahetoaline korter. Väga heas seisukorras. Korter on värskelt korrastatud, uued tapeedid. Keldrikorrusel panipaik. Läheduses Maarjamõisa ja Ülikooli õppehooned, uus toidupood ja Lõunakeskus. Hea bussiühendus.
    #     Helista julgesti ja küsi lisa!"""))


def compute_similarity(input_string, reference_string):
    diff = ndiff(input_string, reference_string)
    diff_count = 0
    for line in diff:
        if line.startswith("-"):
            diff_count += 1
    return 1 - (diff_count / len(input_string))


@ app.get("/test2")
def test2():
    descriptions = []
    kinnisvara = []

    # req = kinnisvara24.queryAllKinnisvara()
    # data1 = req[0]
    # url_dict = req[1]
    # for d in data1:
    #     descriptions.append(
    #         kinnisvara24.getDescriptionKinnisvara(d["permalink"], url_dict))
    #     kinnisvara.append(d)
    # print("33%")

    # data2 = city24.queryAllCity()
    # print(len(data2))
    # i = 0
    # for d in data2:
    #     print(i)
    #     if not city24.getDescriptionCity(d["permalink"]) in descriptions:
    #         kinnisvara.append(d)
    #         descriptions.append(city24.getDescriptionCity(
    #             d["permalink"]))
    #     print(i)
    #     i += 1
    # print("66%")
    data3 = kv.queryAllKV()

    i = 0

    for d in data3:
        print(i)
        if not kv.getDescriptionKV(d["permalink"]) in descriptions:
            kinnisvara.append(d)

        i += 1
    print("100%")

    return kinnisvara


@app.get("/add")
def add():
    from database import Session

    with Session() as session:
        flat = Flat(rooms=2, price=420.2, area=50.5,
                    permalink="abs.kkdsajflk", published=datetime.now())
        session.add(flat)
        session.commit()
