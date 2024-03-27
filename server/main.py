from typing import Union, Optional

from fastapi import FastAPI
from ib_connection import IBConnection

from models import TVWebhook, Securities
from ib_connection import IBConnection

app = FastAPI()
ib = IBConnection()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/positions/")
def get_positions():
    return ib.get_positions()


@app.post("/webhook")
async def handle_webhook(data: TVWebhook):
    trade = await ib.submit_trade(
        sec_type="FUT",
        symbol=data.symbol,
        exchange=data.exchange,
        currency=data.currency,
        action=data.action,
        quantity=data.quantity,
    )
    return trade.dict()
