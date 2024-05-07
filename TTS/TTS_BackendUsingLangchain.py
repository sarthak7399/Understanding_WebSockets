from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from playsound import playsound 
import io
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pdb
import os
import boto3
from pydub import playback, AudioSegment
from pydub.playback import play 


load_dotenv()


# Load environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")

llm_chat = ChatOpenAI(temperature=0, streaming=True, model="gpt-3.5-turbo")

# Initialize Polly client for Text-to-Speech
polly_client = boto3.client(
    'polly',
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def chat_langchain(text):
    messages = [HumanMessage(content=f"Write something about {text}")]
    response_stream = llm_chat.stream(messages)

    return response_stream

def text_to_audio(text):
    # Use Amazon Polly to convert text to audio
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Aditi"  # You can choose different voices here
    )
    audio_data = response['AudioStream'].read()  # Read audio data from the stream
    return audio_data


def consume_and_send_text(stream):
    combined_chunk = ""
    for item in stream:
        content = item.content
        combined_chunk += content
        if combined_chunk:
            if combined_chunk[-1] in [".", "!", "?"]:
                # text_to_audio(combined_chunk)
                audio_data = text_to_audio(combined_chunk)  # Convert text to audio
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")  # Load audio data into Pydub AudioSegment
                play(audio_segment)
                combined_chunk = ""
            else:
                pass



def main():
    text_stream = chat_langchain("Hello")
    consume_and_send_text(text_stream)

# Run the main function
main()
