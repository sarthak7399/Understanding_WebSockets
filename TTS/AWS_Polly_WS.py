# backend.py

import boto3
import io
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


# Load environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


# Initialize Polly client for Text-to-Speech
polly_client = boto3.client(
    'polly',
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

async def synthesize_text_to_audio(text):
    audio_stream = polly_client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Aditi"
    )['AudioStream'].read()
    return audio_stream

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = "Hello I'm Polly, This is a text to speech synthesis example."
        audio_stream = await synthesize_text_to_audio(data)
        await websocket.send_bytes(audio_stream)
    except WebSocketDisconnect:
        pass
