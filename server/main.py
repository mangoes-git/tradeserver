import json

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.encoders import jsonable_encoder

from fastapi_utils.tasks import repeat_every

from models import TVWebhook, TriggerRequest, WSResponse

from websocket_connection import WSConnection

from exception_handlers import (
    request_validation_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)
from middleware import log_request_middleware

import env


app = FastAPI()
ws = WSConnection(env.WS_URL)

app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@repeat_every(seconds=2, wait_first=20)
async def ws_heartbeat():
    await ws.send_msg("KEEPALIVE_HEARTBEAT")


@app.on_event("startup")
async def startup_event():
    await ws.connect()
    await ws_heartbeat()


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
    await ws.receive()
    return {
        "message": f"sent to {env.WS_URL}",
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
