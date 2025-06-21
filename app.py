import streamlit as st
from utils.emotion import detect_emotion
from utils.lastfm import lf_tracks

st.set_page_config(page_title="Moodify 🎵", page_icon="🎵", layout="centered")

st.title("🎵 Moodify – Photo‑to‑Playlist")
st.caption("Upload or snap a photo, AI finds your mood, and we fetch matching songs via Last.fm ✨")

FALLBACK_IMG = "vinyl.png"

def is_placeholder(url: str | None) -> bool:
    return (not url) or "2a96cbd8b46e442fc41c2b86b821562f" in url

# ── Input tabs: Upload or Camera ─────────────────────────────────────
upload_tab, camera_tab = st.tabs(["📁 Upload Photo", "📸 Take Photo"])

with upload_tab:
    uploaded_file = st.file_uploader(
        "Upload a JPG or PNG image", type=["jpg", "jpeg", "png"], accept_multiple_files=False
    )

with camera_tab:
    captured_image = st.camera_input("Take a photo")

# Determine which image to use (camera overrides if both present)
image_source = captured_image or uploaded_file

# ── Main pipeline ────────────────────────────────────────────────────
if image_source:
    st.image(image_source, width=300, caption="Your image")

    # Emotion detection
    with st.spinner("Detecting emotion…"):
        emotion, score = detect_emotion(image_source.getvalue(), st.secrets["HF_TOKEN"])
    st.success(f"**{emotion.title()}** mood detected  ·  confidence {score:.0%}")

    # Last.fm recommendations
    with st.spinner("Fetching songs from Last.fm…"):
        tracks = lf_tracks(emotion, st.secrets["LASTFM_API_KEY"], limit=10)

    st.subheader("Recommended Tracks")
    for t in tracks:
        cols = st.columns([1, 4])
        with cols[0]:
            image_url = t["image_url"] if not is_placeholder(t["image_url"]) else FALLBACK_IMG
            st.image(image_url, use_container_width=True)
        with cols[1]:
            st.markdown(f"**{t['name']}**  \n{t['artist']}")
            st.markdown(f"[Open in Spotify]({t['spotify_url']})")
elif not (uploaded_file or captured_image):
    st.info("⬆️ Upload a photo or switch to the camera tab to snap one.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Hugging Face, and Last.fm API. © 2025 Jenisa Sheth")
