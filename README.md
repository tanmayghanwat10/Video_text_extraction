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

---

## 🐳 Docker Usage (Fully Containerized)

The project is now fully dockerized using Docker Compose for easy management. No local Python setup required!

### Prerequisites
- Docker installed on your system
- Docker Compose (usually included with Docker Desktop)

### Initial Setup and Run

1. **Build and run the container:**
   ```bash
   docker-compose up --build
   ```

2. **Place your files:**
   - Add your `video.mp4` and `phrases.txt` to the `input/` directory
   - The container will automatically process them and output to `output/result.json`

### Subsequent Runs

- **Run without rebuilding (if no code changes):**
  ```bash
  docker-compose up
  ```

- **Rebuild after code changes:**
  ```bash
  docker-compose up --build
  ```

- **Run in background:**
  ```bash
  docker-compose up -d
  ```

- **Stop the container:**
  ```bash
  docker-compose down
  ```

### Legacy Docker Commands (if needed)

If you prefer manual Docker commands instead of Compose:

```bash
# Build image
docker build -t video_text_extraction .

# Run container
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output video_text_extraction
```

**Note:** Docker Compose simplifies volume mounting and container management, making it the recommended approach for full containerization.

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

