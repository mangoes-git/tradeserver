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


@app.get("/account/summary")
async def get_account_summary():
    return await ib.get_summary()


@app.get("/trades/open")
def get_open_trades():
    return ib.get_open_trades()


@app.get("/orders/open")
def get_open_orders():
    return ib.get_open_orders()


@app.get("/status")
def get_ib_connection_status():
    try:
        connection_stats = ib.client.connectionStats()
    except Exception:
        return {
            "is_connected": False,
        }

    return {
        "is_connected": ib.is_connected(),
        "stats": connection_stats._asdict(),
    }


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
