import asyncio
import base64
from collections import deque
import os
import boto3
import io
from openai import OpenAI
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import re
from typing import AsyncGenerator, Generator
import json
from typing_extensions import override
from openai import AssistantEventHandler

load_dotenv()

app = FastAPI()

# Allowing CORS to handle requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Load environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")

# Initialize Polly client for Text-to-Speech
polly_client = boto3.client(
    'polly',
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def text_to_audio(text):
    # Use Amazon Polly to convert text to audio
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Aditi"  # You can choose different voices here
    )
    return response['AudioStream'].read()


async def stream_text_to_audio(response_stream, websocket):
    chunks = await chunk_response(response_stream)
    for chunk in chunks:
        print(f"Playing chunk: {chunk}")  # Print the chunk on the backend
        audio_data = text_to_audio(chunk)
        await websocket.send_bytes(audio_data)
        await asyncio.sleep(1)  # Add a delay between sending each chunk


def chunk_text(text, chunk_size=5):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks


llm_chat = ChatOpenAI(temperature=0, streaming=True, model="gpt-3.5-turbo")
def chat_langchain(text):
    messages = [HumanMessage(content=f"Write something about {text}")]
    response_stream = llm_chat.stream(messages)
    response_stream = aiter_generator(response_stream)
    return response_stream

async def chunk_response(response_stream, chunk_size=5):
    chunks = deque()
    current_chunk = []
    async for chunk in response_stream:
        word = chunk.content.strip()
        if word:
            # Split the word into a list of words and punctuation marks
            word_parts = re.split(r'([?.,!;])', word)
            for i, part in enumerate(word_parts):
                if part:
                    if part in "?.,!;":
                        # If the part is a delimiter, associate it with the next word
                        if i < len(word_parts) - 1:
                            current_chunk.append(part + word_parts[i + 1])
                        else:
                            current_chunk.append(part)
                    else:
                        current_chunk.append(part)
                    if len(current_chunk) == chunk_size:
                        chunks.append(' '.join(current_chunk))
                        current_chunk = []
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


async def text_to_audio_chunks(chunk_list, websocket):
    for chunk in chunk_list:
        await websocket.send_text(chunk)

class Transcript(BaseModel):
    transcript: str


async def aiter_generator(generator: Generator):
    """Convert a generator to an async iterator."""
    for item in generator:
        yield item

@app.websocket("/stts")
async def stts_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    mode = 'receive'  # Initial mode is 'receive'
    while True:
        try:
            if mode == 'receive':                
                data = await websocket.receive_text()
                print(f"Received from frontend: {data}")  # Print the received transcript

                # Use LangChain chat model to generate the response
                response_stream = chat_langchain(data)
                print(response_stream)

                # Stream the text to audio and send to the WebSocket
                await stream_text_to_audio(response_stream, websocket)
                
                mode = 'send'  # Switch mode to 'send' after sending audio
            else:
                # Mode is 'send', wait for the frontend to send new data
                data = await websocket.receive_text()
                print(f"Received from frontend, but mode is send: {data}")
                mode = 'receive'  # Switch mode to 'receive' after receiving new data
        except WebSocketDisconnect:
            break


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)