"""The Quanser 3-DOF helicopter's elevation axis, and the envelope we will fly.

One source for two things that must never disagree: the model students fit in
week 1, and the envelope `scripts/gains.py` uses to decide whether a submitted
set of gains is safe to put on the hardware.

The physics
-----------
Linearised about level, the elevation axis is a **pure double integrator**:

    G(s) = eps(s) / V(s) = K / s^2,     K = La * Kf / Je   [rad / (V s^2)]

where V is the voltage applied to both motors together, about the operating
point Vop that holds the arm up. There is no damping term: nothing in the rig
opposes elevation rate except the air, and at these speeds that is nothing.

That is the whole pedagogical point of week 1. A double integrator has two
poles at the origin, so it cannot be stabilised by proportional feedback alone
at any gain - the root locus leaves the origin straight up and down. Rate
feedback is not a refinement, it is the difference between flying and not. This
is why the open-loop flight attempt fails, and it is why the room's first
instinct, "turn Kp up", makes things worse rather than better.

For a PID controller C(s) = Kd s + Kp + Ki/s the closed-loop characteristic
polynomial is

    s^3 + K Kd s^2 + K Kp s + K Ki = 0

and Routh gives a condition students can check on paper, which is worth putting
on a slide:

    Kd > 0,  Kp > 0,  Ki > 0,  and   K Kd Kp > Ki.

Integral action is therefore not free: raise Ki far enough, with Kp and Kd
fixed, and the loop goes unstable. That inequality is the reason the filter
below exists.

It also says something students find genuinely surprising, and week 1 should
make them meet it: scale the whole loop gain by alpha and the condition becomes
alpha K Kd Kp > Ki, so the loop is stable for *large* alpha and unstable for
small. **This loop is conditionally stable - turning the gain down is what
breaks it.** The textbook reflex, "if it is oscillating, reduce the gain", is
exactly wrong here, and a naive gain-margin test reads every good design as a
failure. So the envelope below asks how far the loop gain can move in *both*
directions, which is the honest question for a plant like this.

The numbers
-----------
`K` is measured, not assumed: week 1's whole first act is fitting it from the
rig's own step response. `load_plant()` reads the fitted value, and refuses to
guess, so nothing is ever filtered against an invented plant.

Hardware limits are from the Quanser 3-DOF Helicopter Laboratory Guide:

  * Amplifier: VoltPAQ-X2, K_AMP = 3, so the DAQ card's own limit never binds.
  * Peak motor voltage +/- 24 V. The controller output rides on top of Vop, the
    operating-point voltage that holds the arm level, so the usable swing is
    smaller than 24 V in one direction.
  * The guide's own caution, which we enforce rather than hope for: "Make sure
    the motor voltages do not switch between negative and positive often."
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Hardware, from the laboratory guide. These are properties of the rig and the
# amplifier, not of any controller, so they do not move between cohorts.
V_MAX = 24.0          # V, peak motor voltage the amplifier can deliver
V_OP = 8.0            # V, provisional: the operating point that holds it level
STEP_DEG = 7.5        # deg, the guide's standard elevation step

# Derivative filter. An ideal PID is not a real controller: its derivative term
# is non-proper, so a step demand asks the motors for an impulse, and any
# estimate of peak voltage made from it is infinite rather than merely wrong.
# Every real implementation filters the derivative, the rig's included. N = 10
# is the course's own convention, set once in week 3 and used everywhere after,
# so a student's gains mean the same thing here as they do on their own plots.
DERIVATIVE_FILTER_N = 10.0


@dataclass(frozen=True)
class Plant:
    """G(s) = K / s^2, with K measured from the rig."""

    K: float                      # rad / (V s^2)
    source: str                   # where the number came from
    measured: str                 # when

    def tf(self):
        import control as ct
        return ct.tf([self.K], [1, 0, 0])


def controller(kp: float, ki: float, kd: float, n: float = DERIVATIVE_FILTER_N):
    """PID with a filtered derivative: Kp + Ki/s + Kd s / (1 + Tf s).

    With Tf = Kd / (n Kp) this is proper, so the demand on the motors can
    actually be computed. Stability is barely affected - the filter pole sits n
    times beyond the derivative zero - which is why routh() can keep using the
    unfiltered form that students check by hand.
    """
    import control as ct
    tf_ = kd / (n * kp)
    return ct.tf([kp * tf_ + kd, kp + ki * tf_, ki], [tf_, 1, 0])


@dataclass(frozen=True)
class Envelope:
    """What we are willing to fly in a room with 190 people in it.

    Every limit is a refusal, never a clamp. A submission that misses one is
    rejected and its owner told why; nothing is quietly adjusted into range,
    because a student whose gains were silently changed learns the wrong thing
    and the room sees a flight that was not theirs.
    """

    gain_min: float = 0.0         # strictly positive is required; see routh()
    kp_max: float = 50.0
    ki_max: float = 50.0
    kd_max: float = 50.0
    routh_margin: float = 1.15    # K Kd Kp must beat Ki by this factor
    damping_min: float = 0.15     # of the dominant closed-loop pole pair
    # How far the loop gain may move before the closed loop goes unstable, down
    # and up. Not ct.margin's gain margin: on a conditionally stable loop that
    # number is below 1 for every good design, and testing it against a floor
    # rejects everything. The rig's own K will not be exactly the fitted one,
    # so both directions have to have room.
    gain_down_min: float = 1.5    # may lose a third of the loop gain
    gain_up_min: float = 2.0      # may double it
    phase_margin_min: float = 20.0                     # degrees
    voltage_peak_max: float = 0.7 * (V_MAX - V_OP)     # V, controller demand
    reversals_max: int = 6        # sign changes of the demand in one step
    settle_max_s: float = 12.0    # a flight nobody wants to watch


def load_plant(path: Path | None = None) -> Plant:
    """Read the fitted elevation model. Refuses to invent one.

    Week 1 measures this from the rig on the day. Filtering submissions against
    a plausible-looking guess would be worse than not filtering at all: the
    report would read as though it meant something.
    """
    path = path or ROOT / "models" / "elevation_plant.json"
    if not path.exists():
        raise SystemExit(
            f"No fitted elevation model at {path.relative_to(ROOT)}.\n"
            "Record a step response from the rig, fit K, and write it there as\n"
            '  {"K": <rad/(V s^2)>, "source": "...", "measured": "YYYY-MM-DD"}\n'
            "There is deliberately no default: gains must never be checked\n"
            "against a guessed plant."
        )
    d = json.loads(path.read_text(encoding="utf-8"))
    for key in ("K", "source", "measured"):
        if key not in d:
            raise SystemExit(f"{path.name} has no {key!r}")
    if not (d["K"] > 0):
        raise SystemExit(f"{path.name}: K must be positive, got {d['K']}")
    return Plant(K=float(d["K"]), source=str(d["source"]), measured=str(d["measured"]))


def routh(plant: Plant, kp: float, ki: float, kd: float) -> tuple[bool, float]:
    """The hand-checkable stability condition, and how much room it has.

    Returns (passes, ratio) where ratio = K Kd Kp / Ki. Above 1 is stable;
    the envelope asks for more than 1 so that a rig which is not quite the
    fitted model still flies.
    """
    if min(kp, ki, kd) <= 0:
        return False, 0.0
    return (plant.K * kd * kp) > ki, (plant.K * kd * kp) / ki


def gain_range(L, lo: float = 1e-3, hi: float = 1e3, n: int = 400) -> tuple[float, float]:
    """How far the loop gain can be scaled, down and up, and stay stable.

    Returns (down, up) as factors: the loop tolerates dividing its gain by
    `down` and multiplying it by `up`. Computed by sweeping rather than from a
    Bode crossing, because this loop is conditionally stable and a crossing
    tells you the wrong thing. Returns (1, 1) if the nominal loop is unstable.
    """
    import control as ct
    import numpy as np

    stable = lambda a: bool(np.max(ct.feedback(a * L, 1).poles().real) < 0)   # noqa: E731
    if not stable(1.0):
        return 1.0, 1.0
    alphas = np.geomspace(lo, hi, n)
    i = int(np.searchsorted(alphas, 1.0))
    down = 1.0
    for a in alphas[:i][::-1]:
        if not stable(a):
            break
        down = 1.0 / a
    up = 1.0
    for a in alphas[i:]:
        if not stable(a):
            break
        up = a
    return down, up
