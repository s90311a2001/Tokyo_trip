"""Build the flip-book magazine from guide/*.md.

Usage: python3 magazine/build.py [--fragment OUT]
  Writes magazine/index.html. With --fragment, also writes a version without the
  doctype/html/head wrapper for publishing as an artifact (photos/ is published
  alongside it).
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "site"))

import art  # noqa: E402
from mdlib import ROMAJI, SHORT, load_chapters  # noqa: E402

PHOTOS = HERE / "photos"

# Illustration placed right after the H2 whose text starts with the key.
ART_AFTER = {
    ("00", "行程總覽"): "timeline",
    ("00", "年末年始營業日曆"): "calendar",
    ("01", "退稅新制"): "taxfree",
    ("01", "天氣與穿搭"): "outfit",
    ("02", "回程 1/2"): "arrival",
    ("03", "先講結論"): "staymap",
    ("05", "沿線站序與景點"): "enoden",
    ("05", "江之島景點詳解"): "enoshima",
    ("06", "12/31 跨年怎麼過"): "nye",
    ("06", "1/1 元旦"): "hatsumode",
    ("07", "東京吃飯的基本規則"): "food",
    ("08", "動漫・遊戲・角色商店"): "animemap",
    ("09", "夜景排行"): "heights",
    ("10", "一眼比較"): "daytrips",
    ("12", "兩人預算表"): "budget",
}

# Photo used as the big picture on each chapter's opening page.
HERO = {
    "00": "tokyo-station", "01": "narita-skyliner", "02": "enoden-train", "03": "toden-arakawa",
    "04": "shibuya-crossing", "05": "enoshima-island", "06": "hatsumode", "07": "sushi",
    "08": "ginza", "09": "tokyo-tower", "10": "chureito", "11": "tokyo-night", "12": "temizuya",
}

WASHI = ["sakura", "matcha", "sora", "yuzu"]


def load_credits():
    path = PHOTOS / "credits.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def photo_html(entry, credits, cls="photo"):
    pid = entry["id"]
    cap = html.escape(entry["caption"])
    c = credits.get(pid)
    if c:
        credit = html.escape(f'{c["author"]}／{c["license"]}')
        return (
            f'<figure class="{cls}" data-photo="{pid}"><img src="photos/{c["file"]}" alt="{cap}" loading="lazy">'
            f'<figcaption><span>{cap}</span><small>{credit}</small></figcaption></figure>'
        )
    return (
        f'<figure class="{cls} pending" data-photo="{pid}"><div class="ph">{art.sticker("camera", 64)}'
        f"<span>照片準備中</span></div><figcaption><span>{cap}</span></figcaption></figure>"
    )


def art_html(key):
    return f'<figure class="artfig" data-art="{key}">{art.ARTS[key]()}</figure>'


def decorate(num, body, photos, credits):
    """Insert illustrations and photos after their headings, and restyle markers."""
    body = body.replace("⚠️", '<span class="stamp" title="出發前再確認">確認</span>')
    body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    body = re.sub(r'href="#ch(\d\d)"', r'href="#ch\1" data-goto="ch\1"', body)
    body = re.sub(r"<li>\[ \]\s*", '<li class="todo"><span class="box"></span>', body)

    def after_heading(m):
        heading = re.sub(r"<[^>]+>", "", m.group(2))
        extra = []
        for (ch, prefix), key in ART_AFTER.items():
            if ch == num and heading.startswith(prefix):
                extra.append(art_html(key))
        for p in photos:
            if p["chapter"] == num and p["id"] != HERO.get(num) and heading == p["after"]:
                extra.append(photo_html(p, credits))
        return m.group(0) + "".join(extra)

    body = re.sub(r"<h([23])>(.*?)</h\1>", after_heading, body)
    # The first blockquote is the chapter's lead; it moves to the opening page.
    lead = ""
    m = re.match(r"\s*(<blockquote>.*?</blockquote>)", body, re.S)
    if m:
        lead, body = m.group(1), body[m.end():]
    return lead, body


def build():
    photos = json.loads((HERE / "photos.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in photos}
    credits = load_credits()
    chapters = []
    for i, (num, title, body) in enumerate(load_chapters()):
        lead, body = decorate(num, body, photos, credits)
        hero = by_id.get(HERO.get(num))
        hero_html = photo_html(hero, credits, "hero") if hero else ""
        chapters.append(
            f'<template class="chapter" data-ch="{num}" data-short="{SHORT[num]}" '
            f'data-washi="{WASHI[i % len(WASHI)]}">'
            f'<div class="meta"><h1>{html.escape(title)}</h1><p class="romaji">{ROMAJI[num]}</p>'
            f'<div class="lead">{lead}</div><div class="hero-src">{hero_html}</div>'
            f'<div class="sticker-src">{art.sticker(art.CHAPTER_STICKER[num], 88)}</div></div>'
            f'<div class="flowsrc">{body}</div></template>'
        )
    credit_rows = "".join(
        f'<li><b>{html.escape(by_id[pid]["caption"]) if pid in by_id else pid}</b>：'
        f'{html.escape(c["author"])}，{html.escape(c["license"])}，'
        f'<a href="{html.escape(c["source"])}" target="_blank" rel="noopener">來源</a></li>'
        for pid, c in credits.items()
    ) or "<li>照片整理中，完成後這裡會列出每張照片的作者與授權。</li>"
    page = (
        (HERE / "template.html").read_text(encoding="utf-8")
        .replace("{{COVER}}", art.cover())
        .replace("{{CHAPTERS}}", "\n".join(chapters))
        .replace("{{CREDITS}}", credit_rows)
        .replace("{{STICKERS}}", "".join(
            f'<template data-sticker="{n}">{art.sticker(s, 30)}</template>'
            for n, s in art.CHAPTER_STICKER.items()))
    )
    standalone = (
        '<!doctype html>\n<html lang="zh-Hant"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
        "</head><body>\n" + page + "\n</body></html>\n"
    )
    (HERE / "index.html").write_text(standalone, encoding="utf-8")
    if "--fragment" in sys.argv:
        Path(sys.argv[sys.argv.index("--fragment") + 1]).write_text(page, encoding="utf-8")


if __name__ == "__main__":
    build()
