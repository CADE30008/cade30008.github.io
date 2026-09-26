"""Why the week 1 system identification measures the trim, not the helicopter.

Writes docs/w01-design-cycle/figures/trim-stiffness.png.

Students fit a second-order model to the rig's elevation step response and get
a clean answer: omega_n = 0.99 rad/s, zeta = 0.06. The fit is good and the
arithmetic is right. The number is a property of **where the arm was sitting**,
not of the rig.

The mechanism
-------------
The arm pivots about a horizontal axis, so the gravity moment on it goes as
cos(eps), with eps measured from horizontal. Differentiating, the *stiffness*
goes as

    k(eps) = m L g sin(eps)

which is **zero at level** and grows with elevation. That is exactly why
Quanser's linearised model, taken about eps = 0, has no restoring term at all
and puts every open-loop pole at the origin: at level, there is no stiffness to
find. Away from level there is, and it depends on the angle.

So the natural frequency the laboratory measures is

    omega_n(eps) = sqrt( m L g sin(eps) / J )

Identify at 5 degrees and get 0.84 rad/s. At 10 degrees, 1.19. At 20, 1.67.
Same rig, same method, three different models, none of them wrong.

Checking it against the measured data
-------------------------------------
`d_Part1.mat` steps 0 -> 2 V and settles at 6.95 degrees, oscillating at
omega_n = 0.9857 rad/s. Inverting the expression above, that needs an
unbalanced moment of 0.7486 kg m. The candidates from Quanser's own constants:

    body alone, 2 m_f La          0.7595 kg m     -1.4%
    counterweight alone, m_w Lw   0.8787 kg m    -14.8%
    their difference              0.1193 kg m   +527.7%

So the measurement matches **the helicopter body with no counterweight
contribution**, to under 2%. Either the counterweight was off for this run or
it was not where the model assumes. It is emphatically not the balanced arm the
linearised model describes.

Open: which way is the arm unbalanced
-------------------------------------
Quanser's constants make the counterweight the heavier end, 0.8787 kg m against
0.7595 for the body, which would rest with the props UP. Steve reports the rigs
sit prop-end on the deck when powered off, which is the other way round. So
either the counterweight is set lighter than the catalogue figure on our rigs,
or it is adjustable and was moved.

That matters, because "the counterweight contributed nothing" is only one
reading of the 1.4% match below. A partial counterweight contribution at some
resting angle would fit too. The sin(eps) mechanism does not depend on which is
right - the stiffness is still zero at level and grows with angle - but the
particular m L should not be treated as settled until somebody weighs the arm.

What still does not close
-------------------------
The DC gain. This model predicts about 10 deg/V and the data shows 3.47, a
factor of 2.9. So the stiffness side is understood and the actuation side is
not: possibly one motor rather than two, possibly a different force constant,
possibly the logged "input" is not volts at the motor. The teaching point rests
on the stiffness, so it survives, but the gain should not be quoted until
somebody puts a meter on the rig.

Run with `npm run models`, or directly.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "cade30008"
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "w01-design-cycle" / "figures" / "trim-stiffness.png"

CURVE, MEASURED, INK, RULE, GRID = "#b01c2e", "#1f6f8b", "#333333", "#8a8a8a", "#d9dcdb"

# Quanser's constants, Lab 2, setup_heli_3d_configuration.m.
m_h, m_w, g = 1.15, 1.87, 9.81
m_f = m_h / 2
La, Lw = 26.0 * 0.0254, 18.5 * 0.0254
J = m_w * Lw**2 + 2 * m_f * La**2       # 0.914 kg m^2
ML = 2 * m_f * La                       # what the data says is unbalanced

EPS_MEAS, WN_MEAS = 6.949, 0.9857       # from d_Part1.mat


def omega_n(eps_deg):
    return np.sqrt(ML * g * np.sin(np.radians(eps_deg)) / J)


def main() -> None:
    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    e = np.linspace(0.05, 35, 600)
    ax.plot(e, omega_n(e), lw=2.4, color=CURVE, zorder=3)

    ax.plot([EPS_MEAS], [WN_MEAS], "o", ms=9, color=MEASURED, mec="white", mew=1.6,
            zorder=5)
    ax.annotate(f"the one run we have:\n{EPS_MEAS:.1f}°, {WN_MEAS:.2f} rad/s",
                xy=(EPS_MEAS, WN_MEAS), xytext=(EPS_MEAS + 3.2, WN_MEAS - 0.34),
                fontsize=9, color=MEASURED, linespacing=1.4,
                arrowprops=dict(arrowstyle="-", color=MEASURED, lw=1.0))

    for e0 in (5, 10, 20):
        w = omega_n(e0)
        ax.plot([e0, e0], [0, w], lw=1.0, ls=(0, (3, 3)), color=INK, alpha=0.5)
        ax.plot([0, e0], [w, w], lw=1.0, ls=(0, (3, 3)), color=INK, alpha=0.5)
        ax.annotate(f"{w:.2f}", xy=(0.4, w + 0.03), fontsize=8.6, color=INK, alpha=0.9)

    ax.annotate("at level there is no stiffness at all:\nthis is the plant the model describes",
                xy=(0.6, 0.12), xytext=(6.5, 0.20), fontsize=8.8, color=INK,
                linespacing=1.4, alpha=0.9,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.9, alpha=0.7))

    ax.set_xlim(0, 35)
    ax.set_ylim(0, 2.3)
    ax.set_xlabel("Elevation the arm was trimmed to (deg)", color=INK)
    ax.set_ylabel(r"$\omega_\mathrm{n}$ you would measure (rad/s)", color=INK)
    ax.set_title("The natural frequency is a property of the trim, not the rig",
                 fontsize=11.5, color=INK, pad=9)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color(RULE)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=130, metadata={"Software": None})
    plt.close(fig)

    implied = J * WN_MEAS**2 / (g * np.sin(np.radians(EPS_MEAS)))
    print(f"{OUT.relative_to(ROOT)}")
    print(f"  measured {WN_MEAS} rad/s at {EPS_MEAS} deg implies m*L = {implied:.4f} kg m")
    print(f"  body alone 2*m_f*La = {ML:.4f} kg m, which is {100 * (implied / ML - 1):+.1f}% away")
    print("  omega_n at 5, 10, 20 deg: " +
          ", ".join(f"{omega_n(x):.2f}" for x in (5, 10, 20)) + " rad/s")


if __name__ == "__main__":
    main()

# tracking: status=draft version=0
