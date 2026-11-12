import librosa
import numpy as np
from tensorflow.keras.models import load_model

# Load pre-trained emotion recognition model
emotion_model = load_model('emotion_recognition_model.h5')

# Define emotion labels corresponding to your model's output
emotion_labels = ['Angry', 'Happy', 'Sad', 'Neutral']  # <-- update this based on your model

def extract_features_for_emotion(filename):
    y, sr = librosa.load(filename, sr=16000)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

def predict_emotion(filename):
    features = extract_features_for_emotion(filename)
    features = np.reshape(features, (1, -1))  # Reshape for model input
    predictions = emotion_model.predict(features)

    predicted_index = np.argmax(predictions)
    confidence = float(np.max(predictions))

    return emotion_labels[predicted_index], confidence

# Example usage
if __name__ == "__main__":
    filename = 'voices/janan1.wav'  # Change path if needed
    emotion, confidence = predict_emotion(filename)
    print(f"[✓] Detected Emotion: {emotion} (Confidence: {confidence:.2f})")
