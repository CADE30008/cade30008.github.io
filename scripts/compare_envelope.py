"""Check that the MATLAB and Python flight envelopes agree.

There are two implementations of the same envelope: models/heli_check_one.m,
which runs in the room, and scripts/gains.py, which runs in the repository.
They must never disagree. A set of gains accepted by one and refused by the
other means somebody's flight depends on which tool happened to be run.

    cd models && matlab -batch compare_envelope     # writes the MATLAB verdicts
    .venv/bin/python scripts/compare_envelope.py    # compares them with Python's

Exits non-zero if any verdict differs, so it can go in a check.

Metrics are compared loosely. The two use different ODE solvers and different
minimal-realisation routines, so settling time to a 2% band can land a sample
apart. Verdicts are compared exactly, because that is what decides what flies.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from models.quanser_elevation import Envelope, Plant, load_plant  # noqa: E402
from scripts.gains import Submission, evaluate  # noqa: E402

# Fractional tolerance per metric. Settling is the loose one: it is read off a
# sampled response, so the two can differ by a sample width.
TOL = {
    "routh_ratio": 1e-6,
    "max_real_pole": 1e-6,
    "damping": 1e-4,
    "phase_margin": 1e-3,
    "peak_volts": 2e-2,
    "settle_s": 5e-2,
    "reversals": 0.0,
    "overshoot_pct": 2e-2,
}


def close(name: str, a: float, b: float) -> bool:
    tol = TOL.get(name, 1e-6)
    if a == b:
        return True
    scale = max(abs(a), abs(b), 1e-9)
    return abs(a - b) / scale <= tol


def main() -> int:
    dump = ROOT / "models" / "envelope-matlab.json"
    if not dump.exists():
        print(f"No MATLAB verdicts at {dump.relative_to(ROOT)}.\n"
              f"Run:  cd models && matlab -batch compare_envelope", file=sys.stderr)
        return 2

    data = json.loads(dump.read_text(encoding="utf-8"))
    mp = data["plant"]
    plant = load_plant()
    for k in ("K", "wn", "zeta"):
        if abs(float(mp[k]) - getattr(plant, k)) > 1e-12:
            print(f"The two are not even reading the same plant: "
                  f"MATLAB {k}={mp[k]}, Python {k}={getattr(plant, k)}", file=sys.stderr)
            return 2

    env = Envelope()
    rows = data["rows"]
    if isinstance(rows, dict):          # jsonencode collapses a 1-element cell
        rows = [rows]

    bad = 0
    print(f"{'Kp':>7}{'Ki':>7}{'Kd':>7}   {'MATLAB':>8} {'Python':>8}   verdict")
    for r in rows:
        kp, ki, kd = float(r["kp"]), float(r["ki"]), float(r["kd"])
        s = Submission(who="cmp", kp=kp, ki=ki, kd=kd, source="compare")
        evaluate(s, plant, env)
        same = bool(r["ok"]) == s.ok
        mark = "agree" if same else "DIFFER"
        if not same:
            bad += 1
        print(f"{kp:7.2f}{ki:7.2f}{kd:7.2f}   {str(bool(r['ok'])):>8} {str(s.ok):>8}   {mark}")
        if not same:
            print(f"        MATLAB said: {r['why'] or 'accepted'}")
            print(f"        Python said: {s.reasons[0] if s.reasons else 'accepted'}")
            continue

        # Verdicts match; now the numbers behind them.
        mm = r.get("metrics") or {}
        for name, mval in mm.items():
            if name not in s.metrics or not isinstance(mval, (int, float)):
                continue
            if not close(name, float(mval), float(s.metrics[name])):
                bad += 1
                print(f"        {name}: MATLAB {float(mval):.6g}, "
                      f"Python {float(s.metrics[name]):.6g}")

    print()
    if bad:
        print(f"{bad} disagreement(s). The two envelopes are not the same envelope.")
        return 1
    print(f"{len(rows)} gain sets, identical verdicts, metrics within tolerance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# tracking: status=draft version=0 assisted=true
