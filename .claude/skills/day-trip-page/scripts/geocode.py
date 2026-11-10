"""用 OpenStreetMap Nominatim 查地點座標（每次查詢間隔 1 秒，遵守使用政策）。

用法：
    python3 geocode.py "明治神宮" "竹下通" "SHIBUYA SKY" [--country jp] [--limit 3]

當地語言的名稱（日文、韓文…）通常比中文準。輸出每個候選的 lat,lng、類型和完整地址，
請挑「類型和地址都對」的那一個；街道（pedestrian/residential）回傳的是其中一點，可再用
`--polygon` 看整條街的頭尾，把站點放在你要的那一端。
"""
import argparse
import json
import time
import urllib.parse
import urllib.request

UA = "DayTripPagePlanner/1.0 (personal trip page)"


def search(q, country, limit, polygon):
    params = {"format": "json", "limit": limit, "q": q}
    if country:
        params["countrycodes"] = country
    if polygon:
        params["polygon_geojson"] = 1
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="+")
    ap.add_argument("--country", default="")
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--polygon", action="store_true", help="also print the first/last point of a street")
    a = ap.parse_args()
    for i, q in enumerate(a.names):
        if i:
            time.sleep(1.1)
        print("==", q)
        res = None
        for attempt in range(4):  # 429 = too many requests: wait and retry
            try:
                res = search(q, a.country, a.limit, a.polygon)
                break
            except Exception as e:
                err = e
                time.sleep(3 * (attempt + 1))
        if res is None:
            print("   error:", err)
            continue
        if not res:
            print("   (no result — try the local-language name)")
        for r in res:
            print(f"   {float(r['lat']):.5f}, {float(r['lon']):.5f}  {r.get('type')}  {r['display_name'][:100]}")
            g = r.get("geojson")
            if a.polygon and g and g.get("type") == "LineString":
                c = g["coordinates"]
                print(f"      street from {c[0][1]:.5f},{c[0][0]:.5f} to {c[-1][1]:.5f},{c[-1][0]:.5f}")


if __name__ == "__main__":
    main()
