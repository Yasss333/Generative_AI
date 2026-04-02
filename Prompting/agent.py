import os 
import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import pyttsx3

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

engine = pyttsx3.init()
text = "Achaa beta"

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()


# engine.runAndWait()

Sytem_prompt = """
You are a helpful cli agent you generate commands through user query 
in response you only give command 
Format: create_express <project_name>
ONLY return command, nothing else.
"""


# ✅ FIXED (renamed to avoid recursion conflict)
def ai_modify_code(user_input, existing_code):
    result = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a backend engineer. Your task is to generate error-free code as the user asks and ONLY return updated full code"
            },
            {
                "role": "user",
                "content": f"Code:\n{existing_code}\n\nTask:\n{user_input}"
            }
        ]
    )   
    return result.choices[0].message.content.strip()


def run_command(command, cwd=None):
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            shell=True,
            capture_output=True
        )
        print(result.stdout)
        if result.stderr:
            print("Failed to execute the command:", result.stderr)
    except Exception as e:
        print("Execution Error:", str(e))


# ❌ COMMENTED (not removed as you said)
# def create_express_app(project_name, ):
#     project_name="my express app"
#     project_path=os.path.join(os.getcwd(),project_name)
#     if os.path.exists(project_path):
#         print("Project already exist")
#         return 
#     print(f"Creating express application Name:{project_name}....")
#     os.mkdir(project_path)
#     run_command("npm init -y",cwd=project_path)
#     run_command("npm install express",cwd=project_path)
#     server_code=f"""
# const express = require('express');
# const app = express();
#
# app.get('/', (req, res) => {{
#   res.send('Hello from {project_name}');
# }});
#
# app.listen(3000, () => {{
#   console.log('Server running on port 3000');
# }});
# """
#     with open(os.path.join(project_path,"server.js"),"w") as f:
#         f.write(server_code)
#     print("Express app created")


# ✅ FIXED main modify function
def modify_code(user_input, project_name):
    project_path = os.path.join(os.getcwd(), project_name)  # ❗ FIXED os.cwd → os.getcwd
    file_path = os.path.join(project_path, "server.js")

    if not os.path.exists(file_path):
        print("server.js does not exist")
        return
    
    print("📖 Reading existing code...")
    existing_code = read_file(file_path)

    print("🤖 Modifying code...")
    updated_code = ai_modify_code(user_input, existing_code)  # ❗ FIXED recursion bug

    with open(file_path, "w") as f:
        f.write(updated_code)

    print("✅ Code updated 💘")


# ❌ COMMENTED (ask_ai not defined yet)
# def handle_command(user_input):
#     if user_input == "exit":
#         print("👋 Exiting agent...")
#         exit()
#
#     if user_input == "help":
#         print("Just type what you want. Example:")
#         print("create backend for blog")
#         return
#
#     print("🤖 Thinking...")
#
#     ai_command = ask_ai(user_input)
#     print("AI says:", ai_command)
#
#     parts = ai_command.split()
#
#     if len(parts) >= 2 and parts[0] == "create_express":
#         project_name = parts[1]
#         create_express_app(project_name)
#     else:
#         print("❌ Could not understand AI command")


def main():
    print("🤖 AI Agent Started (Context Mode)")
    print("Type: <task> <project_name>\n")

    while True:
        user_input = input(">> ").lower()

        # simple parsing (last word = project name)
        parts = user_input.split()

        if len(parts) < 2:
            print("❌ Provide task + project name")
            continue

        project_name = parts[-1]
        modify_code(user_input, project_name)


if __name__ == "__main__":
    main()