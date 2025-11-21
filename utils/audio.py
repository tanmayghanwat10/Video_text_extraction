import subprocess

def extract_audio(video_path: str, audio_path: str):
    """
    Extract audio using ffmpeg (mono, 16kHz). Silent ffmpeg output.
    """
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ac", "1",        # convert to mono to speed up ASR
        "-ar", "16000",    # 16kHz sample rate
        "-loglevel", "quiet",
        audio_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
