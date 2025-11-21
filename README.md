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

### Build image

```bash
docker build -t video_text_extraction .
```

### Run (Windows PowerShell)

```powershell
docker run --rm -v ${PWD}\input:/app/input -v ${PWD}\output:/app/output video_text_extraction
```

### Linux / macOS

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output video_text_extraction
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

