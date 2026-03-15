from dotenv import load_dotenv
from openai import OpenAI
import json
import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

def weather_api(city:str):
    return "31 degree celcius"


system_prompt=''' 
 You are an AI agent that works in steps:
start -> plan -> verify -> action -> output

Always return JSON in this format:

{
 "step": "plan",
 "content": "explanation of what you will do"
}

Only return ONE step at a time.
'''

messages=[
    {"role":"system","content":system_prompt},
    {"role": "user", "content": "What is the weathe in Mumbai rightnow?"}

]
    



while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        # response_format={'type':"json_object"},
        messages=messages
    )

    reply =response.choices[0].message.content  
    data=json.loads(reply)

    print('Agent : ',data)
    step=data["step"]
    #append message in the asisitnat 
    messages.append({
        "role":"assistant",
        "content":reply
    })

    #action step
    if step=="action":
        if "weather_api" in data["content"]:
            result=weather_api("Mumbai")

            messages.append({
                "role":"assistant",
                "content":result
            })
    if step == "output":
        break