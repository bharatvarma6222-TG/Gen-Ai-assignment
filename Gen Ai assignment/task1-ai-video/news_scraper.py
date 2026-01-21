import re
from html import unescape
import requests
import feedparser
from bs4 import BeautifulSoup

def _clean_text(text: str) -> str:
    if not text:
        return ""
    text = unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def _extract_source_from_title(title: str) -> str:
    # Many Google News RSS titles end with " - Publisher"
    if " - " in title:
        return title.split(" - ")[-1].strip()
    return "News"

def _extract_og_image(article_url: str) -> str:
    try:
        r = requests.get(article_url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        tag = soup.find("meta", property="og:image")
        if tag and tag.get("content"):
            return tag["content"].strip()
    except:
        pass
    return ""

def get_trending_news():
    feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        return {"title": "No trending news found", "description": "Please try again later.", "url": "", "image_url": "", "source": "News"}

    first = feed.entries[0]

    raw_title = _clean_text(first.get("title", "Trending News"))
    source = _extract_source_from_title(raw_title)

    # Remove " - Publisher" from headline for cleaner display
    title = raw_title.split(" - ")[0].strip() if " - " in raw_title else raw_title

    desc = _clean_text(first.get("summary", ""))
    url = first.get("link", "")
    image_url = _extract_og_image(url) if url else ""

    return {
        "title": title,
        "description": desc,
        "url": url,
        "image_url": image_url,
        "source": source
    }
