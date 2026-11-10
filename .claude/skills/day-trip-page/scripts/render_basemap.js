// 把手繪底圖預先畫成 PROJECT_DIR/basemap.jpg（2 倍解析度）。
// 地圖移動時頁面改畫這張圖，停下來再換回向量圖，手機才不會卡。改過 basemap.js 之後要重跑。
// 用法：node render_basemap.js PROJECT_DIR      （需要 Playwright；找不到時加 NODE_PATH=$(npm root -g)）
const { chromium } = require("playwright");
const path = require("path");
const serve = require("./_serve");
(async () => {
  const dir = path.resolve(process.argv[2] || ".");
  const srv = await serve(dir);
  const browser = await chromium.launch(serve.launchOpts());
  const page = await browser.newPage({ viewport: { width: 1000, height: 1500 }, deviceScaleFactor: 2 });
  await page.goto(srv.url + "index.html?renderbase", { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const out = path.join(dir, "basemap.jpg");
  await page.locator("#mapBase").screenshot({ path: out, type: "jpeg", quality: 80 });
  console.log("wrote", out);
  await browser.close(); srv.close();
})();
