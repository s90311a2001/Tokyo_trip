// 在手機尺寸（390×844）把頁面從出發一路點到回顧，檢查錯誤並截圖。
// 用法：node check_page.js PROJECT_DIR OUT_DIR [--dpr 2]
// 產出：OUT_DIR/1-cover.png、2-stop.png（第 2 站貼文）、3-walking.png（走路中）、4-recap.png、5-desktop.png
// 並列出：頁面錯誤、壞掉的檔案（404）、走路時地圖是否保持不動、照片是否用小尺寸版本。
const { chromium } = require("playwright");
const path = require("path"), fs = require("fs");
const serve = require("./_serve");
(async () => {
  const dir = path.resolve(process.argv[2] || "."), out = path.resolve(process.argv[3] || "check");
  const dpr = +(process.argv[process.argv.indexOf("--dpr") + 1] || 1) || 1;
  fs.mkdirSync(out, { recursive: true });
  const srv = await serve(dir);
  const browser = await chromium.launch(serve.launchOpts());
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: dpr, isMobile: true, hasTouch: true });
  const p = await ctx.newPage();
  const errors = [], missing = [], photos = [];
  p.on("pageerror", e => errors.push(e.message));
  p.on("response", r => { const u = r.url();
    if (r.status() >= 400 && !/\/photos\/[^/]+\.jpg/.test(decodeURI(u))) missing.push(r.status() + " " + u.replace(srv.url, ""));  // photos/<站名>.jpg probes are expected to 404
    if (/photos\/auto\//.test(u)) photos.push(u.split("photos/auto/")[1]); });
  await p.goto(srv.url + "index.html", { waitUntil: "networkidle" }); await p.waitForTimeout(1200);
  await p.screenshot({ path: path.join(out, "1-cover.png") });
  const n = await p.evaluate(() => window.TRIP.stops.length);
  await p.click("#next"); await p.waitForTimeout(2400);
  let still = null;
  for (let i = 1; i < n; i++) {
    await p.click("#next");
    if (i === 1) {
      await p.waitForTimeout(1300); const a = await p.evaluate(() => document.querySelector("#cam").style.transform);
      await p.screenshot({ path: path.join(out, "3-walking.png") });
      await p.waitForTimeout(400); const b = await p.evaluate(() => document.querySelector("#cam").style.transform);
      still = a === b;
      await p.waitForTimeout(3500); await p.screenshot({ path: path.join(out, "2-stop.png") });
    } else await p.waitForTimeout(5200);
  }
  await p.click("#next"); await p.waitForTimeout(2200);
  await p.screenshot({ path: path.join(out, "4-recap.png") });
  const d = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await d.goto(srv.url + "index.html", { waitUntil: "networkidle" }); await d.waitForTimeout(800);
  await d.click("#dots button >> nth=" + Math.min(1, n - 1)); await d.waitForTimeout(2500);
  await d.screenshot({ path: path.join(out, "5-desktop.png") });
  const full = photos.filter(x => /^[^/]+\.jpg/.test(x));
  console.log(JSON.stringify({ stops: n, pageErrors: errors, missingFiles: [...new Set(missing)], mapStillWhileWalking: still,
    photoRequests: photos.length, fullSizeJpgRequests: full.length, screenshots: out }, null, 2));
  await browser.close(); srv.close();
})();
