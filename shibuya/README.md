# 澀谷散步日（12/27）

手繪風格地圖上一站一站走：按「下一站」，小人沿真實步行路線走到下一站，再跳出一則 Instagram 風格的貼文（照片可左右滑、介紹、要做的事、備註、Google Maps 導航）。直接雙擊 `index.html` 就能開，地圖完全不需要線上載入（只有字型來自 Google Fonts）。

- `index.html`：頁面本體
- `itinerary.js`：行程資料（站名、時段、介紹、照片清單、地圖插圖、步行路線…，欄位說明在檔案開頭）
- `basemap.js`：手繪底圖（由 `tools/make_basemap.py` 從 OpenStreetMap 資料產生）
- `photos/`：放你自己的照片，檔名＝站名，例如 `photos/明治神宮.jpg`、`photos/明治神宮-2.jpg`，會排在輪播最前面
- `photos/auto/`：自動下載的照片；來源與授權見 `photos/credits.txt`

## 操作

- 下方「下一站 ›」：地圖先拉遠看整段路，小人沿路線走過去（地圖不動），再拉近到下一站，「‹」回上一站，數字直接跳站
- 地圖可以拖曳、雙指縮放，右上角 ＋／－／全部
- 手機上點貼文標題列或把手可以收起／展開貼文；點地圖空白處也會收起
- 照片左右滑看更多，點兩下按讚（只存在這台裝置）

## 做其他區域的頁面

1. 改 `tools/make_basemap.py` 裡的 `AREA`（範圍）和 `LABELS`（地名、路名）
2. `python3 tools/make_basemap.py fetch osm_data` → `python3 tools/make_basemap.py build osm_data basemap.js`
3. 產生動畫用的底圖照片：在這個資料夾開 `python3 -m http.server 8765`，再執行 `node tools/render_basemap.js`（會寫出 `basemap.jpg`）
4. 改 `itinerary.js`、換照片，然後 `python3 tools/make_photo_sizes.py` 產生小尺寸照片（`photos/auto/m/`、`photos/auto/t/`）

## 為什麼有 basemap.jpg 和小尺寸照片

- 手繪底圖是向量圖，停著的時候最清楚，但移動時手機每一格都要重畫會卡。所以移動中改把預先畫好的 `basemap.jpg` 畫進一張螢幕大小的 canvas（直接放大整張圖片在手機上會變空白），停下來約半秒後再換回向量圖。
- 輪播照片用 800px 的 WebP（`m/`），頭像和清單用 240px（`t/`），找不到時會自動改用原圖。點「下一站」時就開始下載下一站的照片，其餘的在背景依序預先載入。
