# Project Notes — Audio Anti-Spoofing — Replay Detection

## Project Type

Academic AI / Machine Learning project for replay spoofing detection from WAV files.

## Problem and Approach

The project distinguishes genuine audio from replayed audio. The documented pipeline is WAV preprocessing, MFCC extraction, StandardScaler, and an RBF-kernel SVM.

## Main Files and Folders

- `src/`: audio preprocessing, features, training, evaluation, and prediction code.
- `app/`: Tkinter demonstration interface.
- `data/`: local WAV files and the official protocol used by the project.
- `models/`: saved SVM model.
- `results/`: metrics, predictions, and plots.
- `README.md`: documented setup, measured results, and limitations.
- `requirements.txt`: Python dependencies.
- `run.bat`: Windows launcher.

## Verified Facts from Existing Documentation

The project documents 1,710 labeled files from the ASVspoof 2017 Version 2 Development Set, with a fixed stratified 80/20 split. The documented test accuracy is 0.979532 and the documented Replay F1 score is 0.981818. These values must not be changed or presented as results on an unseen external dataset.

## Running

On Windows, the documented entry point is `run.bat`. The interface loads the saved model and performs prediction; it does not retrain when opened. A local Python environment compatible with the documented requirements is needed.

## Interview Explanation

Explain the project as an academic replay-spoofing detector: describe the threat model, the MFCC feature representation, the role of scaling and the SVM classifier, the fixed evaluation split, and the limitations of evaluating on the Development Set. Do not describe it as a complete speaker-verification system or as production-ready.

## Remaining Work

Review dependency reproducibility, sensitive data exposure, repository size, and whether the local audio dataset may be redistributed. Add a PDF report only after those checks are complete.
