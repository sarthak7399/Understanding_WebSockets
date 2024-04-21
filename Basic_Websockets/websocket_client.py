import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        # Send a message to the server
        await websocket.send("Hello, WebSocket Server!")

        # Receive the echoed message from the server
        response = await websocket.recv()
        print("Received:", response)

# Run the client
asyncio.run(hello())
