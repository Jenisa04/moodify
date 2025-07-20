import streamlit as st
from utils.emotion import detect_emotion
from utils.ytmusic import yt_tracks
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# ─────────────── Streamlit Config ───────────────
st.set_page_config(page_title="Moodify 🎵", page_icon="🎵", layout="centered")
st.title("🎵 Moodify - Your Mood, Your Music")
st.caption("Upload or snap a photo, AI detects your mood and curates a YouTube Music playlist ✨")

FALLBACK_IMG = "vinyl.png"

# ─────────────── Helper Functions ───────────────
def is_placeholder(url: str | None) -> bool:
    """Check if the thumbnail is missing or a placeholder."""
    return (not url) or "data:image" in url

def create_result_card(emotion, track_name, artist_name, thumbnail_url) -> BytesIO:
    """Generate an Instagram-worthy result card image."""
    # Define mood-based gradient colors
    gradients = {
        "happy": ((255, 223, 88), (255, 140, 0)),      # yellow to orange
        "sad": ((88, 104, 255), (0, 34, 102)),         # blue to dark blue
        "angry": ((255, 88, 88), (153, 0, 0)),         # red tones
        "chill": ((88, 255, 171), (0, 102, 68)),       # teal/green
        "neutral": ((200, 200, 200), (120, 120, 120)), # grays
    }
    color_start, color_end = gradients.get(emotion.lower(), ((200, 200, 200), (100, 100, 100)))

    # Create base image (Instagram Story size)
    img = Image.new("RGB", (1080, 1920), color=color_start)
    draw = ImageDraw.Draw(img)

    # Apply gradient
    for y in range(img.height):
        r = int(color_start[0] + (color_end[0] - color_start[0]) * y / img.height)
        g = int(color_start[1] + (color_end[1] - color_start[1]) * y / img.height)
        b = int(color_start[2] + (color_end[2] - color_start[2]) * y / img.height)
        draw.line([(0, y), (img.width, y)], fill=(r, g, b))

    # Fonts (fallback if arial not available)
    try:
        font_large = ImageFont.truetype("arial.ttf", 120)
        font_medium = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        font_large = font_medium = font_small = None

    # Add mood text
    draw.text((50, 100), f"{emotion.title()}", fill="white", font=font_large)

    # Add playlist thumbnail (circular)
    try:
        response = requests.get(thumbnail_url, timeout=10)
        playlist_img = Image.open(BytesIO(response.content)).resize((700, 700)).convert("RGBA")
        mask = Image.new("L", playlist_img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, playlist_img.size[0], playlist_img.size[1]), fill=255)
        img.paste(playlist_img, (190, 500), mask=mask)
    except:
        pass  # Skip thumbnail if failed

    # Add track info below thumbnail
    draw.text((100, 1300), f"{track_name}", fill="white", font=font_medium)
    draw.text((100, 1380), f"by {artist_name}", fill="white", font=font_small)

    # Branding
    draw.text((50, 1800), "Made with Moodify", fill="white", font=font_small)

    # Save to BytesIO buffer
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


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

    # Generate Shareable Result Card
    st.markdown("---")
    st.subheader("📸 Share Your Mood")
    first_track = tracks[0]
    result_card = create_result_card(
        st.session_state.override_mood,
        first_track["name"],
        first_track["artist"],
        first_track["thumbnail"]
    )
    st.download_button(
        "📥 Download & Share on Instagram",
        result_card,
        file_name="moodify_result.png",
        mime="image/png",
        help="Download your mood result to share on Instagram or with friends!"
    )
elif not (uploaded_file or captured_image):
    st.info("⬆️ Upload a photo or switch to the camera tab to snap one.")

# ─────────────── Footer ───────────────
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Hugging Face, and YouTube Music API. © 2025 Jenisa Sheth")
