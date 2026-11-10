# 地圖插圖

插圖定義在 `index.html` 的 `<defs>` 裡（檔案最前面那個 0×0 的 `<svg>`），每個是 `<g id="ic-名稱">`。

## 現有插圖

| icon | 畫的是 | 適合 |
|---|---|---|
| `torii` | 木造鳥居＋樹 | 神社、神宮、森林步道 |
| `shops` | 三間彩色小店＋可麗餅 | 商店街、老街、購物 |
| `avenue` | 玻璃大樓＋冬天的行道樹 | 林蔭大道、建築散步 |
| `park` | 長型建築＋屋頂綠地拱架 | 立體公園、商場 |
| `hachiko` | 銅像＋斑馬線 | 銅像、路口、廣場 |
| `tower` | 高樓＋夕陽 | 展望台、高樓 |
| `lanterns` | 屋台＋紅燈籠 | 居酒屋、美食街、夜市 |
| `pin` | 黃色地標針 | 其他（備用） |

## 加新的插圖

照現有插圖的規則畫，風格才會一致：

- 原點 (0,0) 是插圖的**底部中央**，往上畫（y 為負），寬約 60–76、高約 45–70。
- 外框統一：`stroke="#4a3a2a" stroke-width="1.8" stroke-linejoin="round"` 寫在 `<g>` 上。
- 用簡單形狀（`path`、`rect`、`circle`、`ellipse`），填色用柔和的色票：
  紅 `#d2553f`／`#e0533d`、綠 `#8fb36a`／`#9cc177`、黃 `#f6d68a`／`#e0a23a`、藍 `#bcd3e0`／`#cdd9e6`、木頭 `#a8774c`／`#8a5c36`、淺米 `#ece2cf`、白 `#fffdf8`。
- 冬天要有雪的部分加 `class="snow"`（非冬天會自動隱藏）。
- 畫完放進 `<defs>`，itinerary 裡用 `"icon": "名稱"`（不含 `ic-`）。

範例（燈塔）：

```html
<g id="ic-lighthouse" stroke="#4a3a2a" stroke-width="1.8" stroke-linejoin="round">
  <path d="M-30 0h60l-6-8h-48z" fill="#d9c9a6"/>
  <path d="M-9-8 -6-50h12l3 42z" fill="#fffdf8"/>
  <path d="M-8-22h16M-7-36h14" stroke="#d2553f" stroke-width="4"/>
  <path d="M-8-50h16v-8h-16z" fill="#f6d68a"/><path d="M-10-58h20l-10-8z" fill="#d2553f"/>
</g>
```

畫好後跑 `check_page.js` 看封面和站點截圖，插圖太小或太擠就調整。
