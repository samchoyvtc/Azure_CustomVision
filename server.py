#!/usr/bin/env python3
"""Azure Custom Vision image classifier — Python backend."""

from __future__ import annotations

import base64
import mimetypes
import sys

import requests
from flask import Flask, render_template, request

try:
    import config
except ImportError:
    print("Missing config.py — copy config.example.py to config.py and fill in your Azure credentials.")
    sys.exit(1)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB


def config_is_valid() -> bool:
    values = (
        config.ENDPOINT,
        config.PREDICTION_KEY,
        config.PROJECT_ID,
        config.ITERATION_NAME,
    )
    return all(
        isinstance(value, str)
        and value
        and not (value.startswith("<") and value.endswith(">"))
        for value in values
    )


def confidence_class(probability: float) -> str:
    if probability > 0.8:
        return "top-result--high"
    if probability >= 0.5:
        return "top-result--medium"
    return "top-result--low"


def prediction_url() -> str:
    endpoint = config.ENDPOINT.rstrip("/")
    return (
        f"{endpoint}/customvision/v3.0/Prediction/"
        f"{config.PROJECT_ID}/classify/iterations/{config.ITERATION_NAME}/image"
    )


def classify_image(image_bytes: bytes) -> list[dict]:
    response = requests.post(
        prediction_url(),
        headers={
            "Prediction-Key": config.PREDICTION_KEY,
            "Content-Type": "application/octet-stream",
        },
        data=image_bytes,
        timeout=30,
    )

    if response.status_code in (401, 403):
        raise RuntimeError("Invalid API key")
    if response.status_code == 404:
        raise RuntimeError("Check project ID / iteration name")
    if not response.ok:
        raise RuntimeError(f"API error ({response.status_code})")

    payload = response.json()
    predictions = payload.get("predictions") or []
    return sorted(predictions, key=lambda item: item.get("probability", 0), reverse=True)


def image_data_url(image_bytes: bytes, filename: str) -> str:
    mime, _ = mimetypes.guess_type(filename)
    if not mime or not mime.startswith("image/"):
        mime = "image/jpeg"
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime};base64,{encoded}"


@app.route("/", methods=["GET", "POST"])
def index():
    status = "Choose an image to classify"
    status_error = False
    error = None
    image_url = None
    top_result = None
    top_class = ""
    predictions: list[dict] = []

    if not config_is_valid():
        status = "Configure config.py before uploading"
        status_error = True

    if request.method == "POST":
        if not config_is_valid():
            status = "Configure config.py before uploading"
            status_error = True
            error = "Missing or incomplete Azure credentials in config.py"
        else:
            uploaded = request.files.get("image")
            if uploaded is None or not uploaded.filename:
                status = "Please choose an image file"
                status_error = True
                error = "No image selected"
            else:
                image_bytes = uploaded.read()
                if not image_bytes:
                    status = "Please choose an image file"
                    status_error = True
                    error = "Empty file"
                else:
                    image_url = image_data_url(image_bytes, uploaded.filename)
                    try:
                        raw_predictions = classify_image(image_bytes)
                        if not raw_predictions:
                            error = "No match"
                            status = f"Classified: {uploaded.filename}"
                        else:
                            predictions = [
                                {
                                    "tagName": item.get("tagName", "Unknown"),
                                    "percent": round(float(item.get("probability", 0)) * 100),
                                }
                                for item in raw_predictions
                            ]
                            top = predictions[0]
                            top_result = f"{top['tagName']} — {top['percent']}%"
                            top_class = confidence_class(
                                raw_predictions[0].get("probability", 0)
                            )
                            status = f"Classified: {uploaded.filename}"
                    except requests.RequestException:
                        status = "Connection failed"
                        status_error = True
                        error = "Connection failed"
                    except RuntimeError as exc:
                        status = str(exc)
                        status_error = True
                        error = str(exc)

    return render_template(
        "index.html",
        status=status,
        status_error=status_error,
        error=error,
        image_url=image_url,
        top_result=top_result,
        top_class=top_class,
        predictions=predictions,
    )


def main() -> None:
    host = getattr(config, "HOST", "127.0.0.1")
    port = int(getattr(config, "PORT", 8080))
    print(f"Starting Azure Custom Vision app at http://{host}:{port}")
    if not config_is_valid():
        print("Warning: config.py still has placeholder values.")
    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    main()
