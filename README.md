# 🎥 Video Text Occurrence Extraction  
### (Whisper Medium • Auto GPU Detection • Faster-Whisper CPU Fallback)

This project extracts **phrases with timestamps** from a video by:
1. Extracting audio (FFmpeg)
2. Transcribing speech (Whisper ASR)
3. Searching for phrase occurrences
4. Saving results in JSON format

The system is **fully automatic**, selecting the best transcription engine based on your hardware.

---

## 🚀 Automatic Model Selection

### 🔥 If GPU is available:
- Uses **openai/whisper-medium** (FP16)  
- If VRAM < 3GB → switches to **openai/whisper-small**

### 🧊 If NO GPU:
- Uses **Faster-Whisper Small (INT8)**  
  → Fastest CPU model  
  → Very lightweight  

No manual selection required.

---

## 📦 Project Structure

```
video_text_extraction/
│── main.py
│── requirements.txt
│── Dockerfile
│── .dockerignore
│── utils/
│   ├── audio.py
│   ├── transcript.py
│   ├── search.py
│   └── model_selection.py
│── input/
│   ├── video.mp4
│   ├── phrases.txt
│── output/
│   └── result.json
│── README.md
```

---

## 🧪 Local Setup (Python)

### 1. Create virtual environment

**Windows**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. Run the project

Place your video & phrases file into:

```
input/
 ├── video.mp4
 └── phrases.txt
```

Then run:

```bash
python main.py
```

Output will be saved in:

```
output/result.json
```

---

## 🐳 Docker Usage

### Initial Build

```bash
docker build -t video_text_extraction .
```

### Rebuild image after code changes (fast - uses cached dependencies)

```bash
docker build -t video_text_extraction .
```

### Run (Windows PowerShell)

```powershell
# Stop existing container (keeps it for reuse)
docker stop video_text_extraction_container 2>$null

# Start with updated image and fresh file mounts
docker start video_text_extraction_container 2>$null || docker run --name video_text_extraction_container -v ${PWD}\input:/input -v ${PWD}\output:/output video_text_extraction
```

### Linux / macOS

```bash
# Stop existing container (keeps it for reuse)
docker stop video_text_extraction_container 2>/dev/null

# Restart or create new container with fresh mounts
docker start video_text_extraction_container 2>/dev/null || docker run --name video_text_extraction_container -v $(pwd)/input:/input -v $(pwd)/output:/output video_text_extraction
```

**Note:** Docker containers are immutable. To update code changes:
1. Rebuild the image (step 2 above) - dependencies are cached, only code layer rebuilds
2. Remove old container: `docker rm video_text_extraction_container`
3. Run the container again with the new image

For quick updates, use this one-liner:

**Linux/macOS:**
```bash
docker build -t video_text_extraction . && docker rm -f video_text_extraction_container 2>/dev/null; docker run --name video_text_extraction_container -v $(pwd)/input:/input -v $(pwd)/output:/output video_text_extraction
```

**Windows PowerShell:**
```powershell
docker build -t video_text_extraction . ; docker rm -f video_text_extraction_container 2>$null ; docker run --name video_text_extraction_container -v ${PWD}\input:/input -v ${PWD}\output:/output video_text_extraction
```

---

## 📤 Output Example (`result.json`)

```json
{
    "video": "Sample.mp4",
    "phrases": {
        "hello world": [],
        "go": [
            {"start": 12.5, "end": 15.1}
        ]
    },
    "execution_time_seconds": {
        "audio_extraction": 2.59,
        "transcription": 216.65,
        "phrase_search": 0.0,
        "total": 219.24
    }
}
```

---

## ⭐ Features

- Whisper Medium (GPU) / Small fallback  
- Faster-Whisper CPU mode  
- FFmpeg audio extraction  
- Auto GPU detection  
- Docker-ready  
- Clean architecture  
- Optimized execution  

---

