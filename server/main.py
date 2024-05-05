from typing import Union, Optional
import asyncio

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse

from models import TVWebhook, TriggerResponse, WSResponse

from websockets.sync.client import connect

app = FastAPI()

URL = "ws://10.21.0.1:9234"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/favicon.ico", status_code=204)
def favicon():
    pass


@app.post("/webhook")
async def handle_webhook(data: TriggerResponse) -> WSResponse:
    with connect(URL) as websocket:
        websocket.send(str(data))
        message = websocket.recv()
        return {"message": message}


@app.post("/test")
def handle_test(data: TVWebhook) -> TriggerResponse:
    return {
        "strategy_id": "1234-1234",
        "position": -(1 / 3),
    }


@app.get("/robots.txt", include_in_schema=False)
def get_robots():
    data = ("""User-agent: *\nDisallow: /""",)
    return data
