import asyncio
import logging

from websockets.sync.client import connect

logger = logging.getLogger("uvicorn")


class WSConnection:
    def __init__(self, endpoint="ws://websocket-echo.com"):
        self.endpoint = endpoint
        try:
            logger.info(f"attempting to connect to {self.endpoint}")
            self.conn = connect(self.endpoint)
            logger.info("connected")
        except Exception as e:
            logger.exception("Connection error:")
            exit()

    def reconnect(self):
        logger.info("attempting reconnection...")
        self.conn = connect(self.endpoint)

    async def send_msg(self, msg):
        try:
            logger.debug(f"sending message: {msg}")
            self.conn.send(msg)
        except Exception as e:
            log.exception("error sending message.")
            self.reconnect()
            exit()

    def receive(self):
        try:
            msg = self.conn.recv(0.5)
            logger.info(f"received from websocket: {msg}")
        except:
            pass
