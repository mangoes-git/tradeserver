import os

IBC_HOST = os.environ.get("IBC_HOST", "127.0.0.1")
IBC_PORT = os.environ.get("IBC_PORT", "4002")
IBC_CONN_TIMEOUT = int(os.environ.get("IBC_CONN_TIMEOUT", "10"))
CLIENT_ID = int(os.environ.get("CLIENT_ID", "123"))
