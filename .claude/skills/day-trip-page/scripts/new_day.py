"""建立一個新的一日遊頁面資料夾。

用法：
    python3 new_day.py OUT_DIR --title "澀谷散步日" --date "12/27（六）" [--en "Shibuya Winter Walk"] [--season winter]

產生：
    OUT_DIR/index.html               頁面（來自 assets/template/index.html）
    OUT_DIR/itinerary.js             行程資料骨架（填好每站後再跑 make_routes.py）
    OUT_DIR/basemap.config.json      底圖範圍與地名標籤（填好後跑 make_basemap.py）
    OUT_DIR/photos/auto/             自動下載的照片
    OUT_DIR/README.md
"""
import argparse
import json
import shutil
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TPL = SKILL / "assets" / "template"

HEADER = (TPL / "itinerary.example.js").read_text(encoding="utf-8").split("window.TRIP =")[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--title", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--en", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--season", default="", help='"winter" adds snow caps and snowflakes')
    ap.add_argument("--badge", default="", help="one character shown in the cover avatar (default: first character of the title)")
    a = ap.parse_args()

    out = Path(a.out)
    if (out / "index.html").exists():
        raise SystemExit(f"{out}/index.html already exists; not overwriting")
    (out / "photos" / "auto").mkdir(parents=True, exist_ok=True)

    html = (TPL / "index.html").read_text(encoding="utf-8").replace("__TITLE__", a.title)
    (out / "index.html").write_text(html, encoding="utf-8")

    trip = {"title": a.title, "en": a.en, "date": a.date, "subtitle": a.subtitle, "season": a.season, "badge": a.badge,
            "stops": [{
                "name": "第一站名稱", "en": "", "handle": "", "area": "",
                "period": "早上", "time": "09:00–10:30", "icon": "pin", "iconAt": [0, -58],
                "highlight": "一句話：要做什麼", "desc": ["介紹第一段", "介紹第二段"], "todo": [], "tags": [], "note": "",
                "coords": [0, 0], "maps": "", "photos": []}]}
    (out / "itinerary.js").write_text(HEADER + "window.TRIP = " + json.dumps(trip, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")

    cfg = {"area": {"s": 0, "n": 0, "w": 0, "e": 0}, "snow": a.season == "winter", "labels": []}
    (out / "basemap.config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (out / "README.md").write_text(f"""# {a.title}（{a.date}）

手繪地圖上一站一站走的一日遊頁面。雙擊 `index.html` 就能開（字型來自 Google Fonts，其餘都在資料夾裡）。

- `itinerary.js`：行程資料（欄位說明在檔案開頭）
- `basemap.js` / `basemap.jpg`：手繪底圖（向量／移動時用的預先畫好的圖）
- `photos/<站名>.jpg`、`photos/<站名>-2.jpg`…：放你自己的照片會排在輪播最前面
- `photos/auto/`：自動下載的照片（`m/`、`t/` 是小尺寸版本）；來源與授權見 `photos/credits.txt`
""", encoding="utf-8")
    print("created", out)


if __name__ == "__main__":
    main()
