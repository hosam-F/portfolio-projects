"""Evaluation helpers for the SVM baseline."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def evaluate(y_true, y_pred, output='results/metrics/metrics.json'):
    labels=['GENUINE','REPLAY']; cm=confusion_matrix(y_true,y_pred,labels=labels)
    result={'accuracy':float(accuracy_score(y_true,y_pred)), 'precision':float(precision_score(y_true,y_pred,pos_label='REPLAY',zero_division=0)), 'recall':float(recall_score(y_true,y_pred,pos_label='REPLAY',zero_division=0)), 'f1_score':float(f1_score(y_true,y_pred,pos_label='REPLAY',zero_division=0)), 'labels':labels, 'confusion_matrix':cm.tolist()}
    Path(output).parent.mkdir(parents=True,exist_ok=True); Path(output).write_text(json.dumps(result,indent=2),encoding='utf-8'); return result
