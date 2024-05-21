from models import Flat
from datetime import datetime
from database import Base, engine
import os
from fastapi import FastAPI
from difflib import ndiff
from scrapers import kinnisvara24, kv, city24
from api import API

if not os.path.isfile("./test.db"):
    Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(API, prefix='/api')


@app.get("/")
def read_root():
    return {"status": 200}


@app.get("/test")
def test():
    return kv.query()
