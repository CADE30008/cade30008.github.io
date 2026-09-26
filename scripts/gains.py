"""Check submitted PID gains before they reach the rig, and choose what to fly.

Week 1 ends with the room submitting gains through a form and watching them
flown, in three rounds: a few individuals, then the cohort's average, then the
best few. This is the thing standing between 190 students' arithmetic and a
machine flying in front of them.

    python scripts/gains.py check path/to/responses
    python scripts/gains.py pick  path/to/responses --round 1

Submissions arrive as the form's export. models/collate_gains.m reads that
export directly and applies the same envelope; this tool is the Python side
and reads a folder of per-submission files. Student work is never copied into
this repository; `examples/gains/` holds only fixtures.

`check` writes a report to the terminal and an accepted list to `--out`, which
defaults to the current directory and **never** to the folder it read: that
folder is shared with the cohort.

Two rules it follows, both deliberate:

**Refuse, never clamp.** A set of gains outside the envelope is rejected and
its owner told which limit it missed. Nothing is quietly adjusted into range: a
student whose gains were changed without being told learns the wrong lesson,
and the room watches a flight that was not theirs.

**Refuse to guess the plant.** Without a fitted elevation model the tool exits
rather than falling back on a nominal one. A report produced against an
invented plant would read exactly like a real one.

The envelope and the physics are in `models/quanser_elevation.py`.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from models.quanser_elevation import (  # noqa: E402
    CMD_RATE_DEG_S, STEP_DEG, Envelope, Plant, controller, gain_range,
    load_plant, routh,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = {"accepted.json"}


@dataclass
class Submission:
    who: str                      # name or alias, as they chose
    kp: float
    ki: float
    kd: float
    source: str                   # the file it came from
    reasons: list[str] = field(default_factory=list)   # why it was rejected
    metrics: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.reasons


def read_submissions(folder: Path) -> tuple[list[Submission], list[str]]:
    """Read every *.json and *.csv in the drop folder.

    Students submit under pressure, on their own laptops, in a lecture theatre.
    So this is forgiving about shape - key case, column order, stray whitespace,
    a missing alias - and unforgiving about values. A file it cannot read is
    reported by name rather than skipped silently, because in the room the
    question is always "did mine arrive?".
    """
    subs, bad = [], []
    for path in sorted(folder.rglob("*")):
        if path.suffix.lower() not in (".json", ".csv") or not path.is_file():
            continue
        if path.name in OUTPUTS:              # our own report, not a submission
            continue
        try:
            rows = _rows(path)
        except Exception as e:                       # noqa: BLE001 - report, don't crash
            bad.append(f"{path.name}: unreadable ({type(e).__name__}: {e})")
            continue
        if not rows:
            bad.append(f"{path.name}: no rows")
        for i, row in enumerate(rows, 1):
            low = {str(k).strip().lower(): v for k, v in row.items()}
            who = str(low.get("name") or low.get("alias") or path.stem).strip()
            try:
                kp, ki, kd = (float(low[k]) for k in ("kp", "ki", "kd"))
            except (KeyError, TypeError, ValueError):
                bad.append(f"{path.name}"
                           f"{f' row {i}' if len(rows) > 1 else ''}: needs kp, ki and kd as numbers")
                continue
            subs.append(Submission(who=who or path.stem, kp=kp, ki=ki, kd=kd, source=path.name))
    return subs, bad


def _rows(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        d = json.loads(text)
        return d if isinstance(d, list) else [d]
    return list(csv.DictReader(text.splitlines()))


def evaluate(s: Submission, plant: Plant, env: Envelope) -> None:
    """Fill in s.reasons and s.metrics. Every check is a refusal, not a fix."""
    import control as ct
    import numpy as np

    # 1. Finite and positive. On a double integrator a non-positive gain is not
    #    a slow controller, it is an unstable one.
    for name, v in (("Kp", s.kp), ("Ki", s.ki), ("Kd", s.kd)):
        if not np.isfinite(v):
            s.reasons.append(f"{name} is not a finite number")
        elif v <= env.gain_min:
            s.reasons.append(f"{name} must be greater than {env.gain_min:g}, got {v:g}")
    for name, v, hi in (("Kp", s.kp, env.kp_max), ("Ki", s.ki, env.ki_max), ("Kd", s.kd, env.kd_max)):
        if np.isfinite(v) and v > hi:
            s.reasons.append(f"{name} above the {hi:g} limit, got {v:g}")
    if s.reasons:
        return

    # 2. The hand-checkable condition, with margin for a rig that is not
    #    exactly the fitted model.
    passes, ratio = routh(plant, s.kp, s.ki, s.kd)
    s.metrics["routh_ratio"] = ratio
    if not passes:
        s.reasons.append("unstable: Routh needs a2*a1 > a0 for the closed loop, "
                         f"and the ratio is {ratio:.2f}")
        return
    if ratio < env.routh_margin:
        s.reasons.append(f"too close to unstable: the Routh ratio is only {ratio:.2f}, "
                         f"and we fly nothing below {env.routh_margin:g}")

    # 3. Closed loop: poles, damping, margins.
    #
    # Derivative acts on the measurement, not on the error. That is what the
    # rig does - Quanser feed back the measured elevation rate - and it is what
    # the handout means by rate feedback. It matters here for one reason: with
    # derivative on the error, the demand's own rate goes through Kd, so a
    # 45 deg/s command asks for Kd * 45 volts before the arm has moved at all.
    # At Kd = 1.4 that is 63 V from a 24 V amplifier.
    #
    # The loop transfer is L = G (C1 + D) either way, so the characteristic
    # polynomial, the poles, the damping and the margins are all unchanged.
    # Only the reference path differs:
    #
    #     Y/R = G C1 / (1 + G (C1 + D))      U/R = C1 / (1 + G (C1 + D))
    #
    C = controller(s.kp, s.ki, s.kd)   # filtered derivative, or the effort is an impulse
    C1 = ct.tf([s.kp, s.ki], [1, 0])   # the part the reference is allowed to see
    G = plant.tf()
    L = C * G
    T = ct.feedback(L, 1)              # poles, damping, margins: unchanged by the split
    # The reference paths, reduced. Building these as (G C1)/(1 + L) without
    # minreal leaves the loop's own poles in both numerator and denominator;
    # they cancel mathematically and do not cancel numerically, and what comes
    # back is a high-order system that reports itself unstable.
    y_ref = ct.minreal(G * C1 / (1 + L), verbose=False)
    u_ref = ct.minreal(C1 / (1 + L), verbose=False)
    poles = T.poles()
    s.metrics["max_real_pole"] = float(np.max(poles.real))
    if np.max(poles.real) >= 0:
        s.reasons.append("closed loop is unstable: a pole is on or right of the imaginary axis")
        return
    osc = poles[np.abs(poles.imag) > 1e-9]
    if osc.size:
        zeta = float(np.min(-osc.real / np.abs(osc)))
        s.metrics["damping"] = zeta
        if zeta < env.damping_min:
            s.reasons.append(f"too oscillatory: damping {zeta:.3f} below {env.damping_min:g}")

    down, up = gain_range(L)
    s.metrics["gain_down"] = down
    s.metrics["gain_up"] = up
    if down < env.gain_down_min:
        s.reasons.append(f"only tolerates the loop gain dropping by {down:.2f}x "
                         f"(needs {env.gain_down_min:g}x)")
    if up < env.gain_up_min:
        s.reasons.append(f"only tolerates the loop gain rising by {up:.2f}x (needs {env.gain_up_min:g}x)")

    _, pm, _, _ = ct.margin(L)
    s.metrics["phase_margin"] = float(pm)
    if not np.isfinite(pm) or pm < env.phase_margin_min:
        s.reasons.append(f"phase margin {pm:.1f} deg below {env.phase_margin_min:g}")

    # 4. What the motors are actually asked to do. A design can be perfectly
    #    stable on paper and still slam the amplifier into its rails.
    # Degrees, because the fitted K is deg/V. This read np.deg2rad(STEP_DEG)
    # while the plant was the double integrator in rad/(V s^2); against a
    # deg/V plant that understates every demand by a factor of 57, and the
    # amplifier check would pass almost anything.
    step = float(STEP_DEG)
    t = np.linspace(0, env.settle_max_s * 1.5, 4000)
    # The demand as the rig actually receives it: rate-limited, not a step.
    # Differentiating a discontinuity asks a 24 V amplifier for hundreds of
    # volts and rejects every sane design.
    ref = np.minimum(CMD_RATE_DEG_S * t, step)
    _, v = ct.forced_response(u_ref, T=t, U=ref)
    peak = float(np.max(np.abs(v)))
    s.metrics["peak_volts"] = peak
    if peak > env.voltage_peak_max:
        s.reasons.append(f"demands {peak:.1f} V for a {STEP_DEG:g} deg step, "
                         f"above the {env.voltage_peak_max:.1f} V we allow")

    # The guide's own caution: repeated sign flips are hard on the motors.
    sign = np.sign(v[np.abs(v) > 0.02 * max(peak, 1e-9)])
    reversals = int(np.count_nonzero(np.diff(sign) != 0)) if sign.size else 0
    s.metrics["reversals"] = reversals
    if reversals > env.reversals_max:
        s.reasons.append(f"motor demand changes sign {reversals} times; "
                         f"the rig's guide warns against this above {env.reversals_max}")

    # 5. Settling, to 2%. Room time is finite and so is everyone's patience.
    _, y = ct.forced_response(y_ref, T=t, U=ref)

    # Overshoot against the same rate-limited demand, so it is smaller than
    # stepinfo's figure for the closed loop. It decides nothing; it is here so
    # a flight can be held against the prediction afterwards. Mirrors
    # models/heli_check_one.m.
    s.metrics["overshoot_pct"] = max(0.0, 100.0 * (float(np.max(y)) - step) / step)

    outside = np.where(np.abs(y - step) > 0.02 * step)[0]
    settle = float(t[outside[-1]]) if outside.size and outside[-1] + 1 < t.size else float("inf")
    s.metrics["settle_s"] = settle
    if settle > env.settle_max_s:
        s.reasons.append(f"takes {settle:.1f} s to settle, over the {env.settle_max_s:g} s limit")


def score(s: Submission) -> float:
    """Rank accepted submissions: fast, then well damped, then gentle.

    Only ever applied to gains that already passed every check, so this is a
    preference between safe designs, not a safety judgement.
    """
    m = s.metrics
    return (m.get("settle_s", 1e9)
            + 2.0 * max(0.0, 0.7 - m.get("damping", 0.7)) * 10
            + 0.05 * m.get("peak_volts", 0.0))


def banner(plant: Plant, env: Envelope) -> str:
    return (f"Elevation model: K = {plant.K:g} deg/V, wn = {plant.wn:g} rad/s, "
            f"zeta = {plant.zeta:g}\n  {plant.source}\n  measured {plant.measured}\n"
            f"Envelope: Routh margin {env.routh_margin:g}, damping >= {env.damping_min:g}, "
            f"gain -{env.gain_down_min:g}x/+{env.gain_up_min:g}x, PM >= {env.phase_margin_min:g} deg, "
            f"peak <= {env.voltage_peak_max:.1f} V, settle <= {env.settle_max_s:g} s")


def cmd_check(args) -> int:
    plant, env = load_plant(), Envelope()
    subs, bad = read_submissions(Path(args.folder))
    print(banner(plant, env), "\n")
    for s in subs:
        evaluate(s, plant, env)

    ok = [s for s in subs if s.ok]
    for s in bad:
        print(f"  UNREADABLE  {s}")
    for s in sorted((x for x in subs if not x.ok), key=lambda x: x.who.lower()):
        print(f"  REJECTED    {s.who}: {s.reasons[0]}")
        for r in s.reasons[1:]:
            print(f"                {' ' * len(s.who)}{r}")
    for s in sorted(ok, key=score):
        m = s.metrics
        print(f"  ok          {s.who}: settles {m['settle_s']:.1f} s, "
              f"damping {m.get('damping', float('nan')):.2f}, peak {m['peak_volts']:.1f} V, "
              f"PM {m['phase_margin']:.0f} deg, gain -{m['gain_down']:.1f}x/+{m['gain_up']:.1f}x")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(
        [{"who": s.who, "kp": s.kp, "ki": s.ki, "kd": s.kd, **s.metrics} for s in sorted(ok, key=score)],
        indent=2), encoding="utf-8")
    print(f"\n{len(ok)} of {len(subs)} accepted, {len(bad)} unreadable -> {out}")
    return 0


def cmd_pick(args) -> int:
    """What to fly, in the three rounds week 1 runs.

    Round 2 flies the cohort's average, which is the point of the exercise: the
    average of safe gains is not guaranteed safe, so it is checked like any
    other submission, and if it fails that is the lesson rather than a problem.
    """
    plant, env = load_plant(), Envelope()
    subs, _ = read_submissions(Path(args.folder))
    for s in subs:
        evaluate(s, plant, env)
    ok = sorted((s for s in subs if s.ok), key=score)
    if not ok:
        print("Nothing passed. Fly the lecturer's own gains and say why.")
        return 1

    print(banner(plant, env), "\n")
    if args.round == 1:                       # a spread, not the best
        picks = [ok[0], ok[len(ok) // 2], ok[-1]][: args.n]
        print(f"Round 1 - a spread of {len(picks)}, best to worst of those accepted:")
    elif args.round == 2:
        n = len(ok)
        avg = Submission(who=f"the cohort's average of {n}",
                         kp=sum(s.kp for s in ok) / n, ki=sum(s.ki for s in ok) / n,
                         kd=sum(s.kd for s in ok) / n, source="computed")
        evaluate(avg, plant, env)
        print("Round 2 - the average of every accepted submission:")
        picks = [avg]
        if not avg.ok:
            print(f"  ** the average FAILS: {avg.reasons[0]}")
            print("  ** do not fly it. That is the lesson: averaging safe designs")
            print("  ** does not give a safe design, because the envelope is not convex.")
            return 0
    else:
        picks = ok[: args.n]
        print(f"Round 3 - the best {len(picks)}:")

    for s in picks:
        m = s.metrics
        print(f"  {s.who}: Kp={s.kp:.4g} Ki={s.ki:.4g} Kd={s.kd:.4g}"
              f"   settles {m['settle_s']:.1f} s, peak {m['peak_volts']:.1f} V")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="check every submission against the envelope")
    c.add_argument("folder")
    # Never default the report into the folder it read. That folder is a shared
    # MATLAB Drive, so writing the accepted list there would hand every student
    # a list of whose gains passed - names, numbers and all.
    c.add_argument("--out", default="accepted.json",
                   help="where to write the accepted list (default: ./accepted.json, not the drop folder)")
    c.set_defaults(fn=cmd_check)
    k = sub.add_parser("pick", help="choose what to fly in a given round")
    k.add_argument("folder")
    k.add_argument("--round", type=int, default=1, choices=(1, 2, 3))
    k.add_argument("-n", type=int, default=3)
    k.set_defaults(fn=cmd_pick)
    args = p.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()

# tracking: status=draft version=0
