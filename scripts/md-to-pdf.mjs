// Print Markdown documents to a single PDF.
//
// Converts one or more Markdown files with pandoc into one HTML page, styled by
// scripts/pdf.css, and prints it with headless Chrome, as build-pdfs.mjs does
// for the site. Used for proposals, briefs and rubrics. Each top-level heading
// after the first starts a new page, so appendices can be separate files.
//
//   node scripts/md-to-pdf.mjs note.md appendix-a.md -o out.pdf --title "Footer text"
//
// Needs pandoc on the PATH. Set CHROME_PATH if Chrome isn't in the default
// macOS location.
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import puppeteer from "puppeteer-core";

const args = process.argv.slice(2);
const inputs = [];
let out = null;
let title = "";
for (let i = 0; i < args.length; i++) {
  if (args[i] === "-o") out = args[++i];
  else if (args[i] === "--title") title = args[++i];
  else inputs.push(args[i]);
}
if (!inputs.length || !out) {
  console.error('usage: node scripts/md-to-pdf.mjs input.md [more.md ...] -o output.pdf [--title "Footer text"]');
  process.exit(1);
}

const root = resolve(import.meta.dirname, "..");
const chrome = process.env.CHROME_PATH || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const work = mkdtempSync(join(tmpdir(), "md-to-pdf-"));
const html = join(work, "document.html");
const escape = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");

try {
  const sources = inputs.map((p) => resolve(p));
  execFileSync("pandoc", [
    ...sources,
    "--from", "gfm",
    "--to", "html5",
    "--standalone",
    "--embed-resources",
    "--css", join(root, "scripts", "pdf.css"),
    "--resource-path", [...new Set(sources.map((p) => dirname(p)))].join(":"),
    "--metadata", `pagetitle=${title || "Document"}`,
    "-o", html,
  ]);

  const browser = await puppeteer.launch({ executablePath: chrome, args: ["--no-sandbox"] });
  const page = await browser.newPage();
  await page.goto(pathToFileURL(html).href, { waitUntil: "networkidle0" });
  await page.pdf({
    path: resolve(out),
    format: "A4",
    printBackground: true,
    margin: { top: "16mm", bottom: "18mm", left: "18mm", right: "18mm" },
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate: `<div style="font: 7.5px Helvetica, Arial, sans-serif; width: 100%; padding: 0 18mm; display: flex; justify-content: space-between; color: #666;">
      <span>${escape(title)}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  });
  await browser.close();
  console.log(`printed ${out}`);
} finally {
  rmSync(work, { recursive: true, force: true });
}

// tracking: status=draft version=0
