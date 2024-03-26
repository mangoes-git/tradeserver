from ib_insync import IB, Future, MarketOrder
import nest_asyncio

from models import TradeActions, Securities

nest_asyncio.apply()


class IBConnection:
    def __init__(self):
        self._ib = IB()
        self._ib.connect("localhost", 4002, clientId=123, timeout=10)

    def submit_trade(
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
        ib.qualifyContracts(contract)
        trade = ib.placeOrder(contract, order)
        return trade

    def perform_trade(
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
        ib.qualifyContracts(contract)
        trade = ib.placeOrder(contract, order)
        while not trade.isDone():
            # if there is an error returned by IB this loop will not exit.
            ib.waitOnUpdate()
        return trade
