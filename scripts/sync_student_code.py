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

# Canonical in models/, copied into each folder students are handed.
BUNDLES = {
    ROOT / "docs" / "w01-design-cycle" / "code": [
        "heli_plant.m",
        "heli_envelope.m",
        "heli_check_one.m",
        "elevation_plant.json",
    ],
    ROOT / "docs" / "laboratory" / "code": [
        "fit_second_order.m",
        "heli_plant.m",
        "heli_envelope.m",
        "heli_check_one.m",
        "elevation_plant.json",
    ],
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="verify without copying; non-zero exit if stale")
    args = ap.parse_args()

    wanted = sorted({f for files in BUNDLES.values() for f in files})
    missing = [f for f in wanted if not (SRC / f).exists()]
    if missing:
        print(f"Missing from {SRC.relative_to(ROOT)}: {', '.join(missing)}", file=sys.stderr)
        return 2

    total, copied, stale_any = 0, 0, False
    for dst_dir, files in BUNDLES.items():
        dst_dir.mkdir(parents=True, exist_ok=True)
        stale = [f for f in files
                 if not (dst_dir / f).exists()
                 or not filecmp.cmp(SRC / f, dst_dir / f, shallow=False)]
        total += len(files)
        where = dst_dir.relative_to(ROOT)
        if args.check:
            if stale:
                stale_any = True
                print(f"{where} is out of date: {', '.join(stale)}", file=sys.stderr)
            continue
        for f in stale:
            shutil.copy2(SRC / f, dst_dir / f)
        copied += len(stale)
        print(f"{where}: {len(files)} files, {len(stale)} copied"
              + (f" ({', '.join(stale)})" if stale else ""))

    if args.check:
        if stale_any:
            print("Run: .venv/bin/python scripts/sync_student_code.py", file=sys.stderr)
            return 1
        print(f"{total} files across {len(BUNDLES)} folders, all match models/")
        return 0

    print(f"{total} files checked, {copied} copied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# tracking: status=draft version=0 assisted=true
