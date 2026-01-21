from news_scraper import get_trending_news
from script_generator import generate_script
from video_generator import create_video

def run():
    print("✅ Starting Task1: AI Video Generator...")

    news = get_trending_news()
    print("📰 News fetched:", news.get("title"))

    script = generate_script(news)
    print("📝 Script generated (first 120 chars):", script[:120])

    out_path = create_video(script_text=script, news=news, total_duration_sec=45, fps=24)




    print("🎬 Video created at:", out_path)

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print("❌ ERROR:", e)
        input("Press Enter to close...")
