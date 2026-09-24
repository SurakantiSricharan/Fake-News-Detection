"""
VeritasAI Database Module
SQLite-based persistent storage for scan history, telemetry, analytics, and user feedback.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "veritas_news.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables for queries and feedback."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        title TEXT,
        content_preview TEXT,
        source_type TEXT, -- 'text' or 'url'
        source_url TEXT,
        prediction_label TEXT NOT NULL, -- 'Real News' or 'Fake News' or 'Uncertain'
        confidence_score REAL NOT NULL,
        fake_probability REAL NOT NULL,
        real_probability REAL NOT NULL,
        clickbait_score REAL,
        sensationalism_score REAL,
        subjectivity_score REAL,
        polarity_score REAL,
        domain TEXT,
        domain_trust TEXT,
        model_used TEXT,
        user_feedback TEXT -- 'correct', 'incorrect', or NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_stats (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()


def record_scan(
    title: str,
    content_preview: str,
    source_type: str,
    prediction_label: str,
    confidence_score: float,
    fake_probability: float,
    real_probability: float,
    clickbait_score: float,
    sensationalism_score: float,
    subjectivity_score: float,
    polarity_score: float,
    domain: str = "N/A",
    domain_trust: str = "Neutral",
    source_url: str = "",
    model_used: str = "BiLSTM-CNN-Attention Ensemble"
) -> int:
    """Save a scan result to SQLite history."""
    conn = get_db_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO scan_history (
        timestamp, title, content_preview, source_type, source_url,
        prediction_label, confidence_score, fake_probability, real_probability,
        clickbait_score, sensationalism_score, subjectivity_score, polarity_score,
        domain, domain_trust, model_used
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        title[:250] if title else "Untitled Query",
        content_preview[:400] if content_preview else "",
        source_type,
        source_url,
        prediction_label,
        confidence_score,
        fake_probability,
        real_probability,
        clickbait_score,
        sensationalism_score,
        subjectivity_score,
        polarity_score,
        domain,
        domain_trust,
        model_used
    ))

    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return scan_id


def get_scan_history(limit: int = 50, filter_label: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve scan history with optional filtering."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if filter_label and filter_label.lower() != "all":
        cursor.execute(
            "SELECT * FROM scan_history WHERE prediction_label = ? ORDER BY id DESC LIMIT ?",
            (filter_label, limit)
        )
    else:
        cursor.execute("SELECT * FROM scan_history ORDER BY id DESC LIMIT ?", (limit,))

    rows = cursor.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append(dict(r))
    return history


def record_feedback(scan_id: int, feedback: str) -> bool:
    """Update user feedback for active learning validation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE scan_history SET user_feedback = ? WHERE id = ?", (feedback, scan_id))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected


def get_analytics_summary() -> Dict[str, Any]:
    """Calculate aggregate statistics across all recorded news scans."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scan_history")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE prediction_label = 'Fake News'")
    fake_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE prediction_label = 'Real News'")
    real_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE prediction_label = 'Uncertain'")
    uncertain_count = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(confidence_score) FROM scan_history")
    avg_conf = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT AVG(clickbait_score) FROM scan_history")
    avg_clickbait = cursor.fetchone()[0] or 0.0

    conn.close()

    return {
        "total_scans": total_scans,
        "fake_count": fake_count,
        "real_count": real_count,
        "uncertain_count": uncertain_count,
        "average_confidence": round(float(avg_conf), 2),
        "average_clickbait": round(float(avg_clickbait), 2)
    }


# Automatically create tables on import
init_db()
