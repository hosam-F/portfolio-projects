from __future__ import annotations
import csv, json
from pathlib import Path
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from src.audio_features import extract_mfcc

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'raw' / 'ASVspoof2017_V2_dev'
PROTOCOL = ROOT / 'data' / 'metadata' / 'protocol_official' / 'extracted' / 'protocol_V2' / 'ASVspoof2017_V2_dev.trl.txt'
MODEL = ROOT / 'models' / 'svm_mfcc.joblib'
METRICS = ROOT / 'results' / 'metrics' / 'metrics.json'
PRED = ROOT / 'results' / 'predictions' / 'predictions.csv'

rows=[]
wav_by_name = {p.name: p for p in DATA.rglob('*.wav')}
for line in PROTOCOL.read_text(encoding='utf-8').splitlines():
    f=line.split()
    if len(f)>=2 and f[1].lower() in {'genuine','spoof','replay'}:
        p=wav_by_name.get(Path(f[0]).name)
        if p is not None: rows.append((p, 'GENUINE' if f[1].lower()=='genuine' else 'REPLAY'))
if not rows: raise RuntimeError('No protocol-labeled WAV files matched')
paths=np.array([str(p) for p,_ in rows]); y=np.array([label for _,label in rows])
train_idx,test_idx=train_test_split(np.arange(len(y)), test_size=0.20, random_state=42, stratify=y)
X=np.vstack([extract_mfcc(p) for p in paths])
model=make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True, class_weight='balanced', random_state=42))
model.fit(X[train_idx], y[train_idx])
pred=model.predict(X[test_idx])
proba=model.predict_proba(X[test_idx]); classes=list(model.classes_)
metrics={'dataset':'ASVspoof 2017 Version 2 Development Set','protocol':str(PROTOCOL.relative_to(ROOT)),'random_state':42,'test_size':0.20,'total_samples':int(len(y)),'train_samples':int(len(train_idx)),'test_samples':int(len(test_idx)),'train_distribution':{k:int((y[train_idx]==k).sum()) for k in ['GENUINE','REPLAY']},'test_distribution':{k:int((y[test_idx]==k).sum()) for k in ['GENUINE','REPLAY']},'feature_dimensions':int(X.shape[1]),'accuracy':float(accuracy_score(y[test_idx],pred)),'precision_replay':float(precision_score(y[test_idx],pred,pos_label='REPLAY',zero_division=0)),'recall_replay':float(recall_score(y[test_idx],pred,pos_label='REPLAY',zero_division=0)),'f1_replay':float(f1_score(y[test_idx],pred,pos_label='REPLAY',zero_division=0)),'labels':['GENUINE','REPLAY'],'confusion_matrix':confusion_matrix(y[test_idx],pred,labels=['GENUINE','REPLAY']).tolist()}
METRICS.parent.mkdir(parents=True,exist_ok=True); METRICS.write_text(json.dumps(metrics,indent=2),encoding='utf-8')
PRED.parent.mkdir(parents=True,exist_ok=True)
with PRED.open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['file','true_label','predicted_label','score']);
    for i,pr in zip(test_idx,pred):
        score=float(proba[list(test_idx).index(i), classes.index(pr)])
        w.writerow([Path(paths[i]).name,y[i],pr,score])
MODEL.parent.mkdir(parents=True,exist_ok=True); joblib.dump(model,MODEL)
print(json.dumps(metrics,indent=2))
