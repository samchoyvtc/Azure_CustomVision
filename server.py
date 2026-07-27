#!/usr/bin/env python3
"""Azure Custom Vision image classifier — Python backend."""

from __future__ import annotations

import base64
import mimetypes
import re

import requests
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

HOST = "127.0.0.1"
PORT = 8080

PREDICTION_URL_PATTERN = re.compile(
    r"^(https?://[^/\s]+)/customvision/v3\.0/Prediction/"
    r"([^/\s]+)/classify/iterations/([^/\s]+)/(?:image|url)/?$",
    re.IGNORECASE,
)


def confidence_class(probability: float) -> str:
    if probability > 0.8:
        return "top-result--high"
    if probability >= 0.5:
        return "top-result--medium"
    return "top-result--low"


def parse_prediction_url(raw_url: str) -> tuple[str, str, str]:
    """Return endpoint, project_id, iteration_name from a Prediction URL."""
    match = PREDICTION_URL_PATTERN.match(raw_url.strip())
    if not match:
        raise ValueError(
            "Invalid Prediction URL. Expected a Custom Vision classify URL "
            "ending in /image or /url."
        )
    endpoint, project_id, iteration_name = match.groups()
    return endpoint.rstrip("/"), project_id, iteration_name


def build_image_api_url(endpoint: str, project_id: str, iteration_name: str) -> str:
    return (
        f"{endpoint}/customvision/v3.0/Prediction/"
        f"{project_id}/classify/iterations/{iteration_name}/image"
    )


def classify_image(image_bytes: bytes, api_url: str, prediction_key: str) -> list[dict]:
    response = requests.post(
        api_url,
        headers={
            "Prediction-Key": prediction_key,
            "Content-Type": "application/octet-stream",
        },
        data=image_bytes,
        timeout=30,
    )

    if response.status_code in (401, 403):
        raise RuntimeError("Invalid Prediction Key")
    if response.status_code == 404:
        raise RuntimeError("Check Prediction URL (project ID / iteration name)")
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
    status = "Enter your Azure settings, then choose an image"
    status_error = False
    error = None
    image_url = None
    top_result = None
    top_class = ""
    predictions: list[dict] = []
    prediction_url = ""
    prediction_key = ""

    if request.method == "POST":
        prediction_url = (request.form.get("prediction_url") or "").strip()
        prediction_key = (request.form.get("prediction_key") or "").strip()
        uploaded = request.files.get("image")

        if not prediction_url:
            status = "Prediction URL is required"
            status_error = True
            error = "Please paste your Custom Vision Prediction URL"
        elif not prediction_key:
            status = "Prediction Key is required"
            status_error = True
            error = "Please enter your Prediction Key"
        elif uploaded is None or not uploaded.filename:
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
                    endpoint, project_id, iteration_name = parse_prediction_url(
                        prediction_url
                    )
                    api_url = build_image_api_url(endpoint, project_id, iteration_name)
                    raw_predictions = classify_image(
                        image_bytes, api_url, prediction_key
                    )

                    if not raw_predictions:
                        error = "No match"
                        status = f"Classified: {uploaded.filename}"
                    else:
                        predictions = [
                            {
                                "tagName": item.get("tagName", "Unknown"),
                                "percent": round(
                                    float(item.get("probability", 0)) * 100
                                ),
                            }
                            for item in raw_predictions
                        ]
                        top = predictions[0]
                        top_result = f"{top['tagName']} — {top['percent']}%"
                        top_class = confidence_class(
                            raw_predictions[0].get("probability", 0)
                        )
                        status = f"Classified: {uploaded.filename}"
                except ValueError as exc:
                    status = "Invalid Prediction URL"
                    status_error = True
                    error = str(exc)
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
        prediction_url=prediction_url,
        prediction_key=prediction_key,
    )


def main() -> None:
    print(f"Starting Azure Custom Vision app at http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=False)


if __name__ == "__main__":
    main()
