# 做澀谷那一頁時學到的事

每一條都是實際踩過的坑，照著做可以省很多來回。

## 頁面形式（使用者明確要的）

- **不要自動播放。** 使用者要「點一下才走到下一站」。最早做成自動播放的影片＋Leaflet 即時地圖，被要求整個改掉。
- **手繪風格地圖，不要即時載入第三方地圖。** 用 OSM 圖磚時，鏡頭移動到新地點地圖還沒載入，整片空白。也不要在頁面上用 Leaflet / Google Maps。
- **每站用 Instagram 貼文樣式**：照片可以左右滑、文字要多（2–3 段介紹，不是一句話）。
- **走路時地圖不要跟著小人移動。** 正確流程：先拉遠看整段路 → 地圖不動、小人沿路線走 → 拉近到新站。

## 手機效能

- 整張手繪 SVG（數百棵樹＋全部道路）在移動中每一格重畫 → 卡頓。解法：預先畫成 `basemap.jpg`，移動中隱藏向量底圖（`display:none`，`visibility:hidden` 一樣會耗效能）、改畫圖片，停下約 450ms 後換回向量。
- **不要把大圖片放進會被放大的圖層。** `<img>` 放在 `transform: scale()` 的容器裡，放大到站點比例時圖層約 4600×6500 實體像素，Android 手機直接畫成空白（只剩背景色）。解法：每一格只把螢幕看得到的那塊 `drawImage` 到一張螢幕大小的 `<canvas>`（範本已這樣做）。
- 無頭瀏覽器測試是軟體繪圖，抓不到這類 GPU 問題，數字也和手機不同；最後一定要請使用者用手機看，必要時請他錄影。
- 站點的脈動圈動畫在移動中要暫停。

## 照片

- 照片原圖 1080–1280px 太大，貼文打開才下載會很慢。用 `make_photo_sizes.py` 做 800px（輪播）和 240px（頭像、清單）的 WebP，按「下一站」時就預先載入下一站，其他站在背景依序載入（範本已做）。
- 來源只用可自由使用的圖庫。實測這個環境：
  - **Unsplash**：`curl` 抓網頁會被 401，但 **WebFetch** 抓搜尋頁 `https://unsplash.com/s/photos/<關鍵字>` 或照片頁可以拿到 `images.unsplash.com/photo-<id>` 網址；圖片本身用 curl/Python 直接下載沒問題。看清楚是免費照片，不是 Unsplash+（`plus.unsplash.com`、`premium_photo-` 開頭的不能用）。
  - **Wikimedia Commons**：API 常回 429（被限流），upload.wikimedia.org 連不上。
  - **Pexels**：回 403。
  - Instagram / Threads 需要登入，抓不到。
- 用 WebSearch（`allowed_domains: ["unsplash.com"]`）找候選照片頁也很有效。
- 下載候選後一定要做縮圖總覽（contact sheet）自己看過再選：要一眼認得出地點、白天、構圖乾淨、不要大量文字；同一張照片可能以不同 ID 出現兩次。
- 找不到該地點本身的照片時（例如某間美食街），可以用相似場景，但 `sample: true` 標「示意」，並告訴使用者是哪幾張。
- 每站 3–4 張：第一張是最能代表地點的，其他是細節（招牌、食物、夜景、入口）。

## 地圖資料

- OSM Overpass API 在這個環境連不上；`api.openstreetmap.org/api/0.6/map?bbox=` 可以用（`make_basemap.py fetch` 分 3×3 塊下載，每塊數 MB）。
- 座標用 Nominatim 查（`geocode.py`），用當地語言名稱比較準。街道類回傳的是中間某一點，站點要放在使用者會到的那一端或中段。
- 步行路線用 `routing.openstreetmap.de/routed-foot`（`make_routes.py`）。路線不合理時（例如繞遠路）加 `via` 指定經過點。

## 內容

- 介紹寫有把握的事實：創建年份、規模、為什麼有名、看點。不確定的（今年有沒有燈飾、某店營業時間）不要寫死，營業時間類寫「依官網為準」。
- 日落時間、門票時段這類跟行程有關的細節放進 `desc` 或 `note`，對使用者最有用。
- 繁體中文、台灣用語（例如「捷運／地鐵」「公尺」「步行約 X 分鐘」）。

## 發布成 Artifact

- Artifact 頁面只能從 cdnjs / jsdelivr / unpkg 等載入 script，外部圖片和樣式表（Google Fonts 例外）都被擋，所以地圖圖磚不能用、Leaflet 的 CSS 要內嵌——這也是改成自繪底圖的原因之一。
- 頁面不能有 `<!doctype>/<html>/<head>/<body>`，用 `build_artifact.py` 轉。
- 同一個網址更新：之後的 publish 用同一個 `file_path`，或帶 `url`。只改 index.html 時不用再傳 files。
- `?query` 在 Artifact 裡傳不進頁面，只有 `#name` 可以。
