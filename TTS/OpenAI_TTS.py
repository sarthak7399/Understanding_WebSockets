## Building a Real-Time Audio Chat with OpenAI

# Running the backend - "uvicorn OpenAI_TTS:app --reload"
# Running the frontend - "Run the frontend in the browser - OpenAI_TTS.html"

import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import openai
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = openai.OpenAI()
start_time = time.time()

# Function to send the initial welcome message
async def send_initial_message(websocket: WebSocket):
    initial_message = "Hello, my name is Blue. How may I help you with queries related to computer networking?"
    await websocket.send_text(initial_message)

# Function to get response from OpenAI
def call_openai_api(message):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are an assistant named 'Blue'. You help people to learn about modern computer networking and its workings."},
            {'role': 'user', 'content': message}
        ],
        temperature=0,
        stream=True
    )
    return completion

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await send_initial_message(websocket)  # Send initial welcome message when connection is established

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_text(self, text: str, websocket: WebSocket):
        await websocket.send_text(text)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()
                print(f"Received text: {data}")
                res = call_openai_api(data)
                collected_messages = []
                for chunk in res:
                    chunk_message = chunk.choices[0].delta.content
                    collected_messages.append(chunk_message)
                    if chunk_message is not None and chunk_message.find('.') != -1:
                        message = [m for m in collected_messages if m is not None]
                        full_reply_content = ''.join([m for m in message])
                        await manager.send_text(full_reply_content, websocket)
                        collected_messages = []
                    print(f"Message received: {chunk_message}")
                if len(collected_messages) > 0:
                    message = [m for m in collected_messages if m is not None]
                    full_reply_content = ''.join([m for m in message])
                    await manager.send_text(full_reply_content, websocket)
                    collected_messages = []
            except WebSocketDisconnect:
                manager.disconnect(websocket)
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                break
    finally:
        manager.disconnect(websocket)

@app.get("/")
async def get():
    return FileResponse("openai_tts.html")

