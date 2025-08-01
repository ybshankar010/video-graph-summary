# app/streamlit_app.py
import os
import streamlit as st
from pathlib import Path
from app.utils.constants import SAVE_DIR

st.set_page_config(page_title="Video Graph Summarizer", layout="wide")
st.title("📽️ Video Graph Summarizer")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_VIDEO_DIR = (PROJECT_ROOT / SAVE_DIR).resolve()

# List available videos
video_files = sorted([f for f in RAW_VIDEO_DIR.glob("*.mp4")])

if not video_files:
    st.warning("No videos found. Please run the downloader script first.")
else:
    selected_video = st.selectbox("Select a video to analyze:", video_files)

    # Preview video
    st.video(str(selected_video))

    # Optional chat interface
    st.markdown("### 💬 Ask something about the video")
    user_query = st.text_input("Your question:", placeholder="e.g., What is happening in this video?")

    if user_query:
        # Placeholder for LLM-generated response (mock for now)
        st.info(f"🔍 Processing: '{user_query}'")
        st.success("This is a placeholder response. Graph-based QA will be integrated here.")
