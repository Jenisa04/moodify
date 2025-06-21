import requests
from typing import List, Dict

_EMOTION_TAG_MAP = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "fear": "dark",        # tag with decent coverage
    "disgust": "grunge",
    "surprise": "funk",
    "neutral": "chill",
}

def lf_tracks(emotion: str, api_key: str, limit: int = 10) -> List[Dict]:
    tag = _EMOTION_TAG_MAP.get(emotion.lower(), "pop")
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "tag.gettoptracks",
        "tag": tag,
        "limit": limit,
        "api_key": api_key,
        "format": "json",
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()["tracks"]["track"]

    playlist = []
    for t in data:
        playlist.append(
            {
                "name": t["name"],
                "artist": t["artist"]["name"],
                "image_url": next((i["#text"] for i in t["image"] if i["size"] == "large"), None),
                "spotify_url": f"https://open.spotify.com/search/{t['artist']['name']} {t['name']}",
            }
        )
    return playlist
