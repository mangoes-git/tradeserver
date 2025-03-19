import csv
from contextlib import asynccontextmanager
from io import StringIO

from datetime import datetime, timezone, timedelta

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from models import IncomingData, OutputRow

from order_id import TrackID

from send_email import send_email

from exception_handlers import (
    request_validation_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)
from middleware import log_request_middleware

id_counter = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global id_counter
    id_counter = TrackID()
    yield
    id_counter.close()


app = FastAPI(lifespan=lifespan)

app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/favicon.ico", status_code=204)
def favicon():
    pass


CSV_COLUMNS = [
    "ChinaTradeDate",
    "OrderID",
    "Customer",
    "Account",
    "BuySell",
    "Quantity",
    "Exchange",
    "Symbol",
    "Month",
    "Year",
    "LimitPrice",
    "OrderType",
    "ChinaStartTime",
    "TimeInForce",
    "Close",
    "Description",
]


@app.post("/webhook")
async def handle_webhook(data: IncomingData):
    output_rows = []
    # parse date
    current_datetime = datetime.now(timezone(timedelta(hours=8)))

    output_model = OutputRow(
        **data.dict(),
        ChinaTradeDate=current_datetime.strftime("%m/%d/%Y"),
        ChinaStartTime=current_datetime.strftime("%m/%d/%Y %H:%M"),
        OrderID=None,
    )

    # check if we must split into multiple rows

    accounts = output_model.Account.split(",")
    quantities = output_model.Quantity.split(",")

    for acc, qty in zip(accounts, quantities):
        new_row = output_model.copy(exclude={"Account", "Quantity"})
        new_row.Account = acc
        new_row.Quantity = qty
        new_row.OrderID = f"{id_counter.get_next():05}"
        output_rows.append(new_row.dict())

    csv_file = StringIO()

    writer = csv.DictWriter(
        csv_file, fieldnames=CSV_COLUMNS, delimiter=",", quoting=csv.QUOTE_ALL
    )
    writer.writeheader()
    writer.writerows(output_rows)
    await send_email(body=str(output_rows), file=csv_file)
    return {
        "message": "sent email",
        "data": output_rows,
    }


# @app.post("/test")
# def handle_test(data: TVWebhook) -> TriggerRequest:
#     return {
#         "strategy_id": "1234-1234",
#         "position": -(1 / 3),
#     }


@app.get("/robots.txt", include_in_schema=False)
def get_robots():
    data = ("""User-agent: *\nDisallow: /""",)
    return data
