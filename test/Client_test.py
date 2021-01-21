import asyncio
import websockets

async def hello():
    uri = "ws://localhost:5001"
    async with websockets.connect(uri) as websocket:
        message = input("send some message : ")

        await websocket.send(message)
        print(f"> {message}")

        response = await websocket.recv()
        print(f"< {response}")

asyncio.get_event_loop().run_until_complete(hello())