from typing import List

from ib_insync import IB, Contract, Future, MarketOrder, Trade
import nest_asyncio

from models import TradeActions, Securities
from env import IBC_HOST, IBC_PORT, CLIENT_ID, IBC_CONN_TIMEOUT

nest_asyncio.apply()


class IBConnection:
    def __init__(self):
        self._ib = IB()
        self._ib.connect(
            IBC_HOST,
            IBC_PORT,
            clientId=CLIENT_ID,
            timeout=IBC_CONN_TIMEOUT,
        )
        self.client = self._ib.client

    async def submit_trade(
        self,
        sec_type: str,
        symbol: str,
        exchange: str,
        currency: str,
        action: str,
        quantity: int,
        last_trade_date_or_month: str = "",
    ):
        """
        Submit a trade, does not wait until the trade is done (either
        completely filled or cancelled).
        """
        contract = Future(
            symbol=symbol,
            exchange=exchange,
            currency=currency,
            lastTradeDateOrContractMonth=last_trade_date_or_month,
        )
        order = MarketOrder(action, quantity)
        await self._ib.qualifyContractsAsync(contract)
        trade = self._ib.placeOrder(contract, order)
        return trade

    async def perform_trade(
        self,
        sec_type: str,
        symbol: str,
        exchange: str,
        currency: str,
        action: str,
        quantity: int,
        last_trade_date_or_month: str = "",
    ):
        """
        Submit a trade and wait until it is done (either completely
        filled or cancelled).
        """
        contract = Future(
            symbol=symbol,
            exchange=exchange,
            currency=currency,
            lastTradeDateOrContractMonth=last_trade_date_or_month,
        )
        order = MarketOrder(action, quantity)
        await self._ib.qualifyContractsAsync(contract)
        trade = self._ib.placeOrder(contract, order)
        while not trade.isDone():
            self._ib.waitOnUpdate(2)
        return trade

    def get_positions(self, account: str = "") -> List[dict]:
        positions = self._ib.positions(account)
        result = []
        for p in positions:
            curr = {}
            for k, v in zip(p._fields, p):
                if isinstance(v, Contract):
                    curr[k] = v.dict()
                else:
                    curr[k] = str(v)
            result.append(curr)
        return result

    async def get_summary(self, account: str = ""):
        return await self._ib.accountSummaryAsync()

    def get_open_trades(self):
        return self._ib.openTrades()

    def get_open_orders(self):
        return self._ib.openOrders()

    def is_connected(self):
        return self._ib.isConnected()
