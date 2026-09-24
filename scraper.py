"""
VeritasAI Article Scraper & Extractor
Extracts article content, author, domain, and clean text from news URLs.
"""

import re
import urllib.parse
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 VeritasAI/2.0"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def extract_domain(url: str) -> str:
    """Extract clean base domain from a URL."""
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return "unknown"


def scrape_article_from_url(url: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Scrape article text, title, author, and metadata from a URL.
    Returns structured dictionary with cleaned content.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    domain = extract_domain(url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Failed to fetch webpage: {str(e)}",
            "url": url,
            "domain": domain,
            "title": "",
            "text": ""
        }

    soup = BeautifulSoup(response.content, "html.parser")

    # Remove unwanted scripts, styles, navigations, sidebars, footer
    for elem in soup(["script", "style", "nav", "header", "footer", "aside", "noscript", "form", "svg"]):
        elem.decompose()

    # Extract title
    title = ""
    og_title = soup.find("meta", property="og:title")
    twitter_title = soup.find("meta", attrs={"name": "twitter:title"})
    h1 = soup.find("h1")

    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    elif twitter_title and twitter_title.get("content"):
        title = twitter_title["content"].strip()
    elif h1:
        title = h1.get_text().strip()
    elif soup.title:
        title = soup.title.get_text().strip()

    # Extract Author if available
    author = "Unknown"
    author_meta = soup.find("meta", attrs={"name": re.compile(r"author", re.I)})
    if author_meta and author_meta.get("content"):
        author = author_meta["content"].strip()

    # Extract Publish Date if available
    publish_date = "N/A"
    time_meta = soup.find("meta", property=re.compile(r"article:published_time|date", re.I))
    if time_meta and time_meta.get("content"):
        publish_date = time_meta["content"][:10]

    # Extract main body text
    # Prioritize <article> tags, or fallback to paragraphs
    paragraphs = []
    article_tag = soup.find("article")
    search_context = article_tag if article_tag else soup

    for p in search_context.find_all("p"):
        p_text = p.get_text().strip()
        # Filter out very short snippets, cookies, disclaimers
        if len(p_text.split()) > 5:
            paragraphs.append(p_text)

    full_text = " \n\n".join(paragraphs)

    # If full text is still too short, fallback to body text
    if len(full_text.strip()) < 50:
        body = soup.find("body")
        if body:
            full_text = body.get_text(separator=" ", strip=True)

    # Clean whitespace
    full_text = re.sub(r"\s+", " ", full_text).strip()

    if len(full_text) < 40:
        return {
            "success": False,
            "error": "The page does not contain enough readable article text (may require Javascript or login).",
            "url": url,
            "domain": domain,
            "title": title or "Untitled Article",
            "text": full_text
        }

    return {
        "success": True,
        "url": url,
        "domain": domain,
        "title": title or domain,
        "author": author,
        "publish_date": publish_date,
        "text": full_text[:12000],  # cap reasonable length
        "word_count": len(full_text.split())
    }
