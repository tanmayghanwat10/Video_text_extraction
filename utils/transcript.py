import whisper
import logging

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def generate_transcript(audio_path, model_size="tiny"):
    logging.info(f"🧠 Loading Whisper model: {model_size} (multilingual)")

    model = whisper.load_model(model_size)

    logging.info("Transcribing (auto language detection)...")
    result = model.transcribe(audio_path)

    chunks = []
    for seg in result["segments"]:
        chunks.append({
            "text": seg["text"],
            "timestamp": (seg["start"], seg["end"])
        })

    return chunks
