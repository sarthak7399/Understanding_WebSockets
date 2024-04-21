from fastapi import FastAPI, WebSocket

app = FastAPI()

# Define a WebSocket route
@app.websocket("/ws")   # This line is a WebSocket route, it is a decorator which means that this function is added as a route
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive message from client
        data = await websocket.receive_text()
        
        # Echo the message back to the client
        await websocket.send_text(f"Message text was: {data}")
