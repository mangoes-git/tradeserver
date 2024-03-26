from typing import Union

from fastapi import FastAPI
from ib_connection import IBConnection

from models import TVWebhook, Securities
from ib_connection import submit_trade

app = FastAPI()
ib_api = IBConnection


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/webhook")
def handle_webhook(data: TVWebhook):
    trade = ib_api.submit_trade(
        sec_type="FUT",
        symbol=data.symbol,
        exchange=data.exchange,
        currency=data.currency,
        action=data.action,
        quantity=data.quantity,
    )
    return trade.dict()
