# Audio Anti-Spoofing — Replay Detection

## Project Type

Academic Artificial Intelligence / Machine Learning project.

## Project Overview

The project detects replay spoofing in WAV audio files. Its documented processing pipeline is WAV preprocessing, MFCC feature extraction, StandardScaler normalization, and an RBF-kernel SVM classifier.

## Objective

To distinguish genuine audio from replayed audio using a reproducible local inference workflow and a saved model.

## Technologies

Python, MFCC audio features, scikit-learn SVM, StandardScaler, joblib, Tkinter, WAV audio, and the ASVspoof 2017 Version 2 Development Set protocol.

## Main Features

- Audio preprocessing and deterministic feature extraction.
- Saved-model inference without retraining when the demo opens.
- Evaluation metrics and prediction outputs.
- Windows launcher and a Tkinter demonstration interface.

## Data and Database

The project uses local audio files and the official ASVspoof 2017 Version 2 Development Set protocol. It does not use a database.

## Documented Results

The existing project documentation reports 1,710 labeled files, an 80/20 stratified split, test accuracy of 0.979532, Replay precision of 0.969231, Replay recall of 0.994737, and Replay F1 of 0.981818. These are the project's existing documented results and were not changed.

## How to Run

On Windows, use `run.bat`, or install the documented Python dependencies and run `python app\\demo.py` from the project root. The required model and local audio/protocol files must be present.

## Project Status

Academic project with a documented model, results, and demo interface. It is suitable for portfolio presentation after dependency, data-distribution, and repository-size review. It is not claimed to be production-ready or a complete speaker-verification system.

## What Was Learned

The project demonstrates an end-to-end classical machine-learning workflow for audio classification: preparing labeled data, extracting MFCC statistics, scaling features, training an SVM, evaluating predictions, and integrating a saved model into a small desktop demo.

## Future Improvements

Possible future work documented by the project includes evaluating on additional datasets such as ASVspoof 2019 PA, studying additional acoustic features, and investigating deeper models. These items are not part of the current implementation.

## Academic Context

University academic project focused on replay spoofing detection.
