// 把手繪底圖預先畫成 basemap.jpg（2 倍解析度），動畫移動時用這張圖，手機才不會卡。
// 用法：在 shibuya/ 資料夾執行  python3 -m http.server 8765  然後  node tools/render_basemap.js
// 需要 Playwright（npm i playwright）。改過 basemap.js 之後要重跑一次。
const { chromium } = require("playwright");
const path = require("path");
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY, bypass: "localhost,127.0.0.1" } : undefined;
  const browser = await chromium.launch({ proxy });
  const page = await browser.newPage({ viewport: { width: 1000, height: 1500 }, deviceScaleFactor: 2 });
  await page.goto("http://localhost:8765/index.html?renderbase", { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const out = path.join(__dirname, "..", "basemap.jpg");
  await page.locator("#mapBase").screenshot({ path: out, type: "jpeg", quality: 80 });
  console.log("wrote", out);
  await browser.close();
})();
