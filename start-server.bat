@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
  where python3 >nul 2>&1
  if errorlevel 1 (
    echo Error: Python is not installed or not on PATH.
    pause
    exit /b 1
  )
  set PY=python3
) else (
  set PY=python
)

if not exist .venv (
  echo Creating virtual environment...
  %PY% -m venv .venv
)

call .venv\Scripts\activate.bat

python -c "import flask, requests" >nul 2>&1
if errorlevel 1 (
  echo Installing Python dependencies...
  python -m pip install -r requirements.txt
)

set URL=http://127.0.0.1:8080
echo Starting Azure Custom Vision app at %URL%
echo Close this window or press Ctrl+C to stop the server.
echo.

start "" "%URL%"
python server.py

echo.
echo Server stopped.
pause
