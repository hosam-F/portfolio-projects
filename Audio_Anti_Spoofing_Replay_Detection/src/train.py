"""Train the MFCC + SVM baseline on official labeled WAV paths."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import joblib
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from .audio_features import extract_mfcc

LABELS={'genuine':'GENUINE','bonafide':'GENUINE','bona_fide':'GENUINE','real':'GENUINE','replay':'REPLAY','spoof':'REPLAY','attack':'REPLAY'}

def infer_label(path: Path) -> str | None:
    for part in reversed(path.parts):
        if part.lower() in LABELS: return LABELS[part.lower()]
    return None

def read_protocol(protocol: Path, root: Path):
    """Read whitespace/CSV protocol rows containing a file name and a label."""
    mapping={}
    for line in protocol.read_text(encoding='utf-8', errors='replace').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        fields=next(csv.reader([line], delimiter=',')) if ',' in line else line.split()
        label=None; name=None
        for f in fields:
            key=f.strip().lower()
            if key in LABELS: label=LABELS[key]
            elif key.endswith('.wav') or '/' in key or '\\' in key: name=f.strip()
        if label and name:
            candidate=root/name
            if not candidate.exists(): candidate=next(root.rglob(Path(name).name), None)
            if candidate: mapping[candidate.resolve()]=label
    return mapping

def collect_wavs(root: Path, protocol: Path|None=None, limit_each: int|None=None):
    groups={'GENUINE':[],'REPLAY':[]}; mapping=read_protocol(protocol,root) if protocol else {}
    for p in root.rglob('*.wav'):
        label=mapping.get(p.resolve()) or infer_label(p)
        if label and (limit_each is None or len(groups[label])<limit_each): groups[label].append(p)
    return groups

def train(root: str, model_path: str, limit_each: int=100, protocol: str|None=None):
    groups=collect_wavs(Path(root), Path(protocol) if protocol else None, limit_each)
    if not all(groups.values()): raise RuntimeError('Official labels are required: provide --protocol or labeled GENUINE/REPLAY folders.')
    paths=groups['GENUINE']+groups['REPLAY']; y=np.array(['GENUINE']*len(groups['GENUINE'])+['REPLAY']*len(groups['REPLAY']))
    X=np.vstack([extract_mfcc(str(p)) for p in paths])
    model=make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True, class_weight='balanced', random_state=42)); model.fit(X,y)
    Path(model_path).parent.mkdir(parents=True,exist_ok=True); joblib.dump(model,model_path)
    return {'samples':len(y),'genuine':int(sum(y=='GENUINE')),'replay':int(sum(y=='REPLAY')),'features':int(X.shape[1])}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--data',required=True); ap.add_argument('--model',default='models/svm_mfcc.joblib'); ap.add_argument('--limit-each',type=int,default=100); ap.add_argument('--protocol'); a=ap.parse_args(); print(json.dumps(train(a.data,a.model,a.limit_each,a.protocol),indent=2))
