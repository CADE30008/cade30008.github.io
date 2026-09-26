// Capture still images of the applets, used wherever an applet can't run:
// printed handouts, PDF decks, and anywhere scripts are blocked.
// Run with: node scripts/capture-stills.mjs   (set CHROME_PATH if needed)
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import puppeteer from "puppeteer-core";

const root = resolve(import.meta.dirname, "..");
const chrome = process.env.CHROME_PATH || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const STILLS = [
  {
    applet: "docs/applets/pid-tuner.html",
    query: "kp=2.03&ki=0.678&kd=0.661&n=10&step=10",
    out: "docs/w03-pid-control/figures/pid-tuner-still.png",
  },
];

const browser = await puppeteer.launch({ executablePath: chrome });
const page = await browser.newPage();
const problems = [];
page.on("pageerror", (e) => problems.push(e.message));
page.on("console", (m) => { if (m.type() === "error") problems.push(m.text()); });
await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1.5 });
for (const s of STILLS) {
  await page.goto(`${pathToFileURL(join(root, s.applet)).href}?${s.query}`, { waitUntil: "load" });
  await new Promise((r) => setTimeout(r, 400));
  await page.screenshot({ path: join(root, s.out) });
  console.log(`captured ${s.out}`);
}
await browser.close();
if (problems.length) {
  console.error("applet reported errors:\n  " + problems.join("\n  "));
  process.exit(1);
}

// tracking: status=draft version=0 assisted=true
