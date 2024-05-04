from typing import Union, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse

from models import TVWebhook, TriggerResponse, ProxyResponse

import httpx

app = FastAPI()

URL = "10.21.0.1:9234"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/favicon.ico", status_code=204)
def favicon():
    pass


@app.post("/webhook")
async def handle_webhook(data: TriggerResponse) -> ProxyResponse:
    response = await httpx.post(URL, json=data)

    return {
        "status": response.status_code,
        "content": r.text,
    }


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
