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
import json

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

llm = ChatOpenAI(temperature=0) # Define the langchain chat function

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

def chat_openai(text):
    client = OpenAI()
    prompt = "Hello you need to answer to following questions"
    messages = [
        {"role": "system", "content": "You are an assistant that replies in a poetic manner."},
        {"role": "user", "content": f'Write a few lines on {text}'}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        # stream=True
    )
    
    return response.choices[0].message.content


def text_to_audio(text):
    # Use Amazon Polly to convert text to audio
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Joanna"  # You can choose different voices here
    )
    return response['AudioStream'].read()

class Transcript(BaseModel):
    transcript: str

recieved_data = None

@app.websocket("/stts")
async def stts_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    mode = 'receive'  # Initial mode is 'receive'
    while True:
        try:
            if mode == 'receive':
                data = await websocket.receive_text()
                print(f"Received from frontend: {data}")  # Print the received transcript
                openai_response = chat_openai(data)
                print("Response from OpenAI:", openai_response)
                audio_data = text_to_audio(openai_response)
                await websocket.send_bytes(audio_data)
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
