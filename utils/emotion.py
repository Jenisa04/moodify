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
        resp = requests.post(_API_URL, headers=headers, data=image_bytes, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and data:
            top = max(data, key=lambda x: x["score"])
            return top["label"], top["score"]
        elif isinstance(data, dict) and "error" in data:
            st.error(f"Hugging Face API Error: {data['error']}")
    except requests.exceptions.HTTPError as err:
        # Catch and display the error safely in Streamlit
        status = err.response.status_code
        msg = err.response.text
        st.error(f"💥 Hugging Face API Error ({status}): {msg}")
    except requests.exceptions.Timeout:
        st.error("⏳ Hugging Face API request timed out.")
    except Exception as err:
        st.error(f"🚨 Unexpected error: {err}")

    # Fallback if API call fails
    return "neutral", 0.0

