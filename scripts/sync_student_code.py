"""Copy the files students need into the folder they are given.

The envelope, the plant and the check have one canonical home, models/, so
that the tool Steve runs in the room and the tool a student runs on their
laptop cannot drift apart. Students are handed a folder rather than the
repository, so those files have to be copied into it.

Copying is the whole job, but doing it by hand is how the two ended up
different last time, so it is a script and it runs in `npm run check`'s
company rather than from memory.

    .venv/bin/python scripts/sync_student_code.py           # copy
    .venv/bin/python scripts/sync_student_code.py --check   # verify only

--check exits non-zero if the student folder is out of date, which is what a
build should call.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "models"
DST = ROOT / "docs" / "w01-design-cycle" / "code"

# Canonical in models/, copied into the student bundle.
FILES = [
    "heli_plant.m",
    "heli_envelope.m",
    "heli_check_one.m",
    "elevation_plant.json",
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="verify without copying; non-zero exit if stale")
    args = ap.parse_args()

    missing = [f for f in FILES if not (SRC / f).exists()]
    if missing:
        print(f"Missing from {SRC.relative_to(ROOT)}: {', '.join(missing)}", file=sys.stderr)
        return 2

    DST.mkdir(parents=True, exist_ok=True)
    stale = []
    for f in FILES:
        src, dst = SRC / f, DST / f
        if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
            stale.append(f)

    if args.check:
        if stale:
            print(f"Student folder is out of date: {', '.join(stale)}\n"
                  f"Run: .venv/bin/python scripts/sync_student_code.py", file=sys.stderr)
            return 1
        print(f"{len(FILES)} files, student folder matches models/")
        return 0

    for f in stale:
        shutil.copy2(SRC / f, DST / f)
    print(f"{len(FILES)} files checked, {len(stale)} copied into "
          f"{DST.relative_to(ROOT)}"
          + (f": {', '.join(stale)}" if stale else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
