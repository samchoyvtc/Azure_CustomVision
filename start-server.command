#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

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

(
  sleep 1
  open "${URL}"
) &

python server.py
