from scrape import Scrape
import json
from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from requests import HTTPError, TooManyRedirects
from contextlib import asynccontextmanager


elements_to_scrape = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    f = open("scrape.json")
    data = f.read()
    f.close()
    global elements_to_scrape
    elements_to_scrape = json.loads(data)
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/root")
async def root():
    return "Hello World!"


@app.get("v1/{symbol}/summary/")
async def summary(symbol, q: Optional[List[str]] = Query(None)):
    summary_data = {}

    try:
        s = Scrape(symbol, elements_to_scrape)
        summary_data = s.summary()

        if q is not None:
            if all (k in summary_data for k in q):
                summary_data = {key: summary_data[key] for key in q}

    except TooManyRedirects:
        raise HTTPException(status_code=404, detail="{symbol} doesn't exist or cannot be found")

    except HTTPError:
        raise HTTPException(status_code=500, detail="An error has occurred while processing the request.")

    return summary_data
