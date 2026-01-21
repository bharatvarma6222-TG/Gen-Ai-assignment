def generate_blog(product, keywords):
    title = f"Why {product['title']} is Trending Right Now"
    k1, k2, k3 = (keywords + ["", "", ""])[:3]  # safe fallback

    body = f"""
{product['title']} has quickly become a popular pick for readers who want something engaging without wasting time searching endlessly. If you're looking for {k1}, this title stands out thanks to its strong ratings and great value.

One reason people are talking about it is the balance between quality and affordability. At around {product['price']}, it’s a smart choice for anyone comparing options and reading {k2}. The story and writing style make it easy to recommend, whether you're buying for yourself or as a gift.

If your goal is to {k3}, consider checking availability soon because trending books often go out of stock or fluctuate in price. You can view the product details here: {product['url']}

Final tip: shortlist 2–3 similar titles, compare reviews, and pick the one that matches your reading taste.
""".strip()

    # word trim to ~150–200 range (light trimming)
    words = body.split()
    if len(words) > 205:
        body = " ".join(words[:200]) + "..."

    return title, body
