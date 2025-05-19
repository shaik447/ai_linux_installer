#!/bin/bash
set -e

echo "[INFO] Installing uv (fast Python package manager)..."

# Detect OS and install curl if missing (macOS/Linux)
if ! command -v curl >/dev/null 2>&1; then
  echo "[INFO] curl not found. Installing curl..."
  if [[ "$(uname)" == "Darwin" ]]; then
    brew install curl
  else
    sudo apt-get update -y && sudo apt-get install -y curl
  fi
fi

# Install uv
curl -Ls https://astral.sh/uv/install.sh | sh

# Ensure uv is in PATH (for current shell)
export PATH="$HOME/.cargo/bin:$PATH"

# Create venv if not exists
if [ ! -d "venv" ]; then
  echo "[INFO] Creating Python virtual environment with uv..."
  uv venv venv
fi

# Activate venv
source venv/bin/activate

echo "[INFO] Installing Python dependencies from requirements.txt..."
uv pip install -r requirements.txt

echo "[INFO] Setup complete. To activate your environment, run:"
echo "  source venv/bin/activate"
echo "[INFO] Then run:"
echo "  python3 ai_installer.py"
