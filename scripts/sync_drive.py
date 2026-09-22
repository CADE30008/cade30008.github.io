"""Publish the student files to MATLAB Drive, and stamp them with a version.

Students are given a link to one Drive folder, not to this repository, so the
files have to be copied there. Doing it by hand is how the copies drift, so it
is a script.

    .venv/bin/python scripts/sync_drive.py            # copy, keep the version
    .venv/bin/python scripts/sync_drive.py --bump     # copy and bump the version
    .venv/bin/python scripts/sync_drive.py --check    # report drift, copy nothing

The version is one number for the whole student folder, in VERSION.txt at its
root and in each README's header. Students are told to check it against the
site before each laboratory session, so it has to change whenever the files
do, and it has to be visible without opening anything.

Versions are `<year>.<n>`: the academic year the material is for, and a
counter that starts at 1 each year. Not semantic versioning, because nothing
here has an API; the question a student is answering is only "is mine the
current one?".

Recorded data is forward compatible, deliberately. A recording made under
2026.1 still fits under 2026.4, because the loaders accept the laboratory's
own s_save layout and that is fixed by the rig rather than by us. Scripts may
change; what students measured does not go stale.
"""

from __future__ import annotations

import argparse
import datetime as dt
import filecmp
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRIVE = Path.home() / "MATLAB-Drive" / "Teaching" / "Control 2026" / "cade30008-students"

# The READMEs a student reads are authored in drive/, so they are in version
# control rather than living only in a synced folder on one laptop. The code
# is not duplicated there: it has one home under docs/, because the site and
# the Drive hand out the same files.
AUTHORED = ROOT / "drive"

# Where each student file comes from. Repo path -> path inside the Drive folder.
BUNDLES: dict[str, list[tuple[Path, str]]] = {
    "w01-design-cycle": [
        (AUTHORED / "w01-design-cycle/README.md", "README.md"),
        *[(ROOT / "docs/w01-design-cycle/code" / f, f) for f in (
            "s1_identify.m", "s2_tune.m", "tune_sliders.m", "submit_gains.m",
            "gain_form_url.m", "gain_form.json",
            "heli_check_one.m", "heli_plant.m", "heli_envelope.m",
            "elevation_plant.json",
        )],
        (ROOT / "docs/w01-design-cycle/data/elevation-step.mat", "data/elevation-step.mat"),
        (ROOT / "docs/w01-design-cycle/data/README.md", "data/README.md"),
    ],
    "lab-quanser": [
        (AUTHORED / "lab-quanser/README.md", "README.md"),
        *[(ROOT / "docs/laboratory/code" / f, f) for f in (
            "lab1_fit.m", "lab2_3dof.m", "lab3_statespace.m", "heli3d_model.m",
            "fit_second_order.m",
            "heli_check_one.m", "heli_plant.m", "heli_envelope.m",
            "elevation_plant.json",
        )],
    ],
}

# The version is kept in the repository and copied out, so that what is live
# is visible in a diff rather than only in a synced folder.
VERSION_FILE = ROOT / "drive" / "VERSION.txt"

# The staff test kit. Authored here for the same reason as everything else:
# a script that exists only in a synced folder is part of one laptop rather
# than part of the unit. Not shared with students, and not versioned with
# them: it is a working tool, not something anybody downloads.
STAFF_SRC = ROOT / "drive" / "staff"
STAFF_DST = DRIVE.parent / "cade30008-staff"
STAFF_FILES = [
    "README.md",
    "rig-characterisation/README.md",
    "rig-characterisation/t1_fit_this_rig.m",
    "rig-characterisation/t2_fly_these.m",
    "student-code-test/README.md",
    "student-code-test/run_all_student_code.m",
]
STAMP = re.compile(r"^<!-- version: .* -->$", re.M)

# The share links. The top-level one is the whole student folder; the others
# are the same link with a subfolder on the end, which is how MATLAB Drive
# builds them.
#
# **Check these annually.** A new cohort folder means a new share id, and a
# stale link is a dead link rather than a wrong one, so nothing here will
# notice. teaching/annual-update.md has it on the checklist.
SHARE_URL = ("https://drive.mathworks.com/sharing/"
             "93126ac2-9616-4272-a62c-a7ded0d6f7b8/cade30008-students")
FOLDER_URL = {folder: f"{SHARE_URL}/{folder}" for folder in
              ("w01-design-cycle", "lab-quanser")}

# Site pages that show the current version, so a student can compare it with
# what they downloaded. Filled between markers rather than typed, because a
# version number that has to be edited in four places is a version number that
# will disagree with itself.
# Each page names the folder it is about, so it gets that folder's link, with
# the whole-folder link beside it.
SITE_PAGES = {
    ROOT / "docs/laboratory/index.md": "lab-quanser",
    ROOT / "docs/laboratory/code/index.md": "lab-quanser",
    ROOT / "docs/laboratory/part1-identify.md": "lab-quanser",
    ROOT / "docs/laboratory/part2-design.md": "lab-quanser",
    ROOT / "docs/laboratory/part3-validate.md": "lab-quanser",
    ROOT / "docs/w01-design-cycle/code/index.md": "w01-design-cycle",
}
BLOCK = re.compile(
    r"(<!-- drive-version:start -->).*?(<!-- drive-version:end -->)", re.S)


NAMES = {"w01-design-cycle": "the first session's files",
         "lab-quanser": "the laboratory files"}


def stamp_site(version: str, today: str) -> list[str]:
    """Write the version and the right download links into the site pages."""
    touched = []
    for page, folder in SITE_PAGES.items():
        body = (f"**[Download {NAMES[folder]}]({FOLDER_URL[folder]})** from "
                f"MATLAB Drive, or [everything for the unit]({SHARE_URL}).\n\n"
                f"*Version {version}, {today}. If this differs from the version "
                f"in the folder's own README, download it again.*")
        if not page.exists():
            continue
        text = page.read_text(encoding="utf-8")
        if not BLOCK.search(text):
            continue
        new = BLOCK.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", text)
        if new != text:
            page.write_text(new, encoding="utf-8")
            touched.append(str(page.relative_to(ROOT)))
    return touched


def read_version() -> str:
    if VERSION_FILE.exists():
        v = VERSION_FILE.read_text(encoding="utf-8").strip().splitlines()[0].strip()
        if v:
            return v
    return "2026.1"


def bump(v: str) -> str:
    year, _, n = v.partition(".")
    try:
        return f"{year}.{int(n) + 1}"
    except ValueError:
        return f"{year}.1"


def stamp_readmes(version: str, today: str) -> None:
    """Write the version into the authored READMEs, before they are copied.

    The sources are stamped rather than the copies. Stamping a copy would make
    it differ from its source, so the next run would see it as changed and
    copy it again, for ever. This way the repository also shows the version
    that is live, which is the thing you want to see in a diff.
    """
    line = f"<!-- version: {version} ({today}) -->"
    for readme in sorted(AUTHORED.rglob("README.md")):
        text = readme.read_text(encoding="utf-8")
        if STAMP.search(text):
            text = STAMP.sub(line, text, count=1)
        else:
            text = line + "\n\n" + text
        text = re.sub(r"(?m)^\*\*Version .*?\*\*.*$",
                      f"**Version {version}**, {today}.", text, count=1)
        readme.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bump", action="store_true", help="increment the version")
    ap.add_argument("--check", action="store_true", help="report drift only")
    args = ap.parse_args()

    if not DRIVE.exists():
        print(f"No student folder at\n    {DRIVE}\n"
              f"Is MATLAB Drive syncing on this machine?", file=sys.stderr)
        return 2

    missing = [src for files in BUNDLES.values() for src, _ in files if not src.exists()]
    if not (AUTHORED / "README.md").exists():
        missing.append(AUTHORED / "README.md")
    if missing:
        for m in missing:
            print(f"Missing: {m.relative_to(ROOT)}", file=sys.stderr)
        return 2

    stale: list[str] = []
    if not (DRIVE / "README.md").exists() or not filecmp.cmp(
            AUTHORED / "README.md", DRIVE / "README.md", shallow=False):
        stale.append("README.md")
    for folder, files in BUNDLES.items():
        for src, rel in files:
            dst = DRIVE / folder / rel
            if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                stale.append(f"{folder}/{rel}")

    for rel in STAFF_FILES:
        src, dst = STAFF_SRC / rel, STAFF_DST / rel
        if not src.exists():
            continue
        if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
            stale.append(f"staff/{rel}")

    if args.check:
        if stale:
            print("Drive is out of date:")
            for s in stale:
                print(f"  {s}")
            print("\nRun: .venv/bin/python scripts/sync_drive.py --bump")
            return 1
        print(f"Drive matches the repository, version {read_version()}")
        return 0

    version = read_version()
    if args.bump:
        version = bump(version)
    today = dt.date.today().isoformat()
    stamp_readmes(version, today)

    shutil.copy2(AUTHORED / "README.md", DRIVE / "README.md")
    for folder, files in BUNDLES.items():
        for src, rel in files:
            dst = DRIVE / folder / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    VERSION_FILE.write_text(version + "\n", encoding="utf-8")
    shutil.copy2(VERSION_FILE, DRIVE / "VERSION.txt")

    for rel in STAFF_FILES:
        src, dst = STAFF_SRC / rel, STAFF_DST / rel
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    for page in stamp_site(version, today):
        print(f"  site: {page}")

    n = sum(len(f) for f in BUNDLES.values())
    print(f"{n} files copied into {DRIVE}")
    print(f"version {version}, {today}")
    if stale:
        print(f"{len(stale)} had changed:")
        for s in stale:
            print(f"  {s}")
    else:
        print("nothing had changed")
    if stale and not args.bump:
        print("\nFiles changed but the version did not. If students have already\n"
              "downloaded this, re-run with --bump so they can tell.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
