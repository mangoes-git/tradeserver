from typing import Union, Optional
import asyncio
import json

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

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
    json_data = jsonable_encoder(data)
    json_data.pop("Price")
    await ws.send_msg(json.dumps(json_data))
    try:
        resp = ws.receive()
        print(f"received from websocket: {resp}")
    except:
        pass
    return {
        "message": f"sent to {URL}",
        "strategy_id": data.strategy_id,
        "direction": data.direction,
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
