from typing import List

from ib_insync import IB, Future, MarketOrder, Trade
import nest_asyncio

from models import TradeActions, Securities

nest_asyncio.apply()


class IBConnection:
    def __init__(self):
        self._ib = IB()
        self._ib.connect("ib-gateway", 4004, clientId=123, timeout=60)

    async def submit_trade(
        self,
        sec_type: str,
        symbol: str,
        exchange: str,
        currency: str,
        action: TradeActions,
        quantity: int,
    ):
        """
        Submit a trade, does not wait until the trade is done (either
        completely filled or cancelled).
        """
        contract = Future(
            symbol=symbol,
            exchange=exchange,
            currency=currency,
        )
        order = MarketOrder(str(action), quantity)
        await self._ib.qualifyContractsAsync(contract)
        trade = self._ib.placeOrder(contract, order)
        return trade

    async def perform_trade(
        self,
        sec_type: str,
        symbol: str,
        exchange: str,
        currency: str,
        action: TradeActions,
        quantity: int,
    ):
        """
        Submit a trade and wait until it is done (either completely
        filled or cancelled).
        """
        contract = Future(
            symbol=symbol,
            exchange=exchange,
            currency=currency,
        )
        order = MarketOrder(str(action), quantity)
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
                curr[k] = str(v)
            result.append(curr)
        return result
