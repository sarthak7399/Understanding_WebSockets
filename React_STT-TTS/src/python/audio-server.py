import asyncio
from fastapi import FastAPI, WebSocket

app = FastAPI()

async def stream_audio(websocket: WebSocket):
    await websocket.accept()
    try:
        with open("audio.mp3", "rb") as audio_file:
            while True:
                audio_chunk = audio_file.read(1024 * 1024)  # Read 1MB chunk of the MP3 file
                if not audio_chunk:
                    break
                await websocket.send_bytes(audio_chunk)
                await asyncio.sleep(0.1)  # Adjust the sleep duration as needed
    except Exception as e:
        print(f"Error streaming audio: {e}")

@app.websocket("/audio")
async def audio(websocket: WebSocket):
    print("WebSocket connection established")
    await stream_audio(websocket)
