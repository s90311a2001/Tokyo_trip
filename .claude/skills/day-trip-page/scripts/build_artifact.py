"""把一日遊資料夾整理成可以用 Artifact 工具發布的版本。

用法：
    python3 build_artifact.py PROJECT_DIR OUT_DIR

做的事：
- index.html 去掉 <!doctype>/<html>/<head>/<body> 外框和 charset/viewport meta（發布時會自動包上），<title> 移到最前面
- 複製 itinerary.js、basemap.js、basemap.jpg、photos/auto/m、photos/auto/t；
  只有缺少小尺寸版本的原圖才複製（頁面會自動退回原圖）
- 最後印出 Artifact publish 要用的 files 清單（JSON），發布時：
    file_path = OUT_DIR/index.html, root = OUT_DIR, files = 印出來的清單
"""
import json
import re
import shutil
import sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)
s = (src / "index.html").read_text(encoding="utf-8")
head = re.search(r"<head>(.*?)</head>", s, re.S).group(1)
body = re.search(r"<body>(.*)</body>", s, re.S).group(1)
head = re.sub(r'<meta charset[^>]*>\s*|<meta name="viewport"[^>]*>\s*', "", head)
title = re.search(r"<title>.*?</title>", head).group(0)
head = head.replace(title, "")
(out / "index.html").write_text(title + "\n" + head.strip() + "\n" + body.strip() + "\n", encoding="utf-8")

files = []
for f in ("itinerary.js", "basemap.js", "basemap.jpg"):
    if (src / f).exists():
        shutil.copy(src / f, out / f)
        files.append(f)
    else:
        print(f"! missing {f}", file=sys.stderr)
auto = src / "photos" / "auto"
for sub in ("m", "t"):
    if (auto / sub).exists():
        shutil.copytree(auto / sub, out / "photos" / "auto" / sub)
        files += [f"photos/auto/{sub}/{p.name}" for p in sorted((auto / sub).iterdir()) if p.is_file()]
for jpg in sorted(auto.glob("*.jpg")):
    if not (auto / "m" / (jpg.stem + ".webp")).exists():
        (out / "photos" / "auto").mkdir(parents=True, exist_ok=True)
        shutil.copy(jpg, out / "photos" / "auto" / jpg.name)
        files.append(f"photos/auto/{jpg.name}")
for mine in sorted((src / "photos").glob("*.*")):  # the user's own photos: photos/<站名>.jpg
    if mine.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
        shutil.copy(mine, out / "photos" / mine.name)
        files.append(f"photos/{mine.name}")
size = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
print(f"{len(files)} files + index.html, {size / 1e6:.1f} MB", file=sys.stderr)
if len(files) > 254:
    print("! more than 254 files: publish in two batches to the same url", file=sys.stderr)
print(json.dumps([{"path": f} for f in files], ensure_ascii=False))
