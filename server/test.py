from ib_insync import *
import datetime

# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect("localhost", 4002, clientId=123, timeout=10)

contract = Future("NQ", "20290621", "CME")
# contract = Stock("AMD", "SMART", "USD")
order = MarketOrder("BUY", 1)
ib.qualifyContracts(contract)
# lst = ib.reqContractDetails(contract)
# print(contract)
# print(lst)

trade = ib.placeOrder(contract, order)
while not trade.isDone():
    ib.waitOnUpdate()
print("_____________________________________")
print(trade.dict())
