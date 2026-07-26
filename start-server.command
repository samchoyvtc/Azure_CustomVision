#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -f config.py ]]; then
  echo "Missing config.py — copy config.example.py to config.py and fill in your Azure credentials."
  read -r -p "Press Enter to close..."
  exit 1
fi

if [[ ! -d .venv ]]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

if ! python -c "import flask, requests" >/dev/null 2>&1; then
  echo "Installing Python dependencies..."
  python -m pip install -r requirements.txt
fi

URL="http://127.0.0.1:8080"
echo "Starting Azure Custom Vision app at ${URL}"
echo "Close this Terminal window (or press Ctrl+C) to stop the server."
echo

# Open the browser shortly after the server starts
(
  sleep 1
  open "${URL}"
) &

# Run in the foreground so closing/killing this Terminal stops the server
python server.py
