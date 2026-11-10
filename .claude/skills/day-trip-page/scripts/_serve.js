// Tiny static file server used by render_basemap.js and check_page.js (no other dependencies).
const http = require("http"), fs = require("fs"), path = require("path");
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json",
  ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".svg": "image/svg+xml" };
module.exports = function serve(dir) {
  return new Promise(res => {
    const srv = http.createServer((req, rsp) => {
      const p = path.join(dir, decodeURIComponent(req.url.split("?")[0]));
      if (!p.startsWith(path.resolve(dir))) { rsp.writeHead(403); return rsp.end(); }
      fs.readFile(p, (err, data) => {
        if (err) { rsp.writeHead(404); return rsp.end(); }
        rsp.writeHead(200, { "Content-Type": TYPES[path.extname(p).toLowerCase()] || "application/octet-stream" }); rsp.end(data);
      });
    }).listen(0, "127.0.0.1", () => res({ url: `http://127.0.0.1:${srv.address().port}/`, close: () => srv.close() }));
  });
};
// Playwright launch options: route through the HTTPS proxy when one is configured, but not for the local server
module.exports.launchOpts = () => process.env.HTTPS_PROXY ? { proxy: { server: process.env.HTTPS_PROXY, bypass: "localhost,127.0.0.1" } } : {};
