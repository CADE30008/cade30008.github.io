"""Track what state every source file is in, and who signed it off.

Three questions this answers, which nothing else in the repository does:

  how far has this got?     status
  has a person signed it?   version, and review.lock.json
  did a machine draft it?   assisted

The split that makes it trustworthy: **people declare what they judge, and this
script computes what it can check.** A person moves a file along
outline -> scoped -> draft, because only a person can say whether the content is
a first pass or still a plan. `--approve` is also a person's act, and it records
a fingerprint of what they approved. From then on the fingerprint is the truth:
edit an approved file and this marks it `lapsed` on the next run, without asking
anyone. A word in a header is a claim; a fingerprint is a check.

That is also why `published` is not one of the states. Publication is decided in
publish.yaml, by a person, and a second place to say it would be a second place
to be wrong. STATUS.md already joins the two.

Usage:
  npm run track                     report, and exit 1 if anything is wrong
  npm run track -- --stamp          write the headers (safe to run any time)
  npm run track -- --set draft PATH declare how far a file has got
  npm run approve -- PATH...        record a sign-off. **People only.**

`--approve` is the one command an AI assistant must never run, for the same
reason as `npm run sync:accept`: it is the human check, and a machine running it
would be signing off its own work. See AGENTS.md.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "review.lock.json"

# --------------------------------------------------------------- the words
# The whole vocabulary is here. Renaming a state means editing this table and
# running `npm run track -- --stamp`; nothing else in the repository spells
# these out, so nothing else can disagree with them.
DECLARED = {
    "outline": "Structure only. Headings, slots and scaffolding; no content, and the topic carries no commitment.",
    "scoped": "Structure agreed by a person. What it covers is settled; nothing is written.",
    "draft": "Content written, first pass, by whatever hand. Not signed off.",
}
COMPUTED = {
    "approved": "A person has read it and signed it off. The content still matches what they signed.",
    "lapsed": "Was approved, and has been edited since. The sign-off no longer covers what is here.",
}
STATES = {**DECLARED, **COMPUTED}

FIELDS = {
    "status": "How far this has got, and whether the sign-off still holds.",
    "version": "Sign-offs so far. 0 until a person approves it, then 1, 2, 3 as it is approved again.",
    "parts": "Only on piecewise pages: entries still needing a person's eye, over the number there are.",
    "checked": "Optional. When the facts in here that come from outside the repository were last verified.",
}

# Fields that used to be here. The stamper removes them, so a retired field
# leaves the repository rather than lingering on whatever was not touched since.
#
# `assisted` recorded that an AI assistant had a hand in a file, computed from
# git's Co-Authored-By trailers. It was true for all 188 files on the day it
# was added, so it distinguished nothing, and the disclosure that matters is
# the note AGENTS.md already requires in the document itself.
RETIRED = ("assisted",)

# ----------------------------------------------------------- piecewise pages
# A page that is a hundred independent entries rather than one argument. Change
# one glossary term and only that term needs reading again; making the whole
# page lapse would mean re-reading ninety-seven definitions to find the one that
# moved, which is the sort of check people stop doing.
#
# So these are fingerprinted per entry. The value is the element to split on.
# `rows` means every table row outside the header, keyed by its first cell.
PIECEWISE = {
    "docs/glossary.md": "rows",
    "docs/notation.md": "rows",
}

# ------------------------------------------------------------- what to track
# How the header is written, by extension. A one-line marker rather than a
# block: it survives at the bottom of any file, greps in one pass, and shows up
# in a diff as one line rather than five.
COMMENT = {".m": "%", ".py": "#", ".yaml": "#", ".yml": "#", ".toml": "#",
           ".mjs": "//", ".js": "//", ".css": "/*", ".md": "<!--"}
CLOSE = {"/*": " */", "<!--": " -->"}
MARK = "tracking:"

# Left alone, with the reason, because a header would do harm or cannot be
# written at all. Reported rather than silently skipped: a tracking system whose
# gaps are invisible is worse than none.
SKIP = [
    ("private/**", "assessment material, never committed"),
    ("theme/**", "a submodule; changed in its own repository"),
    ("node_modules/**", "not ours"),
    ("docs/slides/**", "built by npm run slides"),
    ("site/**", "built by npm run site"),
    (".live/**", "built by npm run live"),
    ("STATUS.md", "written by npm run curriculum"),
    ("docs/curriculum.md", "written by npm run curriculum"),
    ("docs/staff/lecture-map.html", "written by npm run curriculum"),
    ("docs/**/figures/*.svg", "drawn by a script in models/ or by npm run curriculum"),
    ("docs/figures/*.svg", "drawn by npm run curriculum"),
    ("docs/includes/**", "appended to every page, so a marker here lands in every built page"),
    ("sync.lock.json", "written by npm run check"),
    ("review.lock.json", "written by this script"),
    ("**/*.json", "JSON has no comment syntax"),
    ("**/*.slx", "binary; Simulink model properties are not diffable"),
    ("**/*.mat", "binary"),
    ("**/*.csv", "data; a header line would change what parsers read"),
    ("**/*.jpg", "binary"), ("**/*.png", "binary"),
    ("**/*.svg", "drawn, not written"),
    ("**/*.txt", "single values read by scripts"),
]


def skip_reason(path: Path) -> str | None:
    return next((why for pat, why in SKIP if path.match(pat)), None)


def tracked() -> tuple[list[Path], list[tuple[Path, str]]]:
    """Every file this covers, and every file it deliberately does not."""
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    keep, skipped = [], []
    for line in out.stdout.splitlines():
        p = Path(line)
        if p.suffix not in COMMENT:
            if reason := skip_reason(p):
                skipped.append((p, reason))
            continue
        if reason := skip_reason(p):
            skipped.append((p, reason))
        else:
            keep.append(p)
    return sorted(keep), sorted(skipped)


# ------------------------------------------------------------------ headers
FM = re.compile(r"\A---\n(.*?\n)---\n", re.S)


def has_front_matter(path: Path, text: str) -> bool:
    """Front matter where the site already reads it; a comment everywhere else.

    Adding front matter to README.md would put a metadata table at the top of
    what people see on GitHub, which is a visible cost for an invisible field.
    So the rule is: if a file already carries front matter, the fields go in it.
    """
    return path.suffix == ".md" and bool(FM.match(text))


def marker(path: Path, meta: dict) -> str:
    open_ = COMMENT[path.suffix]
    body = " ".join(f"{k}={fmt(v)}" for k, v in meta.items() if v not in (None, ""))
    return f"{open_} {MARK} {body}{CLOSE.get(open_, '')}"


def fmt(v) -> str:
    return "true" if v is True else "false" if v is False else str(v)


def parse(v: str):
    if v in ("true", "false"):
        return v == "true"
    return int(v) if v.isdigit() else v


def read_meta(path: Path) -> dict:
    text = (ROOT / path).read_text(encoding="utf-8")
    if has_front_matter(path, text):
        fm = FM.match(text).group(1)
        return {k: parse(v.strip().strip('"')) for k in (*FIELDS, *RETIRED)
                for v in re.findall(rf"^{k}:\s*(.*)$", fm, re.M)}
    if m := re.search(rf"^\S*\s*{MARK}\s*(.*?)(?:\s*\*/|\s*-->)?$", text, re.M):
        return {k: parse(v) for k, v in (kv.split("=", 1) for kv in m.group(1).split() if "=" in kv)}
    return {}


def write_meta(path: Path, meta: dict) -> bool:
    """Write the fields back. Returns whether the file changed."""
    full = ROOT / path
    text = old = full.read_text(encoding="utf-8")
    if has_front_matter(path, text):
        fm = FM.match(text).group(1)
        new_fm = fm
        for k, v in meta.items():
            if v in (None, ""):
                new_fm = re.sub(rf"^{k}:.*\n", "", new_fm, flags=re.M)
                continue
            line = f"{k}: {fmt(v)}"
            new_fm = (re.sub(rf"^{k}:.*$", line, new_fm, flags=re.M) if re.search(rf"^{k}:", new_fm, re.M)
                      else new_fm.rstrip("\n") + f"\n{line}\n")
        text = f"---\n{new_fm}---\n" + text[FM.match(text).end():]
    else:
        line = marker(path, meta)
        text = (re.sub(rf"^\S*\s*{MARK}.*$", line, text, flags=re.M) if re.search(rf"^\S*\s*{MARK}", text, re.M)
                else text.rstrip("\n") + f"\n\n{line}\n")
    if text != old:
        full.write_text(text, encoding="utf-8")
    return text != old


# -------------------------------------------------------------- fingerprints
def without_meta(path: Path) -> str:
    """The file's content with the tracking fields taken out.

    Stamping a file must not invalidate its own sign-off, so everything this
    script writes comes out before anything is hashed. That caught a real one:
    the `parts` count is written into the front matter, so a page whose entries
    had just been approved would immediately report its own prose as changed.
    """
    text = (ROOT / path).read_text(encoding="utf-8")
    if has_front_matter(path, text):
        fm = FM.match(text).group(1)
        for k in FIELDS:
            fm = re.sub(rf"^{k}:.*\n", "", fm, flags=re.M)
        return fm + text[FM.match(text).end():]
    return re.sub(rf"^\S*\s*{MARK}.*$\n?", "", text, flags=re.M)


def fingerprint(path: Path) -> str:
    """A hash of the whole file, for anything that is not piecewise."""
    return digest(without_meta(path))


def load_lock() -> dict:
    return json.loads(LOCK.read_text(encoding="utf-8")) if LOCK.exists() else {}


def save_lock(lock: dict) -> None:
    LOCK.write_text(json.dumps(dict(sorted(lock.items())), indent=2) + "\n", encoding="utf-8")


ROW = re.compile(r"^\|(?!\s*-+\s*\|)(.+)\|\s*$", re.M)


def parts_of(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    """A piecewise page's entries: fingerprint by key, and the name to show.

    The key is a slug, because it has to stay the same in the lock while the
    entry is edited. The label is the first cell as written, because "r-rs" in
    a report of what to go and read is no help to anyone.

    Table rows, keyed by the first cell with the markup stripped, plus one
    `(page)` entry for everything that is not a row. Without that last one the
    prose around the tables would be the only unchecked thing on the page.

    A repeated key would silently drop an entry, so a duplicate is kept under a
    numbered name rather than overwriting: two glossary terms with the same
    name is a fault to see, not one to hide.
    """
    text = without_meta(path)
    parts, labels, rest = {}, {}, text
    for m in ROW.finditer(text):
        cells = [c.strip() for c in m.group(1).split("|")]
        name = re.sub(r"[^a-z0-9]+", "-", re.sub(r"[*`\\()$]|\\mathrm|\[|\]", "", cells[0]).lower()).strip("-")
        if not name or name in ("term", "symbol"):     # the header row
            continue
        key, n = name, 2
        while key in parts:
            key, n = f"{name}-{n}", n + 1
        parts[key] = digest(m.group(0))
        labels[key] = cells[0]
        rest = rest.replace(m.group(0), "")
    parts["(page)"] = digest(rest)
    labels["(page)"] = "the prose around the tables"
    return parts, labels


def digest(text: str) -> str:
    text = re.sub(r"[ \t]+$", "", text, flags=re.M)
    return hashlib.sha256(re.sub(r"\n{3,}", "\n\n", text).strip().encode()).hexdigest()[:12]


def resolve(path: Path, meta: dict, lock: dict) -> tuple[str, int, list[str]]:
    """The effective status, version, and which entries still need an eye.

    For an ordinary file the third value is empty and the whole file is one
    thing. For a piecewise page it names the entries whose fingerprint has
    moved since they were signed, which is the only part a person has to read.
    """
    entry = lock.get(str(path))
    declared = meta.get("status") if meta.get("status") in DECLARED else "draft"
    if str(path) in PIECEWISE:
        now, _ = parts_of(path)
        signed = (entry or {}).get("parts", {})
        stale = sorted(k for k, v in now.items() if signed.get(k) != v)
        gone = sorted(k for k in signed if k not in now)
        if not entry:
            return declared, 0, stale
        if not stale and not gone:
            return "approved", entry["version"], []
        return "lapsed", entry["version"], stale + [f"{k} (removed)" for k in gone]
    if not entry:
        return declared, 0, []
    if entry["fingerprint"] == fingerprint(path):
        return "approved", entry["version"], []
    return "lapsed", entry["version"], []


# ----------------------------------------------------------------- commands
@functools.cache
def lecture_names() -> dict[str, str]:
    """Folder slug -> the name a person uses, from curriculum/weeks.yaml.

    Read rather than restated, so this cannot start calling something Lecture 5
    after the curriculum has moved it.
    """
    import yaml
    weeks = yaml.safe_load((ROOT / "curriculum" / "weeks.yaml").read_text(encoding="utf-8"))["weeks"]
    out, n = {}, 0
    for w in weeks:
        if w["kind"] == "lecture":
            n += 1
            out[w["slug"]] = f"Lecture {n}"
        else:
            out[w["slug"]] = w["title"]
    return out


def group_of(path: Path) -> str:
    """Which chunk a file belongs to.

    A lecture is its handout, its deck, its sheets, its code and its run sheet,
    wherever those sit in the tree, because that is the unit a person reviews.
    Everything else falls into a few named groups rather than one "other": the
    laboratory and the reference pages are also reviewed as a unit.
    """
    # Match on the wNN prefix rather than the whole folder name, so a run sheet
    # at docs/staff/w01-run-sheet.md lands with its lecture instead of becoming
    # a group of one.
    by_number = {slug[:3]: slug for slug in lecture_names()}
    for part in path.parts:
        if (m := re.match(r"(w\d\d)-", part)) and m.group(1) in by_number:
            return by_number[m.group(1)]
    for folder, name in (("laboratory", "laboratory"), ("preparing", "preparing"),
                         ("staff", "staff"), ("teaching", "teaching"), ("models", "models"),
                         ("scripts", "tooling"), ("drive", "drive"), ("curriculum", "curriculum"),
                         ("diagnostics", "diagnostics"), ("examples", "examples")):
        if folder in path.parts:
            return name
    return "reference" if path.parts[0] == "docs" else "repository"


def survey(lock: dict) -> tuple[dict, list, list]:
    """Every tracked file's state, grouped by lecture."""
    files, skipped = tracked()
    groups: dict[str, list] = {}
    for path in files:
        meta = read_meta(path)
        status, version, stale = resolve(path, meta, lock)
        groups.setdefault(group_of(path), []).append(
            {"path": path, "meta": meta, "status": status, "version": version, "stale": stale})
    return groups, files, skipped


BAR = {"outline": ".", "scoped": "-", "draft": "o", "approved": "#", "lapsed": "!"}


def unapproved_published(lock: dict) -> list[tuple[Path, str, list[str]]]:
    """Published pages that nobody has signed off, in the order they are listed.

    publish.yaml's order is the order a person would read them: the front of
    the site, then a lecture's handout before its sheets. Sorting alphabetically
    would scatter that.
    """
    import yaml
    cfg = yaml.safe_load((ROOT / "publish.yaml").read_text(encoding="utf-8"))
    out = []
    for rel in cfg["pages"]:
        path = Path("docs") / rel
        if not (ROOT / path).exists():
            continue
        # A generated page carries no sign-off of its own: its content comes
        # from sources that are themselves tracked, and approving output that
        # the next build rewrites would mean nothing. The gate bites upstream.
        if skip_reason(path):
            continue
        status, _, stale = resolve(path, read_meta(path), lock)
        if status != "approved":
            out.append((path, status, stale))
    return out


def report(stamp: bool) -> int:
    lock = load_lock()
    groups, files, skipped = survey(lock)
    counts, changed, unstamped, needs_eye = {}, [], [], []

    for items in groups.values():
        for it in items:
            counts[it["status"]] = counts.get(it["status"], 0) + 1
            if it["status"] == "lapsed" or (it["stale"] and it["version"]):
                needs_eye.append(it)
            want = {"status": it["status"], "version": it["version"],
                    "parts": (f"{len(it['stale'])}/{len(parts_of(it['path'])[0])}"
                              if str(it["path"]) in PIECEWISE else None),
                    "checked": it["meta"].get("checked"),
                    **{k: None for k in RETIRED}}
            if stamp:
                if write_meta(it["path"], want):
                    changed.append(it["path"])
            elif any(it["meta"].get(k) is not None for k in RETIRED) or \
                    {k: it["meta"].get(k) for k in ("status", "version", "parts")} != {
                        k: want[k] for k in ("status", "version", "parts")}:
                unstamped.append(it["path"])

    # The course, a line per lecture. One character per file, in the order the
    # files come, so a lecture that is all scaffolding and one that is signed
    # off do not look alike at a glance.
    names = lecture_names()
    print("The course, by lecture:\n")
    rows = []
    for name in sorted(groups, key=lambda g: (not g.startswith("w"), g)):
        items = groups[name]
        by: dict[str, int] = {}
        for i in items:
            by[i["status"]] = by.get(i["status"], 0) + 1
        rows.append((names.get(name, name), name if name in names else "",
                     "".join(BAR[i["status"]] for i in items),
                     ", ".join(f"{n} {st}" for st, n in
                               sorted(by.items(), key=lambda x: list(STATES).index(x[0])))))
    w1 = max(len(r[0]) for r in rows)
    w2 = max(len(r[2]) for r in rows)
    for title, slug, bar, summary in rows:
        print(f"  {title:{w1}s}  {bar:{w2}s}  {summary}")
    print(f"\n  key: {'   '.join(f'{c} {st}' for st, c in BAR.items())}")

    print(f"\n{len(files)} files tracked, {len(skipped)} not:")
    for state in STATES:
        if n := counts.get(state):
            print(f"  {n:4d}  {state:9s} {STATES[state]}")
    by_reason: dict[str, int] = {}
    for _, why in skipped:
        by_reason[why] = by_reason.get(why, 0) + 1
    for why, n in sorted(by_reason.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {'':9s} not tracked: {why}")

    if needs_eye:
        print(f"\nNeeds a person's eye ({len(needs_eye)}):")
        for it in needs_eye:
            if it["stale"]:
                labels = parts_of(it["path"])[1]
                shown = [labels.get(k, k) for k in it["stale"][:6]]
                more = f", and {len(it['stale']) - 6} more" if len(it["stale"]) > 6 else ""
                print(f"  {it['path']}: {len(it['stale'])} of "
                      f"{len(parts_of(it['path'])[0])} entries")
                print(f"      {'; '.join(shown)}{more}")
            else:
                print(f"  {it['path']}: edited since it was signed off")

    # What the live build is waiting on. Publication needs two decisions from a
    # person, publish.yaml and a sign-off, and this is the second one's queue.
    if blocking := unapproved_published(lock):
        print(f"\nBlocking the live site ({len(blocking)}), in review order:")
        for path, status, stale in blocking:
            note = f"  ({len(stale)} of its entries)" if stale else ""
            print(f"  {status:8s} {path}{note}")
        print("\n  npm run approve -- --by \"Your Name\" \\\n    "
              + " \\\n    ".join(str(b[0]) for b in blocking))

    if changed:
        print(f"\nstamped {len(changed)} files")
    if unstamped:
        print(f"\n{len(unstamped)} headers are out of date; run `npm run track -- --stamp`")
        return 1
    return 0


def approve(paths: list[str], by: str) -> int:
    """Record a sign-off.

    A piecewise page can be signed whole or one entry at a time: pass
    `docs/glossary.md` for all of it, or `docs/glossary.md:gain-margin` for the
    one entry that moved. Either way the version goes up, because a sign-off
    happened; what differs is how much of the page it covers.
    """
    lock = load_lock()
    for raw in paths:
        raw, _, part = raw.partition(":")
        path = Path(raw).resolve().relative_to(ROOT) if Path(raw).is_absolute() else Path(raw)
        if not (ROOT / path).exists():
            print(f"error    no such file: {path}")
            return 1
        key = str(path)
        entry = lock.get(key, {"version": 0})
        entry = {**entry, "version": entry["version"] + 1, "approver": by,
                 "date": date.today().isoformat()}
        if key in PIECEWISE:
            now, labels = parts_of(path)
            if part:
                if part not in now:
                    print(f"error    {path} has no entry {part!r}; "
                          f"npm run track names the ones that need it")
                    return 1
                entry["parts"] = {**entry.get("parts", {}), part: now[part]}
                print(f"approved {path}: {labels[part]}, as version {entry['version']}, by {by}")
            else:
                # Entries that have gone are dropped rather than kept: a
                # sign-off on a page that no longer has them means nothing.
                entry["parts"] = now
                print(f"approved {path}: all {len(now)} entries, as version {entry['version']}, by {by}")
        else:
            entry["fingerprint"] = fingerprint(path)
            print(f"approved {path} as version {entry['version']}, by {by}")
        lock[key] = entry
    save_lock(lock)
    return report(stamp=True)


def declare(status: str, paths: list[str]) -> int:
    if status not in DECLARED:
        print(f"error    {status!r} is not something a person declares; "
              f"pick one of {', '.join(DECLARED)}")
        return 1
    for raw in paths:
        p = Path(raw)
        meta = read_meta(p)
        write_meta(p, {**meta, "status": status})
        print(f"{p}: {status}")
    return report(stamp=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stamp", action="store_true", help="write the headers")
    ap.add_argument("--approve", nargs="+", metavar="PATH", help="record a sign-off (people only)")
    ap.add_argument("--by", help="who is approving; required with --approve")
    ap.add_argument("--set", nargs="+", metavar=("STATUS", "PATH"), help="declare how far a file has got")
    a = ap.parse_args()
    if a.approve:
        if not a.by:
            print("error    --approve needs --by NAME: a sign-off with no name is not one")
            sys.exit(1)
        sys.exit(approve(a.approve, a.by))
    if a.set:
        sys.exit(declare(a.set[0], a.set[1:]))
    sys.exit(report(a.stamp))


if __name__ == "__main__":
    main()

# tracking: status=draft version=0
