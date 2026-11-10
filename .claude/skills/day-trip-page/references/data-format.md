# 資料格式

## itinerary.js

一定要保持 `window.TRIP = {JSON};` 的形式（純 JSON、雙引號），`make_routes.py` 才能讀寫。檔案開頭的註解可以留著。

```js
window.TRIP = {
  "title": "澀谷散步日",            // 頁面標題、封面大字（每個字輪流上色）
  "en": "Shibuya Winter Walk",      // 封面英文副標
  "date": "12/27（六）",
  "subtitle": "明治神宮 → 原宿 → 表參道 → 澀谷",
  "season": "winter",               // "winter" 才會有樹上的雪；其他季節留空
  "badge": "",                      // 封面頭像裡的一個字，空的就用標題第一個字
  "stops": [ ... ]
};
```

### 每一站

| 欄位 | 必填 | 說明 |
|---|---|---|
| `name` | ✓ | 站名（大字）。使用者自己的照片放 `photos/<name>.jpg`、`<name>-2.jpg`…會排在輪播最前面 |
| `en` | | 英文副標，也顯示在地圖上的站名下面 |
| `handle` | | 貼文帳號名稱，像 `meiji.jingu`（小寫英文加點） |
| `area` | | 貼文帳號下面的地點，像「澀谷區・代代木神園町」 |
| `period` | ✓ | 早上／中午／下午／傍晚／晚上（決定時段標籤顏色） |
| `time` | | 「09:00–10:30」「16:00 入場」 |
| `highlight` | ✓ | 一句話：要做什麼（清單、回顧用） |
| `desc` | ✓ | 介紹，每段一個字串，2–3 段，每段 2–3 句 |
| `todo` | | 「今天要做的事」清單 |
| `tags` | | hashtag，不含 `#` |
| `note` | | 備註（門票、營業時間、交通），沒有就空字串 |
| `coords` | ✓ | `[lat, lng]`，查證過的座標 |
| `maps` | | Google Maps 導航用的名稱（用當地語言），省略時用座標 |
| `photos` | ✓ | `[{ "src": "01-x.jpg", "by": "作者 / Unsplash", "focus": "50% 40%", "sample": true }]`；`src` 在 `photos/auto/`，`focus` 是裁切焦點（object-position），`sample: true` 會在照片上標「示意」 |
| `icon` | | 地圖插圖：`torii` `shops` `avenue` `park` `hachiko` `tower` `lanterns` `pin`，或自己加的（見 icons.md） |
| `iconAt` | | 插圖相對站點的位置 `[dx, dy]`（地圖單位，約 1.8 公尺）。預設 `[0, -58]`＝正上方 |
| `via` | | 給 `make_routes.py`：從上一站走過來要經過的點 `[[lat,lng], ...]` |
| `walk` / `path` | | `make_routes.py` 寫入的步行距離時間與路線，不要手改 |

### iconAt 怎麼排

- 插圖約 70 寬 × 55 高，站名文字在插圖下方約 22–36 單位處。
- 放正上方時用 `dy ≤ -56`，站名才不會被號碼圓圈蓋住。
- 幾站靠很近（同一個車站周邊）時，把插圖往左右推開（`dx` 約 ±60–90）；站名約每個字 17 單位寬，往左放時 `dx` 要大於「字數 × 8.5 + 15」。
- 改完用 `check_page.js` 的封面截圖確認沒有重疊。

## basemap.config.json

```json
{
  "area": { "s": 35.6555, "n": 35.6786, "w": 139.6935, "e": 139.7136 },
  "snow": true,
  "labels": [
    ["代代木公園", "Yoyogi Park", 35.6706, 139.6958, "area"],
    ["明治通", "Meiji-dori", 35.6648, 139.7034, "road", "明治通り"],
    ["JR 原宿站", "Harajuku Sta.", 35.6705, 139.7024, "station"]
  ]
}
```

- `area`：底圖範圍。所有站點外圍至少留約 300 公尺（緯度 0.003、經度 0.0035 左右）。範圍越大 basemap.js 越大；約 2 × 2.5 公里時 basemap.js 約 300 KB、basemap.jpg 約 650 KB。
- `snow`：撒雪花。
- `labels`：地圖上的字。`area` 是區域大字（中文＋英文），`road` 會沿著第 6 個欄位那條 OSM 路名的方向旋轉（路名要用 OSM 裡的原文，用 `make_basemap.py names` 查），`station` 是綠框車站牌。
- 地圖寬固定 1000 單位，高度依範圍比例算。
