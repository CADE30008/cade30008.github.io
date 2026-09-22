"""The Quanser 3-DOF helicopter's elevation axis, and the envelope we will fly.

One source for two things that must never disagree: the model students fit in
week 1, and the envelope `scripts/gains.py` uses to decide whether a submitted
set of gains is safe to put on the hardware.

The physics
-----------
The elevation axis, **as measured on the rig**, is a stable but very lightly
damped second order:

    G(s) = eps(s) / V(s) = K wn^2 / (s^2 + 2 zeta wn s + wn^2)

with K about 3.4 deg/V, wn about 1.0 rad/s and zeta about 0.06, where V is the
voltage applied to both motors together about the operating point that holds
the arm at its trim. Fitted from the laboratory's own recording; the numbers
live in elevation_plant.json and are refitted from the rig each year.

Read those three numbers and you know what the machine does. It is stable:
disturb it and it does come back. But zeta = 0.06 is almost no damping, so the
oscillation has a period of about six seconds and takes something like a
minute to die away.

**This is not the model Quanser's own linearisation gives**, which is a double
integrator with no restoring term at all. Both are defensible and the section
below has the provenance and the unresolved experiment. The short version:
gravity stiffness on the arm goes as sin(elevation), so it vanishes at level,
which is exactly where Quanser linearise. The rig is flown about a trim, and
there it oscillates. We fly the measured model.

For a PID controller C(s) = Kd s + Kp + Ki/s the closed-loop characteristic
polynomial is

    s^3 + (2 zeta wn + K wn^2 Kd) s^2 + (wn^2 + K wn^2 Kp) s + K wn^2 Ki

and Routh on s^3 + a2 s^2 + a1 s + a0 asks for all coefficients positive and

    a2 a1 > a0

which is a condition a student can check on paper. Integral action is
therefore not free: raise Ki far enough, with Kp and Kd fixed, and the loop
goes unstable. That inequality is the reason the filter below exists.

What proportional gain cannot do
--------------------------------
Close a proportional loop alone around this plant and the characteristic
polynomial is

    s^2 + 2 zeta wn s + wn^2 (1 + K Kp)

Kp does not appear in the coefficient of s. The real part of the closed-loop
poles is pinned at -zeta wn however hard you push, so the locus is a vertical
line: the oscillation gets faster, the damping ratio falls as
zeta / sqrt(1 + K Kp), and the settling time does not move at all. Going from
Kp = 0.5 to Kp = 10 takes the overshoot from 89% to 97% and leaves the
settling time at 65 seconds.

So the room's reflex, "turn Kp up", is answered with a number rather than an
assertion, and the derivative term is motivated rather than announced: damping
has to come from somewhere, and Kp is not where. See
models/w01_proportional_limit.py for the figure and the check against MATLAB.

**A correction worth recording.** While this file carried the double
integrator it also claimed the loop was *conditionally stable*: that scaling
every gain by alpha gave alpha K Kd Kp > Ki, so the loop was stable for large
alpha and unstable for small, and that "turning the gain down is what breaks
it". That is true of a double integrator and **false of this plant**. Scaling
the gains of a working design down by a factor of a hundred leaves the second
order loop stable, because the wn^2 term keeps a2 a1 above a0 as the gains
vanish. Checked numerically, not reasoned about. The envelope below still asks
how far the loop gain can move in both directions, which remains the honest
question for a plant whose K is a fit rather than a constant.

Where the double integrator comes from, and why it is disputed
--------------------------------------------------------------
**Provenance, which this file did not carry until 21 September.** The model
above is Quanser's own, not an assumption: `HELI3D_ABCD_eqns.m` in
`private/quanser` (Lab 2, theirs) gives

    A[4,1] = 0                                  no restoring term at level
    B[4,1] = La*Kf/(m_w*Lw^2 + 2*m_f*La^2)      which is this file's La*Kf/Je

and all six open-loop eigenvalues are at the origin. So elevation linearised
about **level** is a driven double integrator, exactly as described.

**But the rig does not behave like one, and the laboratory's own material says
so.** `solution_files/s_1_system_identification.mlx` fits the measured step in
`d_Part1.mat` and gets a stable, lightly damped second order:

    G(s) = 3.4 / (s^2 + 0.12 s + 1)     deg/V,  omega_n = 1, zeta = 0.06

Refitting that data independently gives a DC gain of 3.47 deg/V and the same
frequency and damping, so their numbers hold.

**Steve's account of the hardware**, 21 September: the elevation axis oscillates
about *any* trim point; raising the motor voltage raises the trim elevation;
disturbing it gives a lightly damped oscillation. That is a stable second-order
system, not a double integrator, and it matches the data.

**The two are not in conflict about the physics, only about the operating
point.** The arm's gravity moment goes as cos(elevation), so its *stiffness*
goes as sin(elevation): zero at level, growing as you move away from it. At
level there is nothing to oscillate against, which is what Quanser linearise;
away from level there is, which is what the laboratory measures.

**What is not resolved.** The fitted model has omega_n = 1 at its trim, and
treats it as constant. The geometry above says omega_n should rise with trim
elevation, as sqrt(sin(eps)). One dataset at one trim cannot tell those apart,
and `d_Part3_*.mat` are closed-loop runs, so they do not settle it either.

    The experiment: record open-loop steps to two or three different trim
    elevations and fit each. If omega_n is the same at all of them, the plant
    is linear time-invariant over the working range and the laboratory model is
    simply right. If omega_n rises with trim, the stiffness is geometric and
    the model is only valid near the trim it was fitted at.

**Part of it is already answered, by the recording we have.** Measured on
d_Part1.mat, 22 September: before the step the arm is swinging about roughly
-1.5 degrees, close to the encoder's level datum, with a period of 5.85 s;
after the step it settles at +6.97 degrees and swings with a period of 6.02 s.
The same frequency at level and at seven degrees, within 3%.

That rules out the strong form of the sin(elevation) story. If the only
restoring term were gravity on an offset mass, the stiffness would vanish at
level and the period there would grow without limit. It does not. This rig has
stiffness at level that a pure balance arm cannot produce, which points at the
centre of mass sitting below the line of the arm: a pendulum rather than a
balance.

So the reconciliation offered above is the right shape and the wrong mechanism,
and models/quanser_trim_stiffness.py predicts numbers this rig does not have
(omega_n of 0.84, 1.19 and 1.67 at 5, 10 and 20 degrees). **Do not quote those
in the room.** Two trims seven degrees apart do not establish that omega_n is
constant over the whole working range either, so rig_trim_sweep.m is still
worth running across a wider spread.

**This is not currently said to students.** The laboratory pages and the Drive
README used to carry a note that the two models disagree; it came out on
22 September because presenting an unsettled disagreement to a student who has
just met the material costs more confusion than it buys. The student text now
states what `heli3d_model` is, with no framing, and says to use whichever
model matches where they are flying. Put the note back as a finding once the
trim sweep has settled it.

Until that is done, **do not treat the question as settled**, even though the
code now commits to the measured second order. The envelope and the Routh
condition follow from that choice, and if the trim sweep shows wn moving with
trim then every fit is local and a controller designed at one trim is being
flown at another.

Week 1's hook was rewritten for the same reason. "It cannot be flown by hand"
is true of a double integrator and false of a lightly damped stable system,
which can be flown badly. The hook now rests on the volunteer flying all three
coupled axes, which is hard for reasons that survive either model, and that
failure is what motivates taking elevation alone.

See `models/quanser_trim_stiffness.py` for the geometry and the numbers.

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
# deg/s. Quanser rate-limit the *demand*, not just the output: the block is
# "Des Position Rate Limiter" in q_heli3d.mdl and the value is CMD_RATE_LIMIT
# in setup_lab_heli_3d.m, 45*pi/180 rad/s. The guide says why - it "eliminates
# high-frequency changes ... which places less strain on the actuator".
#
# It has to be modelled, not ignored. Checking a PID design against an
# instantaneous step asks the derivative term to differentiate a discontinuity,
# which demands hundreds of volts from a 24 V amplifier and rejects every
# sane design. The rig is never commanded that way.
CMD_RATE_DEG_S = 45.0

# Derivative filter. An ideal PID is not a real controller: its derivative term
# is non-proper, so a step demand asks the motors for an impulse, and any
# estimate of peak voltage made from it is infinite rather than merely wrong.
# Every real implementation filters the derivative, the rig's included. N = 10
# is the course's own convention, set once in week 3 and used everywhere after,
# so a student's gains mean the same thing here as they do on their own plots.
DERIVATIVE_FILTER_N = 10.0


@dataclass(frozen=True)
class Plant:
    """G(s) = K wn^2 / (s^2 + 2 zeta wn s + wn^2), fitted from the rig.

    Second order, not the double integrator Quanser's own linearisation gives.
    Both are defensible and the section at the top of this file explains why;
    the short version is that gravity stiffness goes as sin(elevation), so it
    vanishes at level, which is exactly where Quanser linearise. The rig is
    flown about a trim, not about level, and there it oscillates.

    K is in degrees per volt, because degrees are what the encoder reports and
    what a student reads off a plot. Anything comparing against Quanser's
    rad/(V s^2) has to convert.
    """

    K: float                      # deg / V
    wn: float                     # rad / s
    zeta: float                   # dimensionless
    source: str                   # where the numbers came from
    measured: str                 # when

    def tf(self):
        import control as ct
        return ct.tf([self.K * self.wn**2],
                     [1, 2 * self.zeta * self.wn, self.wn**2])


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
    routh_margin: float = 1.15    # a2 a1 must beat a0 by this factor
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
    for key in ("K", "wn", "zeta", "source", "measured"):
        if key not in d:
            raise SystemExit(
                f"{path.name} has no {key!r}.\n"
                "A file with only K is the old double-integrator model. The\n"
                "plant is second order now: refit with models/fit_second_order.m\n"
                "and write K, wn and zeta."
            )
    for key in ("K", "wn"):
        if not (d[key] > 0):
            raise SystemExit(f"{path.name}: {key} must be positive, got {d[key]}")
    if not (0 < d["zeta"] < 1):
        raise SystemExit(
            f"{path.name}: zeta must be between 0 and 1, got {d['zeta']}.\n"
            "The fitted axis is underdamped; a value outside that range means\n"
            "the fit failed rather than that the rig changed."
        )
    return Plant(K=float(d["K"]), wn=float(d["wn"]), zeta=float(d["zeta"]),
                 source=str(d["source"]), measured=str(d["measured"]))


def routh(plant: Plant, kp: float, ki: float, kd: float) -> tuple[bool, float]:
    """The hand-checkable stability condition, and how much room it has.

    PID around the second-order plant gives

        s^3 + (2 zeta wn + K wn^2 Kd) s^2 + (wn^2 + K wn^2 Kp) s + K wn^2 Ki

    and Routh on s^3 + a2 s^2 + a1 s + a0 asks for a2 a1 > a0 with all
    positive. Returns (passes, ratio) where ratio = a2 a1 / a0; above 1 is
    stable, and the envelope asks for more so that a rig which is not quite
    the fitted model still flies.

    This replaces the condition K Kd Kp > Ki, which is Routh for the double
    integrator and was used here while that was the assumed plant. It is not a
    conservative version of the one above, it is a different inequality, and
    it accepts gains that this plant would not fly.
    """
    if min(kp, ki, kd) <= 0:
        return False, 0.0
    a2 = 2 * plant.zeta * plant.wn + plant.K * plant.wn**2 * kd
    a1 = plant.wn**2 + plant.K * plant.wn**2 * kp
    a0 = plant.K * plant.wn**2 * ki
    if a0 <= 0:
        return False, 0.0
    return (a2 * a1) > a0, (a2 * a1) / a0


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
