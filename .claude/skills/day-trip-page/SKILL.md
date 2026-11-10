---
name: day-trip-page
description: 製作「一日遊行程頁面」：手繪風格的離線地圖，按「下一站」小人沿真實步行路線走到下一站，每站一則 Instagram 風格貼文（可左右滑的照片、多段介紹、要做的事、備註、Google Maps 導航），手機直式為主，可發布成 Artifact 用手機看。只要使用者想把某一天的旅遊行程、散步路線、景點清單做成可以出發前預習、到現場查詢導航的頁面，就用這個 skill——即使他只說「幫我做 12/28 那天」「把淺草那天也做成一樣的」「做一個鎌倉一日遊的頁面」「行程網頁」「旅遊地圖」「day trip page」「itinerary page」，或給了一串景點和時間。
---

# 一日遊行程頁面

做出來的東西：一個資料夾（`index.html` + `itinerary.js` + `basemap.js` + `basemap.jpg` + `photos/`），雙擊就能開，也能發布成 Artifact 在手機上看。範例成品就是本 repo 的 `shibuya/`（澀谷 12/27）。

使用者用這個頁面做兩件事：**出發前**一站一站點過去，對路線和每一站有畫面記憶；**到現場**查這一站要做什麼、按導航。所有設計決定都從這兩件事出發——所以地圖要好認、文字要具體、照片要一眼認出地點、導航按鈕要好按。

腳本都在這個 skill 的 `scripts/`（下面用 `$SK` 代表 skill 資料夾）。需要 Python 3 + Pillow、Node + Playwright（找不到 playwright 時在指令前加 `NODE_PATH=$(npm root -g)`）。

## 開始前先讀

- `references/lessons.md`：上一次做澀谷頁時使用者的修正和踩過的坑（自動播放被改掉、地圖空白、手機卡頓、照片來源被擋…）。**每次都先讀**，可以避免重做。
- `references/data-format.md`：`itinerary.js` 每個欄位、`basemap.config.json` 格式、插圖位置怎麼排。
- `references/icons.md`：現有地圖插圖、怎麼畫新的。

## 流程

### 1. 確認行程

需要：日期、每站名稱、時段（早上／中午／下午／傍晚／晚上，有確切時間更好）、每站想做什麼、已知備註（門票已訂、入場時間…）、季節。使用者通常一次給齊；缺的才問，順序和時間可以自己合理安排，安排了要告訴他。

### 2. 建資料夾

```bash
python3 $SK/scripts/new_day.py <資料夾> --title "淺草散步日" --date "12/28（日）" --en "Asakusa Winter Walk" --season winter
```

資料夾放在 repo 裡（例如 `asakusa/`），和 `shibuya/` 並列。

### 3. 座標與步行路線

```bash
python3 $SK/scripts/geocode.py "浅草寺" "仲見世通り" --country jp
```

每站挑「類型和地址都對」的候選填進 `coords`（不要用估計值）。`maps` 填 Google Maps 認得的當地名稱。然後：

```bash
python3 $SK/scripts/make_routes.py <資料夾>/itinerary.js
```

看輸出的距離時間是否合理（市區步行一段通常 3–20 分鐘）；繞遠路就加 `via` 再跑一次（`--force`）。

### 4. 手繪底圖

1. 依站點範圍寫 `basemap.config.json` 的 `area`（外圍留約 300 公尺），`snow` 依季節。
2. `python3 $SK/scripts/make_basemap.py fetch <資料夾>/basemap.config.json <暫存資料夾>/osm`（OSM 原始資料放暫存區，不要進 repo）
3. `python3 $SK/scripts/make_basemap.py names <config> <osm>` 列出路名、車站，挑 6–12 個寫進 `labels`：區域名（中文＋英文）、主要道路（第 6 欄填 OSM 原文路名）、車站。地名用繁體中文。
4. `python3 $SK/scripts/make_basemap.py build <config> <osm> <資料夾>/basemap.js`

### 5. 照片

照片依這個順序：

1. 使用者自己的照片：`photos/<站名>.jpg`、`<站名>-2.jpg`…頁面會自動排在最前面，不用設定。
2. 其他從 **Unsplash** 找（這個環境 Commons 被限流、Pexels 被擋，細節見 lessons.md）：用 WebSearch（`allowed_domains: ["unsplash.com"]`）或 WebFetch 抓 `https://unsplash.com/s/photos/<英文關鍵字>`，請它列出免費照片的照片頁、`images.unsplash.com/photo-<id>` 網址和攝影者。
3. 每站下載 5–8 張候選（`?w=800` 小圖）到暫存區，做一張縮圖總覽圖自己看，每站選 3–4 張：第一張最能代表地點（白天、構圖乾淨、沒大量文字），其他是細節（招牌、食物、入口、夜景）。找不到地點本身的就用相似場景並標 `sample: true`。
4. 寫 `photos.json`（格式見 `download_photos.py` 開頭），然後：

```bash
python3 $SK/scripts/download_photos.py <資料夾> photos.json   # 存到 photos/auto/，並寫 photos/credits.txt
python3 $SK/scripts/make_photo_sizes.py <資料夾>               # 產生 800px / 240px 的 WebP
```

把選好的照片清單（縮圖＋來源）給使用者看。

### 6. 寫每站內容

依 `references/data-format.md` 填 `itinerary.js`。內容是使用者最在意的部分：

- `desc` 2–3 段，每段 2–3 句：這是什麼、為什麼有名、看點、跟這趟行程有關的細節（日落時間、人潮時段、從哪個出口進去）。只寫有把握的事實；營業時間類加「依官網為準」。繁體中文、台灣用語。
- `todo` 2–3 條具體動作，`note` 放門票、時間、交通提醒。
- `handle`（小寫英文帳號名）、`area`、`tags`、`icon`、`iconAt`。

### 7. 底圖圖片、檢查

```bash
node $SK/scripts/render_basemap.js <資料夾>                 # 產生 basemap.jpg（每次改 basemap.js 或插圖後都要重跑）
node $SK/scripts/check_page.js <資料夾> <暫存資料夾>/check   # 手機尺寸從出發點到回顧
```

`check_page.js` 會印出頁面錯誤、缺檔、走路時地圖是否不動、是否用小尺寸照片，並存截圖。看截圖檢查：插圖和站名有沒有重疊（調 `iconAt`）、封面標題有沒有蓋住站點、貼文文字是否完整。修到沒有錯誤、沒有重疊為止。

### 8. 給使用者確認

傳截圖給使用者（封面、一站的貼文、回顧總覽），連同照片清單和缺圖／示意圖的站。照他的回饋調整。

### 9. 發布與保存

```bash
python3 $SK/scripts/build_artifact.py <資料夾> <暫存資料夾>/art   # 最後一行印出 files 清單
```

用 Artifact 工具發布：`file_path` = `<暫存資料夾>/art/index.html`、`root` = `<暫存資料夾>/art`、`files` = 印出的清單、`icon` = `map`（發布前依 Artifact 工具規定先載入 artifact-design skill）。之後更新用同一個 `file_path`；只改 index.html 時不用再傳 files。

在 git repo 裡就 commit、push 資料夾（OSM 原始資料和暫存檔不要 commit）。

最後請使用者**用手機**實際點一遍：無頭瀏覽器抓不到手機 GPU 的問題（上次「移動中地圖空白」就是這樣），有問題請他錄影。

## 改頁面本身時

範本是 `assets/template/index.html`。修 bug 或加功能時改範本，再複製到各天的資料夾（各天的 `index.html` 除了 `<title>` 都一樣）。效能相關的設計（預先畫好的底圖、canvas、移動中隱藏向量）不要拿掉，原因在 lessons.md。
