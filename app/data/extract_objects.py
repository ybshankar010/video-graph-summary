import json
from pathlib import Path
from app.utils.constants import CAPTIONS_DIR, TRIPLES_DIR
from app.models.llm_wrappers import extract_triples_with_llm

# Resolve absolute paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CAPTIONS_PATH = (PROJECT_ROOT / CAPTIONS_DIR).resolve()
TRIPLES_PATH = (PROJECT_ROOT / TRIPLES_DIR).resolve()
TRIPLES_PATH.mkdir(exist_ok=True, parents=True)

def extract_triples_for_video(video_id):
    input_path = CAPTIONS_PATH / f"{video_id}.json"
    output_path = TRIPLES_PATH / f"{video_id}_triples.json"

    if not input_path.exists():
        print(f"❌ Caption file not found for {video_id}")
        return

    # Load captions
    with open(input_path, "r") as f:
        captions = json.load(f)

    # Load existing triples if available
    if output_path.exists():
        with open(output_path, "r") as f:
            existing_data = json.load(f)
        existing_frame_ids = {entry["frame_id"] for entry in existing_data}
    else:
        existing_data = []
        existing_frame_ids = set()

    # Process only new frames
    new_data = []
    for frame_id, caption in captions.items():
        if frame_id in existing_frame_ids:
            continue
        triples = extract_triples_with_llm(caption)
        new_data.append({
            "frame_id": frame_id,
            "caption": caption,
            "triples": triples
        })

    if new_data:
        with open(output_path, "w") as f:
            json.dump(existing_data + new_data, f, indent=2)
        print(f"✅ Appended {len(new_data)} new triples to {output_path}")
    else:
        print(f"⚠️ All triples already exist for {video_id}, skipping...")

if __name__ == "__main__":
    for caption_file in CAPTIONS_PATH.glob("*.json"):
        extract_triples_for_video(caption_file.stem)
