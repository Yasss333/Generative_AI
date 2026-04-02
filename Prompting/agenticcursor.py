import os
import subprocess
import json
from openai import OpenAI
from dotenv import load_dotenv

# ---------------- SETUP ----------------
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

ALLOWED_PACKAGES = ["express", "jsonwebtoken", "mongoose", "cors"]


# ---------------- BASIC UTILS ----------------
def run_command(command, cwd=None):
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        text=True,
        capture_output=True
    )
    print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def clean_json_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
    return text.strip()


# ---------------- AI FUNCTIONS ----------------
def plan_actions(user_input, code):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI coding agent.

Return ONLY valid JSON.

Allowed actions:
- install
- create_file
- modify_file

Example:
[
  {"action": "install", "package": "jsonwebtoken"},
  {"action": "create_file", "file": "routes/auth.js"},
  {"action": "modify_file", "file": "server.js"}
]
"""
            },
            {
                "role": "user",
                "content": f"Code:\n{code}\n\nTask:\n{user_input}"
            }
        ]
    )

    return response.choices[0].message.content.strip()


def ai_modify_code(user_input, existing_code):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Modify code based on request. Return ONLY full updated code."
            },
            {
                "role": "user",
                "content": f"Code:\n{existing_code}\n\nTask:\n{user_input}"
            }
        ]
    )
    return response.choices[0].message.content.strip()


def generate_file_code(user_input, file_name):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Generate code for this file. Return ONLY code."
            },
            {
                "role": "user",
                "content": f"Task: {user_input}\nFile: {file_name}"
            }
        ]
    )
    return response.choices[0].message.content.strip()


# ---------------- EXECUTOR ----------------
def execute_actions(actions, project_path, user_input):
    for action in actions:

        if action["action"] == "install":
            pkg = action["package"]

            if pkg not in ALLOWED_PACKAGES:
                print(f"❌ Blocked package: {pkg}")
                continue

            print(f"📦 Installing {pkg}")
            run_command(f"npm install {pkg}", cwd=project_path)

        elif action["action"] == "create_file":
            file_path = os.path.join(project_path, action["file"])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            print(f"📄 Creating {action['file']}")

            code = generate_file_code(user_input, action["file"])

            with open(file_path, "w") as f:
                f.write(code)

        elif action["action"] == "modify_file":
            file_path = os.path.join(project_path, action["file"])

            if not os.path.exists(file_path):
                print(f"❌ File not found: {action['file']}")
                continue

            print(f"✏️ Modifying {action['file']}")

            existing_code = read_file(file_path)
            updated_code = ai_modify_code(user_input, existing_code)

            with open(file_path, "w") as f:
                f.write(updated_code)

#-------------------Create Project -----------------
def create_express_app(project_name):
    project_path = os.path.join(os.getcwd(), project_name)

    if os.path.exists(project_path):
        print("❌ Project already exists")
        return

    print(f"🚀 Creating {project_name}...")

    os.mkdir(project_path)

    run_command("npm init -y", cwd=project_path)
    run_command("npm install express", cwd=project_path)

    server_code = f"""
const express = require('express');
const app = express();

app.get('/', (req, res) => {{
  res.send('Hello from {project_name}');
}});

app.listen(3000, () => {{
  console.log('Server running on port 3000');
}});
"""

    with open(os.path.join(project_path, "server.js"), "w") as f:
        f.write(server_code)

    print("✅ Project created!")

# ---------------- MAIN AGENT ----------------
def agent_run(user_input, project_name):
    project_path = os.path.join(os.getcwd(), project_name)

    server_path = os.path.join(project_path, "server.js")

    if not os.path.exists(server_path):
        print("❌ server.js not found")
        return

    print("📖 Reading code...")
    existing_code = read_file(server_path)

    print("🧠 Planning...")
    raw_plan = plan_actions(user_input, existing_code)

    cleaned = clean_json_response(raw_plan)

    try:
        actions = json.loads(cleaned)
    except:
        print("❌ JSON failed")
        print(cleaned)
        return

    print("⚙️ Executing...")
    execute_actions(actions, project_path, user_input)

    print("✅ Done!")


# ---------------- CLI ----------------
def main():
    print("🤖 AI Agent Ready")
    print("Commands:")
    print("- create <project_name>")
    print("- <task> <project_name>\n")

    while True:
        user_input = input(">> ").lower()

        if user_input == "exit":
            break

        parts = user_input.split()

        if len(parts) < 2:
            print("❌ Invalid input")
            continue

        # ✅ HANDLE CREATE
        if parts[0] == "create":
            project_name = parts[1]
            create_express_app(project_name)
            continue

        # ✅ HANDLE AI TASK
        project_name = parts[-1]
        agent_run(user_input, project_name)


if __name__ == "__main__":
    main()