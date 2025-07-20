from ytmusicapi import YTMusic
from typing import List, Dict
import random

ytmusic = YTMusic()

# Map emotions to search queries
_EMOTION_QUERY_MAP = {
    "happy": ["happy music", "upbeat songs", "feel good playlist"],
    "sad": ["sad songs", "acoustic chill", "lofi for sad vibes"],
    "angry": ["angry music", "metal workout", "trap hype"],
    "fear": ["dark ambient", "cinematic tension music"],
    "disgust": ["grunge", "punk rock"],
    "surprise": ["funk party", "synthwave"],
    "neutral": ["chill vibes", "coffee shop playlist", "indie folk"],
}

def yt_tracks(emotion: str, limit: int = 10) -> List[Dict]:
    """Fetch top tracks from YouTube Music for the given emotion."""
    queries = _EMOTION_QUERY_MAP.get(emotion.lower(), ["chill music"])
    query = random.choice(queries)
    print(f"Searching YouTube Music for: {query}")

    search_results = ytmusic.search(query=query, filter="songs", limit=limit)

    playlist = []
    for song in search_results:
        playlist.append(
            {
                "name": song.get("title"),
                "artist": song["artists"][0]["name"] if song.get("artists") else "Unknown Artist",
                "thumbnail": song["thumbnails"][-1]["url"] if song.get("thumbnails") else None,
                "youtube_url": f"https://music.youtube.com/watch?v={song['videoId']}",
            }
        )
    return playlist
