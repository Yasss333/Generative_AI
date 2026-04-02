# import pyttsx3

# engine = pyttsx3.init()

# text = "Hello Yash, welcome to Swastik Bank!"

# engine.say(text)
# engine.runAndWait()
from openai import OpenAI
from dotenv import load_dotenv
# from openai import OpenAI
import os 

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
# client = OpenAI()

speech = client.audio.speech.create(
    model="openai/gpt-4o-mini-tts",
    voice="alloy",
    input="Hello Yash, welcome to Swastik Bank!"
)

with open("speech.mp3", "wb") as f:
    f.write(speech.read())