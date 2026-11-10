"""依真實路網計算每一段的步行路線，寫回 itinerary.js 的 walk / path。

用法：
    python3 make_routes.py PROJECT_DIR/itinerary.js [--force]

- 用 OSRM 步行路線（routing.openstreetmap.de, foot profile，OSM 資料）。
- 某站想指定「經過哪裡」（例如先走到街口再進去），在那一站加 "via": [[lat,lng], ...]。
- 已經有 path 的站會略過，除非加 --force。
- itinerary.js 必須是 `window.TRIP = {JSON};` 的形式（new_day.py 產生的就是）。
"""
import json
import math
import re
import sys
import time
import urllib.request
from pathlib import Path

UA = "DayTripPagePlanner/1.0 (personal trip page)"
OSRM = "https://routing.openstreetmap.de/routed-foot/route/v1/foot/"


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    den = math.hypot(x2 - x1, y2 - y1) or 1e-12
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i]
        d = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / den
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return rdp(pts[: idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


def load(path):
    txt = Path(path).read_text(encoding="utf-8")
    head, rest = txt.split("window.TRIP =", 1)
    return head, json.loads(rest.strip().rstrip(";"))


def dump(path, head, trip):
    txt = json.dumps(trip, ensure_ascii=False, indent=2)
    txt = re.sub(r"\[\s+(-?[\d.]+),\s+(-?[\d.]+)\s+\]", r"[\1, \2]", txt)  # [lat, lng] on one line
    txt = re.sub(r'"path": \[\s+(.*?)\s+\]\n', lambda m: '"path": [' + re.sub(r"\s+", "", m.group(1)) + "]\n", txt, flags=re.S)
    Path(path).write_text(head + "window.TRIP = " + txt + ";\n", encoding="utf-8")


def main():
    path = sys.argv[1]
    force = "--force" in sys.argv
    head, trip = load(path)
    stops = trip["stops"]
    for i in range(1, len(stops)):
        s, prev = stops[i], stops[i - 1]
        if s.get("path") and not force:
            continue
        wps = [prev["coords"]] + s.get("via", []) + [s["coords"]]
        url = OSRM + ";".join(f"{lng},{lat}" for lat, lng in wps) + "?overview=full&geometries=geojson"
        r = None
        for attempt in range(4):  # the public server sometimes resets connections; retry with backoff
            try:
                r = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30))["routes"][0]
                break
            except Exception as e:
                err = e
                time.sleep(2 ** (attempt + 1))
        if r is None:  # keep going; the page draws a straight line when path is missing
            print(f"✗ {prev['name']} → {s['name']}: {err}  (run again later)")
            continue
        pts = rdp(r["geometry"]["coordinates"], 0.00004)
        s["walk"] = {"m": round(r["distance"]), "min": max(1, round(r["duration"] / 60))}
        s["path"] = [[round(b, 5), round(a, 5)] for a, b in pts]
        print(f"✓ {prev['name']} → {s['name']}: {s['walk']['m']} m, {s['walk']['min']} min, {len(pts)} points")
        time.sleep(1)
    dump(path, head, trip)


if __name__ == "__main__":
    main()
