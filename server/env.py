import os
from dotenv import load_dotenv


load_dotenv()

EMAIL_ADDR = os.getenv("EMAIL_ADDR")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS").split(",")

SSH_HOST = os.getenv("SSH_HOST")
SSH_USER = os.getenv("SSH_USER")
SSH_KEY_PATH = os.getenv(
    "SSH_KEY_PATH",
)
