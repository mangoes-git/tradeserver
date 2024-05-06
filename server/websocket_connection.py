import asyncio
from websockets.sync.client import connect


class WSConnection:
    def __init__(self, endpoint="ws://websocket-echo.com"):
        self.endpoint = endpoint
        self.conn = connect(self.endpoint)
        # self.loop = asyncio.get_event_loop()
        # self.loop.run_until_complete(self.__async__connect())

    async def __async__connect(self):
        print(f"attempting to connect to {self.endpoint}")
        self.conn = await connect(self.endpoint)
        print("connected")

    async def send_msg(self, msg):
        self.conn.send(msg)

    def receive(self):
        return self.conn.recv(0.5)
