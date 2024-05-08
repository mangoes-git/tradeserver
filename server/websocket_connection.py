import asyncio
from websockets.sync.client import connect


class WSConnection:
    def __init__(self, endpoint="ws://websocket-echo.com"):
        self.endpoint = endpoint
        try:
            print(f"attempting to connect to {self.endpoint}")
            self.conn = connect(self.endpoint)
            print("connected")
        except Exception as e:
            print("Connection error:")
            print(e)
            exit()

    def reconnect():
        print(f"attempting reconnection...")
        self.conn = connect(self.endpoint)

    async def send_msg(self, msg):
        try:
            print(f"sending message: {msg}")
            self.conn.send(msg)
        except Exception as e:
            print("error sending message.")
            print(e)
            self.reconnect()
            exit()

    def receive(self):
        return self.conn.recv(0.5)
