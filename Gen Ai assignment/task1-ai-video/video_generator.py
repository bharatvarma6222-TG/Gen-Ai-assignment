import os
import re
import textwrap
import requests
import numpy as np
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from moviepy.editor import ImageClip, concatenate_videoclips, vfx

W, H = 1280, 720

# Pillow resampling compatibility (works across versions)
try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.LANCZOS


def _get_font(size=46, bold=False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()


def _fetch_bg_image(query: str) -> Image.Image:
    """
    Free source endpoint (no API key): https://source.unsplash.com/1280x720/?<query>
    Query improves relevance but Unsplash source is still random-ish.
    """
    q = re.sub(r"[^a-zA-Z0-9\s-]", "", query or "").strip().replace(" ", ",")
    url = f"https://source.unsplash.com/{W}x{H}/?{q if q else 'news'}"
    try:
        r = requests.get(url, timeout=12)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return img.resize((W, H), RESAMPLE)
    except:
        return Image.new("RGB", (W, H), (12, 12, 12))


def _fetch_image_from_url(img_url: str) -> Image.Image:
    """
    Fetch the actual article image (og:image) => truly topic-based.
    """
    try:
        r = requests.get(img_url, timeout=12, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return img.resize((W, H), RESAMPLE)
    except:
        return None


def _chunk_script(script_text: str) -> list[str]:
    cleaned = " ".join((script_text or "").replace("\n", " ").split())
    if not cleaned:
        return []
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    parts = [p.strip() for p in parts if p.strip()]
    return parts


def _dedupe_lines(lines: list[str]) -> list[str]:
    seen = set()
    out = []
    for l in lines:
        k = (l or "").strip().lower()
        if not k:
            continue
        if k in seen:
            continue
        seen.add(k)
        out.append(l.strip())
    return out


def _draw_cute_anchor(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0):
    """
    Draw a simple cute cartoon character (news anchor) with a speech bubble vibe.
    No external assets required.
    """
    # Colors
    skin = (255, 220, 190)
    hair = (35, 35, 35)
    suit = (35, 90, 160)
    shirt = (245, 245, 245)
    tie = (220, 70, 70)
    outline = (20, 20, 20)

    # Sizes
    head_r = int(52 * scale)
    body_w = int(140 * scale)
    body_h = int(170 * scale)

    # Head
    cx, cy = x + head_r, y + head_r
    draw.ellipse((x, y, x + 2 * head_r, y + 2 * head_r), fill=skin, outline=outline, width=3)

    # Hair
    draw.pieslice((x - 6, y - 10, x + 2 * head_r + 6, y + 2 * head_r + 10),
                  start=200, end=360, fill=hair, outline=None)

    # Eyes
    eye_y = y + int(55 * scale)
    draw.ellipse((x + int(35 * scale), eye_y, x + int(48 * scale), eye_y + int(13 * scale)), fill=outline)
    draw.ellipse((x + int(70 * scale), eye_y, x + int(83 * scale), eye_y + int(13 * scale)), fill=outline)

    # Smile
    smile_y = y + int(85 * scale)
    draw.arc((x + int(38 * scale), smile_y, x + int(92 * scale), smile_y + int(40 * scale)),
             start=10, end=170, fill=outline, width=3)

    # Body (suit)
    body_x1 = x - int(18 * scale)
    body_y1 = y + 2 * head_r - int(5 * scale)
    body_x2 = body_x1 + body_w
    body_y2 = body_y1 + body_h
    draw.rounded_rectangle((body_x1, body_y1, body_x2, body_y2), radius=int(22 * scale),
                           fill=suit, outline=outline, width=3)

    # Shirt triangle
    draw.polygon([
        (x + int(25 * scale), body_y1 + int(10 * scale)),
        (x + int(55 * scale), body_y1 + int(10 * scale)),
        (x + int(40 * scale), body_y1 + int(70 * scale)),
    ], fill=shirt)

    # Tie
    draw.polygon([
        (x + int(40 * scale), body_y1 + int(25 * scale)),
        (x + int(52 * scale), body_y1 + int(50 * scale)),
        (x + int(40 * scale), body_y1 + int(75 * scale)),
        (x + int(28 * scale), body_y1 + int(50 * scale)),
    ], fill=tie)

    # Little mic
    mic_x = body_x2 - int(30 * scale)
    mic_y = body_y1 + int(60 * scale)
    draw.ellipse((mic_x, mic_y, mic_x + int(18 * scale), mic_y + int(18 * scale)), fill=(90, 90, 90), outline=outline)
    draw.line((mic_x + int(9 * scale), mic_y + int(18 * scale),
               mic_x + int(9 * scale), mic_y + int(45 * scale)), fill=outline, width=3)


def _render_slide(
    title: str,
    body_lines: list[str],
    bg: Image.Image,
    source: str = "News",
    show_character: bool = True
) -> np.ndarray:
    img = bg.copy().convert("RGB")
    draw = ImageDraw.Draw(img)

    # Dark overlay panel for readability
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(panel)
    pdraw.rounded_rectangle(
        (60, 70, W - 60, H - 70),
        radius=32,
        fill=(0, 0, 0, 150),
        outline=(255, 255, 255, 35),
        width=2
    )
    img = Image.alpha_composite(img.convert("RGBA"), panel).convert("RGB")
    draw = ImageDraw.Draw(img)

    title_font = _get_font(60, bold=True)
    body_font = _get_font(42, bold=False)
    src_font = _get_font(30, bold=True)

    # Layout: reserve right area for character
    left_x = 100
    right_reserved = 330 if show_character else 60
    max_text_width = W - left_x - right_reserved

    # Title
    draw.text((left_x, 110), title, font=title_font, fill=(255, 255, 255))

    # Source label (top-right)
    source_text = f"Source: {source}"
    draw.text((W - 520, 125), source_text, font=src_font, fill=(220, 220, 220))

    # Body bullets (wrapped)
    y = 215
    for line in body_lines:
        line = (line or "").strip()
        if not line:
            continue

        wrapped = textwrap.wrap(line, width=44)  # approximate; panel + fonts vary
        for i, wline in enumerate(wrapped[:2]):  # keep it neat
            prefix = "• " if i == 0 else "  "
            draw.text((left_x, y), f"{prefix}{wline}", font=body_font, fill=(245, 245, 245))
            y += 58
        y += 10
        if y > H - 160:
            break

    # Cute character on right
    if show_character:
        # Position the anchor to the right within the panel
        char_x = W - 280
        char_y = 230
        _draw_cute_anchor(draw, char_x, char_y, scale=1.05)

        # Speech bubble small
        bubble_x1, bubble_y1 = W - 520, 210
        bubble_x2, bubble_y2 = W - 290, 310
        draw.rounded_rectangle((bubble_x1, bubble_y1, bubble_x2, bubble_y2),
                               radius=18, fill=(255, 255, 255, 235), outline=(30, 30, 30), width=2)
        draw.polygon([(bubble_x2, bubble_y1 + 55), (bubble_x2 + 25, bubble_y1 + 75), (bubble_x2, bubble_y1 + 95)],
                     fill=(255, 255, 255, 235), outline=None)
        bubble_font = _get_font(26, bold=True)
        draw.text((bubble_x1 + 18, bubble_y1 + 22), "Quick update!", font=bubble_font, fill=(10, 10, 10))

    return np.array(img)


def create_video(script_text: str, news: dict = None, total_duration_sec: int = 45, fps: int = 24) -> str:
    os.makedirs("output", exist_ok=True)
    out_path = os.path.join("output", "news_video.mp4")

    source = "News"
    headline = ""
    image_url = ""
    if news and isinstance(news, dict):
        source = news.get("source") or source
        headline = news.get("title") or ""
        image_url = news.get("image_url") or ""

    # Extract sentences, build bullet list, dedupe
    sentences = _chunk_script(script_text)
    if not sentences:
        sentences = [headline] if headline else ["Breaking News.", "Stay tuned for more updates."]

    # Prefer headline as first bullet if present
    bullets = []
    if headline:
        bullets.append(headline.strip())

    # Add more bullets from script sentences excluding near-duplicates
    for s in sentences:
        s = (s or "").strip()
        if not s:
            continue
        bullets.append(s)

    bullets = _dedupe_lines(bullets)

    # Keep it short and readable
    bullets = bullets[:4] if len(bullets) > 4 else bullets
    if not bullets:
        bullets = ["Latest update", "Key details", "More updates soon"]

    outro = "For more updates, stay tuned."

    # Topic-based background: use article OG image first, else keyword search
    article_img = _fetch_image_from_url(image_url) if image_url else None

    # Build clips
    clips = []

    # Slide 1: headline
    bg1 = article_img if article_img is not None else _fetch_bg_image(bullets[0])
    frame1 = _render_slide("Breaking News", [bullets[0]], bg1, source=source, show_character=True)
    c1 = ImageClip(frame1).set_duration(6)
    c1 = c1.fx(vfx.resize, lambda t: 1.0 + 0.03 * t).fx(vfx.fadein, 0.6).fx(vfx.fadeout, 0.6)
    clips.append(c1)

    # Slide 2: key points (avoid repeating headline if possible)
    key_points = bullets[1:4] if len(bullets) > 1 else bullets[:2]
    key_points = _dedupe_lines(key_points)
    if not key_points:
        key_points = [bullets[0]]

    topic_query = " ".join(key_points[:2])
    bg2 = article_img if article_img is not None else _fetch_bg_image(topic_query)
    frame2 = _render_slide("Key Points", key_points[:3], bg2, source=source, show_character=True)
    c2 = ImageClip(frame2).set_duration(10).fx(vfx.fadein, 0.6).fx(vfx.fadeout, 0.6)
    c2 = c2.fx(vfx.resize, lambda t: 1.02 + 0.02 * t)
    clips.append(c2)

    # Slide 3: outro
    bg3 = _fetch_bg_image(f"{source} news update")
    frame3 = _render_slide("That’s it!", [outro], bg3, source=source, show_character=True)
    c3 = ImageClip(frame3).set_duration(6).fx(vfx.fadein, 0.6).fx(vfx.fadeout, 0.8)
    clips.append(c3)

    # Adjust total duration by extending middle slide
    base = sum(c.duration for c in clips)
    if base < total_duration_sec:
        extra = total_duration_sec - base
        clips[1] = clips[1].set_duration(clips[1].duration + extra)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(out_path, fps=fps, codec="libx264", audio=False)

    return out_path
