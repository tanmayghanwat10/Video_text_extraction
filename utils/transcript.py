import whisper
import torch
import logging
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


def generate_transcript(audio_path):
    # Decide model based on hardware
    if torch.cuda.is_available():
        model_size = "medium"
        device = "cuda"
        logging.info("🚀 GPU detected → using Whisper MEDIUM")
    else:
        model_size = "tiny"
        device = "cpu"
        logging.info("⚡ CPU detected → using Whisper TINY")

    logging.info(f"🧠 Loading Whisper model: {model_size} (multilingual)")
    model = whisper.load_model(model_size).to(device)

    logging.info("🎧 Transcribing (auto language detection)...")
    result = model.transcribe(audio_path)

    chunks = []
    for seg in result["segments"]:
        chunks.append({
            "text": seg["text"],
            "timestamp": (seg["start"], seg["end"])
        })

    return chunks
