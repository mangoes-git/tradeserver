import csv
from contextlib import asynccontextmanager
from io import StringIO

from datetime import datetime, timezone, timedelta

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from models import IncomingData, OutputRow

from order_id import TrackID
from sftp_connection import SFTP_Connection

import utils

from send_email import send_email

from env import EMAIL_RECIPIENTS, SSH_HOST, SSH_USER, SSH_KEY_PATH, SFTP_PATH

from exception_handlers import (
    request_validation_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)
from middleware import log_request_middleware

DB = None
SFTP = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global DB
    global SFTP
    DB = TrackID()
    SFTP = SFTP_Connection(
        hostname=SSH_HOST,
        username=SSH_USER,
        key_path=SSH_KEY_PATH,
    )
    yield
    DB.close()
    SFTP.close()


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
    current_date_str = current_datetime.strftime("%m-%d-%Y")

    default_time = (
        "9:03" if utils.is_time_between(check_time=current_datetime.time()) else "21:03"
    )
    entry_type = data.Type
    output_model = OutputRow(
        **data.dict(),
        ChinaTradeDate=current_date_str,
        ChinaStartTime=f"{current_date_str} {default_time}",
        OrderID=None,
    )

    # check if we must split into multiple rows

    accounts = output_model.Account.split(",")
    quantities = output_model.Quantity.split(",")

    for acc, qty in zip(accounts, quantities):
        new_row = output_model.copy(exclude={"Account", "Quantity", "Type"})
        new_row.Account = acc
        new_row.Quantity = qty
        new_row.OrderID = f"{DB.get_next_id():05}"
        output_rows.append(new_row.dict())

    csv_file = StringIO()

    writer = csv.DictWriter(
        csv_file, fieldnames=CSV_COLUMNS, delimiter=",", quoting=csv.QUOTE_ALL
    )
    writer.writeheader()
    writer.writerows(output_rows)

    todays_mail_number = DB.get_todays_email_number(current_datetime)
    mail_subject = f"UC_CHINA_{current_date_str}_{todays_mail_number}"
    attachment_name = (
        f"{entry_type}_UC_CHINA_{current_date_str}_{todays_mail_number}.csv"
    )

    SFTP.put(csv_file, attachment_name, remotedir=SFTP_PATH)

    await send_email(
        recipients=EMAIL_RECIPIENTS,
        subject=mail_subject,
        body="",
        file=csv_file,
        attachment_name=attachment_name,
    )

    return {
        "message": "sent email",
        "recipients": EMAIL_RECIPIENTS,
        "mail_subject": mail_subject,
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
