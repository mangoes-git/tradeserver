from pydantic import BaseModel

from enum import StrEnum


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

    open: float
    high: float
    low: float
    close: float
    exchange: str
    symbol: str
    volume: int
    time: str
    timenow: str
    action: TradeActions
    currency: str
    quantity: int
