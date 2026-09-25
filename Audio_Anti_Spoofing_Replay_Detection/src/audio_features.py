"""MFCC feature extraction."""
from __future__ import annotations
import numpy as np
import librosa
from .preprocessing import load_audio, TARGET_SR


def extract_mfcc(path: str, sr: int = TARGET_SR, n_mfcc: int = 20) -> np.ndarray:
    y, sr = load_audio(path, sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=512, hop_length=256)
    delta = librosa.feature.delta(mfcc)
    return np.concatenate([mfcc.mean(axis=1), mfcc.std(axis=1), delta.mean(axis=1), delta.std(axis=1)]).astype(np.float32)
