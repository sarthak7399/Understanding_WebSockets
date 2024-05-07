## Speech-to-Text & Text-to-Audio Streaming

This project consists of a frontend and backend for performing speech-to-text and text-to-audio streaming using FastAPI, WebSocket, and OpenAI. Below are the instructions to run both the frontend and backend components.

## Backend

### Prerequisites
- Python 3.7 or higher
- AWS account with Polly service enabled
- OpenAI API key

### Install the required Python packages:
1. pip install openai langchain asyncio base64 boto3 dotenv fastapi langchain-openai pydantic typing-extensions uvicorn


### Configuration
1. Set up environment variables:
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
- `OPENAI_API_KEY`: Your OpenAI API key.

### Running the Backend
1. Run the FastAPI server using Uvicorn:
'''
uvicorn chunked_audio_streaming:app --reload
'''


## Frontend

### Prerequisites
- Web browser with WebSocket support

### Running the Frontend
1. Open `chunked_audio_streaming.html` in a web browser.
2. Click on the "Start Listening" button to start speech recognition.
3. Speak into your microphone. Your speech will be converted to text and sent to the backend.
4. The backend will process the text, generate a response, and stream the audio back to the frontend for playback.

## Usage
- The frontend provides a simple interface for initiating speech recognition and listening to the response from the backend.
- The backend uses AWS Polly for text-to-audio conversion and OpenAI's language model for generating responses.

