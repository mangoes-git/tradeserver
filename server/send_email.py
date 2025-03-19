from fastapi import UploadFile
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List

import env


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME=env.EMAIL_ADDR,
    MAIL_PASSWORD=env.EMAIL_PASS,
    MAIL_FROM=env.EMAIL_ADDR,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="UC244",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(
    recipients,
    body=None,
    file=None,
):
    file.seek(0)
    upload_file = UploadFile(filename="data.csv", file=file)
    message = MessageSchema(
        subjet="mail subject",
        recipients=recipients,
        body=body,
        subtype="html",
        attachments=[upload_file],
    )
    fm = FastMail(conf)
    await fm.send_message(message)
