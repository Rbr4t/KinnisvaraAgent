from models import Flat
from datetime import datetime
from database import Base, engine
import os
from fastapi import FastAPI


if not os.path.isfile("./test.db"):
    Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/add")
def add():
    from database import Session

    with Session() as session:
        flat = Flat(rooms=2, price=420.2, area=50.5,
                    permalink="abs.kkdsajflk", published=datetime.now())
        session.add(flat)
        session.commit()
