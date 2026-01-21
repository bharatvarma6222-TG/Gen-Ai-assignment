import json
import os
from scraper import scrape_trending_products
from seo_keywords import pick_main_keywords
from blog_generator import generate_blog

def run():
    os.makedirs("output", exist_ok=True)

    products = scrape_trending_products(limit=5)
    with open("output/products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    # pick 1 product (top trending)
    product = products[0]
    keywords = pick_main_keywords(product["title"])

    title, blog = generate_blog(product, keywords)

    md = f"""# {title}

**Main SEO keywords:** {", ".join(keywords)}

{blog}
"""
    with open("output/blog.md", "w", encoding="utf-8") as f:
        f.write(md)

    print("✅ Products scraped:", len(products))
    print("✅ Chosen product:", product["title"])
    print("✅ Keywords:", keywords)
    print("✅ Blog saved to: output/blog.md")

if __name__ == "__main__":
    run()
