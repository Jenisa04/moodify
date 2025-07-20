# 🎵 Moodify – Your Mood, Your Music

**Moodify** is an AI-powered web app that detects your mood from a photo and curates a custom YouTube Music playlist to match your vibe.  
It’s fast, fun, and perfect for sharing on Instagram with friends! 📸✨  

---

## 🌟 Features

- 🎭 **AI Mood Detection** – Snap a photo or upload one and let the AI detect your mood.  
- 🎵 **Custom Playlists** – Instantly fetches a mood-matched playlist from YouTube Music.  
- ✨ **Custom Mood Selector** – Not feeling the detected mood? Pick your own vibe.  
- 📸 **Instagram-Ready Cards** – Download beautiful shareable cards to post on social media.  

---

## 🚀 Try It Out
👉 [**Live Demo on Streamlit Cloud**](https://moodify-now.streamlit.app/)

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – Frontend & UI
- [Hugging Face](https://huggingface.co/) – AI model for mood detection
- [YouTube Music API (ytmusicapi)](https://github.com/sigma67/ytmusicapi) – Music recommendations
- Python (Pillow, Requests)

---

## 🏗️ Setup Locally
Clone the repo and run the app:  
```bash
git clone https://github.com/Jenisa04/moodify.git
cd moodify
pip install -r requirements.txt
streamlit run app.py
