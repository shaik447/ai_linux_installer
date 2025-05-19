# 🤖 AI-Powered Linux Installer

This project uses OpenAI GPT-4o + LangChain to generate fully automated, production-ready shell scripts based on your natural language input.

---

## 🧠 What It Does

* Understands requests like:
  `Install Docker, Node.js 20, and Git`

* Detects your OS (Ubuntu, Debian, CentOS, RHEL, Alpine, macOS)

* Generates a self-contained, non-interactive Bash script tailored to your OS

* Saves the script with a unique filename

* Streams the script’s output as it runs

* Fixes formatting if the script is wrapped in markdown (`bash ... `)

---

## ⚙️ Requirements

* Python 3.8+
* An OpenAI API Key with GPT-4o access
* Linux/macOS system (or VM)

---

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourname/ai-installer.git
cd ai-installer
```

### 2. Install `uv` (Fast Python Package Manager)

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### 3. Create a `.env` file

```bash
echo "OPENAI_API_KEY=your-openai-key-here" > .env
```

### 4. Install Dependencies

```bash
uv venv venv
source venv/bin/activate
uv pip install -r requirements.txt
```

> If you're using `pip`, replace `uv pip` with `pip`.

---

## 📦 Run the Program

```bash
source venv/bin/activate
python3 ai_installer.py
```

---

## 💬 Example Interaction

```bash
📬 What do you want to install?
> Install docker, node 20, and git

💻 Detected OS: Ubuntu

📜 Generated Bash Script:
#!/bin/bash
set -e
...
✅ Do you want to run this script? (y/n): y
🚀 Running: ./install_23abcd45.sh
[INFO] Installing Docker...
...
✅ Script completed successfully.
```

---

## 🛡 Features

* Detects your OS automatically
* Cleans up markdown formatting from GPT output
* Creates unique filenames (e.g. `install_98afd123.sh`)
* Requires no manual intervention during install
* Supports GPT-4o for fast and cost-effective performance

---

## 🧼 Cleanup

You can remove generated files with:

```bash
rm install_*.sh
```

---

## 📌 Notes

* This script uses `sudo` to run installation commands.
* Review the script before approving it to run.
* The assistant will ask for confirmation and allow modification before execution.

---

## 👨‍💻 Author

Built by \[Your Name] — DevOps & AI Automation Enthusiast
Feel free to fork, improve, and share!
