import os
import json
from pathlib import Path
from PIL import Image
from tqdm import tqdm

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from app.utils.constants import FRAMES_DIR, CAPTIONS_DIR

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRAME_DIR = (PROJECT_ROOT / FRAMES_DIR).resolve()
CAPTION_DIR = (PROJECT_ROOT / CAPTIONS_DIR).resolve()
CAPTION_DIR.mkdir(parents=True, exist_ok=True)

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
model.eval()

BATCH_SIZE = 4

def caption_batch(images):
    inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=20)
    captions = processor.batch_decode(output, skip_special_tokens=True)
    return captions

def caption_video_frames(video_folder):
    caption_output_path = CAPTION_DIR / f"{video_folder.name}.json"
    if caption_output_path.exists():
        print(f"Captions for {video_folder.name} already exist. Skipping.")
        return

    print(f"Generating captions for: {video_folder.name}")
    captions = {}
    image_paths = sorted(video_folder.glob("*.jpg"))

    for i in tqdm(range(0, len(image_paths), BATCH_SIZE)):
        batch_paths = image_paths[i:i + BATCH_SIZE]
        batch_images = []
        for p in batch_paths:
            try:
                img = Image.open(p).convert("RGB")
                batch_images.append(img)
            except Exception as e:
                print(f"Failed to load image {p.name}: {e}")
                batch_images.append(Image.new("RGB", (224, 224)))  # Dummy blank if needed

        try:
            batch_captions = caption_batch(batch_images)
            for p, cap in zip(batch_paths, batch_captions):
                captions[p.name] = cap
        except Exception as e:
            print(f"Captioning failed for batch starting at {batch_paths[0].name}: {e}")

    with open(caption_output_path, "w") as f:
        json.dump(captions, f, indent=2)

def caption_all_frames():
    for video_folder in FRAME_DIR.iterdir():
        if not video_folder.is_dir():
            continue
        caption_video_frames(video_folder)

if __name__ == "__main__":
    caption_all_frames()