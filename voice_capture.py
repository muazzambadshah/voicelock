# voice_capture.py

import sounddevice as sd
import numpy as np
import wave
from tkinter import filedialog
import tkinter as tk
import os

# Record from microphone
def record_voice(duration=5, fs=16000, filename="recorded_voice.wav"):
    print(f"[INFO] Recording started for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("[INFO] Recording finished.")

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())

    print(f"[SAVED] Audio saved to {filename}")
    return filename

# Load existing audio file using file dialog
def load_audio_file():
    root = tk.Tk()
    root.withdraw()  # Hide GUI window
    file_path = filedialog.askopenfilename(
        filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
    )
    if not file_path:
        print("[WARNING] No file selected.")
        return None
    print(f"[LOADED] Selected file: {file_path}")
    return file_path

# CLI Testing
if __name__ == "__main__":
    choice = input("Choose: [1] Record Voice  [2] Load Existing File: ")
    if choice == "1":
        duration = int(input("Enter recording duration (seconds): "))
        filename = record_voice(duration)
    elif choice == "2":
        filename = load_audio_file()
    else:
        print("[ERROR] Invalid choice.")
