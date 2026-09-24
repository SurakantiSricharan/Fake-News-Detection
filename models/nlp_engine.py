"""
VeritasAI NLP & Stylometrics Engine
Comprehensive Natural Language Processing pipeline:
- Text Cleaning, Normalization, Tokenization, Lemmatization
- Explainable AI (XAI) Token Deception Attribution
- Clickbait & Sensationalism Scoring
- Emotional Polarity & Subjectivity Analysis
- Domain Reputation Knowledge Engine
"""

import re
import math
from typing import Dict, List, Any, Tuple
from textblob import TextBlob


# Verified Reliable vs Misinformation/Satire Domains
TRUSTED_DOMAINS = {
    "reuters.com": "Verified High Credibility International News Agency",
    "apnews.com": "Verified High Credibility News Wire",
    "bbc.com": "Verified Public Broadcaster",
    "bbc.co.uk": "Verified Public Broadcaster",
    "nytimes.com": "Established News Publisher",
    "wsj.com": "Established Financial & News Publisher",
    "bloomberg.com": "Verified Financial & Global News",
    "theguardian.com": "Established Independent Journalism",
    "washingtonpost.com": "Established News Publisher",
    "nature.com": "Peer-Reviewed Scientific Journal",
    "science.org": "Peer-Reviewed Scientific Journal",
    "nih.gov": "Official Government Health Institution",
    "cdc.gov": "Official Public Health Agency",
    "who.int": "World Health Organization",
    "economist.com": "Established Analytical Journalism",
    "npr.org": "Verified Public Radio & Journalism",
    "aljazeera.com": "International News Network",
    "ft.com": "Financial Times Journal"
}

QUESTIONABLE_DOMAINS = {
    "theonion.com": "Known Satirical Publication (Humor/Parody)",
    "babylonbee.com": "Known Satirical Publication (Humor/Parody)",
    "infowars.com": "Flagged for Conspiracy Theories & Disinformation",
    "naturalnews.com": "Flagged for Health & Medical Misinformation",
    "beforeitsnews.com": "Unverified User-Submitted Blog with High Disinformation Rate",
    "worldnewsdailyreport.com": "Fabricated Hoax & Satire Stories",
    "empirenews.net": "Known Satirical/Hoax Website",
    "nationalreport.net": "Known Fake News / Satire Website",
    "yournewswire.com": "Flagged Sensationalist Disinformation Site",
    "newspunch.com": "Flagged Misinformation Network"
}

# Deceptive & Sensational Clickbait Triggers
SENSATIONAL_PATTERNS = [
    r"\b(shocking|unbelievable|miracle cure|mind-blowing|secret they don't want you to know)\b",
    r"\b(mainstream media is lying|they are hiding this|wake up sheeple|proof of alien)\b",
    r"\b(cure for cancer found|you won't believe|will blow your mind|doctors hate this)\b",
    r"\b(illuminati|conspiracy exposed|leaked document proves|total blackout)\b",
    r"\b(censored by big tech|100% guaranteed|instant cure|hoax revealed)\b",
    r"\b(share before it gets deleted|classified video shows|deep state agenda)\b",
    r"\b(bombshell|emergency alert|emergency leak|retweet immediately|share immediately|share with family)\b",
    r"\b(bank run|freeze bank accounts|cancel paper cash|whistleblower leaked|secret memo)\b"
]

FACTUAL_CORROBORATION_MARKERS = [
    r"\b(according to|stated in a statement|published in the journal|official report)\b",
    r"\b(data released by|peer-reviewed|spokesperson confirmed|survey conducted by)\b",
    r"\b(clinical trial|evidence suggests|university researchers|spokeswoman said)\b",
    r"\b(statistical analysis|investigators said|recorded by|verified by)\b",
    r"\b(in an interview with|documents show|government officials said|agencies reported)\b"
]

STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
    "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once"
}


def clean_text(text: str) -> str:
    """
    Standardize text according to Section 4.3 of the report:
    Lowercasing, removing URLs, punctuation, extra spaces, keeping alphabetic tokens.
    """
    if not text:
        return ""
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)
    # Convert to lowercase
    text = text.lower()
    # Remove non-alphanumeric (keep spaces and basic punctuation for sentence structure)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_and_filter(text: str) -> List[str]:
    """Tokenize and remove standard stopwords."""
    cleaned = clean_text(text)
    tokens = cleaned.split()
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


def compute_stylometrics(raw_text: str) -> Dict[str, Any]:
    """
    Analyze stylistic and psychological deception markers:
    - Clickbait & Sensationalism Index
    - Caps-lock abuse ratio
    - Punctuation abuse (exclamations, question marks)
    - Sentiment Polarity & Subjectivity
    - Lexical Richness (Type-Token Ratio)
    - Citation / Quote density
    """
    if not raw_text or not raw_text.strip():
        return {
            "clickbait_index": 0.0,
            "sensationalism_score": 0.0,
            "subjectivity_score": 0.0,
            "polarity_score": 0.0,
            "caps_ratio": 0.0,
            "exclamation_count": 0,
            "quote_count": 0,
            "lexical_diversity": 0.0,
            "word_count": 0,
            "readability": "Neutral"
        }

    words = raw_text.split()
    total_words = max(len(words), 1)

    # 1. Caps Ratio (excluding short words)
    caps_words = [w for w in words if w.isupper() and len(w) > 2]
    caps_ratio = min(round((len(caps_words) / total_words) * 100, 2), 100.0)

    # 2. Punctuation Abuse
    exclamation_count = raw_text.count("!")
    question_count = raw_text.count("?")
    quote_count = raw_text.count('"') + raw_text.count("'") + raw_text.count("“") + raw_text.count("”")

    # 3. Sentiment & Subjectivity via TextBlob
    try:
        blob = TextBlob(raw_text[:3000])
        sentiment_polarity = round(blob.sentiment.polarity, 3)
        sentiment_subjectivity = round(blob.sentiment.subjectivity * 100, 2)
    except Exception:
        sentiment_polarity = 0.0
        sentiment_subjectivity = 50.0

    # 4. Clickbait & Sensationalism Pattern Matching
    sensational_hits = 0
    lower_raw = raw_text.lower()
    for pattern in SENSATIONAL_PATTERNS:
        matches = re.findall(pattern, lower_raw)
        sensational_hits += len(matches)

    factual_hits = 0
    for pattern in FACTUAL_CORROBORATION_MARKERS:
        matches = re.findall(pattern, lower_raw)
        factual_hits += len(matches)

    # Base clickbait index calculation
    clickbait_index = (
        (sensational_hits * 18.0) +
        (caps_ratio * 1.5) +
        (min(exclamation_count, 10) * 4.0) +
        (max(0, sentiment_subjectivity - 60.0) * 0.5)
    )
    # Diminish if reputable journalistic markers are present
    clickbait_index = max(0.0, min(100.0, clickbait_index - (factual_hits * 10.0)))
    clickbait_index = round(clickbait_index, 1)

    # Sensationalism score (0-100)
    sensationalism_score = round(min(100.0, (clickbait_index * 0.7) + (sentiment_subjectivity * 0.3)), 1)

    # 5. Lexical Diversity (Type-Token Ratio)
    clean_words = [w.lower() for w in words if w.isalpha()]
    unique_words = set(clean_words)
    ttr = round((len(unique_words) / max(len(clean_words), 1)) * 100, 2)

    # 6. Readability Assessment
    avg_word_len = sum(len(w) for w in clean_words) / max(len(clean_words), 1)
    if avg_word_len > 6.0:
        readability = "Academic / Complex"
    elif avg_word_len < 4.5:
        readability = "Elementary / Informal"
    else:
        readability = "Standard Journalistic"

    return {
        "clickbait_index": clickbait_index,
        "sensationalism_score": sensationalism_score,
        "subjectivity_score": sentiment_subjectivity,
        "polarity_score": sentiment_polarity,
        "caps_ratio": caps_ratio,
        "exclamation_count": exclamation_count,
        "quote_count": quote_count,
        "lexical_diversity": ttr,
        "word_count": total_words,
        "readability": readability
    }


def evaluate_domain_credibility(domain: str) -> Dict[str, Any]:
    """Check domain against trusted and questionable registries."""
    if not domain or domain == "N/A":
        return {
            "status": "Unknown",
            "trust_level": "Neutral",
            "description": "No verified domain metadata provided (Direct text scan).",
            "trust_score": 50
        }

    domain_lower = domain.lower()

    for trusted, desc in TRUSTED_DOMAINS.items():
        if trusted in domain_lower:
            return {
                "status": "Verified Trusted",
                "trust_level": "High Trust",
                "description": desc,
                "trust_score": 95
            }

    for questionable, desc in QUESTIONABLE_DOMAINS.items():
        if questionable in domain_lower:
            return {
                "status": "High Risk / Satire",
                "trust_level": "Low Trust",
                "description": desc,
                "trust_score": 15
            }

    return {
        "status": "Unverified Independent Domain",
        "trust_level": "Moderate",
        "description": "Domain not in major verified or blacklist directories. Content-based AI inspection applied.",
        "trust_score": 55
    }


def generate_explainable_tokens(raw_text: str, fake_prob: float) -> List[Dict[str, Any]]:
    """
    Generate Explainable AI (XAI) token-level attribution:
    Tag each word in the input text with an influence score and classification:
    - 'suspicious' (red badge): buzzwords, clickbait, conspiratorial or deceptive rhetoric
    - 'factual' (green badge): citations, data markers, formal reporting attribution
    - 'neutral' (default): normal informative text
    """
    words = raw_text.split()
    tokens_xai = []

    # High risk deceptive keywords
    suspicious_lexicon = {
        "shocking", "unbelievable", "secret", "censored", "conspiracy", "hoax",
        "miracle", "cure", "banned", "classified", "exposed", "truth", "traitor",
        "agenda", "deep-state", "aliens", "blackout", "sheeple", "fraud", "poison",
        "catastrophe", "bombshell", "leaked", "rigged", "faked", "cover-up", "bioweapon"
    }

    # Credible journalistic attribution keywords
    factual_lexicon = {
        "reuters", "spokesperson", "statement", "confirmed", "official", "published",
        "researchers", "study", "analysis", "statistics", "report", "verified",
        "department", "investigation", "recorded", "evidence", "witnesses", "data"
    }

    for word in words[:250]:  # Keep UI responsive
        clean_word = re.sub(r"[^a-zA-Z]", "", word).lower()

        if clean_word in suspicious_lexicon:
            score = 0.85
            token_type = "suspicious"
        elif word.isupper() and len(word) > 2:
            score = 0.70
            token_type = "suspicious"
        elif "!" in word:
            score = 0.65
            token_type = "suspicious"
        elif clean_word in factual_lexicon:
            score = -0.75
            token_type = "factual"
        else:
            score = 0.0
            token_type = "neutral"

        tokens_xai.append({
            "word": word,
            "type": token_type,
            "score": round(score, 2)
        })

    return tokens_xai
