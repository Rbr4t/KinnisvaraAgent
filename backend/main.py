from models import Flat
from datetime import datetime
from database import Base, engine
import os
from fastapi import FastAPI, Request
from difflib import ndiff
from scrapers import kinnisvara24, kv, city24
from api import API
from auth import auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse


if not os.path.isfile("./test.db"):
    Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(API, prefix='/api')
app.include_router(auth, prefix='/auth')

app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"),
          name="assets")
templates = Jinja2Templates(directory="../frontend/dist")


@app.get("/test")
def test():
    return kinnisvara24.query()

# Jinja2 mallimootoriga Reacti lehele suunamine


@app.get("/")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{rest_of_path:path}")
async def react_app(req: Request, rest_of_path: str):
    return templates.TemplateResponse('index.html', {'request': req})
