import requests
from typing import Tuple

_MODEL_REPO = "dima806/facial_emotions_image_detection"
_API_URL = f"https://router.huggingface.co/hf-inference/models/{_MODEL_REPO}"

def detect_emotion(image_bytes: bytes, hf_token: str) -> Tuple[str, float]:
    """Return (label, confidence) from Hugging Face model."""
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "image/jpeg",
    }
    try:
        st.write("DEBUG: Sending request to Hugging Face API...")
        resp = requests.post(_API_URL, headers=headers, data=image_bytes, timeout=60)
        st.write(f"DEBUG: Hugging Face API response status: {resp.status_code}")
        resp.raise_for_status()
        data = resp.json()
        st.write(f"DEBUG: API response data: {data}")

        if isinstance(data, list) and data:
            top = max(data, key=lambda x: x["score"])
            return top["label"], top["score"]
        elif isinstance(data, dict) and "error" in data:
            st.error(f"Hugging Face API Error: {data['error']}")
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP Error {err.response.status_code}: {err.response.text}")
    except requests.exceptions.Timeout:
        st.error("Hugging Face API request timed out.")
    except Exception as err:
        st.error(f"Unexpected error: {err}")

    # Fallback
    return "neutral", 0.0

