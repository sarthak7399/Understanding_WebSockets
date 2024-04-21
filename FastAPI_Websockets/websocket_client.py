import asyncio
import websockets

async def main():
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        while True:
            message = input("Enter message to send (type 'exit' to quit): ")
            if message.lower() == "exit":
                break
            
            # Send the message to the WebSocket server
            await websocket.send(message)
            
            # Receive the echoed message from the WebSocket server
            response = await websocket.recv()
            print("Received:", response)

# Run the client
asyncio.run(main())
