import os
import re
from utils.constants import VIDEOS_DIR
from yt_dlp import YoutubeDL

video_urls = [
    "https://www.youtube.com/watch?v=aqz-KE-bpKQ",
    "https://www.youtube.com/watch?v=2Xc9gXyf2G4",
    "https://www.youtube.com/watch?v=1La4QzGeaaQ",
    "https://www.youtube.com/watch?v=ScMzIvxBSi4",
    "https://www.youtube.com/watch?v=F1B9Fk_SgI0"
]

def extract_video_id(url):
    match = re.search(r"v=([\w-]+)", url)
    return match.group(1) if match else None

def already_downloaded(video_id, save_dir):
    for file in os.listdir(save_dir):
        if video_id in file:
            return True
    return False


def download_videos(urls, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    for url in urls:
        video_id = extract_video_id(url)
        if already_downloaded(video_id, save_dir):
            print(f"[✓] Skipping {video_id} — already downloaded.")
            continue

        ydl_opts = {
            'outtmpl': os.path.join(save_dir, f'%(title)s-{video_id}.%(ext)s'),
            'format': 'mp4/bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }
        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                print(f"[!] Failed to download {url}: {e}")


if __name__ == "__main__":
    download_videos(video_urls, VIDEOS_DIR)