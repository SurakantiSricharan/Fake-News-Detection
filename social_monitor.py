"""
VeritasAI Social Media & Live Stream Disinformation Monitor
Direct automated extraction, real-time feed processing, and batch deep learning verification.
Supports:
- Reddit Live Feeds (r/news, r/worldnews, r/conspiracy, r/technology, r/science) via Atom/RSS
- Global News Wire Feeds (BBC, NPR, The Verge, Hacker News, The Onion)
- Google News Live Query Search (any topic/hashtag)
- High-Velocity Viral Social Media Stream Simulator (X/Threads style with engagement & bot forensics)
"""

import re
import html
import random
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any, Optional
import xml.etree.ElementTree as ET
import requests

from scraper import extract_domain
from models.deep_learning_model import get_classifier

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 VeritasAI-SocialMonitor/2.0"
    ),
    "Accept": "application/atom+xml,application/rss+xml,application/xml,text/xml,*/*",
}

# Pre-curated high-velocity social posts for instant demonstration & offline resilience
SIMULATED_VIRAL_POSTS = [
    {
        "id": "sim-fake-01",
        "platform": "Viral Social (X/Threads)",
        "author": "TruthSeeker_Global",
        "handle": "@DeepStateUnmasked",
        "channel": "Viral Claims",
        "title": "EMERGENCY ALERT: Classified memo leaks proving drinking sodium chlorite cures 100% of viral infections!",
        "text": "EMERGENCY LEAK: Whistleblower scientists just declassified confidential military reports confirming common mineral drops and distilled lemon cure all deadly respiratory viruses overnight! Big Pharma is actively paying social media platforms billions to censor this before tomorrow morning! RETWEET IMMEDIATELY to save lives before this account gets banned forever! #HealthTruth #Whistleblower #PharmaScam",
        "domain": "whistleblower-patriot-leaks.info",
        "url": "https://twitter.com/DeepStateUnmasked/status/188402919382",
        "likes": 48200,
        "shares": 19400,
        "comments": 6120,
        "virality_velocity": 92.5,
        "bot_risk_score": 88.0,
        "timestamp_str": "12m ago"
    },
    {
        "id": "sim-fake-02",
        "platform": "Viral Social (X/Threads)",
        "author": "ApexFinancialPulse",
        "handle": "@ApexFinAlerts",
        "channel": "Crypto & Finance",
        "title": "LEAKED: Federal Reserve to permanently cancel paper cash this Monday and freeze bank accounts!",
        "text": "BOMBSHELL ECONOMIC LEAK: Emergency directives leaked from central bank headquarters reveal all retail banks will shut ATM withdrawals starting midnight Monday! All citizen accounts will be liquidated into centralized digital tracking tokens! Withdraw all your cash NOW before your lifetime savings are zeroed out! Share with family immediately! #BankRun #EmergencyAlert #CBDC #Hyperinflation",
        "domain": "coinalert-deepthreats.com",
        "url": "https://twitter.com/ApexFinAlerts/status/188402988102",
        "likes": 34100,
        "shares": 14200,
        "comments": 4230,
        "virality_velocity": 85.0,
        "bot_risk_score": 79.0,
        "timestamp_str": "25m ago"
    },
    {
        "id": "sim-real-01",
        "platform": "Viral Social (X/Threads)",
        "author": "SpaceFlight_Daily",
        "handle": "@SpaceFlightDaily",
        "channel": "Science & Space",
        "title": "NASA James Webb Space Telescope confirms spectroscopic signatures of atmospheric water vapor on exoplanet",
        "text": "Astronomers analyzing data from the James Webb Space Telescope's Near-Infrared Spectrograph have detected distinct transmission spectra corresponding to atmospheric water vapor and carbon dioxide on an exoplanet 700 light-years away. The peer-reviewed study, published in Nature Astronomy, provides the clearest spectroscopic evidence to date of atmospheric composition on distant gas giants. #SpaceScience #JWST #NASA #Astrophysics",
        "domain": "nasa.gov",
        "url": "https://twitter.com/SpaceFlightDaily/status/188401123490",
        "likes": 28900,
        "shares": 6800,
        "comments": 1450,
        "virality_velocity": 45.0,
        "bot_risk_score": 12.0,
        "timestamp_str": "42m ago"
    },
    {
        "id": "sim-real-02",
        "platform": "Viral Social (X/Threads)",
        "author": "GlobalTechWire",
        "handle": "@GlobalTechWire",
        "channel": "Tech & AI",
        "title": "Semiconductor manufacturing consortium announces 2-nanometer test chips entering trial production",
        "text": "Leading international semiconductor fabricators announced on Thursday that pilot production lines for next-generation 2-nanometer nanosheet transistors have achieved operational stability. According to technical specifications presented at the IEEE International Solid-State Circuits Conference, the architecture promises up to 15 percent performance gains and 30 percent reduced power consumption over existing 3nm nodes.",
        "domain": "reuters.com",
        "url": "https://twitter.com/GlobalTechWire/status/188399812401",
        "likes": 19400,
        "shares": 4100,
        "comments": 890,
        "virality_velocity": 38.0,
        "bot_risk_score": 8.0,
        "timestamp_str": "1h ago"
    },
    {
        "id": "sim-fake-03",
        "platform": "Viral Social (X/Threads)",
        "author": "PatriotEchoes99",
        "handle": "@PatriotEchoes99",
        "channel": "Politics & Viral",
        "title": "SHOCKING VIDEO: Microscopic surveillance nanobots discovered swimming inside new seasonal flu vaccines!",
        "text": "WAKE UP PEOPLE! Independent microscopic video footage proves brand new vaccine batches contain self-assembling biological tracking devices designed to emit radio frequencies! Doctors are threatening anyone who posts this video with license revocation! Watch the secret footage before big tech scrubs it completely! Repost everywhere! #VaccineTruth #SecretAgenda #Exposed",
        "domain": "banned-video-truth.net",
        "url": "https://twitter.com/PatriotEchoes99/status/188398412999",
        "likes": 56200,
        "shares": 27800,
        "comments": 8950,
        "virality_velocity": 96.0,
        "bot_risk_score": 92.0,
        "timestamp_str": "1h 15m ago"
    },
    {
        "id": "sim-satire-01",
        "platform": "Viral Social (X/Threads)",
        "author": "The Daily Satirist",
        "handle": "@DailySatirist",
        "channel": "Satire & Parody",
        "title": "Government institutes mandatory 15-minute nap requirement for all arguing internet commenters",
        "text": "WASHINGTON—In an effort to lower ambient online hostility, federal regulators announced that any user typing in ALL CAPS for more than three consecutive sentences will have their screen replaced with soothing pictures of golden retriever puppies accompanied by mandatory chamomile tea reminders. 'We believe aggressive forum debaters are simply in need of a good juice box and nap time,' explained lead officials.",
        "domain": "theonion.com",
        "url": "https://twitter.com/DailySatirist/status/188397120011",
        "likes": 42000,
        "shares": 15400,
        "comments": 3100,
        "virality_velocity": 62.0,
        "bot_risk_score": 15.0,
        "timestamp_str": "2h ago"
    }
]

REDDIT_SUBREDDITS = {
    "news": "r/news (Breaking General News)",
    "worldnews": "r/worldnews (Global Affairs)",
    "conspiracy": "r/conspiracy (Viral Claims & Conspiracy)",
    "technology": "r/technology (Tech & Digital Issues)",
    "science": "r/science (Scientific Findings)"
}

NEWS_WIRE_FEEDS = {
    "bbc": {
        "name": "BBC News World",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "domain": "bbc.co.uk"
    },
    "npr": {
        "name": "NPR National News",
        "url": "https://feeds.npr.org/1001/rss.xml",
        "domain": "npr.org"
    },
    "verge": {
        "name": "The Verge (Tech & Media)",
        "url": "https://www.theverge.com/rss/index.xml",
        "domain": "theverge.com"
    },
    "hackernews": {
        "name": "Hacker News Top Discussions",
        "url": "https://news.ycombinator.com/rss",
        "domain": "news.ycombinator.com"
    },
    "theonion": {
        "name": "The Onion (Satire / Parody Benchmark)",
        "url": "https://theonion.com/feed/",
        "domain": "theonion.com"
    }
}


def clean_html_markup(raw_html: str) -> str:
    """Strip HTML tags and unescape entities."""
    if not raw_html:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw_html)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_reddit_posts(subreddit: str = "news", limit: int = 15) -> List[Dict[str, Any]]:
    """
    Fetch live posts directly from Reddit via public Atom/RSS feed.
    Zero API credentials or authentication required.
    """
    sub = subreddit.replace("r/", "").strip().lower()
    rss_url = f"https://www.reddit.com/r/{sub}/.rss"
    posts = []

    try:
        response = requests.get(rss_url, headers=HEADERS, timeout=8)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entries = root.findall("atom:entry", ns)

            for i, entry in enumerate(entries[:limit]):
                title_elem = entry.find("atom:title", ns)
                title = clean_html_markup(title_elem.text) if title_elem is not None else ""

                author_elem = entry.find("atom:author/atom:name", ns)
                author = author_elem.text if author_elem is not None else "/u/reddit_user"

                content_elem = entry.find("atom:content", ns)
                content_html = content_elem.text if content_elem is not None else ""
                clean_content = clean_html_markup(content_html)

                link_elem = entry.find("atom:link", ns)
                post_url = link_elem.attrib.get("href", "") if link_elem is not None else ""

                id_elem = entry.find("atom:id", ns)
                post_id = id_elem.text.split("/")[-1] if id_elem is not None else f"reddit-{i}"

                # Extract linked article domain if present
                domain = "reddit.com"
                url_match = re.search(r'href="(https?://[^"]+)"', content_html)
                if url_match and "reddit.com" not in url_match.group(1):
                    domain = extract_domain(url_match.group(1))

                # Synthesize realistic engagement metrics from rank position
                base_score = max(50, 4500 - (i * 240) + random.randint(-80, 80))
                comments_count = max(10, int(base_score * 0.18) + random.randint(-15, 20))
                shares_count = max(5, int(base_score * 0.08) + random.randint(-10, 15))

                posts.append({
                    "id": f"reddit-{post_id}",
                    "platform": "Reddit",
                    "channel": f"r/{sub}",
                    "author": author,
                    "handle": author,
                    "title": title,
                    "text": clean_content[:600] if clean_content else title,
                    "domain": domain,
                    "url": post_url,
                    "likes": base_score,
                    "shares": shares_count,
                    "comments": comments_count,
                    "virality_velocity": round(min(98.0, (base_score / 40.0) + random.uniform(5, 20)), 1),
                    "bot_risk_score": round(random.uniform(5.0, 28.0) if sub != "conspiracy" else random.uniform(40.0, 82.0), 1),
                    "timestamp_str": f"{random.randint(5, 59)}m ago"
                })
    except Exception as e:
        print(f"Reddit RSS fetch notice: {e}")

    # Fallback to simulated if offline or network error
    if not posts:
        return [p for p in SIMULATED_VIRAL_POSTS if "reddit" in p.get("platform", "").lower() or True][:limit]

    return posts


def fetch_news_wire_posts(feed_key: str = "bbc", limit: int = 15) -> List[Dict[str, Any]]:
    """
    Fetch live headlines and dispatches from global RSS news wires.
    """
    feed_info = NEWS_WIRE_FEEDS.get(feed_key, NEWS_WIRE_FEEDS["bbc"])
    feed_url = feed_info["url"]
    domain = feed_info["domain"]
    posts = []

    try:
        response = requests.get(feed_url, headers=HEADERS, timeout=8)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            items = root.findall(".//item")

            for i, item in enumerate(items[:limit]):
                title_elem = item.find("title")
                title = clean_html_markup(title_elem.text) if title_elem is not None else ""

                desc_elem = item.find("description")
                desc = clean_html_markup(desc_elem.text) if desc_elem is not None else ""

                link_elem = item.find("link")
                link = link_elem.text if link_elem is not None else ""

                pub_elem = item.find("pubDate")
                pub_date = pub_elem.text[:16] if pub_elem is not None and pub_elem.text else "Recent"

                posts.append({
                    "id": f"wire-{feed_key}-{i}",
                    "platform": "News Wire",
                    "channel": feed_info["name"],
                    "author": feed_info["name"],
                    "handle": f"@{feed_key}_wire",
                    "title": title,
                    "text": desc or title,
                    "domain": domain,
                    "url": link,
                    "likes": random.randint(800, 15000),
                    "shares": random.randint(200, 4800),
                    "comments": random.randint(50, 950),
                    "virality_velocity": round(random.uniform(20.0, 65.0), 1),
                    "bot_risk_score": 4.5,
                    "timestamp_str": pub_date
                })
    except Exception as e:
        print(f"News Wire fetch notice: {e}")

    if not posts:
        # Fallback to simulated
        return [p for p in SIMULATED_VIRAL_POSTS if p.get("platform") == "News Wire"][:limit]

    return posts


def fetch_google_news_query(query: str = "technology", limit: int = 15) -> List[Dict[str, Any]]:
    """
    Search real-time news headlines across any topic/hashtag via Google News RSS.
    """
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    posts = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=8)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            items = root.findall(".//item")

            for i, item in enumerate(items[:limit]):
                title_elem = item.find("title")
                raw_title = clean_html_markup(title_elem.text) if title_elem is not None else ""

                # Google News titles usually have format: "Headline - Source Name"
                parts = raw_title.rsplit(" - ", 1)
                headline = parts[0]
                source_name = parts[1] if len(parts) > 1 else "News Source"

                link_elem = item.find("link")
                link = link_elem.text if link_elem is not None else ""

                desc_elem = item.find("description")
                desc = clean_html_markup(desc_elem.text) if desc_elem is not None else headline

                pub_elem = item.find("pubDate")
                pub_date = pub_elem.text[:16] if pub_elem is not None and pub_elem.text else "Today"

                domain = extract_domain(link)
                if domain == "unknown" or "google.com" in domain:
                    domain = source_name.lower().replace(" ", "") + ".com"

                posts.append({
                    "id": f"gnews-{i}",
                    "platform": "Google News",
                    "channel": f"Search: '{query}'",
                    "author": source_name,
                    "handle": f"@{source_name.lower().replace(' ', '')}",
                    "title": headline,
                    "text": headline + ". " + desc,
                    "domain": domain,
                    "url": link,
                    "likes": random.randint(1200, 25000),
                    "shares": random.randint(400, 6000),
                    "comments": random.randint(80, 1200),
                    "virality_velocity": round(random.uniform(25.0, 75.0), 1),
                    "bot_risk_score": round(random.uniform(5.0, 20.0), 1),
                    "timestamp_str": pub_date
                })
    except Exception as e:
        print(f"Google News search notice: {e}")

    return posts


def calculate_virality_threat(fake_probability: float, virality_velocity: float, clickbait_index: float) -> Dict[str, Any]:
    """
    Multi-dimensional Disinformation Virality Threat Index.
    Combines DL Deception Probability with Social Spread Velocity and Agitation Index.
    """
    # Threat score from 0 to 100
    base_threat = (fake_probability * 0.6) + ((virality_velocity / 100.0) * 0.25) + ((clickbait_index / 100.0) * 0.15)
    threat_score = round(min(99.9, max(0.5, base_threat * 100.0)), 1)

    if fake_probability >= 70.0 and virality_velocity >= 50.0:
        level = "CRITICAL THREAT"
        badge = "🚨 CRITICAL DISINFORMATION"
        color = "danger"
        summary = "Viral deceptive claim spreading rapidly across social feeds; high priority fact-check alert."
    elif fake_probability >= 60.0 or threat_score >= 60.0:
        level = "ELEVATED RISK"
        badge = "⚠️ SUSPECTED FAKE"
        color = "warning"
        summary = "Substantial linguistic deception markers and speculative rhetoric detected."
    elif clickbait_index >= 50.0:
        level = "MODERATE"
        badge = "⚡ SENSATIONALIST CLICKBAIT"
        color = "amber"
        summary = "Sensationalized headline phrasing designed to provoke emotional engagement."
    else:
        level = "LOW / VERIFIED"
        badge = "✅ VERIFIED FACTUAL"
        color = "success"
        summary = "Consistent with standard journalistic attribution and objective lexical coherence."

    return {
        "threat_score": threat_score,
        "threat_level": level,
        "threat_badge": badge,
        "threat_color": color,
        "threat_summary": summary
    }


def analyze_social_posts_batch(posts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Execute automated deep learning verification and stylometric analysis across a batch of social posts.
    Calculates batch-wide disinformation prevalence, threat rankings, and top hoaxes.
    """
    classifier = get_classifier()
    scanned_posts = []

    fake_count = 0
    real_count = 0
    critical_alerts = 0
    total_clickbait = 0.0

    for post in posts:
        # Full content to analyze
        content_to_analyze = f"{post.get('title', '')} {post.get('text', '')}".strip()
        domain = post.get("domain", "N/A")

        # Run VeritasAI DL Classifier
        result = classifier.predict(text=content_to_analyze, domain=domain, source_url=post.get("url", ""))

        fake_prob = result["fake_probability"]
        real_prob = result["real_probability"]
        clickbait = result["stylometrics"]["clickbait_index"]
        virality = post.get("virality_velocity", 40.0)

        # Threat Assessment
        threat_info = calculate_virality_threat(
            fake_probability=fake_prob,
            virality_velocity=virality,
            clickbait_index=clickbait
        )

        if threat_info["threat_level"] == "CRITICAL THREAT":
            critical_alerts += 1

        if result["verdict"] == "Fake News":
            fake_count += 1
        elif result["verdict"] == "Real News":
            real_count += 1

        total_clickbait += clickbait

        # Extract top deceptive tokens for quick preview
        suspicious_cues = [
            t["word"] for t in result.get("explainable_tokens", [])
            if t.get("category") == "suspicious"
        ][:4]

        scanned_post = {
            **post,
            "verdict": result["verdict"],
            "confidence": result["confidence"],
            "fake_probability": fake_prob,
            "real_probability": real_prob,
            "stylometrics": result["stylometrics"],
            "domain_intel": result["domain_intel"],
            "threat": threat_info,
            "suspicious_cues": suspicious_cues,
            "key_reasons": result.get("reasons", [])[:2]
        }
        scanned_posts.append(scanned_post)

    total_posts = len(scanned_posts)
    misinformation_rate = round((fake_count / total_posts * 100.0), 1) if total_posts > 0 else 0.0
    avg_clickbait = round((total_clickbait / total_posts), 1) if total_posts > 0 else 0.0

    # Sort posts by threat score descending so highest risks appear first
    scanned_posts.sort(key=lambda p: p["threat"]["threat_score"], reverse=True)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_posts": total_posts,
        "fake_detected_count": fake_count,
        "real_verified_count": real_count,
        "critical_alerts_count": critical_alerts,
        "misinformation_prevalence_pct": misinformation_rate,
        "average_clickbait_index": avg_clickbait,
        "stream_threat_index": round(min(100.0, (misinformation_rate * 0.7) + (avg_clickbait * 0.3)), 1),
        "posts": scanned_posts
    }


def get_social_trending_topics() -> List[Dict[str, Any]]:
    """Return pre-computed trending topics and hashtags with misinformation alerts."""
    return [
        {"topic": "#HealthHoaxes", "label": "Miracle Cures & Wellness Hoaxes", "category": "Health", "alert_level": "High"},
        {"topic": "#BreakingConspiracy", "label": "Classified Leaks & Tower Claims", "category": "Conspiracy", "alert_level": "Critical"},
        {"topic": "#SpaceDiscovery", "label": "NASA Rover & JWST Spectra", "category": "Science", "alert_level": "Low / Verified"},
        {"topic": "#EconomyAlert", "label": "Federal Reserve & Inflation Data", "category": "Finance", "alert_level": "Moderate"},
        {"topic": "#AIControversy", "label": "Deepfakes & Silicon Fabrication", "category": "Technology", "alert_level": "Moderate"},
        {"topic": "#SatireWire", "label": "The Onion & Digital Speed Bumps", "category": "Satire", "alert_level": "Satire"}
    ]
