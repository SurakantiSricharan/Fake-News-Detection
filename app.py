"""
VeritasAI - FastAPI Server & REST API Endpoints
Main application providing real-time fake news detection, web scraping,
model benchmarking, SQLite audit trail, and explainable AI visualizations.
"""

import os
import uvicorn
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import record_scan, get_scan_history, record_feedback, get_analytics_summary
from scraper import scrape_article_from_url, extract_domain
from models.deep_learning_model import get_classifier
from models.benchmark import get_model_benchmarks
from social_monitor import (
    fetch_reddit_posts,
    fetch_news_wire_posts,
    fetch_google_news_query,
    analyze_social_posts_batch,
    get_social_trending_topics,
    REDDIT_SUBREDDITS,
    NEWS_WIRE_FEEDS,
    SIMULATED_VIRAL_POSTS
)
import io
import csv
import random
from datetime import datetime
from fastapi.responses import Response

app = FastAPI(
    title="VeritasAI - Deep Learning Fake News Intelligence API",
    description="Based on S Sricharan's Project Report (Malla Reddy University, 2025)",
    version="2.0.0"
)

# CORS middleware for open web access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# Pydantic Request Models
class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10, description="News article text or headline")
    title: Optional[str] = Field(default="", description="Optional news headline")
    domain: Optional[str] = Field(default="N/A", description="Optional source domain")


class UrlAnalysisRequest(BaseModel):
    url: str = Field(..., min_length=5, description="Full HTTP/HTTPS URL of news article")


class FeedbackRequest(BaseModel):
    scan_id: int
    feedback: str = Field(..., description="'correct' or 'incorrect'")


class SocialBatchScanRequest(BaseModel):
    posts: List[Dict[str, Any]] = Field(..., description="List of social posts to verify")


# Real-World Curated Case Studies
CASE_STUDIES = [
    {
        "id": "case-fake-1",
        "category": "Health & Medicine",
        "expected": "Fake News",
        "title": "SHOCKING: Big Pharma Hiding Miracle 24-Hour Cancer Cure In Common Lemon Peels!",
        "domain": "naturalnews-miracle.com",
        "text": "SHOCKING TRUTH EXPOSED: Mainstream media is completely silent as independent whistleblowers leak classified reports proving that boiled lemon peels and baking soda destroy 100% of cancer cells in just 24 hours! Greedy pharmaceutical executives and corrupt medical boards have suppressed this ancient knowledge for decades to protect their multibillion-dollar chemotherapy profits! Doctors are furious this leaked out! Share this immediately before government censors scrub this webpage forever!"
    },
    {
        "id": "case-fake-2",
        "category": "Conspiracy & Technology",
        "expected": "Fake News",
        "title": "BOMBSHELL LEAK: 5G Cell Towers Transmitting Secret Mind-Control Waves to Alter DNA",
        "domain": "beforeitsnews-unfiltered.com",
        "text": "DEEP STATE AGENDA REVEALED: Rogue engineers have declassified secret Pentagon documents proving that new high-frequency 5G cellular antennas are emitting pulsed electromagnetic radiation specifically calibrated to manipulate neurological brainwaves and modify human DNA! Insiders confirm a total nationwide electrical grid blackout is scheduled for this Friday to wipe out bank balances and reset credit systems! Wake up sheeple, withdraw all cash now before the globalist cabal takes full control!"
    },
    {
        "id": "case-real-1",
        "category": "Science & Space Exploration",
        "expected": "Real News",
        "title": "NASA Perseverance Rover Detects Organic Molecules in Ancient Jezero Crater Lakebed",
        "domain": "reuters.com",
        "text": "NASA scientists confirmed on Thursday that the Perseverance Mars rover has discovered diverse organic carbon compounds in sedimentary rock cores collected from the Jezero Crater delta. According to research published in the peer-reviewed journal Nature, the findings offer compelling insights into the geochemical environment that existed on the Red Planet more than three billion years ago. Lead mission investigators noted that while organic molecules can form through non-biological processes, their presence provides critical data for future sample-return missions."
    },
    {
        "id": "case-real-2",
        "category": "Economy & Central Banking",
        "expected": "Real News",
        "title": "Federal Reserve Holds Benchmark Interest Rate Steady Amid Moderating Inflation",
        "domain": "apnews.com",
        "text": "The Federal Reserve concluded its two-day policy meeting on Wednesday by voting unanimously to maintain the benchmark federal funds rate in a target range of 5.25% to 5.50%. In an official statement, the Federal Open Market Committee indicated that recent economic indicators suggest economic activity has been expanding at a solid pace, with job gains remaining robust and the unemployment rate remaining low. Chairman Jerome Powell stated in a subsequent press conference that policymakers require greater confidence that inflation is moving sustainably toward the central bank's two percent target before considering rate adjustments."
    },
    {
        "id": "case-satire",
        "category": "Satire & Parody",
        "expected": "Satire / High Risk",
        "title": "Department of Transportation Installs Speed Bumps on Internet to Slow Spread of Bad Information",
        "domain": "theonion.com",
        "text": "WASHINGTONâ€”In an ambitious attempt to regulate the rapid velocity of modern digital discourse, the Federal Highway Administration announced Tuesday that it has begun deploying millions of virtual rubber speed bumps across global fiber-optic cables. Agency officials stated the newly installed digital speed humps will force high-speed packet traffic to decelerate from 100 megabits per second down to an orderly 15 miles per hour whenever entering controversial comment sections or clickbait headlines."
    }
]


@app.api_route("/", methods=["GET", "HEAD"])
def serve_index():
    """Serve main single-page application."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "VeritasAI Backend is running. Frontend index.html is being prepared."}


@app.post("/api/analyze-text")
def analyze_text(payload: TextAnalysisRequest):
    """Analyze raw article text or headline."""
    classifier = get_classifier()
    result = classifier.predict(
        text=payload.text,
        domain=payload.domain or "N/A"
    )

    # Record scan into SQLite database
    scan_id = record_scan(
        title=payload.title or payload.text[:80],
        content_preview=payload.text[:300],
        source_type="text",
        prediction_label=result["verdict"],
        confidence_score=result["confidence"],
        fake_probability=result["fake_probability"],
        real_probability=result["real_probability"],
        clickbait_score=result["stylometrics"]["clickbait_index"],
        sensationalism_score=result["stylometrics"]["sensationalism_score"],
        subjectivity_score=result["stylometrics"]["subjectivity_score"],
        polarity_score=result["stylometrics"]["polarity_score"],
        domain=payload.domain or "N/A",
        domain_trust=result["domain_intel"]["trust_level"],
        source_url=""
    )
    result["scan_id"] = scan_id
    result["input_title"] = payload.title
    return result


@app.post("/api/analyze-url")
def analyze_url(payload: UrlAnalysisRequest):
    """Scrape live news article from URL and perform automated fact-checking & classification."""
    scraped = scrape_article_from_url(payload.url)

    if not scraped["success"]:
        raise HTTPException(
            status_code=400,
            detail=scraped.get("error", "Failed to scrape readable text from provided URL.")
        )

    classifier = get_classifier()
    result = classifier.predict(
        text=scraped["text"],
        domain=scraped["domain"],
        source_url=payload.url
    )

    # Record scan into SQLite database
    scan_id = record_scan(
        title=scraped["title"],
        content_preview=scraped["text"][:300],
        source_type="url",
        prediction_label=result["verdict"],
        confidence_score=result["confidence"],
        fake_probability=result["fake_probability"],
        real_probability=result["real_probability"],
        clickbait_score=result["stylometrics"]["clickbait_index"],
        sensationalism_score=result["stylometrics"]["sensationalism_score"],
        subjectivity_score=result["stylometrics"]["subjectivity_score"],
        polarity_score=result["stylometrics"]["polarity_score"],
        domain=scraped["domain"],
        domain_trust=result["domain_intel"]["trust_level"],
        source_url=payload.url
    )

    result["scan_id"] = scan_id
    result["article_metadata"] = {
        "url": scraped["url"],
        "domain": scraped["domain"],
        "title": scraped["title"],
        "author": scraped["author"],
        "publish_date": scraped["publish_date"],
        "word_count": scraped["word_count"]
    }
    return result


# ==============================================================================
# AUTOMATED SOCIAL MEDIA & LIVE STREAM INTELLIGENCE ENDPOINTS
# ==============================================================================

@app.get("/api/social/channels")
def get_social_channels():
    """Return available social media and news wire channels for automated scanning."""
    return {
        "reddit_subreddits": [
            {"id": k, "name": v} for k, v in REDDIT_SUBREDDITS.items()
        ],
        "news_wire_feeds": [
            {"id": k, "name": v["name"], "domain": v["domain"]} for k, v in NEWS_WIRE_FEEDS.items()
        ],
        "platforms": [
            {"id": "all", "name": "ðŸŒ All Live Sources (Auto-Aggregated)"},
            {"id": "reddit", "name": "ðŸ¤– Reddit Public Feeds (Live)"},
            {"id": "news_wire", "name": "ðŸ“° Global News Wires (RSS Live)"},
            {"id": "google_news", "name": "ðŸ” Google News Live Search"},
            {"id": "simulated", "name": "ðŸ¦ High-Velocity Viral Social Stream (X/Threads)"}
        ]
    }


@app.get("/api/social/trending")
def get_social_trending():
    """Return trending social hashtags and misinformation alert topics."""
    return {
        "topics": get_social_trending_topics()
    }


@app.get("/api/social/feed")
def get_social_feed(
    platform: str = Query(default="all", description="Platform: all, reddit, news_wire, google_news, simulated"),
    channel: Optional[str] = Query(default=None, description="Subreddit or News wire key"),
    query: Optional[str] = Query(default=None, description="Topic search query or hashtag"),
    limit: int = Query(default=12, ge=3, le=30),
    auto_scan: bool = Query(default=True, description="Automatically run Deep Learning verification")
):
    """
    Fetch and automatically verify social media posts and live news dispatches.
    Zero manual user input required â€” pulls live from Reddit, News Wires, Google News, or Viral Social Streams.
    """
    posts = []

    # 1. Fetch posts based on platform
    if platform == "reddit":
        sub = channel or "news"
        posts = fetch_reddit_posts(subreddit=sub, limit=limit)
    elif platform == "news_wire":
        feed_key = channel or "bbc"
        posts = fetch_news_wire_posts(feed_key=feed_key, limit=limit)
    elif platform == "google_news" or (query and platform != "simulated"):
        search_term = query or "breaking news"
        posts = fetch_google_news_query(query=search_term, limit=limit)
    elif platform == "simulated":
        posts = list(SIMULATED_VIRAL_POSTS)
        if query:
            q_lower = query.lower()
            filtered = [p for p in posts if q_lower in p["title"].lower() or q_lower in p["text"].lower()]
            if filtered:
                posts = filtered
        posts = posts[:limit]
    else:
        # "all" - Aggregate mix of Reddit, News Wires, and High-Velocity Viral Social
        sub = channel or "news"
        reddit_batch = fetch_reddit_posts(subreddit=sub, limit=max(3, limit // 3))
        wire_batch = fetch_news_wire_posts(feed_key="bbc", limit=max(3, limit // 3))
        sim_batch = list(SIMULATED_VIRAL_POSTS)[:max(3, limit // 3)]
        posts = sim_batch + reddit_batch + wire_batch
        random.shuffle(posts)
        posts = posts[:limit]

    # 2. Automated Deep Learning & Stylometrics Batch Verification
    if auto_scan and posts:
        analysis_result = analyze_social_posts_batch(posts)
        # Record scanned social posts into database for audit history
        for p in analysis_result["posts"]:
            try:
                record_scan(
                    title=f"[{p.get('platform', 'Social')}] {p.get('title', '')[:120]}",
                    content_preview=p.get('text', '')[:300],
                    source_type="social",
                    prediction_label=p["verdict"],
                    confidence_score=p["confidence"],
                    fake_probability=p["fake_probability"],
                    real_probability=p["real_probability"],
                    clickbait_score=p["stylometrics"]["clickbait_index"],
                    sensationalism_score=p["stylometrics"]["sensationalism_score"],
                    subjectivity_score=p["stylometrics"]["subjectivity_score"],
                    polarity_score=p["stylometrics"]["polarity_score"],
                    domain=p.get("domain", "social.media"),
                    domain_trust=p.get("domain_intel", {}).get("trust_level", "Neutral"),
                    source_url=p.get("url", ""),
                    model_used="BiLSTM-CNN Dual Ensemble"
                )
            except Exception:
                pass
        return analysis_result

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_posts": len(posts),
        "posts": posts
    }


@app.get("/api/social/live-pulse")
def get_live_pulse():
    """
    Auto-pilot real-time polling endpoint.
    Returns the latest high-velocity incoming social claim with instant neural verdict for live toast alerts.
    """
    sample = random.choice(SIMULATED_VIRAL_POSTS)
    classifier = get_classifier()
    text = f"{sample['title']} {sample['text']}"
    res = classifier.predict(text=text, domain=sample.get("domain", "N/A"))

    from social_monitor import calculate_virality_threat
    threat = calculate_virality_threat(
        fake_probability=res["fake_probability"],
        virality_velocity=sample.get("virality_velocity", 50.0),
        clickbait_index=res["stylometrics"]["clickbait_index"]
    )

    return {
        "post_id": sample["id"],
        "platform": sample["platform"],
        "author": sample["author"],
        "handle": sample["handle"],
        "title": sample["title"],
        "text": sample["text"],
        "url": sample["url"],
        "verdict": res["verdict"],
        "confidence": res["confidence"],
        "threat": threat,
        "shares": sample.get("shares", 1000),
        "likes": sample.get("likes", 5000),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }


@app.get("/api/social/export")
def export_social_telemetry(format: str = Query(default="json", description="'json' or 'csv'")):
    """Export recent social misinformation telemetry to JSON or CSV."""
    posts = list(SIMULATED_VIRAL_POSTS)
    analysis = analyze_social_posts_batch(posts)

    if format.lower() == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Post ID", "Platform", "Author", "Verdict", "Confidence (%)",
            "Fake Prob (%)", "Real Prob (%)", "Threat Level", "Threat Score",
            "Clickbait (%)", "Bot Risk (%)", "Title", "URL"
        ])
        for p in analysis["posts"]:
            writer.writerow([
                p.get("id"), p.get("platform"), p.get("author"), p.get("verdict"),
                p.get("confidence"), p.get("fake_probability"), p.get("real_probability"),
                p.get("threat", {}).get("threat_level"), p.get("threat", {}).get("threat_score"),
                p.get("stylometrics", {}).get("clickbait_index"), p.get("bot_risk_score"),
                p.get("title"), p.get("url")
            ])
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=veritas_social_telemetry.csv"}
        )

    return analysis


@app.get("/api/benchmark")
def benchmark_endpoint():
    """Return model comparative benchmarks (LSTM, BiLSTM, CNN, BERT, Confusion Matrix)."""
    return get_model_benchmarks()


@app.get("/api/case-studies")
def case_studies_endpoint():
    """Return curated real-world case studies for 1-click demonstration."""
    return CASE_STUDIES


@app.get("/api/history")
def history_endpoint(limit: int = Query(default=30, ge=1, le=100), filter: Optional[str] = None):
    """Retrieve audit history and aggregate statistics."""
    history = get_scan_history(limit=limit, filter_label=filter)
    analytics = get_analytics_summary()
    return {
        "history": history,
        "analytics": analytics
    }


@app.post("/api/feedback")
def feedback_endpoint(payload: FeedbackRequest):
    """Record user confirmation or correction for continuous learning."""
    success = record_feedback(payload.scan_id, payload.feedback)
    return {"success": success, "scan_id": payload.scan_id, "feedback": payload.feedback}


@app.get("/api/health")
def health_endpoint():
    """System health and metadata endpoint."""
    return {
        "status": "healthy",
        "service": "VeritasAI Fake News Intelligence System",
        "student": "S Sricharan (2311CS020639)",
        "university": "Malla Reddy University",
        "department": "CSE - Artificial Intelligence and Machine Learning",
        "year": "2025"
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
