from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
import boto3
import websockets
from langchain_openai import ChatOpenAI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Allow all origins for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AWS Polly client
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
polly_client = boto3.client(
    'polly',
    region_name="us-west-2",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Initialize OpenAI language model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm_chat = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, streaming=True, model="gpt-3.5-turbo")

# Function to generate response using OpenAI language model
def chat_langchain(text):
    messages = [
        ("system", "You are a helpful assistant."),
        ("human", f"Write something about {text}"),
    ]
    response_stream = llm_chat.stream(messages)
    return response_stream

# Function to synthesize text to audio using AWS Polly
def text_to_audio(text):
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Aditi"
    )
    audio_data = response['AudioStream'].read()
    return audio_data

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("WebSocket connection established")
    await websocket.accept()
    initial_flag = True

    try:
        while True:
            # Receive message from client
            if initial_flag:
                initial_flag = False
                initial_audio = text_to_audio("Hi, I'm your personal assistant. How can I help you today?")
                await websocket.send_bytes(initial_audio)
            message = await websocket.receive_text()
            print("Received text:", message)

            if message:
                # Get response stream
                response_stream = chat_langchain(message)

                # Initialize combined_chunk
                combined_chunk = ""

                # Read and process chunks from the response stream
                try:
                    for item in response_stream:
                        content = item.content
                        combined_chunk += content

                        # Check if combined_chunk ends with a sentence-ending punctuation
                        if combined_chunk and combined_chunk[-1] in [".", "!", "?"]:
                            # Process combined_chunk (e.g., perform chunk processing logic)
                            processed_chunk = combined_chunk  # Placeholder for your chunk processing logic
                            # Synthesize text to audio
                            audio_data = text_to_audio(processed_chunk)
                            # Send audio data to client
                            await websocket.send_bytes(audio_data)
                            print(combined_chunk)
                            # Clear combined_chunk
                            combined_chunk = ""

                except StopIteration:
                    pass

                # If there's any remaining content in combined_chunk, process and send it
                if combined_chunk:
                    # Process combined_chunk (e.g., perform chunk processing logic)
                    processed_chunk = combined_chunk  # Placeholder for your chunk processing logic
                    # Synthesize text to audio
                    audio_data = text_to_audio(processed_chunk)
                    
                    # Send audio data to client
                    await websocket.send_bytes(audio_data)

                # Send last chunk indicator
                await websocket.send_text("LAST_CHUNK")

    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket connection closed")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

