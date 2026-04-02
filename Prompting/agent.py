import os 
import subprocess
import pyttsx3
engine = pyttsx3.init()

text = "Achaa beta"

# engine.runAndWait()
def run_command(command, cwd=None):
    try:
        result=subprocess.run(command, cwd=cwd , text=True, shell=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print("Failed to execute teh comannad")
    except Exception as e:
        print("Execution ",str(e))


def create_express_app(project_name):
    project_name="my express app"
    project_path=os.path.join(os.getcwd(),project_name)
    if os.path.exists(project_path):
        print("Project already exist")
        return 
    print(f"Creating express application Name:{project_name}....")
    os.mkdir(project_path)
    run_command("npm init -y",cwd=project_path)
    run_command("npm install express",cwd=project_path)
    server_code=f"""
const express = require('express');
const app = express();

app.get('/', (req, res) => {{
  res.send('Hello from {project_name}');
}});

app.listen(3000, () => {{
  console.log('Server running on port 3000');
}});
"""
    with open(os.path.join(project_path,"server.js"),"w") as f:
        f.write(server_code)
    print("Express app created")
     
def handle_command(user_input):
    parts=user_input.split()
    if len(parts)>3 and parts[0]=="create" and parts[1]=="express":
        project_name=parts[2]
        create_express_app(project_name)
    elif user_input=="help":
        print(""" 
Commands:
- create express <project_name>
- exit
""")
    elif user_input == "exit":
        print("👋 Exiting agent...")
        exit()

    else:
        print("❌ Unknown command. Type 'help'")


def main():
    print("🤖 AI Agent Started (Step 2)")
    print("Type 'help' for commands\n")

    while True:
        user_input = input(">> ").lower()
        handle_command(user_input)




if __name__=="__main__":
    main()