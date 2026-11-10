"""下載已選好的 Unsplash 照片到 photos/auto/，並寫 photos/credits.txt。

用法：
    python3 download_photos.py PROJECT_DIR photos.json

photos.json 是一個清單，每張照片一筆：
    [{"file": "01-meiji-jingu.jpg",              存成的檔名（photos/auto/ 底下）
      "id": "1758557901510-d9091ddd9ea6",         images.unsplash.com/photo-<id> 的那一段
      "by": "Lex Brogan",                         攝影者
      "page": "https://unsplash.com/photos/...",  照片頁網址
      "desc": "明治神宮 森林中的大鳥居",            一句說明
      "sample": false}]                           true = 示意圖（不是那個地點本身）

- 照片縮成最寬 1280px（JPEG q80）。原圖小於 1080px 寬會警告。
- credits.txt 會依 photos.json 全部重寫（舊的內容會被取代）。
"""
import io
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

from PIL import Image

UA = "DayTripPagePlanner/1.0 (personal trip page)"


def main():
    proj, spec = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    out = proj / "photos" / "auto"
    out.mkdir(parents=True, exist_ok=True)
    lines = [f"照片來源（{date.today().isoformat()} 下載；Unsplash License：https://unsplash.com/license）",
             "頁面會先用 photos/<站名>.jpg、<站名>-2.jpg…（你自己的照片），再用下面這些。", ""]
    for p in spec:
        url = f"https://images.unsplash.com/photo-{p['id']}?fm=jpg&q=90&w=1400&fit=max"
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except Exception as e:
            print(f"✗ {p['file']}: {e}")
            continue
        im = Image.open(io.BytesIO(data)).convert("RGB")
        if im.width < 1080:
            print(f"! {p['file']}: only {im.width}px wide")
        if im.width > 1280:
            im = im.resize((1280, round(im.height * 1280 / im.width)), Image.LANCZOS)
        im.save(out / p["file"], "JPEG", quality=80, optimize=True, progressive=True)
        print(f"✓ {p['file']} {im.size}")
        tag = "【示意】" if p.get("sample") else ""
        lines += [f"{p['file']}  {p.get('desc', '')}{tag}", f"  作者：{p.get('by', '')}（Unsplash）", f"  來源：{p.get('page', '')}", ""]
    (proj / "photos" / "credits.txt").write_text("\n".join(lines), encoding="utf-8")
    print("wrote", proj / "photos" / "credits.txt")


if __name__ == "__main__":
    main()
