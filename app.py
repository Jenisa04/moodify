import streamlit as st
from utils.emotion import detect_emotion
from utils.ytmusic import yt_tracks
from PIL import Image
import requests

# ─────────────── Streamlit Config ───────────────
st.set_page_config(page_title="Moodify 🎵", page_icon="🎵", layout="centered")
st.title("🎵 Moodify - Your Mood, Your Music")
st.caption("Upload or snap a photo, AI detects your mood and curates a YouTube Music playlist ✨")

FALLBACK_IMG = "vinyl.png"

# ─────────────── Helper Functions ───────────────
def is_placeholder(url: str | None) -> bool:
    """Check if the thumbnail is missing or a placeholder."""
    return (not url) or "data:image" in url

# ─────────────── Input Tabs ───────────────
upload_tab, camera_tab = st.tabs(["📁 Upload Photo", "📸 Take Photo"])

# Session state to manage clearing images and mood override
if "image_source" not in st.session_state:
    st.session_state.image_source = None
if "override_mood" not in st.session_state:
    st.session_state.override_mood = None

# File uploader
with upload_tab:
    uploaded_file = st.file_uploader(
        "Upload a JPG or PNG image", type=["jpg", "jpeg", "png"], accept_multiple_files=False
    )
    if uploaded_file:
        st.session_state.image_source = uploaded_file

# Camera input
with camera_tab:
    captured_image = st.camera_input("Take a photo")
    if captured_image:
        st.session_state.image_source = captured_image

# Clear button
if st.session_state.image_source:
    if st.button("❌ Clear Photo"):
        st.session_state.image_source = None
        st.session_state.override_mood = None

# ─────────────── Main Pipeline ───────────────
if st.session_state.image_source:
    st.image(st.session_state.image_source, width=300, caption="Your image")

    # Emotion detection
    with st.spinner("Detecting emotion…"):
        detected_emotion, score = detect_emotion(
            st.session_state.image_source.getvalue(), st.secrets["HF_TOKEN"]
        )

    # Mood display with override option
    st.success(f"**{detected_emotion.title()}** mood detected  ·  confidence {score:.0%}")
    st.markdown("Not quite right? Pick your own mood:")
    moods = ["happy", "sad", "angry", "fear", "disgust", "surprise", "neutral", "chill", "energetic", "romantic"]
    selected_mood = st.selectbox("🎭 Select a mood:", moods, index=moods.index(detected_emotion.lower()))

    # Store override in session
    st.session_state.override_mood = selected_mood

    # YouTube Music recommendations
    with st.spinner("Fetching songs from YouTube Music…"):
        tracks = yt_tracks(st.session_state.override_mood)

    st.subheader("Recommended Tracks")
    for t in tracks:
        cols = st.columns([1, 4])
        with cols[0]:
            thumbnail = t["thumbnail"] if not is_placeholder(t["thumbnail"]) else FALLBACK_IMG
            st.image(thumbnail, use_container_width=True)
        with cols[1]:
            st.markdown(f"**{t['name']}**  \n{t['artist']}")
            st.markdown(f"[🎵 Listen on YouTube Music]({t['youtube_url']})")
elif not (uploaded_file or captured_image):
    st.info("⬆️ Upload a photo or switch to the camera tab to snap one.")

# ─────────────── Footer ───────────────
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Hugging Face, and YouTube Music API. © 2025 Jenisa Sheth")
