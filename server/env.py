import os
from dotenv import load_dotenv


load_dotenv()

EMAIL_ADDR = os.getenv("EMAIL_ADDR")
EMAIL_PASS = os.getenv("EMAIL_PASS")
