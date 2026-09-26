// Print each lesson's handout, example sheet and solutions to PDF.
//
// Serves the built site (site/) on a local port, opens each page in headless
// Chrome, waits for MathJax, and prints with the site's print styles, which
// swap applets for still images and show every code tab. PDFs go to
// site/downloads/ for publishing and docs/downloads/ for `zensical serve`.
//
// Run after `npm run site`. Set CHROME_PATH if Chrome isn't in the default
// macOS location.
import { createServer } from "node:http";
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, statSync } from "node:fs";
import { extname, join, normalize, resolve } from "node:path";
import puppeteer from "puppeteer-core";

const root = resolve(import.meta.dirname, "..");
const site = join(root, "site");
const chrome = process.env.CHROME_PATH || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
if (!existsSync(join(site, "index.html"))) {
  console.error("site/ is missing: run `npm run site` first");
  process.exit(1);
}

const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml",
  ".png": "image/png", ".json": "application/json", ".woff2": "font/woff2", ".pdf": "application/pdf" };
const server = createServer((req, res) => {
  let path = normalize(decodeURIComponent(new URL(req.url, "http://x").pathname)).replace(/^(\.\.[/\\])+/, "");
  let file = join(site, path);
  if (existsSync(file) && statSync(file).isDirectory()) file = join(file, "index.html");
  if (!existsSync(file)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "Content-Type": TYPES[extname(file)] || "application/octet-stream" });
  res.end(readFileSync(file));
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}`;

const lessons = readdirSync(join(root, "slides"), { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name);
const pages = lessons.flatMap((l) => [
  { url: `/${l}/`, out: `${l}-handout.pdf` },
  { url: `/${l}/example-sheet/`, out: `${l}-example-sheet.pdf` },
  { url: `/${l}/solutions/`, out: `${l}-solutions.pdf` },
]);

const browser = await puppeteer.launch({ executablePath: chrome, args: ["--no-sandbox"] });
const outDirs = [join(site, "downloads"), join(root, "docs", "downloads")];
outDirs.forEach((d) => mkdirSync(d, { recursive: true }));
let failed = 0;
for (const p of pages) {
  const page = await browser.newPage();
  const res = await page.goto(base + p.url, { waitUntil: "networkidle0", timeout: 60000 });
  if (!res || !res.ok()) { console.error(`failed to load ${p.url}`); failed++; await page.close(); continue; }
  await page.evaluate(() => window.MathJax?.startup?.promise);
  await page.emulateMediaType("print");
  const title = await page.title();
  const out = join(outDirs[0], p.out);
  await page.pdf({
    path: out, format: "A4", printBackground: true,
    margin: { top: "16mm", bottom: "18mm", left: "16mm", right: "16mm" },
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate: `<div style="font: 8px Helvetica, Arial, sans-serif; width: 100%; padding: 0 16mm; display: flex; justify-content: space-between; color: #666;">
      <span>${title.replace(/</g, "&lt;")}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  });
  copyFileSync(out, join(outDirs[1], p.out));
  console.log(`printed downloads/${p.out}`);
  await page.close();
}
await browser.close();
server.close();
process.exit(failed ? 1 : 0);

// tracking: status=draft version=0 assisted=true
