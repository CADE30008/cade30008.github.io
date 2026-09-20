"""Build the live site: only what publish.yaml lists.

The in-progress site is docs/ as it stands, built by zensical.toml. The live
site is a filtered copy of it:

  1. docs/ is copied to .live/docs, leaving out every page not listed in
     publish.yaml, every week folder whose handout isn't listed, and the
     lecture map unless it is listed;
  2. in the pages that remain, <!-- in-progress:start --> ... <!-- in-progress:end -->
     blocks are removed, and any link to a page that was left out becomes plain
     text;
  3. .live/zensical.toml is written from zensical.toml, with the nav cut down to
     the published pages, the live site_url, and the "in progress" label taken
     off the site name;
  4. the site is built into .live/site, and every internal link in it is
     checked. So are the live-site URLs in teaching/blackboard.md, since
     Blackboard links to them.

Exits non-zero if the build fails or any link is broken, so a deploy can't
publish a broken site. Preview the result with `npm run preview:live`.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
LIVE = ROOT / ".live"
IN_PROGRESS = " · in progress"

problems: list[str] = []


def published_pages() -> tuple[set[str], str]:
    cfg = yaml.safe_load((ROOT / "publish.yaml").read_text(encoding="utf-8"))
    pages = set(cfg["pages"])
    for p in pages:
        if not (DOCS / p).exists():
            problems.append(f"publish.yaml lists {p}, which doesn't exist")
    return pages, cfg["site_url"]


def copy_docs(pages: set[str]) -> None:
    """Copy docs/ to .live/docs, leaving out unpublished pages and week folders."""
    shutil.copytree(DOCS, LIVE / "docs", ignore=shutil.ignore_patterns("slides", "downloads"))
    out = LIVE / "docs"
    for d in list(out.iterdir()):
        if d.is_dir() and re.match(r"^w\d\d-", d.name) and f"{d.name}/index.md" not in pages:
            shutil.rmtree(d)
    if "planning/lecture-map.html" not in pages and (out / "planning").exists():
        shutil.rmtree(out / "planning")
    for md in out.rglob("*.md"):
        rel = md.relative_to(out).as_posix()
        if rel.startswith("includes/"):
            continue                      # snippets, appended to every page
        if rel not in pages:
            md.unlink()
    # Built slides and PDFs, for published weeks only.
    for kind in ("slides", "downloads"):
        src = DOCS / kind
        if not src.exists():
            continue
        for item in src.iterdir():
            slug = item.name.split("-handout")[0].split("-example-sheet")[0].split("-solutions")[0]
            if f"{slug}/index.md" in pages:
                dest = out / kind / item.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                (shutil.copytree if item.is_dir() else shutil.copy2)(item, dest)


LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)([^)]*)\)")


def rewrite_pages() -> None:
    """Strip in-progress blocks, and turn links to unpublished pages into text."""
    out = LIVE / "docs"
    for md in out.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        text = re.sub(r"<!-- in-progress:start -->.*?<!-- in-progress:end -->\n?", "", text, flags=re.S)

        def fix(m: re.Match) -> str:
            label, target = m.group(1), m.group(2)
            if re.match(r"^(https?:|mailto:|#)", target):
                return m.group(0)
            path = target.split("#")[0]
            if not path:
                return m.group(0)
            resolved = (md.parent / unquote(path)).resolve()
            if resolved.exists():
                return m.group(0)
            return label                  # unpublished: keep the words, drop the link

        md.write_text(LINK.sub(fix, text), encoding="utf-8")


def nav_entries(block: str, pages: set[str]) -> list[str]:
    """Filter the nav block of zensical.toml to published pages, keeping its order."""
    lines, out, i = block.splitlines(), [], 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^\s*\{ "[^"]+" = \[$', line):          # a section with children
            j = i
            while not re.match(r"^\s*\] \},$", lines[j]):
                j += 1
            children = [c for c in lines[i + 1:j] if (m := re.search(r'= "([^"]+)"', c)) and m.group(1) in pages]
            if children:
                out += [line, *children, lines[j]]
            i = j + 1
            continue
        m = re.search(r'= "([^"]+)" \},$', line)
        if m and m.group(1) in pages:
            out.append(line)
        i += 1
    return out


def write_config(pages: set[str], site_url: str) -> None:
    base = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    start = base.index("nav = [")
    end = base.index("\n]\n", start)
    entries = nav_entries(base[start + len("nav = [") : end], pages)
    text = base[:start] + "nav = [\n" + "\n".join(entries) + base[end:]
    text = re.sub(r'^site_name = "(.*?)"', lambda m: f'site_name = "{m.group(1).replace(IN_PROGRESS, "")}"', text, count=1, flags=re.M)
    text = re.sub(r'^site_url = ".*?"', f'site_url = "{site_url}"', text, count=1, flags=re.M)
    text = text.replace("[project]\n", '[project]\ndocs_dir = "docs"\nsite_dir = "site"\n', 1)
    text = text.replace('pymdownx.snippets.base_path = ["docs"]', 'pymdownx.snippets.base_path = [".live/docs"]')
    tomllib.loads(text)                   # fail here, not in the build, if it's malformed
    (LIVE / "zensical.toml").write_text(text, encoding="utf-8")


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.go: list[str] = []           # links marked { .go }; see javascripts/links.js

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.refs.append(v)
        if tag == "a" and "go" in (d.get("class") or "").split():
            self.go.append(d.get("href") or "")


def resolves(site: Path, page: Path, ref: str) -> bool:
    u = urlparse(ref)
    if u.scheme or u.netloc or ref.startswith(("#", "mailto:", "data:", "javascript:")):
        return True
    path = unquote(u.path)
    if not path:
        return True
    target = (site / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
    target = target.resolve()
    return target.exists() or (target / "index.html").exists()


def check_links(site_url: str) -> None:
    site = LIVE / "site"
    for page in site.rglob("*.html"):
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        for ref in parser.refs:
            if not resolves(site, page, ref):
                problems.append(f"broken link in {page.relative_to(site)}: {ref}")
        # { .go } says "leave the site, do this, come back". On a link that
        # stays here it would draw the eye for nothing, so catch it.
        for ref in parser.go:
            if not urlparse(ref).netloc or urlparse(ref).netloc == urlparse(site_url).netloc:
                problems.append(f"{page.relative_to(site)}: {{ .go }} on a link that doesn't leave the site: {ref}")
    sheet = ROOT / "teaching" / "blackboard.md"
    if sheet.exists():
        for url in sorted(set(re.findall(re.escape(site_url) + r"[\w./#-]*", sheet.read_text(encoding="utf-8")))):
            path = urlparse(url).path.lstrip("/")
            target = site / path
            if not (target.exists() or (target / "index.html").exists()):
                problems.append(f"teaching/blackboard.md links to {url}, which the live site doesn't have")


def main() -> None:
    pages, site_url = published_pages()
    if LIVE.exists():
        shutil.rmtree(LIVE)
    LIVE.mkdir()
    copy_docs(pages)
    rewrite_pages()
    write_config(pages, site_url)
    build = subprocess.run([sys.executable, "-m", "zensical", "build", "-f", str(LIVE / "zensical.toml"), "--clean"],
                           cwd=ROOT, capture_output=True, text=True)
    if build.returncode != 0:
        # Fall back to the zensical executable beside this Python, for installs without a __main__.
        exe = Path(sys.executable).with_name("zensical")
        build = subprocess.run([str(exe), "build", "-f", str(LIVE / "zensical.toml"), "--clean"],
                               cwd=ROOT, capture_output=True, text=True)
    print((build.stdout + build.stderr).strip())
    if build.returncode != 0:
        sys.exit(build.returncode)
    check_links(site_url)
    for p in problems:
        print(f"error    {p}")
    print(f"\nlive site: {len(pages)} pages -> .live/site ({'OK' if not problems else f'{len(problems)} problem(s)'})")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
