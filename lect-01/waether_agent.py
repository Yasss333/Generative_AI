from dotenv import load_dotenv
from openai import OpenAI
import requests
import json
import os
import subprocess


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

command=input("Enter task : ")

def run_command(command:str):
    result=subprocess.run(
        command,
         capture_output=True,
        text=True
    )
    return result.stdout + result.stderr

def weather_api(city:str):
    print("🏹 Tool si called ")
    api_key = os.getenv("WEATHER_API_KEY")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)

    data = response.json()

    temp = data["main"]["temp"]
    weather = data["weather"][0]["description"]

    return f"{temp}°C, {weather}"


system_prompt=''' 
 You are an AI agent that works in steps:
start -> plan -> verify -> action -> output
keep you text concise and clear 
Always return JSON in this format:

{
 "step": "plan",
 "content": "explanation of what you will do"
}

Only return ONE step at a time.
'''

messages=[
    {"role":"system","content":system_prompt},
    {"role": "user", "content": "What is the weathe in {city} rightnow?"}

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
    if step == "action":
      command = data["content"]

      result = run_command(command)

      messages.append({
        "role": "assistant",
        "content": result
    })
    if step == "output":
        break