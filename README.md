# Azure Custom Vision — Image Classifier

A Python (Flask) web app that lets you upload an image and classify it with Azure Custom Vision. The Prediction API key stays on the server — no JavaScript frontend logic.

## Prerequisites

- Python 3.10+
- An Azure Custom Vision **Classification** project with a **published** iteration

## Setup

1. Copy the config template:

   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` with values from your Custom Vision **Prediction URL**:

   ```python
   ENDPOINT = "https://your-resource.cognitiveservices.azure.com"
   PREDICTION_KEY = "your-prediction-key"
   PROJECT_ID = "your-project-guid"
   ITERATION_NAME = "Iteration1"
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Run

**Mac:** double-click `start-server.command` (opens Terminal).  
**Windows:** double-click `start-server.bat` (opens Command Prompt).  

Close that window or press Ctrl+C to stop the server.

Or from a terminal:

```bash
source .venv/bin/activate   # Windows: .venv\Scripts\activate
python server.py
```

Open http://127.0.0.1:8080 in your browser.

## How It Works

1. Choose an image and click **Classify Image**.
2. The Python backend sends the image bytes to Azure Custom Vision.
3. Predictions are rendered below the image (top label + confidence bars).

## Security Note

`config.py` holds your Prediction key and is listed in `.gitignore`. Do not commit it.
