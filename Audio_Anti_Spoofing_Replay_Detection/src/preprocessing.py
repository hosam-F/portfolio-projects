"""Simple, deterministic audio preprocessing for the academic prototype."""
from __future__ import annotations
import numpy as np
import librosa

TARGET_SR = 16000


def load_audio(path: str, sr: int = TARGET_SR) -> tuple[np.ndarray, int]:
    """Load a WAV file as mono and resample it to a fixed sample rate."""
    y, _ = librosa.load(path, sr=sr, mono=True)
    if y.size == 0:
        raise ValueError(f"Empty audio file: {path}")
    y = librosa.util.normalize(y).astype(np.float32)
    return y, sr
