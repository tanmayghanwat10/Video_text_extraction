import warnings
warnings.filterwarnings("ignore")

from utils.model_selection import select_model

# We'll import modules lazily to avoid heavy imports when not needed.
def transcribe_audio(audio_path: str):
    cfg = select_model()
    engine = cfg["engine"]

    print(f"\n⚙ Model selection result: engine={engine}, model={cfg['model_name']}, device={cfg['device']}")

    if engine == "hf":
        # HuggingFace pipeline approach (uses transformers + torch). GPU path.
        try:
            from transformers import pipeline
            import torch
        except Exception as e:
            raise RuntimeError("Missing transformers/torch for HuggingFace path. Install requirements.") from e

        device = 0 if cfg["device"] == "cuda" else -1

        # Use return_timestamps=True for chunk timestamps (supported in recent transformers)
        # Force language to English for speed; remove if you need auto language detection.
        pipe = pipeline(
            "automatic-speech-recognition",
            model=cfg["model_name"],
            device=device,
            return_timestamps=True,
            chunk_length_s=30,               # larger chunks on GPU are fine
            generate_kwargs={"language": "en"}
        )

        print("🔁 Running HuggingFace Whisper pipeline...")
        out = pipe(audio_path)
        # out may contain "chunks" or "segments" depending on HF version -> normalize
        chunks = out.get("chunks") or out.get("segments") or []
        results = []
        for ch in chunks:
            # chunk structure may differ; support common shapes:
            text = ch.get("text") if isinstance(ch, dict) else str(ch)
            ts = ch.get("timestamp") or ch.get("timeframe") or ch.get("start_end") or None
            if ts:
                start, end = ts[0], ts[1]
            else:
                # fallback: if pipeline returns 'chunk' list of dicts with 'start'/'end'
                start = ch.get("start", 0)
                end = ch.get("end", 0)
            results.append({"text": text, "timestamp": (float(start), float(end))})
        return results

    else:
        # Faster-Whisper CPU path (fast on CPU)
        try:
            from faster_whisper import WhisperModel
        except Exception as e:
            raise RuntimeError("Missing faster-whisper/ctranslate2 for CPU fallback. Install requirements.") from e

        print("🔁 Running Faster-Whisper (CPU optimized) ...")
        model = WhisperModel(cfg["model_name"], device=cfg["device"], compute_type=cfg["compute_type"])

        segments, info = model.transcribe(
            audio_path,
            beam_size=1,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500}
        )

        results = []
        for s in segments:
            results.append({"text": s.text, "timestamp": (s.start, s.end)})
        return results
