# Video Text Occurrence Extraction (Whisper Medium primary, automatic selection)

**Auto behavior**
- If a CUDA GPU is available → uses **HuggingFace Whisper (openai/whisper-medium)** on GPU (float16).
  - If GPU VRAM is detected < 3000MB → uses **openai/whisper-small** instead to prevent OOM.
- If no GPU → uses **Faster-Whisper small** (int8) on CPU (fast fallback).

## Files / structure
(see repo root for structure)

## Quick start (local)
1. Create & activate venv:

python -m venv .venv

Windows

.venv\Scripts\activate

Linux/macOS

source .venv/bin/activate

pip install - requirements.txt - for installing all dependencies and modules

 Docker (CPU) Build:

docker build -t text-extract-app .

Run:

docker run --rm -v ${PWD}\input:/app/input -v ${PWD}\output:/app/output video_text_extraction



