# 🎥 Video Text Occurrence Extraction
*(Offline • Multilingual • Whisper Auto CPU/GPU • Regex Phrase Matching)*

This project extracts **phrase occurrences with timestamps** from video files using the **open-source OpenAI Whisper** speech-to-text model.

The pipeline works as follows:
1. 🎧 Extracts audio from video using FFmpeg  
2. 🧠 Generates a speech transcript using Whisper  
3. 🔍 Searches for user-defined phrases using regex-based matching  
4. 📄 Saves results in structured JSON format  

✅ Fully offline  
✅ Free (no OpenAI API key required)  
✅ Supports Hindi, English, Hinglish, and other languages  

---

## 🚀 Automatic Model Selection

The transcription model is selected automatically at runtime:

- **GPU available** → Uses **Whisper MEDIUM** for higher accuracy  
- **CPU only** → Uses **Whisper TINY** for fast and lightweight processing  

This ensures:
- Fast execution on GPU systems  
- Safe and portable execution on CPU-only machines  
- Stable behavior inside Docker containers  

---

## ⭐ Key Features

- Offline and free speech transcription  
- Multilingual support (Hindi, English, Hinglish, etc.)  
- Regex-based **root word matching**  
  - Example: `fuck` matches `fuck`, `fucking`, `fucked`  
- Avoids false positives (e.g. does not match `firetruck`)  
- Handles multiple videos by prompting user selection  
- Execution time logging  
- Docker-ready with CPU-safe defaults  

---

## 📝 phrases.txt (Example)

```txt
fuck
go
ladki
alert
```
### 📦 Project Structure

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
### ENV setup 

```bash
python -m venv .venv
.venv\Scripts\activate
source .venv/bin/activate #for linux and macos
pip install -r requirements.txt

```
### Run Locally 

```bash

python main.py

```
### Docker Usage...

```bash
# Build image
docker build -t video_text_extraction .
```
### For Wins 

```bash
# Run container
docker run -it --rm \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  video_text_extraction

```

### For Linux MAcos
```bash
docker run -it --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  video_text_extraction

```
---

## 📤 Output Example (`result.json`)

```json
{
    "video": "video.mp4",
    "matches": {
        "go": [
            {
                "start": 30.32,
                "end": 36.64
            },
            {
                "start": 48.48,
                "end": 56.48
            },
            {
                "start": 56.48,
                "end": 63.12
            },
            {
                "start": 63.12,
                "end": 71.52
            },
            {
                "start": 72.8,
                "end": 78.24
            },
            {
                "start": 244.88,
                "end": 252.32
            },
            {
                "start": 282.08,
                "end": 288.0
            },
            {
                "start": 319.76,
                "end": 325.28
            },
            {
                "start": 326.0,
                "end": 331.44
            },
            {
                "start": 337.52,
                "end": 343.76
            },
            {
                "start": 349.04,
                "end": 354.96
            },
            {
                "start": 354.96,
                "end": 362.48
            },
            {
                "start": 391.36,
                "end": 397.6
            },
            {
                "start": 545.68,
                "end": 552.48
            }
        ],
        "come": [
            {
                "start": 0.0,
                "end": 11.6
            },
            {
                "start": 84.4,
                "end": 91.36
            },
            {
                "start": 534.88,
                "end": 541.44
            },
            {
                "start": 541.44,
                "end": 545.68
            }
        ],
        "alert": [],
        "ladki": [],
        "अब": []
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

