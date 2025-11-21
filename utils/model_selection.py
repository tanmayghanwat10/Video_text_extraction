import torch
import subprocess
import re

def _get_gpu_vram_mb():
    """
    Returns total GPU VRAM in MB if nvidia-smi available and a CUDA GPU exists.
    Returns None if not available.
    """
    try:
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"], text=True)
        # take first GPU
        mb = int(out.strip().splitlines()[0])
        return mb
    except Exception:
        return None

def select_model():
    """
    Fully automatic selection logic:
    - If GPU available: try use HuggingFace whisper-medium on GPU (float16).
      If GPU VRAM is very low (<3000 MB), fallback to whisper-small.
    - If no GPU: use Faster-Whisper small (int8) on CPU.
    Returns a dict with keys: 'engine' ('hf' or 'faster'), 'model_name', 'device', 'compute_type'
    """
    gpu_available = torch.cuda.is_available()
    gpu_vram_mb = _get_gpu_vram_mb()

    if gpu_available:
        # choose medium if VRAM seems sufficient; medium typically needs ~2.5-3.0GB
        if gpu_vram_mb is None or gpu_vram_mb >= 3000:
            return {"engine": "hf", "model_name": "openai/whisper-medium", "device": "cuda", "compute_type": "float16"}
        else:
            # VRAM is low — use smaller model on GPU
            return {"engine": "hf", "model_name": "openai/whisper-small", "device": "cuda", "compute_type": "float16"}
    else:
        # No GPU: use faster-whisper small optimized for CPU
        return {"engine": "faster", "model_name": "small", "device": "cpu", "compute_type": "int8"}
