"""
VeritasAI - Prediction CLI Script
Faithful implementation and enhancement of Chapter 5.1 (page 29) of the Project Report:
'Fake news detection using deep learning' - S Sricharan (2311CS020639)
Department of CSE - AI & ML, Malla Reddy University.
"""

import os
import sys

# Configure UTF-8 stdout encoding for Windows console compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

MODEL_PATH_KERAS = os.path.join(os.path.dirname(__file__), "fake_news_model.keras")
MODEL_PATH_H5 = os.path.join(os.path.dirname(__file__), "fake_news_model.h5")
TOKENIZER_PATH = os.path.join(os.path.dirname(__file__), "tokenizer.pkl")


def load_artifacts():
    """Load trained deep learning model and fitted tokenizer."""
    if os.path.exists(MODEL_PATH_KERAS):
        model = load_model(MODEL_PATH_KERAS)
    elif os.path.exists(MODEL_PATH_H5):
        model = load_model(MODEL_PATH_H5)
    else:
        raise FileNotFoundError("Model file not found. Please run 'python model_training.py' first.")

    if os.path.exists(TOKENIZER_PATH):
        with open(TOKENIZER_PATH, "rb") as f:
            tokenizer = pickle.load(f)
    else:
        from tensorflow.keras.preprocessing.text import Tokenizer
        tokenizer = Tokenizer(num_words=5000)

    return model, tokenizer


def predict_news_article(news_text: str, model=None, tokenizer=None):
    """
    Run prediction on news text as specified in Chapter 5 of the project report.
    Label 1 = Real News, Label 0 = Fake News
    """
    if model is None or tokenizer is None:
        model, tokenizer = load_artifacts()

    # Preprocess input sequence
    sequence = tokenizer.texts_to_sequences([news_text])
    padded = pad_sequences(sequence, maxlen=200, padding='post', truncating='post')

    # Predict
    prediction = model.predict(padded, verbose=0)
    raw_score = float(prediction[0][0])

    # In training, label 1 is Real News, 0 is Fake News
    if raw_score > 0.5:
        confidence = round(raw_score, 4)
        verdict = "Real News"
        symbol = "✅"
        print(f"{symbol} Real News (Confidence: {round(confidence * 100, 2)}%)")
    else:
        confidence = round(1.0 - raw_score, 4)
        verdict = "Fake News"
        symbol = "⚠️"
        print(f"{symbol} Fake News (Confidence: {round(confidence * 100, 2)}%)")

    return {
        "verdict": verdict,
        "confidence": confidence,
        "raw_score": raw_score,
        "real_probability": round(raw_score, 4),
        "fake_probability": round(1.0 - raw_score, 4)
    }


def main():
    print("==================================================================")
    print("VeritasAI: Deep Learning Fake News Detector (CLI Interface)")
    print("Malla Reddy University - S Sricharan (2311CS020639)")
    print("==================================================================")

    model, tokenizer = load_artifacts()

    if len(sys.argv) > 1:
        # Command-line argument mode
        news_input = " ".join(sys.argv[1:])
        print(f"\nAnalyzing input: \"{news_input}\"\n")
        predict_news_article(news_input, model, tokenizer)
    else:
        # Interactive mode as in PDF page 29
        news_input = input("\nEnter the news article: ")
        if not news_input.strip():
            print("No input provided. Exiting.")
            return
        print("\n--- Model Output ---")
        predict_news_article(news_input, model, tokenizer)


if __name__ == "__main__":
    main()
