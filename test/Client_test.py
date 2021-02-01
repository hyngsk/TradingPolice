import asyncio
import json

import websockets


async def hello():
    uri = "ws://localhost:5001"
    async with websockets.connect(uri) as websocket:
        while True:
            func = input("send func : ").split(',')
            param = []
            for i in range(len(func)):
                tmp = input("send param : ").split(',')
                param.append(tmp)
            message = {"func": [i for i in func], "param": [i for i in param]}
            if func is None or param is None:
                break
            await websocket.send(json.dumps(message))
            print(f"> {message}")

            response = await websocket.recv()
            print(f"< {response}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(hello())
