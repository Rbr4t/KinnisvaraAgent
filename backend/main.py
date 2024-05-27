from database import Base, engine
import os
from fastapi import FastAPI, Request
from scrapers import kinnisvara24, kv, city24
from api import API
from auth import auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import asyncio
from api import regular_query

if not os.path.isfile("./test.db"):
    Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(API, prefix='/api')
app.include_router(auth, prefix='/auth')

app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"),
          name="assets")
templates = Jinja2Templates(directory="../frontend/dist")


async def periodic_task():
    while True:
        print("Running the periodic task...")
        await regular_query()

        # Sleep for 20 minutes (20 * 60 seconds)
        await asyncio.sleep(2*60)


@app.on_event("startup")
async def startup_event():
    # Start the periodic task
    asyncio.create_task(periodic_task())

# Jinja2 mallimootoriga Reacti lehele suunamine


@app.get("/test")
def index():
    return kv.query()


@app.get("/")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{rest_of_path:path}")
async def react_app(req: Request, rest_of_path: str):
    return templates.TemplateResponse('index.html', {'request': req})
