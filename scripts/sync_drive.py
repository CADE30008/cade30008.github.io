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
# The two folders are siblings in Teaching/, which is not shared, and each is
# shared on its own. They were briefly inside a shared parent, which meant
# Drive's web interface offered a breadcrumb up to it and from there into the
# staff folder. Sharing the leaves rather than the branch removes that.
#
# The folder names are in these paths, so renaming either one in Drive breaks
# the sync silently. The script checks and says so.
DRIVE_ROOT = Path.home() / "MATLAB-Drive" / "Teaching"
DRIVE = DRIVE_ROOT / "cade30008-students"

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
        # The rig models. Authored here rather than under docs/ because they
        # are only usable on a laboratory machine with QUARC, so serving them
        # from the website would be offering something that cannot be opened.
        # In-house work, not Quanser's: see the provenance note in private/.
        (AUTHORED / "lab-quanser/part1_identify.slx", "part1_identify.slx"),
        (AUTHORED / "lab-quanser/part3_validate.slx", "part3_validate.slx"),
        *[(ROOT / "docs/laboratory/code" / f, f) for f in (
            "lab1_fit.m", "lab2_3dof.m", "lab3_statespace.m", "heli3d_model.m",
            "level_rig.m", "save_recording.m", "plot_recording.m",
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
STAFF_DST = DRIVE_ROOT / "cade30008-staff"
STAFF_FILES = [
    "README.md",
    # The rig models, so they can be opened at the bench from the staff link
    # without signing in to Drive. Same two files the students get.
    "rig-characterisation/part1_identify.slx",
    "rig-characterisation/part3_validate.slx",
    "rig-characterisation/level_rig.m",
    "rig-characterisation/save_recording.m",
    "rig-characterisation/plot_recording.m",
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
# One share per folder. Neither reaches the other, and neither offers a way
# up: Teaching/ is not shared.
#
# The staff link is on the public staff page deliberately, so that the kit can
# be fetched on a laboratory machine without signing in to MATLAB Drive. It is
# therefore **staff-facing, not private**: working files yes, anything with a
# student's name on it or anything about assessment no.
SHARE_URL = "https://drive.mathworks.com/sharing/ad3e3e94-cfda-486b-ad94-d8c0d52afbc0"
STAFF_SHARE_URL = "https://drive.mathworks.com/sharing/a3596484-f0e7-4d6b-bbb8-46d263c3cc4b"
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

# The staff area's own table of every Drive link, written from the same place
# the student pages are, so the two cannot disagree.
STAFF_PAGE = ROOT / "docs/staff/index.md"
LINKS_BLOCK = re.compile(
    r"(<!-- drive-links:start -->).*?(<!-- drive-links:end -->)", re.S)


def stamp_staff_page(version: str, today: str) -> bool:
    """Write the link table into the staff area page."""
    if not STAFF_PAGE.exists():
        return False
    rows = [f"| **The staff test kit** | [{STAFF_SHARE_URL}]({STAFF_SHARE_URL}) |",
            f"| Everything students get | [{SHARE_URL}]({SHARE_URL}) |"]
    for folder, url in FOLDER_URL.items():
        rows.append(f"| `{folder}` | [{url}]({url}) |")
    body = ("| Folder | Link |\n|---|---|\n" + "\n".join(rows) +
            f"\n\nStudent files are at **version {version}**, {today}.\n\n"
            "!!! warning \"The staff link is public, on purpose\"\n"
            "    It is here so the test kit can be fetched on a laboratory\n"
            "    machine without signing in to MATLAB Drive. That makes\n"
            "    `cade30008-staff/` **staff-facing, not private**: working files\n"
            "    yes, anything with a student's name on it or anything about\n"
            "    assessment no. Those live in `private/` in the repository and\n"
            "    are never committed.\n\n"
            "    The two folders are shared separately and sit in an unshared\n"
            "    `Teaching/`, so neither link offers a way up into the other.\n\n"
            "**Check these annually.** A new cohort folder means a new share "
            "id, and a stale share link is dead rather than wrong, so nothing "
            "in the build will notice. See `teaching/annual-update.md`.")
    text = STAFF_PAGE.read_text(encoding="utf-8")
    if not LINKS_BLOCK.search(text):
        return False
    new = LINKS_BLOCK.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(2)}", text)
    if new != text:
        STAFF_PAGE.write_text(new, encoding="utf-8")
        return True
    return False


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


CHANGELOG_ROW = re.compile(r"^\|\s*(\d{4}\.\d+)\s*\|", re.M)


def changelog_top() -> str | None:
    """The version on the newest row of the changelog students read."""
    readme = AUTHORED / "README.md"
    if not readme.exists():
        return None
    m = CHANGELOG_ROW.search(readme.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def check_changelog(version: str) -> bool:
    """Does the changelog's newest row agree with the version we just wrote?

    The row is written by hand and the version is incremented by this script,
    so the two drift the moment somebody guesses the next number. A student
    told to compare versions cannot do it if the page disagrees with itself.
    """
    top = changelog_top()
    if top == version:
        return True
    print(f"\nThe changelog's newest row says {top}, and the version is "
          f"{version}.\nFix the row in drive/README.md: it is what students "
          f"read to see what changed.", file=sys.stderr)
    return False


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
              f"Is MATLAB Drive syncing, and are the folders still called\n"
              f"cade30008-students and cade30008-staff? Renaming either breaks\n"
              f"these paths and nothing else will notice.", file=sys.stderr)
        return 2

    missing = [src for files in BUNDLES.values() for src, _ in files if not src.exists()]
    if not (AUTHORED / "README.md").exists():
        missing.append(AUTHORED / "README.md")
    if missing:
        for m in missing:
            print(f"Missing: {m.relative_to(ROOT)}", file=sys.stderr)
        return 2

    # Anything in the student folder that is not in the manifest is ours and
    # stale: students cannot write there, so nothing else puts a file in it.
    # Without this a renamed file lingers for ever beside its replacement,
    # which is how lab-quanser briefly offered the same model under two names.
    #
    # The staff folder is deliberately not pruned. It holds recordings and
    # working copies that nothing here manages.
    expected = {DRIVE / "README.md", DRIVE / "VERSION.txt"}
    for folder, files in BUNDLES.items():
        expected |= {DRIVE / folder / rel for _, rel in files}
    orphans = sorted(
        f for f in DRIVE.rglob("*")
        if f.is_file()
        and not f.name.startswith(".")
        and f.resolve() not in {e.resolve() for e in expected})

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
        for o in orphans:
            print(f"Stale in the Drive, not in the manifest: "
                  f"{o.relative_to(DRIVE)}", file=sys.stderr)
        if stale or orphans:
            print("Drive is out of date:")
            for s in stale:
                print(f"  {s}")
            print("\nRun: .venv/bin/python scripts/sync_drive.py --bump")
            return 1
        if not check_changelog(read_version()):
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
    if stamp_staff_page(version, today):
        print("  site: docs/staff/index.md")

    n = sum(len(f) for f in BUNDLES.values())
    for o in orphans:
        o.unlink()
        print(f"  removed (stale): {o.relative_to(DRIVE)}")

    print(f"{n} files copied into {DRIVE}")
    print(f"version {version}, {today}")
    if stale:
        print(f"{len(stale)} had changed:")
        for s in stale:
            print(f"  {s}")
    else:
        print("nothing had changed")
    check_changelog(version)
    if stale and not args.bump:
        print("\nFiles changed but the version did not. If students have already\n"
              "downloaded this, re-run with --bump so they can tell.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
