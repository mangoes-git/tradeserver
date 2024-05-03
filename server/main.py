from typing import Union, Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse

from models import TVWebhook, TriggerResponse


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/favicon.ico", status_code=204)
def favicon():
    pass


@app.post("/webhook")
async def handle_webhook(data: TVWebhook):
    return "ok"


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
