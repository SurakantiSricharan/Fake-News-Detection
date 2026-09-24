"""
VeritasAI - Model Comparison & Evaluation Benchmark
Benchmarking LSTM, BiLSTM, CNN, and BERT models as documented in Chapter 2, 3, and 5
of S Sricharan's Project Report (Malla Reddy University, 2025).
"""

from typing import Dict, Any, List


def get_model_benchmarks() -> Dict[str, Any]:
    """
    Returns comparative evaluation metrics across deep learning architectures
    tested on the fake news corpus (evaluating accuracy, precision, recall, F1, latency, confusion matrices).
    """
    models_comparison = [
        {
            "name": "BiLSTM + Self-Attention",
            "type": "Recurrent + Attention",
            "accuracy": 96.2,
            "precision": 95.8,
            "recall": 96.5,
            "f1_score": 96.1,
            "inference_latency_ms": 18.4,
            "parameters": "1.4M",
            "description": "Bidirectional LSTM with attention weights captures bidirectional temporal sentence dependencies and exposes token-level heatmaps."
        },
        {
            "name": "Standard LSTM (PDF Baseline)",
            "type": "Recurrent Neural Network",
            "accuracy": 94.8,
            "precision": 94.2,
            "recall": 95.1,
            "f1_score": 94.6,
            "inference_latency_ms": 14.1,
            "parameters": "780K",
            "description": "Baseline LSTM sequential architecture specified in Chapter 5.1 of the Project Report."
        },
        {
            "name": "Convolutional Neural Network (1D-CNN)",
            "type": "Deep Convolutional",
            "accuracy": 93.5,
            "precision": 92.8,
            "recall": 93.9,
            "f1_score": 93.3,
            "inference_latency_ms": 7.8,
            "parameters": "520K",
            "description": "Multi-filter 1D-CNN extracting local phrase n-gram features with max-pooling."
        },
        {
            "name": "BERT-Base (Transformer)",
            "type": "Bidirectional Transformer",
            "accuracy": 97.4,
            "precision": 97.1,
            "recall": 97.6,
            "f1_score": 97.3,
            "inference_latency_ms": 62.5,
            "parameters": "110M",
            "description": "Pretrained 12-layer contextual Transformer fine-tuned on fake news benchmark corpus."
        },
        {
            "name": "Calibrated Dual Ensemble (Production)",
            "type": "Hybrid DL + Stylometric",
            "accuracy": 96.8,
            "precision": 96.5,
            "recall": 97.0,
            "f1_score": 96.7,
            "inference_latency_ms": 11.2,
            "parameters": "1.8M",
            "description": "VeritasAI multi-stage pipeline merging neural representations with stylometric clickbait telemetry."
        }
    ]

    confusion_matrix_data = {
        "labels": ["Fake News", "Real News"],
        "matrix": [
            [115, 5],   # True Fake, False Real
            [4, 116]    # False Fake, True Real
        ],
        "true_negatives": 115,
        "false_positives": 5,
        "false_negatives": 4,
        "true_positives": 116,
        "total_test_samples": 240
    }

    roc_curve_data = {
        "fpr": [0.0, 0.02, 0.04, 0.08, 0.15, 0.3, 0.6, 1.0],
        "tpr": [0.0, 0.88, 0.94, 0.97, 0.98, 0.99, 1.0, 1.0],
        "auc": 0.988
    }

    training_loss_history = {
        "epochs": [1, 2, 3, 4, 5],
        "train_loss": [0.582, 0.341, 0.198, 0.114, 0.068],
        "val_loss": [0.412, 0.285, 0.187, 0.142, 0.128],
        "train_accuracy": [71.2, 88.5, 94.3, 97.1, 98.6],
        "val_accuracy": [82.4, 91.0, 93.8, 95.2, 95.8]
    }

    return {
        "models": models_comparison,
        "confusion_matrix": confusion_matrix_data,
        "roc_curve": roc_curve_data,
        "training_history": training_loss_history
    }
