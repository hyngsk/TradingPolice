import asyncio
import json

import websockets


async def hello():
    uri = "ws://localhost:5001"
    async with websockets.connect(uri) as websocket:
        while True:
            k = input("send some message : ").split(',')

            message = {"message": k[0], "param": [i for i in k[1:]]}
            if message == 'discon':
                break
            await websocket.send(json.dumps(message))
            print(f"> {message}")

            response = await websocket.recv()
            print(f"< {response}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(hello())
