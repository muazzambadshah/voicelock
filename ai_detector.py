import librosa
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model  # <-- You missed this import

def extract_spectrogram_features(filename):
    y, sr = librosa.load(filename, sr=16000)
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    spectrogram = np.log(spectrogram + 1e-9)
    
    # Ensure consistent input shape: resize or pad/truncate to (128, 128)
    if spectrogram.shape[1] < 128:
        pad_width = 128 - spectrogram.shape[1]
        spectrogram = np.pad(spectrogram, ((0, 0), (0, pad_width)), mode='constant')
    else:
        spectrogram = spectrogram[:, :128]

    return spectrogram

def detect_ai_voice(model, audio_file):
    spectrogram_features = extract_spectrogram_features(audio_file)
    spectrogram_features = np.expand_dims(spectrogram_features, axis=-1)  # shape: (128, 128, 1)

    # Convert (128, 128, 1) → (128, 128, 3)
    spectrogram_features = np.repeat(spectrogram_features, 3, axis=-1)

    spectrogram_features = np.expand_dims(spectrogram_features, axis=0)  # shape: (1, 128, 128, 3)
    prediction = model.predict(spectrogram_features)
    return "AI-generated" if prediction[0] > 0.5 else "Human"

# Example usage
model = load_model("ai_voice_cnn.h5")
result = detect_ai_voice(model, 'voices/janan1.wav')

print("[✓] Result:", result)
