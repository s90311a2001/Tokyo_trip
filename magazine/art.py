"""Hand-drawn watercolor illustrations for the magazine, as inline SVG strings.

Every drawing relies on three filters defined once in template.html:
  #rough  wobbles strokes so lines look drawn by hand
  #wc1..#wc3  watercolor blobs (displaced, softened edges) with different seeds
Text is never filtered so it stays legible.
"""
import math

INK = "#3B3431"
MUTED = "#8A7F77"
SAKURA = "#EBA9A7"
MATCHA = "#A9C796"
SORA = "#9CC3DE"
YUZU = "#F3CD73"
BENI = "#C9473E"
AI = "#3D5A87"
KUSA = "#6E9F5E"
PAPER = "#FBF6EC"
SNOW = "#FFFFFF"


def svg(w, h, body, label):
    return (
        f'<svg class="art" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" '
        f'xmlns="http://www.w3.org/2000/svg">{body}</svg>'
    )


def wash(cx, cy, rx, ry, color, op=0.55, n=1, rot=0):
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" opacity="{op}" '
        f'filter="url(#wc{n})" transform="rotate({rot} {cx} {cy})"/>'
    )


def rect_wash(x, y, w, h, color, op=0.5, n=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{color}" opacity="{op}" filter="url(#wc{n})"/>'


def rough(inner):
    return f'<g filter="url(#rough)" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{inner}</g>'


def t(x, y, s, size=16, anchor="start", color=INK, weight=400, cls="hand"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
        f'font-weight="{weight}" class="{cls}">{s}</text>'
    )


# ---------------------------------------------------------------- stickers

def _sticker_body(name):
    """Return drawing for a 64x64 sticker."""
    if name == "torii":
        return wash(32, 34, 26, 24, SAKURA, 0.6) + rough(
            '<path d="M10 18 Q32 12 54 18" stroke="#B23A32" stroke-width="5"/>'
            '<path d="M14 26 H50" stroke="#B23A32" stroke-width="4"/>'
            '<path d="M20 20 V54 M44 20 V54" stroke="#B23A32" stroke-width="4"/>'
        )
    if name == "tower":
        return wash(32, 36, 22, 26, SORA, 0.55) + rough(
            '<path d="M32 6 L22 56 M32 6 L42 56 M25 40 H39 M28 26 H36 M22 56 H42" stroke="#C8443A" stroke-width="3"/>'
            '<path d="M26 34 L38 46 M38 34 L26 46" stroke="#C8443A" stroke-width="1.5"/>'
        )
    if name == "fuji":
        return wash(32, 40, 28, 20, SORA, 0.6) + rough(
            f'<path d="M4 54 L26 16 Q32 12 38 16 L60 54 Z" fill="{AI}" fill-opacity=".55"/>'
            f'<path d="M20 26 L26 16 Q32 12 38 16 L44 26 L39 23 L35 28 L31 22 L26 28 Z" fill="{SNOW}"/>'
        )
    if name == "train":
        return wash(32, 36, 26, 22, MATCHA, 0.55) + rough(
            '<rect x="10" y="16" width="44" height="32" rx="7" fill="#F5EFD8"/>'
            '<path d="M10 36 H54" stroke="#3F7A3A" stroke-width="7"/>'
            '<rect x="16" y="21" width="12" height="9" rx="2"/><rect x="36" y="21" width="12" height="9" rx="2"/>'
            '<circle cx="20" cy="52" r="3"/><circle cx="44" cy="52" r="3"/>'
        )
    if name == "sushi":
        return wash(32, 38, 26, 18, YUZU, 0.5) + rough(
            '<path d="M12 40 Q12 32 22 32 H44 Q54 32 54 40 Q54 46 44 46 H22 Q12 46 12 40 Z" fill="#FFFDF6"/>'
            '<path d="M10 34 Q14 22 32 22 Q50 22 56 32 Q44 30 32 32 Q20 30 10 34 Z" fill="#F08A6C"/>'
            '<path d="M22 26 L26 32 M32 24 L36 31 M42 25 L46 31" stroke="#FFF2EA" stroke-width="2"/>'
        )
    if name == "ramen":
        return wash(32, 38, 26, 20, YUZU, 0.55) + rough(
            '<path d="M8 30 H56 Q54 54 32 54 Q10 54 8 30 Z" fill="#E9B24A"/>'
            '<path d="M14 30 Q20 24 26 30 Q32 24 38 30 Q44 24 50 30" stroke="#FFF6D8" stroke-width="2"/>'
            '<path d="M40 8 L28 36 M48 10 L34 36" stroke="#8B5A2B" stroke-width="2.5"/>'
            '<circle cx="22" cy="40" r="5" fill="#FFF6D8"/>'
        )
    if name == "camera":
        return wash(32, 36, 26, 22, SORA, 0.5) + rough(
            '<rect x="8" y="20" width="48" height="32" rx="6" fill="#F7F1E6"/>'
            '<path d="M22 20 L26 13 H38 L42 20"/><circle cx="32" cy="36" r="10"/><circle cx="32" cy="36" r="4" fill="#3B3431"/>'
        )
    if name == "bag":
        return wash(32, 38, 24, 22, SAKURA, 0.55) + rough(
            '<path d="M14 24 H50 L54 56 H10 Z" fill="#F7E1E0"/>'
            '<path d="M24 24 Q24 10 32 10 Q40 10 40 24"/>'
            '<path d="M24 34 Q32 42 40 34" stroke="#C9473E"/>'
        )
    if name == "heart":
        return wash(32, 34, 24, 22, SAKURA, 0.6) + rough(
            '<path d="M32 52 C12 38 8 28 14 20 C20 12 30 16 32 24 C34 16 44 12 50 20 C56 28 52 38 32 52 Z" fill="#E7837F"/>'
        )
    if name == "onsen":
        return wash(32, 40, 26, 18, SORA, 0.6) + rough(
            '<path d="M10 40 Q32 60 54 40"/>'
            '<path d="M22 32 Q16 24 22 18 Q28 12 22 6 M32 32 Q26 24 32 18 Q38 12 32 6 M42 32 Q36 24 42 18 Q48 12 42 6" stroke="#C9473E"/>'
        )
    if name == "coffee":
        return wash(32, 38, 24, 20, YUZU, 0.45) + rough(
            '<path d="M14 26 H46 L42 54 H18 Z" fill="#FFF8EE"/><path d="M46 32 Q56 34 52 42 Q50 46 44 46"/>'
            '<path d="M24 20 Q22 14 26 10 M32 20 Q30 14 34 10" stroke="#8A7F77"/>'
        )
    if name == "gift":
        return wash(32, 38, 26, 22, YUZU, 0.55) + rough(
            '<rect x="12" y="24" width="40" height="30" rx="3" fill="#E9584E"/>'
            '<path d="M32 24 V54 M12 36 H52" stroke="#FFF2C8" stroke-width="4"/>'
            '<path d="M32 24 Q22 10 18 18 Q16 24 32 24 Q48 24 46 18 Q42 10 32 24"/>'
        )
    if name == "star":
        pts = " ".join(
            f"{32 + (24 if i % 2 == 0 else 10) * math.sin(i * math.pi / 5):.1f},"
            f"{34 - (24 if i % 2 == 0 else 10) * math.cos(i * math.pi / 5):.1f}"
            for i in range(10)
        )
        return wash(32, 34, 22, 22, YUZU, 0.55) + rough(f'<polygon points="{pts}" fill="#F3CD73"/>')
    if name == "wave":
        return wash(32, 38, 28, 18, SORA, 0.6) + rough(
            '<path d="M6 36 Q14 26 22 36 T38 36 T54 36" stroke="#3D5A87" stroke-width="3"/>'
            '<path d="M6 46 Q14 36 22 46 T38 46 T54 46" stroke="#3D5A87"/>'
        )
    if name == "niku":
        return wash(32, 38, 26, 20, SAKURA, 0.5) + rough(
            '<path d="M8 44 H56 M8 50 H56" stroke="#5B514C"/>'
            '<path d="M12 40 Q14 24 30 26 Q40 22 50 30 Q56 38 46 42 Z" fill="#D9675F"/>'
            '<path d="M20 32 Q30 30 40 34 M24 38 Q32 36 42 38" stroke="#FBE3DC" stroke-width="2"/>'
        )
    if name == "nabe":
        return wash(32, 40, 26, 18, YUZU, 0.5) + rough(
            '<path d="M8 32 H56 Q56 54 32 54 Q8 54 8 32 Z" fill="#5B514C" fill-opacity=".85"/>'
            '<path d="M14 32 Q22 26 30 32 Q38 26 46 32" stroke="#F4C2A8" stroke-width="3"/>'
            '<path d="M24 22 Q20 16 24 10 M34 22 Q30 16 34 10 M44 22 Q40 16 44 10" stroke="#8A7F77"/>'
        )
    if name == "food":
        return _sticker_body("sushi")
    if name == "yen":
        return wash(32, 34, 24, 24, MATCHA, 0.55) + rough(
            '<circle cx="32" cy="34" r="20" fill="#FFF8E6"/>'
            '<path d="M24 22 L32 34 L40 22 M32 34 V48 M25 36 H39 M25 42 H39"/>'
        )
    raise KeyError(name)


def sticker(name, size=56):
    return (
        f'<svg class="sticker" width="{size}" height="{size}" viewBox="0 0 64 64" aria-hidden="true" '
        f'xmlns="http://www.w3.org/2000/svg">{_sticker_body(name)}</svg>'
    )


CHAPTER_STICKER = {
    "00": "star", "01": "bag", "02": "train", "03": "onsen", "04": "tower", "05": "wave",
    "06": "torii", "07": "ramen", "08": "gift", "09": "heart", "10": "fuji", "11": "camera",
    "12": "yen",
}

# ---------------------------------------------------------------- cover


def cover():
    w, h = 560, 790
    b = []
    b.append(f'<rect width="{w}" height="{h}" fill="{PAPER}"/>')
    b.append(wash(280, 120, 330, 170, SORA, 0.45, 1))
    b.append(wash(420, 210, 160, 90, SAKURA, 0.35, 2))
    b.append(wash(120, 640, 260, 110, SORA, 0.55, 3))
    b.append(wash(460, 700, 200, 90, MATCHA, 0.35, 1))
    # Mt Fuji
    b.append(rough(
        f'<path d="M-10 520 L170 300 Q190 284 210 300 L390 520 Z" fill="{AI}" fill-opacity=".45"/>'
        f'<path d="M128 352 L170 300 Q190 284 210 300 L252 352 L232 340 L216 360 L198 338 L180 362 L160 340 Z" fill="{SNOW}"/>'
    ))
    # Tokyo Tower
    tower = (
        '<path d="M430 140 L398 560 M430 140 L462 560" stroke="#C8443A" stroke-width="4"/>'
        '<path d="M404 470 H456 M412 360 H448 M418 270 H442 M424 200 H436" stroke="#C8443A" stroke-width="5"/>'
        '<path d="M404 470 L448 360 M456 470 L412 360 M412 360 L442 270 M448 360 L418 270" stroke="#C8443A" stroke-width="1.6"/>'
        '<path d="M398 560 Q430 520 462 560" stroke="#C8443A" stroke-width="3"/>'
        '<path d="M430 140 V112" stroke="#C8443A" stroke-width="3"/>'
    )
    b.append(rough(tower))
    # torii on a small hill
    b.append(wash(110, 548, 120, 40, MATCHA, 0.6, 2))
    b.append(rough(
        '<path d="M60 500 Q100 490 140 500" stroke="#B23A32" stroke-width="7"/>'
        '<path d="M68 514 H132" stroke="#B23A32" stroke-width="5"/>'
        '<path d="M78 502 V556 M122 502 V556" stroke="#B23A32" stroke-width="6"/>'
    ))
    # sea
    b.append(rough(
        f'<path d="M0 600 Q35 586 70 600 T140 600 T210 600 T280 600 T350 600 T420 600 T490 600 T560 600" stroke="{AI}" stroke-width="2.5"/>'
        f'<path d="M0 630 Q35 616 70 630 T140 630 T210 630 T280 630 T350 630 T420 630 T490 630 T560 630" stroke="{AI}" stroke-width="1.6"/>'
    ))
    # Enoden train
    train = (
        '<rect x="250" y="640" width="250" height="70" rx="14" fill="#F6EED3"/>'
        '<path d="M250 684 H500" stroke="#3F7A3A" stroke-width="16"/>'
        '<rect x="268" y="652" width="40" height="24" rx="4" fill="#DCEBF3"/>'
        '<rect x="322" y="652" width="40" height="24" rx="4" fill="#DCEBF3"/>'
        '<rect x="376" y="652" width="40" height="24" rx="4" fill="#DCEBF3"/>'
        '<rect x="430" y="652" width="52" height="24" rx="4" fill="#DCEBF3"/>'
        '<circle cx="290" cy="716" r="9" fill="#5B514C"/><circle cx="460" cy="716" r="9" fill="#5B514C"/>'
        '<path d="M230 728 H540" stroke-width="3"/>'
    )
    b.append(rough(train))
    # snow dots
    for i in range(26):
        x = (i * 97) % 540 + 10
        y = (i * 53) % 260 + 30
        b.append(f'<circle cx="{x}" cy="{y}" r="{2 + i % 3}" fill="{SNOW}" opacity=".9"/>')
    return svg(w, h, "".join(b), "封面插畫：富士山、東京鐵塔、鳥居與江之電")


# ---------------------------------------------------------------- chapter 0

DAYS = [
    ("12/25", "五", "抵達・丸之內燈飾", "上野", "star"),
    ("12/26", "六", "淺草和服・晴空塔", "上野", "tower"),
    ("12/27", "日", "原宿・澀谷 SKY 夕陽", "上野", "camera"),
    ("12/28", "一", "鎌倉・江之電・燈飾", "江之島", "train"),
    ("12/29", "二", "江之島 → 新宿夜景", "上野", "wave"),
    ("12/30", "三", "teamLab・台場・銀座", "上野", "heart"),
    ("12/31", "四", "秋葉原・麻布台・鐵塔跨年", "上野", "torii"),
    ("1/1", "五", "初詣・福袋・夜景", "上野", "gift"),
    ("1/2", "六", "初賣或參賀 → 回國", "✈", "fuji"),
]


def timeline():
    w, row = 480, 62
    h = row * len(DAYS) + 30
    b = [wash(70, h / 2, 60, h / 2 - 10, SAKURA, 0.25, 2)]
    b.append(rough(f'<path d="M70 24 V{h - 24}" stroke-dasharray="6 7" stroke="{MUTED}"/>'))
    for i, (d, wd, theme, stay, icon) in enumerate(DAYS):
        y = 30 + i * row
        color = MATCHA if stay == "江之島" else (SORA if stay == "✈" else YUZU)
        b.append(wash(70, y + 8, 24, 20, color, 0.75, 1 + i % 3))
        b.append(t(70, y + 14, f"D{i + 1}", 16, "middle", INK, 700, "latin"))
        b.append(t(108, y + 6, f"{d}（{wd}）", 14, "start", MUTED, 400, "latin"))
        b.append(t(108, y + 28, theme, 19, "start", INK, 700))
        b.append(t(470, y + 28, f"住 {stay}" if stay != "✈" else "回國 ✈", 13, "end", MUTED))
        b.append(f'<g transform="translate(6 {y - 10}) scale(.5)">{_sticker_body(icon)}</g>')
    return svg(w, h, "".join(b), "九天行程手繪時間軸")


CAL = [
    ("12/25", "五", "正常", MATCHA, "聖誕燈飾最後一晚"),
    ("12/26", "六", "正常", MATCHA, "美術館最後機會"),
    ("12/27", "日", "正常", MATCHA, "小店照常"),
    ("12/28", "一", "正常", MATCHA, "年末市集開始"),
    ("12/29", "二", "部分休", YUZU, "公家機關、部分館休"),
    ("12/30", "三", "部分休", YUZU, "市場、小店陸續休"),
    ("12/31", "四", "提早關", SAKURA, "百貨約 18 點關"),
    ("1/1", "五", "大多休", BENI, "百貨全休、神社最熱鬧"),
    ("1/2", "六", "初賣", SORA, "百貨開賣福袋"),
]


def calendar():
    w, h = 480, 330
    cw, ch = 150, 96
    b = []
    for i, (d, wd, status, color, note) in enumerate(CAL):
        x = 12 + (i % 3) * (cw + 8)
        y = 10 + (i // 3) * (ch + 8)
        b.append(rect_wash(x, y, cw, ch, color, 0.42 if color != BENI else 0.3, 1 + i % 3))
        b.append(rough(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="8" stroke="{MUTED}" stroke-width="1.4"/>'))
        b.append(t(x + 12, y + 30, d, 24, "start", INK, 700, "latin"))
        b.append(t(x + cw - 12, y + 28, f"週{wd}", 13, "end", MUTED))
        b.append(t(x + 12, y + 58, status, 19, "start", BENI if color == BENI else INK, 700))
        b.append(t(x + 12, y + 82, note, 12.5, "start", INK))
    return svg(w, h, "".join(b), "年末年始營業日曆")


# ---------------------------------------------------------------- chapter 1


def outfit():
    w, h = 480, 300
    b = [wash(240, 150, 230, 130, SORA, 0.28, 3)]
    # thermometer
    b.append(rough('<rect x="28" y="30" width="26" height="200" rx="13" fill="#FFFDF8"/><circle cx="41" cy="244" r="22" fill="#E7837F"/>'
                   '<rect x="35" y="150" width="12" height="94" fill="#E7837F" stroke="none"/>'))
    for temp, y in ((15, 40), (10, 100), (5, 160), (0, 220)):
        b.append(rough(f'<path d="M54 {y} H64"/>'))
        b.append(t(70, y + 5, f"{temp}°", 14, "start", MUTED, 400, "latin"))
    b.append(t(100, 112, "白天 10～12°C", 15, "start", INK, 700))
    b.append(t(100, 222, "早晚 1～4°C", 15, "start", INK, 700))
    items = [
        (230, "發熱衣", '<path d="M-26 -30 L-12 -38 Q0 -30 12 -38 L26 -30 L22 -14 L16 -16 V34 H-16 V-16 L-22 -14 Z" fill="#F4E6D4"/>'),
        (320, "毛衣", '<path d="M-30 -30 L-12 -38 Q0 -28 12 -38 L30 -30 L28 0 L18 -2 V34 H-18 V-2 L-28 0 Z" fill="#E7B7A0"/>'
               '<path d="M-14 10 H14 M-14 20 H14" stroke-dasharray="3 4"/>'),
        (410, "羽絨外套", '<path d="M-34 -30 L-14 -40 Q0 -32 14 -40 L34 -30 L32 8 L22 6 V40 H-22 V6 L-32 8 Z" fill="#9CB4D6"/>'
                     '<path d="M-22 -6 H22 M-22 10 H22 M-22 26 H22 M0 -32 V40"/>'),
        (275, "圍巾・手套・毛帽", '<path d="M-30 -10 Q0 6 30 -10 L30 0 Q0 16 -30 0 Z" fill="#C9473E"/><path d="M14 2 L18 36 L8 36 L6 6" fill="#C9473E"/>'),
        (390, "好走的鞋", '<path d="M-34 10 Q-34 -12 -18 -12 L-4 -12 Q2 2 30 4 Q36 6 36 16 H-34 Z" fill="#FFFDF8"/><path d="M-34 16 H36" stroke-width="4"/>'),
    ]
    for i, (x, label, shape) in enumerate(items):
        y = 90 if i < 3 else 210
        b.append(f'<g transform="translate({x} {y})">{rough(shape)}</g>')
        b.append(t(x, y + 62, label, 14, "middle", INK, 700))
    return svg(w, h, "".join(b), "冬季穿搭與氣溫")


def taxfree():
    w, h = 480, 210
    steps = [
        ("1", "結帳出示護照", "或 VJW 免稅 QR"),
        ("2", "先付含稅價", "保留收據"),
        ("3", "出境時海關確認", "商品要帶在身上"),
        ("4", "退回稅金", "多為退回信用卡"),
    ]
    b = []
    colors = [SAKURA, YUZU, SORA, MATCHA]
    for i, (n, a, c) in enumerate(steps):
        x = 60 + i * 120
        b.append(wash(x, 74, 50, 46, colors[i], 0.6, 1 + i % 3))
        b.append(t(x, 66, n, 30, "middle", INK, 700, "latin"))
        b.append(t(x, 132, a, 14.5, "middle", INK, 700))
        b.append(t(x, 154, c, 12, "middle", MUTED))
        if i < 3:
            b.append(rough(f'<path d="M{x + 40} 74 H{x + 78} M{x + 70} 66 L{x + 80} 74 L{x + 70} 82"/>'))
    b.append(t(240, 196, "2026/11/1 起的新制：先付後退，商品須 90 天內帶出境", 13, "middle", BENI, 700))
    return svg(w, h, "".join(b), "免稅新制四步驟")


# ---------------------------------------------------------------- chapter 2


def _clock_row(y, title, color, events):
    b = [t(16, y - 30, title, 18, "start", INK, 700)]
    x0, x1 = 44, 436
    b.append(rect_wash(10, y - 16, 462, 40, color, 0.35, 2))
    b.append(rough(f'<path d="M{x0} {y} H{x1}" stroke-width="3"/>'))
    n = len(events)
    for i, (time, label) in enumerate(events):
        x = x0 + i * (x1 - x0) / (n - 1)
        b.append(rough(f'<circle cx="{x}" cy="{y}" r="7" fill="{PAPER}"/>'))
        b.append(t(x, y + 32, time, 15, "middle", INK, 700, "latin"))
        lines = label.split("|")
        for j, ln in enumerate(lines):
            b.append(t(x, y + 52 + j * 17, ln, 13, "middle", INK))
    return "".join(b)


def arrival_return():
    w, h = 480, 330
    b = _clock_row(60, "12/25 抵達之夜", SORA, [
        ("19:00", "成田 T2|降落"), ("20:00", "入境|領行李"), ("20:20", "搭|Skyliner"),
        ("21:00", "京成上野"), ("21:15", "飯店|check-in"),
    ])
    b += _clock_row(220, "1/2 回國日（最晚時間）", SAKURA, [
        ("15:30", "飯店拿行李"), ("16:30", "京成上野|Skyliner"), ("17:15", "成田 T2|報到"),
        ("18:30", "退稅確認|出境"), ("20:10", "起飛 ✈"),
    ])
    return svg(w, h, b, "抵達與回國時間軸")


# ---------------------------------------------------------------- chapter 3 / 8 map

# Rough geographic positions on a 480x420 canvas.
STATIONS = {
    "池袋": (150, 92), "大塚": (196, 78), "日暮里": (318, 82), "上野": (346, 128),
    "秋葉原": (352, 186), "東京": (346, 246), "新橋": (318, 294), "品川": (262, 352),
    "澀谷": (138, 290), "原宿": (122, 238), "新宿": (106, 172),
}
LOOP = ["池袋", "大塚", "日暮里", "上野", "秋葉原", "東京", "新橋", "品川", "澀谷", "原宿", "新宿"]


def _loop_path():
    pts = [STATIONS[s] for s in LOOP] + [STATIONS[LOOP[0]]]
    d = f"M{pts[0][0]} {pts[0][1]}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d += f" Q{(x0 + x1) / 2 + (y1 - y0) * 0.12:.0f} {(y0 + y1) / 2 - (x1 - x0) * 0.12:.0f} {x1} {y1}"
    return d


def yamanote(extras, title, highlight=("上野",), alt=("大塚",), names=True):
    w, h = 480, 430
    b = [wash(230, 220, 200, 190, MATCHA, 0.22, 3)]
    b.append(wash(420, 380, 90, 60, SORA, 0.5, 2))  # Tokyo Bay
    b.append(t(430, 404, "東京灣", 13, "middle", AI))
    b.append(rough(f'<path d="{_loop_path()}" stroke="#7DB65A" stroke-width="9" stroke-opacity=".85"/>'))
    for s, (x, y) in STATIONS.items():
        hot = s in highlight
        alt_ = s in alt
        if hot:
            b.append(wash(x, y, 30, 26, SAKURA, 0.8, 1))
        elif alt_:
            b.append(wash(x, y, 26, 22, YUZU, 0.8, 2))
        b.append(rough(f'<circle cx="{x}" cy="{y}" r="6" fill="{PAPER}" stroke-width="2.4"/>'))
        if not names:
            continue
        dx = 12 if x > 240 else -12
        b.append(t(x + dx, y + 5, s, 15 if hot or alt_ else 13.5, "start" if dx > 0 else "end",
                   BENI if hot else INK, 700 if hot or alt_ else 400))
    for name, (x, y), note, color, side in extras:
        b.append(wash(x, y, 22, 18, color, 0.65, 3))
        b.append(rough(f'<path d="M{x - 5} {y - 5} L{x + 5} {y + 5} M{x + 5} {y - 5} L{x - 5} {y + 5}" stroke="{BENI}"/>'))
        dx, anchor = (12, "start") if side == "r" else (-12, "end")
        b.append(t(x + dx, y - 3, name, 13.5, anchor, INK, 700))
        if note:
            b.append(t(x + dx, y + 13, note, 11.5, anchor, MUTED))
    b.append(t(16, 26, title, 17, "start", INK, 700))
    b.append(t(16, 46, "綠色環線 = JR 山手線", 12, "start", MUTED))
    return svg(w, h, "".join(b), title)


def stay_map():
    extras = [
        ("淺草", (404, 132), "寺廟・下町", SAKURA, "r"),
        ("晴空塔", (440, 172), "", SORA, "l"),
        ("銀座", (382, 276), "購物", YUZU, "r"),
        ("麻布台・東京鐵塔", (262, 300), "跨年", SAKURA, "l"),
        ("台場・豐洲", (420, 330), "teamLab", SORA, "l"),
        ("成田機場 →", (452, 52), "Skyliner 41 分", MATCHA, "l"),
    ]
    return yamanote(extras, "住哪裡？上野是首選，大塚是安靜替代")


def anime_map():
    extras = [
        ("池袋", (150, 92), "寶可夢 MEGA・乙女路", SAKURA, "l"),
        ("中野百老匯", (60, 150), "二手寶庫", YUZU, "r"),
        ("秋葉原", (352, 186), "電器街・公仔・扭蛋", SORA, "r"),
        ("東京站", (346, 246), "動漫人物街", MATCHA, "r"),
        ("晴空塔", (440, 120), "Kirby Café", SORA, "l"),
        ("澀谷 PARCO 6F", (138, 290), "任天堂・寶可夢・JUMP", SAKURA, "l"),
        ("原宿", (122, 238), "Kiddy Land", YUZU, "l"),
        ("台場", (420, 340), "鋼彈 Base", MATCHA, "l"),
        ("日本橋", (300, 228), "寶可夢中心 DX", YUZU, "l"),
    ]
    return yamanote(extras, "動漫遊戲購物地圖", highlight=(), alt=(), names=False)


# ---------------------------------------------------------------- chapter 5

ENODEN = [  # west -> east
    ("藤澤", 30, 120, ""), ("江之島", 92, 150, "步行過橋到島上"), ("腰越", 140, 170, "吻仔魚"),
    ("鎌倉高校前", 196, 196, "灌籃高手平交道"), ("七里濱", 250, 206, "夕陽・bills"),
    ("稻村崎", 300, 210, "富士山＋夕陽"), ("極樂寺", 344, 196, ""), ("長谷", 384, 176, "大佛・長谷寺"),
    ("鎌倉", 440, 132, "八幡宮・小町通"),
]


def enoden():
    w, h = 480, 380
    b = [wash(240, 330, 260, 90, SORA, 0.6, 1), wash(240, 70, 250, 70, MATCHA, 0.25, 2)]
    # Fuji on the horizon
    b.append(rough(f'<path d="M6 300 L46 252 Q52 247 58 252 L98 300" fill="{AI}" fill-opacity=".35"/>'
                   f'<path d="M38 262 L46 252 Q52 247 58 252 L66 262 L58 258 L52 264 L46 258 Z" fill="{SNOW}"/>'))
    b.append(t(52, 320, "富士山", 12, "middle", AI))
    # Enoshima island
    b.append(wash(96, 292, 46, 28, MATCHA, 0.7, 3))
    b.append(rough('<path d="M96 168 V262" stroke-dasharray="4 5"/>'))
    b.append(t(96, 300, "江之島", 15, "middle", INK, 700))
    # sea waves
    b.append(rough(f'<path d="M150 300 Q170 290 190 300 T230 300 T270 300 T310 300 T350 300 T390 300 T430 300" stroke="{AI}" stroke-width="1.6"/>'))
    b.append(t(300, 340, "相模灣", 14, "middle", AI))
    pts = " ".join(f"{x},{y}" for _, x, y, _ in ENODEN)
    b.append(rough(f'<polyline points="{pts}" stroke="#3F7A3A" stroke-width="8" stroke-opacity=".8"/>'))
    b.append(rough(f'<polyline points="{pts}" stroke="#F6EED3" stroke-width="2" stroke-dasharray="6 8"/>'))
    for i, (name, x, y, note) in enumerate(ENODEN):
        key = bool(note)
        b.append(rough(f'<circle cx="{x}" cy="{y}" r="{7 if key else 5}" fill="{PAPER}"/>'))
        up = i % 2 == 0
        ty = y - 16 if up else y + 24
        b.append(t(x, ty, name, 14 if key else 12, "middle", INK, 700 if key else 400))
        if note:
            b.append(t(x, ty + (-16 if up else 16), note, 11, "middle", BENI))
    b.append(t(470, 30, "江之電 全程約 25 分", 14, "end", INK, 700))
    b.append(t(470, 50, "往江之島方向坐右側看海", 12, "end", MUTED))
    b.append(t(12, 30, "← 西", 12, "start", MUTED, 400, "latin"))
    return svg(w, h, "".join(b), "江之電沿線手繪路線圖")


def enoshima_map():
    w, h = 480, 400
    b = [wash(240, 220, 250, 200, SORA, 0.45, 1)]
    island = ("M150 150 Q190 96 270 104 Q350 100 392 150 Q430 210 392 270 Q350 330 262 330 "
              "Q170 334 120 288 Q86 240 108 196 Q120 168 150 150 Z")
    b.append(f'<path d="{island}" fill="{MATCHA}" opacity=".55" filter="url(#wc2)"/>')
    b.append(rough(f'<path d="{island}" stroke="{KUSA}" stroke-width="2"/>'))
    # bridge to the north-east (Katase)
    b.append(rough('<path d="M330 112 L392 20 M346 116 L408 24" stroke-width="2.4"/>'))
    b.append(t(470, 44, "片瀨・江之島站", 13, "end", INK, 700))
    b.append(t(352, 64, "弁天橋", 12, "end", MUTED))
    stops = [
        ("青銅鳥居・仲見世通", 328, 132, SAKURA), ("邊津宮", 300, 160, YUZU), ("中津宮", 260, 178, YUZU),
        ("Samuel Cocking 苑", 232, 212, SAKURA), ("Sea Candle", 224, 236, SAKURA),
        ("戀人之丘・龍戀之鐘", 214, 300, SAKURA), ("奧津宮", 170, 248, YUZU),
        ("稚兒之淵", 116, 286, SORA), ("岩屋洞窟", 92, 252, SORA),
    ]
    path = " ".join(f"{x},{y}" for name, x, y, _ in stops if name != "戀人之丘・龍戀之鐘")
    b.append(rough(f'<polyline points="{path}" stroke="{BENI}" stroke-dasharray="3 7" stroke-width="2.6"/>'))
    b.append(rough('<path d="M200 230 Q206 270 214 300" stroke="#C9473E" stroke-dasharray="3 7" stroke-width="2.6"/>'))
    for i, (name, x, y, color) in enumerate(stops):
        b.append(wash(x, y, 14, 12, color, 0.9, 1 + i % 3))
        b.append(rough(f'<circle cx="{x}" cy="{y}" r="4" fill="{INK}" stroke="none"/>'))
        right = x > 200 and name not in ("Sea Candle",)
        if name == "Sea Candle":
            b.append(t(x + 12, y + 18, name, 13, "start", INK, 700))
        else:
            b.append(t(x + (12 if right else -12), y + 5, name, 13, "start" if right else "end", INK, 700))
    b.append(sticker_at("heart", 236, 316, 0.45))
    b.append(t(30, 384, "西邊看富士山・夕陽 ←", 13, "start", AI, 700))
    b.append(t(450, 384, "紅色虛線＝建議散步路線", 12, "end", MUTED))
    return svg(w, h, "".join(b), "江之島島內散步地圖")


def sticker_at(name, x, y, scale):
    return f'<g transform="translate({x} {y}) scale({scale})">{_sticker_body(name)}</g>'


# ---------------------------------------------------------------- chapter 6

NYE = [
    ("18:00", "年越蕎麥麵", "早點吃晚餐"), ("20:00", "芝公園", "拍東京鐵塔"),
    ("22:30", "增上寺卡位", "越晚越擠"), ("23:30", "除夜之鐘", "108 響"),
    ("0:00", "新年快樂", "鐵塔燈光倒數"), ("0:15", "初詣", "排隊參拜"), ("1:00", "回飯店", "GO App 叫車"),
]


def nye():
    w, h = 480, 400
    b = [f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="#25324F" opacity=".92" filter="url(#wc1)"/>']
    for i in range(22):
        x = (i * 71) % 460 + 10
        y = (i * 37) % 160 + 14
        b.append(f'<circle cx="{x}" cy="{y}" r="{1 + i % 2}" fill="#FFF6D8"/>')
    b.append(f'<g filter="url(#rough)" fill="none" stroke="#FF8A5C" stroke-width="3">'
             '<path d="M400 60 L370 380 M400 60 L430 380 M378 300 H422 M384 220 H416 M390 150 H410"/>'
             '<path d="M378 300 L416 220 M422 300 L384 220" stroke-width="1.5"/></g>')
    b.append(wash(400, 140, 70, 90, "#FFB37A", 0.25, 2))
    for i, (time, a, c) in enumerate(NYE):
        y = 46 + i * 50
        star = time == "0:00"
        b.append(f'<circle cx="40" cy="{y}" r="{10 if star else 6}" fill="{"#F3CD73" if star else "#FFF6D8"}" filter="url(#rough)"/>')
        if i < len(NYE) - 1:
            b.append(f'<path d="M40 {y + 10} V{y + 40}" stroke="#FFF6D8" stroke-dasharray="3 5" filter="url(#rough)"/>')
        b.append(t(64, y + 6, time, 18, "start", "#F3CD73" if star else "#FFF6D8", 700, "latin"))
        b.append(t(130, y + 6, a, 18, "start", "#FFFFFF", 700))
        b.append(t(130, y + 24, c, 12.5, "start", "#C9D2E6"))
    b.append(t(400, 396, "增上寺＋東京鐵塔", 13, "middle", "#FFF6D8", 700))
    return svg(w, h, "".join(b), "跨年夜時間軸")


def hatsumode():
    w, h = 480, 330
    steps = [
        ("鳥居前鞠躬", "走參道兩側", "torii"), ("手水舍", "洗左手→右手→漱口", "wave"),
        ("投香油錢", "5 円＝好緣分", "yen"), ("二拜二拍手一拜", "寺廟只合掌", "heart"),
        ("抽籤", "壞籤綁在架上", "star"), ("買御守", "縁結び・恋愛成就", "gift"),
    ]
    b = []
    for i, (a, c, icon) in enumerate(steps):
        x = 12 + (i % 3) * 156
        y = 8 + (i // 3) * 160
        b.append(rect_wash(x, y, 146, 150, [SAKURA, YUZU, SORA, MATCHA, YUZU, SAKURA][i], 0.3, 1 + i % 3))
        b.append(t(x + 16, y + 30, str(i + 1), 26, "start", BENI, 700, "latin"))
        b.append(sticker_at(icon, x + 46, y + 8, 0.8))
        b.append(t(x + 73, y + 112, a, 15, "middle", INK, 700))
        b.append(t(x + 73, y + 134, c, 12, "middle", MUTED))
    return svg(w, h, "".join(b), "初詣參拜六步驟")


# ---------------------------------------------------------------- chapter 7

FOODS = [
    ("壽司", "2,000～40,000", "sushi", "美登利・根室花まる"),
    ("燒肉和牛", "4,000～15,000", "niku", "六歌仙・敘敘苑"),
    ("拉麵", "1,000～1,800", "ramen", "鳴龍・AFURI・風雲兒"),
    ("壽喜燒", "4,000～15,000", "nabe", "淺草今半"),
    ("吻仔魚丼", "1,300～1,700", "wave", "江之島とびっちょ"),
    ("甜點咖啡", "800～2,000", "coffee", "I'm donut?・Le Souffle"),
]


def food_zukan():
    w, h = 480, 420
    b = [t(16, 28, "東京・湘南 美食圖鑑", 18, "start", INK, 700), t(464, 28, "每人參考價（円）", 12, "end", MUTED)]
    for i, (name, price, icon, shops) in enumerate(FOODS):
        x = 12 + (i % 2) * 234
        y = 44 + (i // 2) * 124
        b.append(rect_wash(x, y, 224, 114, [YUZU, SAKURA, YUZU, SAKURA, SORA, MATCHA][i], 0.3, 1 + i % 3))
        b.append(sticker_at(icon, x + 8, y + 22, 1.0))
        b.append(t(x + 84, y + 38, name, 20, "start", INK, 700))
        b.append(t(x + 84, y + 62, price, 15, "start", BENI, 700, "latin"))
        b.append(t(x + 84, y + 88, shops, 11.5, "start", MUTED))
    return svg(w, h, "".join(b), "美食圖鑑")


# ---------------------------------------------------------------- chapter 9

TOWERS = [  # name, total height (m), observation decks (m)
    ("晴空塔", 634, [350, 450], SORA),
    ("東京鐵塔", 333, [150, 250], SAKURA),
    ("六本木之丘", 238, [], YUZU),
    ("SHIBUYA SKY", 229, [229], MATCHA),
    ("都廳", 243, [202], SORA),
]


def heights():
    w, h = 480, 440
    base, top = 400, 40
    scale = (base - top) / 650
    b = []
    for m in (0, 100, 200, 300, 400, 500, 600):
        y = base - m * scale
        b.append(f'<path d="M40 {y:.1f} H470" stroke="{MUTED}" stroke-width=".6" stroke-dasharray="2 5"/>')
        b.append(t(34, y + 4, f"{m}", 11, "end", MUTED, 400, "latin"))
    b.append(t(34, top - 12, "公尺", 11, "end", MUTED))
    for i, (name, ht, decks, color) in enumerate(TOWERS):
        cx = 92 + i * 88
        y = base - ht * scale
        bw = 26 if i != 1 else 34
        b.append(f'<path d="M{cx - bw} {base} L{cx - 6} {y:.1f} L{cx + 6} {y:.1f} L{cx + bw} {base} Z" fill="{color}" opacity=".6" filter="url(#wc{1 + i % 3})"/>')
        b.append(rough(f'<path d="M{cx - bw} {base} L{cx - 6} {y:.1f} L{cx + 6} {y:.1f} L{cx + bw} {base}" stroke-width="1.8"/>'))
        for d in decks:
            dy = base - d * scale
            b.append(rough(f'<path d="M{cx - 14} {dy:.1f} H{cx + 14}" stroke="{BENI}" stroke-width="4"/>'))
            b.append(t(cx + 18, dy + 4, f"{d}", 11.5, "start", BENI, 700, "latin"))
        b.append(t(cx, y - 8, f"{ht}m", 12.5, "middle", INK, 700, "latin"))
        b.append(t(cx, base + 22, name, 13, "middle", INK, 700))
    b.append(rough(f'<path d="M40 {base} H470" stroke-width="2.4"/>'))
    b.append(t(470, 22, "紅線＝展望台高度", 12, "end", BENI, 700))
    b.append(t(470, 38, "六本木 Tokyo City View 在 52F", 11.5, "end", MUTED))
    return svg(w, h, "".join(b), "東京展望台高度比較（依實際高度等比例）")


# ---------------------------------------------------------------- chapter 10

TRIPS = [  # name, angle (deg, 0 = north, clockwise), minutes, note, label side
    ("迪士尼", 100, 40, "JR 京葉線", "r"), ("川越", 315, 60, "小江戶", "l"),
    ("哈利波特影城", 290, 45, "練馬", "l"), ("PokéPark", 250, 60, "讀賣樂園", "l"),
    ("鎌倉・江之島", 200, 75, "本書第 5 章", "r"), ("箱根", 235, 120, "1/2～1/3 驛傳", "l"),
    ("河口湖・富士山", 262, 150, "冬天最清楚", "l"), ("日光", 2, 120, "冬天很冷", "r"),
]


def day_trips():
    w, h = 480, 440
    cx, cy = 300, 220
    b = [wash(cx, cy, 200, 190, MATCHA, 0.18, 1)]
    for mins in (60, 120, 180):
        r = mins * 0.95
        b.append(rough(f'<circle cx="{cx}" cy="{cy}" r="{r:.0f}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 7"/>'))
        b.append(t(cx + 4, cy - r - 4, f"{mins // 60} 小時", 11, "start", MUTED))
    b.append(wash(cx, cy, 26, 22, SAKURA, 0.9, 2))
    b.append(t(cx, cy + 6, "上野", 15, "middle", BENI, 700))
    for i, (name, ang, mins, note, side) in enumerate(TRIPS):
        r = mins * 0.95
        x = cx + r * math.sin(math.radians(ang))
        y = cy - r * math.cos(math.radians(ang))
        b.append(rough(f'<path d="M{cx} {cy} L{x:.0f} {y:.0f}" stroke-width="1.2" stroke="{MUTED}"/>'))
        b.append(wash(x, y, 14, 12, [SORA, YUZU, SAKURA, MATCHA][i % 4], 0.95, 1 + i % 3))
        right = side == "r"
        b.append(t(x + (10 if right else -10), y - 2, name, 13.5, "start" if right else "end", INK, 700))
        b.append(t(x + (10 if right else -10), y + 14, f"約 {mins} 分・{note}", 11, "start" if right else "end", MUTED))
    b.append(t(20, 28, "↑ 北", 13, "start", MUTED))
    b.append(t(20, 46, "圓圈＝單程時間", 12, "start", MUTED))
    return svg(w, h, "".join(b), "一日遊方位與時間圖")


# ---------------------------------------------------------------- chapter 12

BUDGET = [  # version, items (label, 10k yen)
    ("省錢版", [10.5, 2.0, 2.5, 9.0, 2.5]),
    ("舒適版", [17.5, 3.5, 3.0, 15.0, 4.5]),
    ("享受版", [28.0, 6.0, 4.5, 25.0, 8.0]),
]
BUDGET_ITEMS = [("東京住宿", SORA), ("江之島", MATCHA), ("交通", YUZU), ("餐飲", SAKURA), ("門票體驗", "#C9B3E0")]


def budget():
    w, h = 480, 260
    x0, scale = 76, 4.4  # px per 10k yen; 71.5 -> 315px
    b = []
    for i, (name, vals) in enumerate(BUDGET):
        y = 30 + i * 62
        b.append(t(x0 - 10, y + 24, name, 15, "end", INK, 700))
        x = x0
        for (label, color), v in zip(BUDGET_ITEMS, vals):
            b.append(f'<rect x="{x:.1f}" y="{y}" width="{v * scale:.1f}" height="34" fill="{color}" opacity=".75" filter="url(#wc{1 + i % 3})"/>')
            x += v * scale
        b.append(rough(f'<rect x="{x0}" y="{y}" width="{x - x0:.1f}" height="34" stroke-width="1.4"/>'))
        b.append(t(x + 8, y + 23, f"約 {sum(vals):.1f} 萬円", 13.5, "start", INK, 700, "latin"))
    for j, (label, color) in enumerate(BUDGET_ITEMS):
        lx = 20 + j * 92
        b.append(f'<rect x="{lx}" y="224" width="16" height="12" fill="{color}" opacity=".8"/>')
        b.append(t(lx + 22, 235, label, 12.5, "start", INK))
    return svg(w, h, "".join(b), "兩人預算三種版本（不含機票、購物）")


ARTS = {
    "timeline": timeline, "calendar": calendar, "outfit": outfit, "taxfree": taxfree,
    "arrival": arrival_return, "staymap": stay_map, "animemap": anime_map, "enoden": enoden,
    "enoshima": enoshima_map, "nye": nye, "hatsumode": hatsumode, "food": food_zukan,
    "heights": heights, "daytrips": day_trips, "budget": budget,
}
