import logging

from websockets.client import connect

logger = logging.getLogger("uvicorn")


class WSConnection:
    def __init__(self, endpoint="ws://websocket-echo.com"):
        self.endpoint = endpoint

    async def connect(self):
        try:
            logger.info(f"attempting to connect to {self.endpoint}")
            self.conn = await connect(self.endpoint)
            logger.info("connected")
        except Exception as e:
            logger.exception("Connection error:")
            exit()

    async def reconnect(self):
        logger.info("attempting reconnection...")
        self.conn = await connect(self.endpoint)

    async def send_msg(self, msg):
        try:
            logger.info(f"sending message: {msg}")
            await self.conn.send(msg)
        except Exception as e:
            logger.exception("error sending message.")
            self.reconnect()
            exit()

    async def receive(self):
        try:
            msg = await self.conn.recv(0.01)
            logger.info(f"received from websocket: {msg}")
        except:
            pass
