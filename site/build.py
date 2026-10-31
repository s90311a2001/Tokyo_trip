"""Build the single-page mobile guide from guide/*.md.

Usage: python3 site/build.py [--fragment OUT]
  Writes site/index.html (standalone page). With --fragment, also writes a
  version without the doctype/html/head wrapper for publishing as an artifact.
"""
import html
import re
import sys
from pathlib import Path

from mdlib import ROMAJI, ROOT, SHORT, load_chapters

TEMPLATE = Path(__file__).resolve().parent / "template.html"


def render_chapter(num, title, out):
    # Wide tables scroll inside their own box.
    out = out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    # Warning marker becomes a chip.
    out = out.replace("⚠️", '<span class="warn" title="出發前再確認">確認</span>')
    # Checklist items become persistent checkboxes.
    counter = iter(range(1000))
    out = re.sub(
        r"<li>\[ \]\s*",
        lambda m: f'<li class="chk"><input type="checkbox" id="chk-{num}-{next(counter)}"> ',
        out,
    )
    # Wrap each h2 and its following content in a collapsible block.
    parts = re.split(r"(?=<h2>)", out)
    head, subs = parts[0], parts[1:]
    blocks = [head]
    for i, s in enumerate(subs):
        m = re.match(r"<h2>(.*?)</h2>(.*)", s, re.S)
        blocks.append(
            f'<details class="sub" open id="ch{num}-{i}"><summary><h3>{m.group(1)}</h3></summary>'
            f'<div class="subbody">{m.group(2)}</div></details>'
        )
    return num, title, "\n".join(blocks)


def build():
    chapters = [render_chapter(*c) for c in load_chapters()]
    nav = "\n".join(
        f'<a class="stop" href="#ch{n}"><span class="code">TK{n}</span><span class="nm">{SHORT[n]}</span></a>'
        for n, _, _ in chapters
    )
    secs = []
    for i, (n, title, body) in enumerate(chapters):
        prev_link = (
            f'<a href="#ch{chapters[i-1][0]}">← {SHORT[chapters[i-1][0]]}</a>' if i > 0 else "<span></span>"
        )
        next_link = (
            f'<a href="#ch{chapters[i+1][0]}">{SHORT[chapters[i+1][0]]} →</a>'
            if i < len(chapters) - 1 else "<span></span>"
        )
        secs.append(
            f'<section class="chapter" id="ch{n}">'
            f'<header class="sign"><div class="sign-top"><span class="num">TK<b>{n}</b></span>'
            f'<div class="sign-name"><h2>{html.escape(title)}</h2><p class="romaji">{ROMAJI[n]}</p></div></div>'
            f'<div class="sign-line"></div><nav class="sign-adj">{prev_link}{next_link}</nav></header>'
            f'<div class="chbody">{body}</div></section>'
        )
    page = TEMPLATE.read_text(encoding="utf-8").replace("{{NAV}}", nav).replace("{{CHAPTERS}}", "\n".join(secs))
    standalone = (
        '<!doctype html>\n<html lang="zh-Hant"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
        "</head><body>\n" + page + "\n</body></html>\n"
    )
    (ROOT / "site" / "index.html").write_text(standalone, encoding="utf-8")
    if "--fragment" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--fragment") + 1])
        out.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    build()
