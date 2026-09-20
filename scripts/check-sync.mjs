// Keep lecture slides and handouts in step.
//
// The contract (see AGENTS.md):
//   - handout headings carry stable IDs:          ## The lift equation {#lift-equation}
//   - handout-only sections add a class:          ## Further reading {#reading .no-slides}
//   - each content slide cites what it covers:    <!-- handout: lift-equation -->
//   - sync.lock.json records, per section, fingerprints of the handout text and
//     of the slides citing it, as they were when someone last confirmed they match.
//
// Usage:
//   node scripts/check-sync.mjs            report problems (exit 1 on errors)
//   node scripts/check-sync.mjs --json     the same, machine-readable
//   node scripts/check-sync.mjs --strict   also exit 1 on warnings
//   node scripts/check-sync.mjs --accept   record the current state as in sync
//
// Errors: citations of missing sections, figures or snippets that don't exist.
// Warnings: uncovered sections, numbers on a slide that its cited sections don't
// contain, and drift since the last accepted sync.
import { createHash } from "node:crypto";
import { existsSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join, relative, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const docs = join(root, "docs");
const lockPath = join(root, "sync.lock.json");
const args = new Set(process.argv.slice(2));

const hash = (text) =>
  createHash("sha256").update(text.replace(/[ \t]+$/gm, "").replace(/\n{3,}/g, "\n\n").trim()).digest("hex").slice(0, 12);

// ------------------------------------------------------------------ handout
function parseHandout(file) {
  const text = readFileSync(file, "utf8").replace(/^---\n[\s\S]*?\n---\n/, "");
  const lines = text.split("\n");
  const sections = new Map();
  let current = null;
  let inFence = false;
  for (const line of lines) {
    if (/^\s*(```|~~~)/.test(line)) inFence = !inFence;
    const m = !inFence && line.match(/^(#{1,6})\s+(.*?)\s*\{([^}]*)\}\s*$/);
    const plain = !inFence && /^#{1,6}\s/.test(line);
    if (m) {
      const attrs = m[3];
      const id = (attrs.match(/#([\w-]+)/) || [])[1];
      current = id ? { id, title: m[2], noSlides: /\.no-slides\b/.test(attrs), lines: [line] } : null;
      if (current) sections.set(id, current);
    } else if (plain) {
      current = null;               // a heading without an ID ends the previous section
    } else if (current) {
      current.lines.push(line);
    }
  }
  for (const s of sections.values()) s.text = s.lines.join("\n");
  return { text, sections };
}

// -------------------------------------------------------------------- slides
function parseDeck(file) {
  const text = readFileSync(file, "utf8").replace(/^---\n[\s\S]*?\n---\n/, "");
  const chunks = text.split(/^---\s*$/m);
  return chunks.map((body, i) => {
    const cites = [];
    for (const m of body.matchAll(/<!--\s*handout:\s*\[?([^\]>]*?)\]?\s*-->/g)) {
      cites.push(...m[1].split(",").map((s) => s.trim()).filter(Boolean));
    }
    return { number: i + 1, body, cites };
  });
}

const NUMBER = /\d+\.\d+|\d{2,}/g;
function numbersIn(markdown) {
  const cleaned = markdown
    .replace(/<!--[\s\S]*?-->/g, " ")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, " ")      // images, including Marp size hints
    .replace(/<[^>]+>/g, " ")                   // HTML tags and their attributes
    .replace(/https?:\/\/\S+/g, " ");
  return new Set(cleaned.match(NUMBER) || []);
}

// ------------------------------------------------------------ path checking
function assetRefs(markdown) {
  const refs = [];
  for (const m of markdown.matchAll(/!\[[^\]]*\]\(([^)\s]+)[^)]*\)/g)) refs.push({ kind: "markdown", path: m[1] });
  for (const m of markdown.matchAll(/<(?:img|iframe|source|video)\b[^>]*\bsrc="([^"]+)"/g)) refs.push({ kind: "html", path: m[1] });
  for (const m of markdown.matchAll(/^\s*--8<--\s+"([^"]+)"/gm)) refs.push({ kind: "snippet", path: m[1] });
  return refs.filter((r) => !/^(https?:|data:|#)/.test(r.path)).map((r) => ({ ...r, path: r.path.split(/[?#]/)[0] }));
}

function checkHandoutAssets(file, errors) {
  const md = readFileSync(file, "utf8");
  const fileDir = dirname(file);
  // Raw HTML resolves against the page URL: docs/x/index.md -> /x/, docs/x/y.md -> /x/y/
  const pageDir = basename(file) === "index.md" ? fileDir : join(fileDir, basename(file, ".md"));
  for (const r of assetRefs(md)) {
    const base = r.kind === "markdown" ? fileDir : r.kind === "html" ? pageDir : docs;
    const target = resolve(base, r.path);
    if (!existsSync(target)) errors.push(`${relative(root, file)}: ${r.kind} reference not found: ${r.path}`);
  }
}

// ---------------------------------------------------------------------- main
const lessons = readdirSync(join(root, "slides"), { withFileTypes: true })
  .filter((d) => d.isDirectory() && existsSync(join(root, "slides", d.name, "index.md")))
  .map((d) => d.name);
const lock = existsSync(lockPath) ? JSON.parse(readFileSync(lockPath, "utf8")) : {};
const errors = [];
const warnings = [];
const state = {};

for (const md of readdirSync(docs, { recursive: true })) {
  if (String(md).endsWith(".md")) checkHandoutAssets(join(docs, String(md)), errors);
}

// A week whose handout says `status: draft` has no content to keep in sync yet:
// checking it would bury real drift under warnings about scaffolding. Remove
// that line from the front matter when the week is written, and the week is
// checked from then on. `--all` checks drafts too.
const isDraft = (file) => /^---\n[\s\S]*?^status:\s*draft\s*$/m.test(readFileSync(file, "utf8"));
const drafts = [];

for (const lesson of lessons) {
  const handoutFile = join(docs, lesson, "index.md");
  const deckFile = join(root, "slides", lesson, "index.md");
  if (!existsSync(handoutFile)) {
    errors.push(`${lesson}: slides exist but there is no handout at docs/${lesson}/index.md`);
    continue;
  }
  if (isDraft(handoutFile) && !args.has("--all")) {
    drafts.push(lesson);
    continue;
  }
  const handout = parseHandout(handoutFile);
  const slides = parseDeck(deckFile);
  state[lesson] = {};

  for (const r of assetRefs(readFileSync(deckFile, "utf8"))) {
    if (!existsSync(resolve(dirname(deckFile), r.path))) {
      errors.push(`slides/${lesson}: ${r.kind} reference not found: ${r.path}`);
    }
  }

  const citedBy = new Map();
  for (const slide of slides) {
    for (const id of slide.cites) {
      if (!handout.sections.has(id)) {
        errors.push(`slides/${lesson} slide ${slide.number}: cites #${id}, which the handout doesn't have`);
        continue;
      }
      if (!citedBy.has(id)) citedBy.set(id, []);
      citedBy.get(id).push(slide);
    }
    if (!slide.cites.length) continue;
    const sectionText = slide.cites.filter((id) => handout.sections.has(id)).map((id) => handout.sections.get(id).text).join("\n");
    const inSections = numbersIn(sectionText);
    const inHandout = numbersIn(handout.text);
    for (const n of numbersIn(slide.body)) {
      if (inSections.has(n)) continue;
      warnings.push(inHandout.has(n)
        ? `slides/${lesson} slide ${slide.number}: ${n} isn't in the cited section (${slide.cites.join(", ")}), though the handout has it elsewhere`
        : `slides/${lesson} slide ${slide.number}: ${n} doesn't appear anywhere in the handout`);
    }
  }

  for (const [id, section] of handout.sections) {
    const citing = citedBy.get(id) || [];
    if (!citing.length) {
      if (!section.noSlides) warnings.push(`${lesson}: handout section #${id} has no slides (mark it {#${id} .no-slides} if that's intended)`);
      continue;
    }
    const now = { handout: hash(section.text), slides: hash(citing.map((s) => s.body).join("\n---\n")), slideNumbers: citing.map((s) => s.number) };
    state[lesson][id] = now;
    const then = lock[lesson]?.[id];
    if (!then) {
      warnings.push(`${lesson} #${id}: not yet accepted as in sync (run npm run sync:accept after checking)`);
    } else if (then.handout !== now.handout || then.slides !== now.slides) {
      const side = then.handout !== now.handout && then.slides !== now.slides ? "handout and slides both"
        : then.handout !== now.handout ? "handout" : "slides";
      const todo = side === "handout" ? `review slide(s) ${now.slideNumbers.join(", ")}`
        : side === "slides" ? `check handout section #${id} still matches` : "review both";
      warnings.push(`${lesson} #${id}: ${side} changed since last sync; ${todo}`);
    }
  }
}

if (args.has("--accept")) {
  writeFileSync(lockPath, JSON.stringify(state, null, 2) + "\n");
  console.log(`sync.lock.json updated for ${Object.keys(state).join(", ")}`);
}

if (args.has("--json")) {
  console.log(JSON.stringify({ errors, warnings }, null, 2));
} else if (!args.has("--accept")) {
  for (const e of errors) console.log(`error    ${e}`);
  for (const w of warnings) console.log(`warning  ${w}`);
  const checked = lessons.length - drafts.length;
  const draftNote = drafts.length ? `; ${drafts.length} in draft, not checked (--all to include them)` : "";
  console.log(`\n${errors.length} error(s), ${warnings.length} warning(s) across ${checked} lesson(s)${draftNote}`);
}
process.exit(errors.length || (args.has("--strict") && warnings.length) ? 1 : 0);
