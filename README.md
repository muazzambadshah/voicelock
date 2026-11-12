# VoiceLock - AI Voice Authentication & Secure Messaging

Voice-biometric authentication combined with encryption and audio steganography, plus an AI-generated-voice (deepfake) detector and emotion analysis.

## Features
- Speaker verification from voice samples
- AI/deepfake voice detection CNN
- Message encryption (cryptography) and audio steganography
- Emotion analysis and self-destructing messages
- Streamlit web UI

## Tech Stack
Python, TensorFlow, Librosa, Scikit-learn, Cryptography, Streamlit

## Getting Started
```bash
git clone https://github.com/muazzambadshah/voicelock.git
cd voicelock
python -m venv venv
venv\Scripts\activate        # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
streamlit run web_ui.py
```

> **Note:** Trained model weights and datasets are not included in this repository (size). Place trained `ai_voice_cnn.h5` / `voice_model.pkl` (create with `build_ai_model.py`) before running.

## Screenshots
_Screenshots coming soon._

## Author
**Muazzam Badshah** - AI Researcher, NCAI (NUST), Islamabad
[Portfolio](https://muazzam-portfolio-2wk1.vercel.app/) | [LinkedIn](https://www.linkedin.com/in/muazzam-badshah-338881381) | [GitHub](https://github.com/muazzambadshah)
