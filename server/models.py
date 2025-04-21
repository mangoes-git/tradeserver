from enum import StrEnum

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


class IncomingData(BaseModel):
    Customer: str
    Account: str
    BuySell: str
    Quantity: str
    Exchange: str
    Symbol: str
    Month: str
    Year: str
    LimitPrice: str | None
    OrderType: str
    TimeInForce: str
    Close: str | None
    Description: str
    Type: str | None


class OutputRow(IncomingData):
    ChinaTradeDate: str | None
    OrderID: str | None
    ChinaStartTime: str | None
