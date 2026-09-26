"""Check that Python and MATLAB agree on every week 3 (PID) design number.

Run after models/pitch.py and models/pitch_check.m:

    .venv/bin/python models/compare.py

Exits non-zero if any number differs by more than the tolerance.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
py = json.loads((HERE / "pitch_numbers.json").read_text())
ml = json.loads((HERE / "pitch_numbers_matlab.json").read_text())

# Relative tolerance; settling time is sensitive to the 2% band crossing, so
# it gets a looser limit.
TOL = {"settling_time": 0.02}
DEFAULT_TOL = 0.005

rows, bad = [], 0
for name, m in ml["designs"].items():
    p = py["designs"][name]
    for key, mv in m.items():
        pv = p[key]
        tol = TOL.get(key, DEFAULT_TOL)
        scale = max(abs(pv), abs(mv), 1e-9)
        ok = abs(pv - mv) / scale <= tol or abs(pv - mv) < 1e-6
        bad += not ok
        rows.append((name, key, pv, mv, "ok" if ok else "MISMATCH"))

pk = py["kick"]["peak_elevator_deg_D_on_error"]
mk = ml["kick"]["peak_elevator_deg_D_on_error"]
ok = abs(pk - mk) / mk <= DEFAULT_TOL
bad += not ok
rows.append(("PD", "kick_peak_deg", pk, mk, "ok" if ok else "MISMATCH"))

width = max(len(r[1]) for r in rows)
for name, key, pv, mv, status in rows:
    print(f"{name:7} {key:{width}}  python {pv:10.4f}  matlab {mv:10.4f}  {status}")
print(f"\n{len(rows) - bad}/{len(rows)} numbers agree")
sys.exit(1 if bad else 0)

# tracking: status=draft version=0
