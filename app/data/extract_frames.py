import cv2
import os
from pathlib import Path

from app.utils.constants import VIDEOS_DIR, FRAMES_DIR

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VIDEO_DIR = (PROJECT_ROOT / VIDEOS_DIR).resolve()
FRAMES_DIR = (PROJECT_ROOT / FRAMES_DIR).resolve()
FRAMES_DIR.mkdir(parents=True, exist_ok=True)

def extract_frames(video_path, output_dir, frame_rate=1):
    cap = cv2.VideoCapture(str(video_path))
    count = 0
    saved = 0

    output_dir.mkdir(parents=True, exist_ok=True)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if count % frame_rate == 0:
            frame_path = output_dir / f"frame_{saved:05d}.jpg"
            cv2.imwrite(str(frame_path), frame)
            saved += 1

        count += 1

    cap.release()
    print(f"Extracted {saved} frames from {video_path.name}")

def extract_all():
    for video_file in VIDEO_DIR.glob("*.mp4"):
        output_path = FRAMES_DIR / video_file.stem
        if not output_path.exists():
            extract_frames(video_file, output_path, frame_rate=30)

if __name__ == "__main__":
    extract_all()