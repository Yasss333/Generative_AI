from dotenv import load_dotenv
from openai import OpenAI
import subprocess
import requests
import json
import os

# ------------------------
# Setup
# ------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ------------------------
# Tools
# ------------------------

def run_command(command: str):
    """Execute shell command"""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr


def create_file(filename: str, content: str):
    """Create a file and write content"""
    with open(filename, "w") as f:
        f.write(content)

    return f"File '{filename}' created successfully."


def read_file(filename: str):
    """Read file content"""
    try:
        with open(filename, "r") as f:
            return f.read()
    except:
        return "File not found."


def weather_api(city: str):
    """Get weather from OpenWeather"""
    api_key = os.getenv("WEATHER_API_KEY")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    temp = data["main"]["temp"]
    weather = data["weather"][0]["description"]

    return f"{temp}°C, {weather}"


# ------------------------
# Tool Router
# ------------------------

def execute_tool(tool, args):

    if tool == "run_command":
        return run_command(args["command"])

    if tool == "create_file":
        return create_file(args["filename"], args["content"])

    if tool == "read_file":
        return read_file(args["filename"])

    if tool == "weather_api":
        return weather_api(args["city"])

    return "Unknown tool"


# ------------------------
# Agent Prompt
# ------------------------

system_prompt = """
You are an AI agent.

You solve tasks step by step.

Steps:
plan -> question -> action -> output

Tools available:

run_command
args: {"command": "shell command"}

create_file
args: {"filename": "...", "content": "..."}

read_file
args: {"filename": "..."}

weather_api
args: {"city": "..."}

Always respond ONLY in JSON:

{
 "step": "plan | question | action | output",
 "tool": "tool_name",
 "args": {},
 "content": "explanation"
}

Rules:
- Only ONE step at a time
- If information missing → ask question
- If tool needed → action
- If task finished → output
"""

messages = [
    {"role": "system", "content": system_prompt}
]

print("\n🤖 AI Agent Ready (type 'exit' to quit)\n")

# ------------------------
# Agent Loop
# ------------------------

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    while True:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        reply = response.choices[0].message.content

        try:
            data = json.loads(reply)
        except:
            print("Invalid JSON from model:", reply)
            break

        print("\nAgent:", data)

        step = data["step"]

        messages.append({
            "role": "assistant",
            "content": reply
        })

        # ------------------------
        # Question Step
        # ------------------------

        if step == "question":

            question = data["content"]
            print("\nAgent asks:", question)

            user_reply = input("Your answer: ")

            messages.append({
                "role": "user",
                "content": user_reply
            })

            continue

        # ------------------------
        # Action Step
        # ------------------------

        if step == "action":

            tool = data["tool"]
            args = data["args"]

            result = execute_tool(tool, args)

            print("\nTool Result:", result)

            messages.append({
                "role": "assistant",
                "content": f"Observation: {result}"
            })

            continue

        # ------------------------
        # Output Step
        # ------------------------


        if step == "output":

            print("\nFinal Answer:", data["content"])
            break