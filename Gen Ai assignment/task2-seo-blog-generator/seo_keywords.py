import requests

def google_suggest(query: str, limit: int = 8):
    url = "https://suggestqueries.google.com/complete/search"
    params = {"client": "firefox", "q": query}
    r = requests.get(url, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()
    suggestions = data[1] if len(data) > 1 else []
    # keep unique, short-ish
    out = []
    for s in suggestions:
        s = s.strip()
        if s and s.lower() not in [x.lower() for x in out]:
            out.append(s)
        if len(out) >= limit:
            break
    return out

def pick_main_keywords(product_title: str):
    # seed queries (simple but effective)
    seeds = [
        product_title,
        f"best {product_title}",
        f"{product_title} price",
        f"{product_title} review",
    ]

    pool = []
    for q in seeds:
        pool.extend(google_suggest(q, limit=5))

    # rank by “SEO-ish” words
    boosters = ["best", "review", "price", "buy", "top", "cheap", "2026", "online"]
    def score(k: str):
        k_l = k.lower()
        return sum(1 for b in boosters if b in k_l) + (1 if len(k) <= 45 else 0)

    pool = sorted(set(pool), key=score, reverse=True)

    # return 3-4 keywords
    return pool[:4] if len(pool) >= 4 else pool[:3]
