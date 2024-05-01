import os
from dotenv import load_dotenv

from deepgram import DeepgramClient,SpeakOptions

load_dotenv()

SPEAK_OPTIONS = {"text": """Carbon fiber is a lightweight, yet incredibly strong and durable material that has numerous applications across various industries. Here are some of the most common uses of carbon fiber:
                Aerospace: Carbon fiber is widely used in the aerospace industry for the production of aircraft, spacecraft, and missiles due to its high strength-to-weight ratio, corrosion resistance, and ability to withstand extreme temperatures.
                Automotive: Carbon fiber is used in high-performance vehicles, sports cars, and luxury cars to reduce weight, improve fuel efficiency, and enhance handling.
                Sports equipment: Carbon fiber is used in various sports equipment, such as golf clubs, tennis rackets, bicycle frames, and high-end fishing rods, due to its high strength, stiffness, and durability."""}
filename = "output.mp3"


def main():
    try:
        # STEP 1 Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

        # STEP 3 Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav",
            url="https://api.deepgram.com/v1/speak?http://localhost:8000/audio",
        )

        # STEP 2 Call the save method on the speak property
        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()