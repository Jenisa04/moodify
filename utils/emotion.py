import requests
from typing import Tuple

_MODEL_REPO = "dima806/facial_emotions_image_detection"
_API_URL = f"https://router.huggingface.co/hf-inference/models/{_MODEL_REPO}"

def detect_emotion(image_bytes: bytes, hf_token: str) -> Tuple[str, float]:
    """Return (label, confidence) from Hugging Face model."""
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "image/jpeg",          # important for router endpoint
    }
    resp = requests.post(_API_URL, headers=headers, data=image_bytes, timeout=30)
    resp.raise_for_status()
    data = resp.json()                         # list of {label, score}

    if isinstance(data, list) and data:
        top = max(data, key=lambda x: x["score"])
        return top["label"], top["score"]
    return "neutral", 0.0                      # graceful fallback
