// Build every lecture deck in slides/<lesson>/index.md into the site.
//
// Each deck becomes docs/slides/<lesson>/index.html plus slides.pdf. Both are
// generated files (ignored by git), placed inside docs/ so that `zensical
// serve` and `zensical build` publish them with everything else.
//
// Decks refer to shared figures and applets as ../../docs/..., which is right
// for the source file and for VS Code's preview. The published deck sits in
// docs/slides/<lesson>/, one level nearer the site root, so those paths are
// rewritten to ../../... in the HTML. Marp itself is used unmodified.
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const marp = join(root, "node_modules", ".bin", "marp");
const lessons = readdirSync(join(root, "slides"), { withFileTypes: true })
  .filter((d) => d.isDirectory() && existsSync(join(root, "slides", d.name, "index.md")))
  .map((d) => d.name);

const only = process.argv.includes("--html-only") ? ["html"] : ["html", "pdf"];
let failed = 0;
for (const lesson of lessons) {
  const src = join(root, "slides", lesson, "index.md");
  const outDir = join(root, "docs", "slides", lesson);
  mkdirSync(outDir, { recursive: true });
  if (!existsSync(join(root, "docs", lesson, "index.md"))) {
    console.warn(`warning: slides/${lesson} has no handout at docs/${lesson}/index.md`);
  }
  for (const kind of only) {
    const out = join(outDir, kind === "html" ? "index.html" : "slides.pdf");
    const r = spawnSync(marp, [src, "--no-stdin", "-o", out], { cwd: root, stdio: ["ignore", "inherit", "inherit"] });
    if (r.status !== 0) { failed++; continue; }
    if (kind === "html") {
      const html = readFileSync(out, "utf8").replace(/((?:src|href)=")\.\.\/\.\.\/docs\//g, "$1../../");
      writeFileSync(out, html);
    }
    console.log(`built docs/slides/${lesson}/${kind === "html" ? "index.html" : "slides.pdf"}`);
  }
}
process.exit(failed ? 1 : 0);

// tracking: status=draft version=0 assisted=true
