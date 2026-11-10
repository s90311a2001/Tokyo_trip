"""為 photos/auto/*.jpg 產生小尺寸版本，讓手機載入更快：
    photos/auto/m/<名稱>.webp  輪播用（寬 800px）
    photos/auto/t/<名稱>.webp  頭像、清單縮圖用（寬 240px）
頁面找不到小尺寸時會自動改用原圖。

用法：python3 make_photo_sizes.py PROJECT_DIR   （需要 Pillow）
"""
import sys
from pathlib import Path

from PIL import Image

root = Path(sys.argv[1]) / "photos" / "auto"
for sub, width, q in (("m", 800, 74), ("t", 240, 70)):
    (root / sub).mkdir(exist_ok=True)
    for f in sorted(root.glob("*.jpg")):
        out = root / sub / (f.stem + ".webp")
        if out.exists() and out.stat().st_mtime >= f.stat().st_mtime:
            continue
        im = Image.open(f).convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(out, "WEBP", quality=q, method=6)
        print(out.relative_to(root), im.size, out.stat().st_size // 1024, "KB")
