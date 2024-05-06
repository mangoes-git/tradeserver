from typing import Union, Optional
import asyncio

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse

from models import TVWebhook, TriggerRequest, WSResponse

from websocket_connection import WSConnection

URL = "ws://10.21.0.1:9234"

app = FastAPI()
ws = WSConnection(URL)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/favicon.ico", status_code=204)
def favicon():
    pass


@app.post("/webhook")
async def handle_webhook(data: TriggerRequest) -> WSResponse:
    await ws.send_msg(str(data))
    message = ws.receive()
    return {
        "message": message,
        "strategy_id": data.strategy_id,
        "position": data.position,
        "Price": data.Price,
    }


@app.post("/test")
def handle_test(data: TVWebhook) -> TriggerRequest:
    return {
        "strategy_id": "1234-1234",
        "position": -(1 / 3),
    }


@app.get("/robots.txt", include_in_schema=False)
def get_robots():
    data = ("""User-agent: *\nDisallow: /""",)
    return data
