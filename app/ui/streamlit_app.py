import os
import streamlit as st
from pathlib import Path
from app.utils.constants import VIDEOS_DIR
from app.generators.chat_retriever import answer_query

st.set_page_config(page_title="Video Graph Summarizer", layout="wide")
st.title("📽️ Video Graph Summarizer")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_VIDEO_DIR = (PROJECT_ROOT / VIDEOS_DIR).resolve()

# List available videos
video_files = sorted([f for f in RAW_VIDEO_DIR.glob("*.mp4")])

if not video_files:
    st.warning("No videos found. Please run the downloader script first.")
else:
    selected_video = st.selectbox("Select a video to analyze:", video_files)

    if st.button("🎬 Show Video Preview"):
        st.video(str(selected_video), format="video/mp4", start_time=0)

    st.markdown("### 💬 Ask something about the video")
    user_query = st.text_input("Your question:", placeholder="e.g., What is happening in this video?")

    if user_query:
        st.info(f"🔍 Processing: '{user_query}'")
        video_id = selected_video.stem

        with st.spinner("Running agent..."):
            tool_trace, final_answer = answer_query(video_id, user_query)

        st.success(final_answer)

        with st.sidebar:
            st.markdown("### 🛠️ Tool Calls")
            st.code(tool_trace, language="text")