"""Predict GENUINE or REPLAY for one WAV file."""
from __future__ import annotations
import argparse, joblib
from .audio_features import extract_mfcc

def predict(audio_path: str, model_path: str='models/svm_mfcc.joblib'):
    model=joblib.load(model_path); x=extract_mfcc(audio_path).reshape(1,-1); label=str(model.predict(x)[0]); score=float(max(model.predict_proba(x)[0])); return {'label':label,'confidence':score}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('--model',default='models/svm_mfcc.joblib'); a=ap.parse_args(); print(predict(a.audio,a.model))
