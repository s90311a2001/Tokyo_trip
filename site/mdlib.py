"""Shared Markdown loading for the guide web page and the magazine."""
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
GUIDE = ROOT / "guide"

# Short chapter names and romanized subtitles used by both outputs.
SHORT = {
    "00": "速覽", "01": "行前準備", "02": "交通", "03": "住宿", "04": "東京分區",
    "05": "鎌倉・江之島", "06": "年末年始", "07": "美食", "08": "購物",
    "09": "約會・拍照", "10": "一日遊", "11": "行程表", "12": "預算・避雷",
}
ROMAJI = {
    "00": "Overview", "01": "Junbi", "02": "Kōtsū", "03": "Shukuhaku", "04": "Tōkyō",
    "05": "Kamakura・Enoshima", "06": "Nenmatsu Nenshi", "07": "Gurume", "08": "Kaimono",
    "09": "Dēto", "10": "Higaeri", "11": "Nittei", "12": "Yosan",
}


def load_chapters():
    """Return [(num, title, html)] for guide/NN-*.md, title taken from the H1."""
    chapters = []
    for path in sorted(GUIDE.glob("[0-9][0-9]-*.md")):
        text = path.read_text(encoding="utf-8")
        first, _, body = text.partition("\n")
        title = re.sub(r"^#\s*\d+\.\s*", "", first).strip()
        md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
        chapters.append((path.name[:2], title, md.convert(body)))
    return chapters
