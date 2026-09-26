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
    "assisted": "An AI assistant helped draft this at some point. Never goes back to false.",
    "checked": "Optional. When the facts in here that come from outside the repository were last verified.",
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


def tracked() -> tuple[list[Path], list[tuple[Path, str]]]:
    """Every file this covers, and every file it deliberately does not."""
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    keep, skipped = [], []
    for line in out.stdout.splitlines():
        p = Path(line)
        if p.suffix not in COMMENT:
            reason = next((why for pat, why in SKIP if p.match(pat)), None)
            if reason:
                skipped.append((p, reason))
            continue
        if reason := next((why for pat, why in SKIP if p.match(pat)), None):
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
        return {k: parse(v.strip().strip('"')) for k in FIELDS
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
def fingerprint(path: Path) -> str:
    """A hash of the content, with the tracking fields taken out.

    Stamping a file must not invalidate its own sign-off, so the fields this
    script writes are removed before hashing. Trailing space and runs of blank
    lines go too, so reformatting does not read as a change of substance.
    """
    text = (ROOT / path).read_text(encoding="utf-8")
    if has_front_matter(path, text):
        fm = FM.match(text).group(1)
        for k in FIELDS:
            fm = re.sub(rf"^{k}:.*\n", "", fm, flags=re.M)
        text = fm + text[FM.match(text).end():]
    else:
        text = re.sub(rf"^\S*\s*{MARK}.*$\n?", "", text, flags=re.M)
    text = re.sub(r"[ \t]+$", "", text, flags=re.M)
    return hashlib.sha256(re.sub(r"\n{3,}", "\n\n", text).strip().encode()).hexdigest()[:12]


def assisted_paths() -> set[str]:
    """Every path an AI assistant has had a hand in, taken from git.

    Computed rather than declared. Nobody maintains a disclosure field on two
    hundred files by hand, and git already knows: the assistant appears as a
    Co-Authored-By trailer on the commits it helped make.

    git's own author field is no use here. Every commit in this repository is
    authored by its owner with the assistant in a trailer, so `git blame`
    attributes all of it to one person and never shows the trailer. That is
    also the answer to "who was the last author": the question git answers
    badly, and the question that matters, are not the same one. Who is
    responsible is the approver in review.lock.json.

    Monotonic on purpose. A later edit by a person does not un-draft what came
    before it, so this never goes back to false.
    """
    out = subprocess.run(
        ["git", "log", "--format=%x00%(trailers:key=Co-Authored-By,valueonly,separator=;)", "--name-only"],
        cwd=ROOT, capture_output=True, text=True, check=True)
    seen, ai = set(), False
    for line in out.stdout.splitlines():
        if line.startswith("\0"):
            ai = bool(line[1:].strip())
        elif line.strip() and ai:
            seen.add(line.strip())
    return seen


def load_lock() -> dict:
    return json.loads(LOCK.read_text(encoding="utf-8")) if LOCK.exists() else {}


def save_lock(lock: dict) -> None:
    LOCK.write_text(json.dumps(dict(sorted(lock.items())), indent=2) + "\n", encoding="utf-8")


def resolve(path: Path, meta: dict, lock: dict) -> tuple[str, int]:
    """The effective status and version: what the file declares, checked."""
    entry = lock.get(str(path))
    declared = meta.get("status") if meta.get("status") in DECLARED else "draft"
    if not entry:
        return declared, 0
    if entry["fingerprint"] == fingerprint(path):
        return "approved", entry["version"]
    return "lapsed", entry["version"]


# ----------------------------------------------------------------- commands
def report(stamp: bool) -> int:
    files, skipped = tracked()
    lock, ai = load_lock(), assisted_paths()
    counts, lapsed, changed, unstamped = {}, [], [], []
    for p in files:
        meta = read_meta(p)
        status, version = resolve(p, meta, lock)
        counts[status] = counts.get(status, 0) + 1
        if status == "lapsed":
            lapsed.append(p)
        want = {"status": status, "version": version,
                "assisted": str(p) in ai or bool(meta.get("assisted")), "checked": meta.get("checked")}
        if stamp:
            if write_meta(p, want):
                changed.append(p)
        elif {k: meta.get(k) for k in ("status", "version", "assisted")} != {
                k: want[k] for k in ("status", "version", "assisted")}:
            unstamped.append(p)

    print(f"{len(files)} files tracked, {len(skipped)} not:")
    for state in STATES:
        if n := counts.get(state):
            print(f"  {n:4d}  {state:9s} {STATES[state]}")
    by_reason: dict[str, int] = {}
    for _, why in skipped:
        by_reason[why] = by_reason.get(why, 0) + 1
    for why, n in sorted(by_reason.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {'':9s} not tracked: {why}")

    if lapsed:
        print(f"\n{len(lapsed)} approved and edited since; re-approve or revert:")
        for p in lapsed:
            print(f"  {p}")
    if changed:
        print(f"\nstamped {len(changed)} files")
    if unstamped:
        print(f"\n{len(unstamped)} headers are out of date; run `npm run track -- --stamp`")
        return 1
    return 0


def approve(paths: list[str], by: str) -> int:
    lock = load_lock()
    for raw in paths:
        p = Path(raw).resolve().relative_to(ROOT) if Path(raw).is_absolute() else Path(raw)
        if not (ROOT / p).exists():
            print(f"error    no such file: {p}")
            return 1
        entry = lock.get(str(p), {"version": 0})
        lock[str(p)] = {"fingerprint": fingerprint(p), "version": entry["version"] + 1,
                        "approver": by, "date": date.today().isoformat()}
        print(f"approved {p} as version {lock[str(p)]['version']}, by {by}")
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
