"""
VeritasAI - Model Training Pipeline
Faithful implementation of Chapter 5.1 of the Project Report:
'Fake news detection using deep learning' - S Sricharan (2311CS020639)
Department of CSE - AI & ML, Malla Reddy University.
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

DATASET_PATH = os.path.join(os.path.dirname(__file__), "fake_news_dataset.csv")
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "fake_news_model.keras")
MODEL_H5_PATH = os.path.join(os.path.dirname(__file__), "fake_news_model.h5")
TOKENIZER_SAVE_PATH = os.path.join(os.path.dirname(__file__), "tokenizer.pkl")
METRICS_PATH = os.path.join(os.path.dirname(__file__), "training_metrics.json")


def train_fake_news_model():
    print("==========================================================")
    print("VeritasAI: Training Deep Learning Model (LSTM)")
    print("Referenced from Project Report Chapter 5 (Malla Reddy Univ)")
    print("==========================================================")

    # 1. Load dataset
    print(f"Loading dataset from: {DATASET_PATH}")
    data = pd.read_csv(DATASET_PATH)
    print(f"Dataset shape: {data.shape}")

    # 2. Preprocessing
    texts = data['text'].astype(str)
    labels = data['label']

    max_words = 5000
    maxlen = 200

    tokenizer = Tokenizer(num_words=max_words, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    x = pad_sequences(sequences, maxlen=maxlen, padding='post', truncating='post')
    y = np.array(labels)

    # Save tokenizer for inference in predict_news.py and web app
    with open(TOKENIZER_SAVE_PATH, "wb") as f:
        pickle.dump(tokenizer, f)
    print(f"Tokenizer saved successfully to {TOKENIZER_SAVE_PATH}")

    # 3. Split data (80% train, 20% test as per project report)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples: {len(x_train)}, Testing samples: {len(x_test)}")

    # 4. Model Definition (Sequential Bidirectional LSTM + Conv1D architecture)
    from tensorflow.keras.layers import Conv1D, GlobalMaxPooling1D, Bidirectional
    from tensorflow.keras.optimizers import Adam

    model = Sequential([
        Input(shape=(maxlen,)),
        Embedding(input_dim=max_words, output_dim=128),
        Conv1D(filters=64, kernel_size=5, activation='relu', padding='same'),
        Bidirectional(LSTM(64, dropout=0.2, return_sequences=True)),
        GlobalMaxPooling1D(),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(1, activation='sigmoid')
    ])

    model.compile(
        loss='binary_crossentropy',
        optimizer=Adam(learning_rate=0.002),
        metrics=['accuracy']
    )

    model.summary()

    # 5. Model Training
    print("\nStarting Training (6 Epochs, batch_size=32)...")
    history = model.fit(
        x_train, y_train,
        epochs=6,
        batch_size=32,
        validation_split=0.2,
        verbose=1
    )

    # 6. Evaluation on Unseen Test Data
    print("\n=================== EVALUATION RESULTS ===================")
    y_pred_prob = model.predict(x_test)
    y_pred = (y_pred_prob > 0.5).astype("int32")

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"Accuracy:  {acc:.4f} ({acc*100:.2f}%)")
    print(f"Precision: {prec:.4f} ({prec*100:.2f}%)")
    print(f"Recall:    {rec:.4f} ({rec*100:.2f}%)")
    print(f"F1 Score:  {f1:.4f} ({f1*100:.2f}%)")
    print("Confusion Matrix:")
    print(cm)
    print("==========================================================")

    # 7. Model Saving (Native .keras and .h5)
    try:
        model.save(MODEL_SAVE_PATH)
        print(f"Trained model saved to: {MODEL_SAVE_PATH}")
    except Exception as e:
        print(f"Could not save .keras: {e}")

    try:
        model.save(MODEL_H5_PATH)
        print(f"Trained model saved to: {MODEL_H5_PATH}")
    except Exception as e:
        print(f"Legacy .h5 save note: {e}")

    # Save metrics for web benchmark display
    import json
    metrics = {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "confusion_matrix": cm.tolist(),
        "epochs": 5,
        "train_loss": [float(v) for v in history.history['loss']],
        "train_accuracy": [float(v) for v in history.history['accuracy']],
        "val_loss": [float(v) for v in history.history.get('val_loss', [])],
        "val_accuracy": [float(v) for v in history.history.get('val_accuracy', [])]
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    return model, tokenizer, metrics


if __name__ == "__main__":
    train_fake_news_model()
