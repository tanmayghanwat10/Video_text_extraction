import os
import json
import logging
import time
from utils.audio import extract_audio
from utils.transcript import generate_transcript
from utils.search import find_phrase_occurrences

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

INPUT_DIR = "input"
OUTPUT_DIR = "output"
VIDEO_EXTENSIONS = (".mp4", ".mkv", ".avi", ".mov", ".webm")


def select_video(input_dir):
    videos = [
        f for f in os.listdir(input_dir)
        if f.lower().endswith(VIDEO_EXTENSIONS)
    ]

    if not videos:
        raise FileNotFoundError("❌ No video files found in input/ folder")

    if len(videos) == 1:
        logging.info(f"🎬 Single video detected: {videos[0]}")
        return videos[0]

    # Multiple videos → ask user
    logging.info("🎬 Multiple videos detected. Please choose one:\n")
    for idx, video in enumerate(videos, start=1):
        print(f"{idx}. {video}")

    while True:
        try:
            choice = int(input("\nEnter video number to process: "))
            if 1 <= choice <= len(videos):
                return videos[choice - 1]
        except ValueError:
            pass

        print("❌ Invalid selection. Try again.")


def main():
    start_time = time.time()
    logging.info("🚀 Starting Video Text Extraction")

    phrases_path = os.path.join(INPUT_DIR, "phrases.txt")
    if not os.path.exists(phrases_path):
        raise FileNotFoundError("❌ input/phrases.txt not found")

    video_name = select_video(INPUT_DIR)
    video_path = os.path.join(INPUT_DIR, video_name)

    audio_path = extract_audio(video_path, OUTPUT_DIR)

    # chunks = generate_transcript(audio_path, model_size="tiny")
    chunks = generate_transcript(audio_path)

    with open(phrases_path, "r", encoding="utf-8") as f:
        phrases = [line.strip() for line in f if line.strip()]

    results = find_phrase_occurrences(chunks, phrases)

    output = {
        "video": video_name,
        "matches": results
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "result.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    elapsed = time.time() - start_time
    logging.info(f"✅ Done! Results saved to {output_path}")
    logging.info(f"⏱️ Total execution time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
