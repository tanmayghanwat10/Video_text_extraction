import os
import json
import time

from utils.audio import extract_audio
from utils.transcript import transcribe_audio
from utils.search import find_phrase_occurrences

def load_phrases(path):
    # handle UTF-8 with BOM and common Windows encodings
    with open(path, "r", encoding="utf-8-sig") as f:
        return [line.strip() for line in f if line.strip()]

def find_video_file(input_dir="input"):
    for name in os.listdir(input_dir):
        if name.lower().endswith(".mp4"):
            return os.path.join(input_dir, name)
    return None

def main():
    print("\n🚀 Video Text Occurrence Extraction — start\n")

    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    video_path = find_video_file(input_dir)
    phrases_path = os.path.join(input_dir, "phrases.txt")
    audio_temp = "temp_audio.wav"
    output_path = os.path.join(output_dir, "result.json")

    if video_path is None:
        raise FileNotFoundError("No .mp4 found in input/ — add input/video.mp4 or drop a .mp4 into input/")
    if not os.path.exists(phrases_path):
        raise FileNotFoundError("phrases.txt missing in input/ — create one phrase per line (UTF-8)")

    total_start = time.time()

    # 1) Extract audio
    print("🎵 Extracting audio from:", video_path)
    t0 = time.time()
    extract_audio(video_path, audio_temp)
    t_audio = round(time.time() - t0, 2)
    print(f"✔️ Audio extraction completed ({t_audio} s)\n")

    # 2) Transcribe (auto GPU selection inside)
    print("🔊 Transcribing audio (auto model selection)...")
    t1 = time.time()
    segments = transcribe_audio(audio_temp)  # returns list of {"text","timestamp":(s,e)}
    t_trans = round(time.time() - t1, 2)
    print(f"✔️ Transcription completed ({t_trans} s)\n")

    # 3) Load phrases
    phrases = load_phrases(phrases_path)
    print(f"🔎 Loaded {len(phrases)} phrase(s) from {phrases_path}")

    # 4) Find occurrences
    print("🔍 Searching for phrase occurrences...")
    t2 = time.time()
    occurrences = find_phrase_occurrences(segments, phrases)
    t_search = round(time.time() - t2, 2)
    print(f"✔️ Phrase search completed ({t_search} s)\n")

    # 5) Save results
    result = {
        "video": os.path.basename(video_path),
        "phrases": occurrences,
        "execution_time_seconds": {
            "audio_extraction": t_audio,
            "transcription": t_trans,
            "phrase_search": t_search,
            "total": round(time.time() - total_start, 2)
        }
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    # cleanup
    try:
        if os.path.exists(audio_temp):
            os.remove(audio_temp)
    except Exception:
        pass

    print("🎉 Done! Output saved to:", output_path)
    print("⏱ Total runtime (s):", result["execution_time_seconds"]["total"])

if __name__ == "__main__":
    main()
