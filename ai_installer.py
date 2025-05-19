import os
import uuid
import subprocess
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Load OpenAI key
load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Detect OS type
def detect_os():
    try:
        with open("/etc/os-release") as f:
            data = f.read().lower()
            if "ubuntu" in data:
                return "Ubuntu"
            elif "debian" in data:
                return "Debian"
            elif "centos" in data:
                return "CentOS"
            elif "rhel" in data:
                return "RHEL"
            elif "alpine" in data:
                return "Alpine"
            elif "fedora" in data:
                return "Fedora"
    except:
        pass
    try:
        uname = subprocess.check_output("uname", shell=True).decode().strip()
        if uname == "Darwin":
            return "macOS"
    except:
        pass
    return "Unknown"

# Prompt Template for GPT
task_to_bash = PromptTemplate.from_template("""
You are a DevOps assistant. The user is using: {os}

Given this user request:

"{task}"

Provide a clean, production-ready **pure bash script** that can be saved and executed **independently**.

✅ Requirements:
- Tailor the script based on the detected OS: {os}
- Output only the shell script (no markdown, no formatting, no extra text).
- Start the script with `#!/bin/bash`.
- Include `set -e` for fail-fast behavior.
- The script must be fully non-interactive — do not include any commands that pause for input.
- Use proper flags for silent/automatic execution (`-y`, `--yes`, `--noconfirm`, etc.).
- Include logging (`echo`) for key steps.
- Check if the script is run as root or with sudo.
- Do not return explanations, comments, or markdown — only the final bash script content.
""")

# Clean script if GPT wraps in ```bash ... ```
def clean_script_output(script: str) -> str:
    lines = script.strip().splitlines()
    if lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)

# Save script to file with unique name
def save_script_to_file(script_str):
    filename = f"install_{uuid.uuid4().hex[:8]}.sh"
    with open(filename, "w") as f:
        f.write(script_str)
    subprocess.run(["chmod", "+x", filename])
    return filename

# Stream output while running bash script
def run_bash_script(filename):
    print(f"\n🚀 Running: ./{filename}\n")
    process = subprocess.Popen(
        ["sudo", f"./{filename}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    for line in process.stdout:
        print(line, end='')
    process.wait()
    if process.returncode == 0:
        print("\n✅ Script completed successfully.")
    else:
        print(f"\n❌ Script exited with code {process.returncode}.")

# Generate + approve bash script via AI
def get_install_script(task):
    os_type = detect_os()
    print(f"🖥️ Detected OS: {os_type}")
    current_task = task

    while True:
        script = llm.predict(task_to_bash.format(task=current_task, os=os_type)).strip()
        script = clean_script_output(script)

        print("\n📜 Generated Bash Script:")
        print("=" * 50)
        print(script)
        print("=" * 50)

        confirm = input("✅ Do you want to run this script? (y/n): ").strip().lower()
        if confirm == "y":
            return script

        correction = input("✏️  What needs to be modified in the script?\n> ").strip()
        current_task = f"{task}\nModify it like this: {correction}"

# Main program
if __name__ == "__main__":
    user_input = input("💬 What do you want to install?\n> ")
    final_script = get_install_script(user_input)
    filename = save_script_to_file(final_script)
    run_bash_script(filename)
