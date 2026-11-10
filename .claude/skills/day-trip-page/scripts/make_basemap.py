"""手繪風格底圖產生器：OpenStreetMap 資料 → basemap.js（一段 SVG，頁面直接內嵌，不需要線上地圖服務）。

用法（CONFIG 是 basemap.config.json，格式見 references/data-format.md）：
    python3 make_basemap.py fetch CONFIG DATA_DIR            下載範圍內的 OSM 資料（分 3x3 塊，OSM API）
    python3 make_basemap.py names CONFIG DATA_DIR            列出範圍內的主要路名、車站，方便寫 labels
    python3 make_basemap.py build CONFIG DATA_DIR OUT.js     產生 basemap.js

地圖資料 © OpenStreetMap contributors (ODbL)。
"""
import glob
import json
import math
import os
import random
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------- config
if len(sys.argv) < 4:
    print(__doc__); sys.exit(1)
CFG = json.load(open(sys.argv[2], encoding="utf-8"))
AREA = dict(width=1000, **CFG["area"])
# label: [中文, English, lat, lng, kind("area"|"road"|"station")(, OSM road name to align with)]
LABELS = [tuple(l) for l in CFG.get("labels", [])]
SNOW = bool(CFG.get("snow", False))

INK = "#5a4632"
PAPER = "#f7efdc"

# ---------------------------------------------------------------- fetch
UA = "TokyoTripPlanner/1.0 (personal trip page; https://github.com/s90311a2001/Tokyo_trip)"


def fetch(out):
    os.makedirs(out, exist_ok=True)
    nx, ny = 3, 3
    dx = (AREA["e"] - AREA["w"]) / nx
    dy = (AREA["n"] - AREA["s"]) / ny
    for i in range(ny):
        for j in range(nx):
            f = f"{out}/c_{i}_{j}.xml"
            if os.path.exists(f) and os.path.getsize(f) > 0:
                continue
            bb = f"{AREA['w']+j*dx:.5f},{AREA['s']+i*dy:.5f},{AREA['w']+(j+1)*dx:.5f},{AREA['s']+(i+1)*dy:.5f}"
            req = urllib.request.Request("https://api.openstreetmap.org/api/0.6/map?bbox=" + bb, headers={"User-Agent": UA})
            open(f, "wb").write(urllib.request.urlopen(req, timeout=180).read())
            print("fetched", f)
            time.sleep(1)


# ---------------------------------------------------------------- geometry helpers
LATM = (AREA["s"] + AREA["n"]) / 2
KX = AREA["width"] / ((AREA["e"] - AREA["w"]) * math.cos(math.radians(LATM)))
W = AREA["width"]
H = round((AREA["n"] - AREA["s"]) * KX)


def P(lat, lng):
    return ((lng - AREA["w"]) * KX * math.cos(math.radians(LATM)), (AREA["n"] - lat) * KX)


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    den = math.hypot(x2 - x1, y2 - y1) or 1e-9
    dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        x0, y0 = pts[i]
        d = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1) / den
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        return rdp(pts[: idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]


def wobble(pts, amp, step=9.0, seed=0):
    """Resample a polyline and push it sideways with smooth noise, for a hand-drawn line."""
    rnd = random.Random(seed)
    ph1, ph2 = rnd.random() * 6.28, rnd.random() * 6.28
    out, acc = [], 0.0
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L == 0:
            continue
        nx_, ny_ = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
        n = max(1, int(L / step))
        for k in range(n):
            t = k / n
            s = acc + L * t
            off = amp * (math.sin(s / 23 + ph1) * 0.6 + math.sin(s / 9 + ph2) * 0.4)
            out.append((a[0] + (b[0] - a[0]) * t + nx_ * off, a[1] + (b[1] - a[1]) * t + ny_ * off))
        acc += L
    out.append(pts[-1])
    return out


def smooth_d(pts, closed=False):
    if len(pts) < 2:
        return ""
    f = lambda p: f"{p[0]:.1f} {p[1]:.1f}"
    if len(pts) == 2:
        return f"M{f(pts[0])}L{f(pts[1])}"
    d = f"M{f(pts[0])}"
    for i in range(1, len(pts) - 1):
        m = ((pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2)
        d += f"Q{f(pts[i])} {f(m)}"
    d += f"L{f(pts[-1])}"
    return d + ("Z" if closed else "")


def inside(pt, poly):
    x, y = pt
    c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-9) + x1:
            c = not c
    return c


def area(poly):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]))) / 2


def in_view(pts, m=40):
    return any(-m <= x <= W + m and -m <= y <= H + m for x, y in pts)


# ---------------------------------------------------------------- build
def load(d):
    nodes, ways, rels, named_nodes = {}, {}, {}, {}
    for f in sorted(glob.glob(d + "/c_*.xml")):
        for _, el in ET.iterparse(f):
            if el.tag == "node":
                nodes[el.get("id")] = (float(el.get("lat")), float(el.get("lon")))
            elif el.tag == "way":
                ways[el.get("id")] = ([n.get("ref") for n in el.findall("nd")], {t.get("k"): t.get("v") for t in el.findall("tag")})
                el.clear()
            elif el.tag == "relation":
                rels[el.get("id")] = ([(m.get("type"), m.get("ref"), m.get("role")) for m in el.findall("member")], {t.get("k"): t.get("v") for t in el.findall("tag")})
                el.clear()
    return nodes, ways, rels


def build(d, out):
    nodes, ways, rels = load(d)
    pts_of = lambda nd: [P(*nodes[n]) for n in nd if n in nodes]
    rnd = random.Random(7)

    road = {"big": [], "mid": [], "minor": [], "hwy": []}
    rails, greens, waters, streams = [], [], [], []
    named = {}
    for wid, (nd, t) in ways.items():
        hw = t.get("highway")
        tunnel = t.get("tunnel") in ("yes", "culvert", "building_passage") or (t.get("layer", "0").lstrip("-").isdigit() and int(t.get("layer", "0")) < 0)
        pts = pts_of(nd)
        if len(pts) < 2 or not in_view(pts):
            continue
        if hw and not tunnel:
            if t.get("name"):
                named.setdefault(t["name"], []).append(pts)
            if hw == "motorway":
                road["hwy"].append(pts)
            elif hw in ("trunk", "primary", "trunk_link", "primary_link"):
                road["big"].append(pts)
            elif hw in ("secondary", "tertiary", "secondary_link", "tertiary_link"):
                road["mid"].append(pts)
            elif hw in ("residential", "unclassified", "pedestrian", "living_street"):
                road["minor"].append(pts)
        if t.get("railway") == "rail" and not tunnel:
            rails.append(pts)
        closed = nd[0] == nd[-1]
        if closed and (t.get("leisure") in ("park", "garden") or t.get("landuse") in ("forest", "grass", "recreation_ground")
                       or t.get("natural") in ("wood", "scrub")):
            greens.append((pts[:-1], t.get("landuse") == "forest" or t.get("natural") == "wood"))
        if closed and t.get("natural") == "water":
            waters.append(pts[:-1])
        if t.get("waterway") in ("river", "stream") and not tunnel:
            streams.append(pts)
    # multipolygon parks (e.g. 代々木公園): stitch outer members
    for rid, (mem, t) in rels.items():
        if t.get("type") == "multipolygon" and (t.get("leisure") == "park" or t.get("landuse") == "forest"):
            for typ, ref, role in mem:
                if typ == "way" and role == "outer" and ref in ways:
                    pts = pts_of(ways[ref][0])
                    if len(pts) > 3 and ways[ref][0][0] == ways[ref][0][-1]:
                        greens.append((pts[:-1], t.get("landuse") == "forest"))

    svg = []
    add = svg.append
    # paper texture blobs
    for _ in range(60):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(30, 120)
        add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#efe2c4" opacity=".35"/>')

    # greens
    gd = []
    tree_spots = []
    for i, (poly, forest) in enumerate(greens):
        poly = rdp(poly, 1.2)
        if len(poly) < 3 or area(poly) < 150:
            continue
        gd.append(smooth_d(wobble(poly + poly[:1], 1.2, 10, i), True))
        if area(poly) > 1500:
            xs, ys = [p[0] for p in poly], [p[1] for p in poly]
            step = 24 if forest else 34
            y = min(ys)
            while y < max(ys):
                x = min(xs)
                while x < max(xs):
                    q = (x + rnd.uniform(-8, 8), y + rnd.uniform(-8, 8))
                    if inside(q, poly) and 0 < q[0] < W and 0 < q[1] < H:
                        tree_spots.append(q)
                    x += step
                y += step * 0.86
    add(f'<path d="{"".join(gd)}" fill="#cfe0ad" stroke="#8fae6b" stroke-width="1.6" stroke-linejoin="round"/>')

    # water
    if waters:
        add(f'<path d="{"".join(smooth_d(wobble(p + p[:1], 1, 8, 3), True) for p in waters if len(p) > 2)}" fill="#bfe0ea" stroke="#78aec2" stroke-width="1.5"/>')
    if streams:
        sd = "".join(smooth_d(wobble(rdp(p, 1), 1, 8, 5)) for p in streams)
        add(f'<path d="{sd}" fill="none" stroke="#78aec2" stroke-width="7" stroke-linecap="round"/>')
        add(f'<path d="{sd}" fill="none" stroke="#bfe0ea" stroke-width="4" stroke-linecap="round"/>')

    def lines(key, eps, amp, seed):
        return "".join(smooth_d(wobble(rdp(p, eps), amp, 9, seed + i) if amp else rdp(p, eps)) for i, p in enumerate(road[key]))

    minor = lines("minor", 1.4, 0, 0)
    add(f'<path d="{minor}" fill="none" stroke="#e6d6b4" stroke-width="2.4" stroke-linecap="round"/>')
    mid, big, hwy = lines("mid", 1.0, 0.9, 100), lines("big", 1.0, 1.0, 300), lines("hwy", 1.0, 1.0, 500)
    for d_, cw, fw, fc in ((mid, 9, 6, "#fbf4e2"), (big, 15, 11, "#f6deb0"), (hwy, 16, 12, "#e9c88f")):
        add(f'<path d="{d_}" fill="none" stroke="#b39268" stroke-width="{cw}" stroke-linecap="round" stroke-linejoin="round"/>')
        add(f'<path d="{d_}" fill="none" stroke="{fc}" stroke-width="{fw}" stroke-linecap="round" stroke-linejoin="round"/>')

    # rails
    rd = "".join(smooth_d(wobble(rdp(p, 1), 0.7, 9, 900 + i)) for i, p in enumerate(rails))
    add(f'<path d="{rd}" fill="none" stroke="#7a6550" stroke-width="6" stroke-linecap="round"/>')
    add(f'<path d="{rd}" fill="none" stroke="#fbf4e2" stroke-width="2.6" stroke-dasharray="7 7"/>')

    # trees (sorted top→bottom so lower trees overlap upper ones)
    tree_spots.sort(key=lambda p: p[1])
    for x, y in tree_spots:
        v = rnd.choice(["t1", "t1", "t2", "t3"])
        s = rnd.uniform(0.75, 1.1)
        add(f'<use href="#{v}" transform="translate({x:.0f} {y:.0f}) scale({s:.2f})"/>')

    # labels
    def road_angle(name, x, y):
        best, ang = 1e9, 0
        for pts in named.get(name, []):
            for a, b in zip(pts, pts[1:]):
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                dd = (mx - x) ** 2 + (my - y) ** 2
                if dd < best and math.hypot(b[0] - a[0], b[1] - a[1]) > 4:
                    best = dd
                    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
                    bx, by = mx, my
        if best == 1e9:
            return x, y, 0
        if ang > 90: ang -= 180
        if ang < -90: ang += 180
        return bx, by, ang

    for lab in LABELS:
        zh, en, lat, lng, kind = lab[:5]
        x, y = P(lat, lng)
        if kind == "area":
            add(f'<g class="lb lb-area" transform="translate({x:.0f} {y:.0f})"><text class="zh" y="0">{zh}</text><text class="en" y="17">{en}</text></g>')
        elif kind == "road":
            x, y, a = road_angle(lab[5], x, y)
            add(f'<g class="lb lb-road" transform="translate({x:.0f} {y:.0f}) rotate({a:.0f})"><text class="zh" y="4">{zh}</text></g>')
        elif kind == "station":
            add(f'<g class="lb lb-sta" transform="translate({x:.0f} {y:.0f})"><rect x="-34" y="-13" width="68" height="22" rx="11"/><text class="zh" y="3">{zh}</text></g>')

    # decorations: compass + snowflakes
    add(f'<use href="#compass" transform="translate({W-70} 80)"/>')
    for _ in range(40 if SNOW else 0):
        x, y = rnd.uniform(10, W - 10), rnd.uniform(10, H - 10)
        add(f'<use href="#flake" transform="translate({x:.0f} {y:.0f}) scale({rnd.uniform(.5,1.1):.2f}) rotate({rnd.randint(0,60)})" opacity="{rnd.uniform(.35,.7):.2f}"/>')

    data = dict(w=W, h=H, area={k: AREA[k] for k in ("s", "n", "w", "e")}, kx=KX, latm=LATM, svg="".join(svg),
                attribution="地圖資料 © OpenStreetMap contributors")
    with open(out, "w", encoding="utf-8") as fp:
        fp.write("/* 自動產生：tools/make_basemap.py（地圖資料 © OpenStreetMap contributors, ODbL） */\n")
        fp.write("window.BASEMAP = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    print("wrote", out, os.path.getsize(out) // 1024, "KB;", len(tree_spots), "trees;", W, "x", H)


def names(d):
    """Print named major roads (with a point near their middle) and stations, to help write labels."""
    nodes, ways, _ = load(d)
    roads = {}
    for nd, t in ways.values():
        if t.get("highway") in ("trunk", "primary", "secondary", "tertiary", "pedestrian") and t.get("name"):
            pts = [nodes[n] for n in nd if n in nodes]
            if pts:
                roads.setdefault(t["name"], []).extend(pts)
    print("# roads: name  points  middle lat,lng")
    for n, p in sorted(roads.items(), key=lambda x: -len(x[1]))[:40]:
        m = p[len(p) // 2]
        print(f"{n}\t{len(p)}\t{m[0]:.5f},{m[1]:.5f}")
    print("# stations / named places")
    for f in sorted(glob.glob(d + "/c_*.xml")):
        for _, el in ET.iterparse(f):
            if el.tag == "node":
                t = {x.get("k"): x.get("v") for x in el.findall("tag")}
                if t.get("name") and (t.get("railway") == "station" or t.get("place") in ("neighbourhood", "quarter", "suburb")):
                    print(f"{t['name']}\t{t.get('railway') or t.get('place')}\t{float(el.get('lat')):.5f},{float(el.get('lon')):.5f}")
            if el.tag in ("node", "way", "relation"):
                el.clear()


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch(sys.argv[3])
    elif cmd == "names":
        names(sys.argv[3])
    elif cmd == "build":
        build(sys.argv[3], sys.argv[4])
    else:
        print(__doc__)
