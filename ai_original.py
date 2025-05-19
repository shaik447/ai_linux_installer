import subprocess
import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Load .env file
load_dotenv()

# Use OpenAI API key from environment
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Prompt: Convert user request to install script
task_to_bash = PromptTemplate.from_template("""
You are a DevOps assistant. Given this user request:

"{task}"

Write a bash script with only the necessary shell commands to install these tools on Ubuntu. 
Do NOT wrap the output in triple backticks, markdown, or quotes. 
Just return raw shell commands — one per line.
No explanations, no comments.
""")


# Prompt: Fix broken shell command
error_fixer = PromptTemplate.from_template("""
You're a Linux troubleshooting expert.
Given this command error:

{error}

Suggest a corrected shell command to fix the problem. Only return the command.
""")

def get_install_commands(task):
    print("🧠 Generating install script...")
    current_task = task

    while True:
        bash_script = llm.predict(task_to_bash.format(task=current_task)).strip()

        # Remove markdown ``` if present
        if bash_script.startswith("```"):
            bash_script = "\n".join(
                line for line in bash_script.splitlines() if not line.startswith("```")
            )

        print("\n📜 Generated Shell Script:")
        print("=" * 40)
        print(bash_script)
        print("=" * 40)

        confirm = input("✅ Do you want to run this script? (y/n): ").strip().lower()

        if confirm == "y":
            return bash_script.splitlines()

        # If user wants changes
        correction = input("✏️  What needs to be modified in the script?\n> ").strip()
        # Construct a new task prompt with correction
        current_task = f"{task}\nModify it like this: {correction}"


def run_command(command):
    print(f"\n🚀 Running: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,            # Decode bytes to string
        bufsize=1             # Line-buffered
    )

    output = ""
    for line in process.stdout:
        print(line, end='')   # Stream to console in real-time
        output += line        # Collect for error analysis

    process.wait()
    success = (process.returncode == 0)

    if success:
        print("✅ Success")
    else:
        print("❌ Error")

    return success, output

def auto_fix(error_output):
    print("🤖 Diagnosing error...")
    fix_command = llm.predict(error_fixer.format(error=error_output)).strip()
    print(f"🛠 Suggested Fix:\n{fix_command}")
    input("Press Enter to apply fix...")
    run_command(fix_command)
    return fix_command

def execute_script(commands):
    for cmd in commands:
        success, output = run_command(cmd)
        if not success:
            fix = auto_fix(output)
            print("🔁 Retrying original command...")
            run_command(cmd)

if __name__ == "__main__":
    user_request = input("💬 What do you want to install?\n> ")
    commands = get_install_commands(user_request)
    execute_script(commands)