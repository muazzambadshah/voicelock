# voice_auth.py

import librosa
import numpy as np
from sklearn.svm import SVC
import os
import pickle

# --- Extract MFCC Features ---
def extract_mfcc(file_path, n_mfcc=13):
    y, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return np.mean(mfcc.T, axis=0)

# --- Train SVM Voiceprint Model ---
def train_voice_model(data_dir):
    X = []
    y = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".wav"):
            # Auto extract label by removing numbers and extension
            name_part = ''.join([c for c in filename if not c.isdigit()]).split('.')[0].lower()
            label = name_part
            path = os.path.join(data_dir, filename)
            features = extract_mfcc(path)
            X.append(features)
            y.append(label)
            print(f"[+] Extracted MFCC for {filename} -> label: {label}")

    if len(set(y)) < 2:
        print("[!] ERROR: You need at least 2 different speaker recordings to train the model.")
        return

    model = SVC(kernel='linear', probability=True)
    model.fit(X, y)

    with open("voice_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("[✓] Voice model trained and saved to voice_model.pkl")

# --- Authenticate New Voice Sample ---
def authenticate_voice(test_file):
    if not os.path.exists("voice_model.pkl"):
        print("[!] ERROR: Model not found. Please train the model first (Option 1).")
        return

    with open("voice_model.pkl", "rb") as f:
        model = pickle.load(f)

    if not os.path.isfile(test_file):
        print(f"[!] ERROR: File not found: {test_file}")
        return

    features = extract_mfcc(test_file)
    prediction = model.predict([features])[0]
    confidence = model.predict_proba([features]).max()

    print(f"[RESULT] Voice identified as: {prediction} (confidence: {confidence:.2f})")
    return prediction, confidence

# --- CLI Interface ---
if __name__ == "__main__":
    print("1. Train Voice Model\n2. Authenticate Voice\n")
    choice = input("Select an option: ").strip()

    if choice == "1":
        train_voice_model("voices")
    elif choice == "2":
        test_file = input("Enter path to test WAV file (e.g., recorded_voice.wav): ").strip()
        authenticate_voice(test_file)
    else:
        print("[!] Invalid choice.")
