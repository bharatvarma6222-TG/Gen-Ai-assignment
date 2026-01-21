import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/"

def scrape_trending_products(limit: int = 5):
    html = requests.get(BASE, timeout=15).text
    soup = BeautifulSoup(html, "lxml")

    items = []
    for a in soup.select("article.product_pod")[:limit]:
        title = a.h3.a.get("title", "").strip()
        price = a.select_one(".price_color").get_text(strip=True)
        rating = a.select_one("p.star-rating")["class"][1]  # One, Two, Three...
        link = a.h3.a.get("href", "")
        product_url = BASE + link.replace("../", "")

        items.append({
            "title": title,
            "price": price,
            "rating": rating,
            "url": product_url
        })

    return items
