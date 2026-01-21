import re

def _sentences(text: str):
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]

def generate_script(news: dict) -> str:
    title = news.get("title", "").strip()
    desc = news.get("description", "").strip()

    # Pick 2 short points from description without repeating title
    points = []
    for s in _sentences(desc):
        s_clean = s.replace("\u00a0", " ").strip()
        if not s_clean:
            continue
        # skip if same as title
        if title and s_clean.lower() in title.lower():
            continue
        points.append(s_clean)
        if len(points) >= 2:
            break

    # Fallback if description is weak
    if len(points) < 2 and desc:
        points = [desc[:140].strip()] if len(desc) > 0 else points

    # Return a structured script (title + bullets + outro)
    script_lines = [
        title,
        *points,
        "For more updates, stay tuned."
    ]
    return "\n".join([l for l in script_lines if l])
