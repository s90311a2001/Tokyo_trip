"""Download freely licensed photos for the magazine from Wikimedia Commons.

Run on a machine that can reach commons.wikimedia.org:
    python3 magazine/fetch_photos.py            # fetch every photo in photos.json not yet downloaded
    python3 magazine/fetch_photos.py --redo ID   # fetch ID again, taking the next candidate
    python3 magazine/fetch_photos.py --pick ID=FILE_TITLE   # use a specific Commons file

Only CC0, public-domain, CC BY and CC BY-SA files are accepted. Results go to
magazine/photos/<id>.jpg and magazine/photos/credits.json (author, license,
source page), which build.py reads to print the credits.
"""
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "photos"
API = "https://commons.wikimedia.org/w/api.php"
UA = "TokyoShonanTravelJournal/1.0 (personal travel guide; https://github.com/s90311a2001/Tokyo_trip)"
WIDTH = 1400
OK_LICENSE = re.compile(r"^(CC0|Public domain|PD|CC BY(-SA)? \d)", re.I)


def get_json(params):
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def candidates(query=None, title=None):
    params = {
        "action": "query", "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
        "iiurlwidth": WIDTH,
    }
    if title:
        params["titles"] = title if title.startswith("File:") else "File:" + title
    else:
        params.update({"generator": "search", "gsrsearch": f"{query} filetype:bitmap",
                       "gsrnamespace": 6, "gsrlimit": 20})
    pages = get_json(params).get("query", {}).get("pages", {})
    found = []
    for p in sorted(pages.values(), key=lambda p: p.get("index", 0)):
        info = (p.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        lic = plain(meta.get("LicenseShortName", {}).get("value"))
        if not OK_LICENSE.match(lic) or info.get("mime") not in ("image/jpeg", "image/png"):
            continue
        w, h = info.get("width", 0), info.get("height", 0)
        if not title and (w < 1200 or w < h * 0.9):  # prefer large, landscape-ish shots
            continue
        found.append({
            "title": p["title"], "thumb": info.get("thumburl"), "source": info.get("descriptionurl"),
            "author": plain(meta.get("Artist", {}).get("value")) or "Unknown",
            "license": lic, "size": f"{w}x{h}",
        })
    return found


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        path.write_bytes(r.read())
    try:  # optional recompression to keep the published page light
        from PIL import Image
        im = Image.open(path).convert("RGB")
        im.thumbnail((WIDTH, WIDTH))
        im.save(path, "JPEG", quality=80, optimize=True, progressive=True)
    except ImportError:
        pass


def main():
    OUT.mkdir(exist_ok=True)
    spec = json.loads((HERE / "photos.json").read_text(encoding="utf-8"))
    cred_path = OUT / "credits.json"
    credits = json.loads(cred_path.read_text(encoding="utf-8")) if cred_path.exists() else {}
    redo = set(a.split("=")[0] for a in sys.argv[2:]) if "--redo" in sys.argv else set()
    picks = dict(a.split("=", 1) for a in sys.argv[2:] if "--pick" in sys.argv and "=" in a)
    for entry in spec:
        pid = entry["id"]
        if pid in credits and pid not in redo and pid not in picks:
            continue
        try:
            if pid in picks:
                cands = candidates(title=picks[pid])
            else:
                cands = candidates(query=entry["query"])
                used = credits.get(pid, {}).get("title")
                if used:
                    cands = [c for c in cands if c["title"] != used] or cands
        except Exception as e:  # network or API error: report and move on
            print(f"✗ {pid}: {e}")
            continue
        if not cands:
            print(f"✗ {pid}: no freely licensed match for '{entry['query']}'")
            continue
        c = cands[0]
        file = f"{pid}.jpg"
        download(c["thumb"], OUT / file)
        credits[pid] = {"file": file, "title": c["title"], "author": c["author"],
                        "license": c["license"], "source": c["source"]}
        cred_path.write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ {pid}: {c['title']} ({c['license']}, {c['author']})")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
