from typing import Union, Optional

from fastapi import FastAPI, HTTPException
from ib_connection import IBConnection

from models import TVWebhook, Securities
from ib_connection import IBConnection

app = FastAPI()
ib = IBConnection()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/account/positions")
def get_positions():
    return ib.get_positions()


@app.post("/webhook")
async def handle_webhook(data: TVWebhook):
    if data.security_type != Securities.FUTURE:
        raise HTTPException(
            400,
            "Invalid security_type. Only the trading of futures is available.",
        )
    trade = await ib.submit_trade(
        sec_type=data.security_type,
        symbol=data.symbol,
        exchange=data.exchange,
        currency=data.currency,
        action=data.action,
        quantity=data.quantity,
        last_trade_date_or_month=data.last_trade_date_or_month,
    )
    return trade.dict()


@app.post("/test")
def handle_test(data: TVWebhook):
    return data
