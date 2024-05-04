from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class TradeActions(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class Securities(StrEnum):
    """
    Types of financial securities. The values correspond to
    `ib_insync.Contract`s secTypes.
    See: https://ib-insync.readthedocs.io/api.html#ib_insync.contract.Contract
    """

    STOCK = "STK"
    OPTION = "OPT"
    FUTURE = "FUT"
    INDEX = "IND"
    FUTURES_OPTION = "FOP"
    FOREX = "CASH"
    CFD = "CFD"
    BOND = "BOND"
    MUTUAL_FUND = "FUND"


class TVWebhook(BaseModel):
    """
    Incoming request from TradingView's webhooks.
    """

    security_type: Optional[Securities] = Securities.FUTURE
    exchange: str
    symbol: str
    action: TradeActions
    currency: str
    quantity: int
    strategy_id: str
    position: float  # has range [-1.0, 1.0]
    last_trade_date_or_month: str


class TriggerResponse(BaseModel):
    strategy_id: str
    position: float  # has range [-1.0, 1.0]


class ProxyResponse(BaseModel):
    status = int
    content = str
