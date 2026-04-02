from dotenv import load_dotenv
from openai import OpenAI
import pyttsx3

engine = pyttsx3.init()
import os 

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# 👇 take id once
id = int(input("Enter your ID: "))

# 👇 clean system prompt (no dynamic variables inside)
system_prompt = """
You are a banking assistant for Swastik Bank.

Rules:
- Always respond in English
- Always respond in valid JSON format
- Start with a welcome message

Valid IDs: 1 to 9

Logic:
- If ID < 5 → balance = 1000
- If ID >= 5 → balance = 2000

Supported actions:
- Check balance
- Add money
- Change PIN

If invalid input → return error message
"""

# 👇 memory
messages = [{"role": "system", "content": system_prompt}]

while True:
    user_input = input("\nEnter your query (type 'exit' to stop): ")

    if user_input.lower() == "exit":
        break

    options = input("1. Check balance\n2. Add money\n3. Change Pin\n")

    # 👇 combine everything into user message
    full_input = f"""
User ID: {id}
User Query: {user_input}
Selected Option: {options}
"""

    messages.append({"role": "user", "content": full_input})

    result = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=messages
    )

    ans = result.choices[0].message.content
  
    print("\nAssistant:", ans)
    engine.say(ans)
    engine.runAndWait()
    # ✅ correct role
    messages.append({"role": "assistant", "content": ans})