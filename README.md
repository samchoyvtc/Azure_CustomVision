# Azure Custom Vision — Image Classifier

A Python (Flask) web app that lets you paste your Azure Custom Vision Prediction URL and key, upload an image, and see classification results.

## Prerequisites

- Python 3.10+
- An Azure Custom Vision **Classification** project with a **published** iteration

## Setup

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

## How to use

1. Paste your **Prediction URL** from the Custom Vision portal, for example:

   ```
   https://your-resource-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/00000000-0000-0000-0000-000000000000/classify/iterations/Iteration1/image
   ```

   The app reads the endpoint, project ID, and iteration name from this URL.

2. Enter your **Prediction Key**.
3. Choose an image and click **Classify Image**.
4. Results appear below the image (top label + confidence bars).

## Security Note

Credentials are entered in the browser form and sent only to your local Python server, which then calls Azure. Do not deploy this demo publicly without protecting access — Prediction keys should not be shared.
