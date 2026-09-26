"""Why turning the gain up does not help on the elevation axis.

Writes docs/w01-design-cycle/figures/proportional-limit.png, which week 1's
handout and slides both embed.

The rig's elevation axis, fitted from the laboratory's own recording, is a
stable but very lightly damped second order:

    G(s) = K * wn^2 / (s^2 + 2*zeta*wn*s + wn^2),  K = 3.4, wn = 1.0, zeta = 0.06

Close a proportional loop around it and the characteristic polynomial is

    s^2 + 2*zeta*wn*s + wn^2 * (1 + K*Kp)

The coefficient of s does not contain Kp. Two things follow, and the figure
shows both because prose can only assert them:

  * the real part of the closed-loop poles is pinned at -zeta*wn = -0.06
    whatever the gain, so the locus is a vertical line and the settling time
    does not improve at all;
  * the damping ratio falls as zeta/sqrt(1 + K*Kp), so the overshoot gets
    steadily worse.

This replaces an earlier argument built on a double-integrator model, which
said proportional feedback could not stabilise the axis at any gain. That is
true of a double integrator and false here: this plant is already stable. The
honest version is that proportional feedback cannot *damp* it, which is the
same lesson and survives contact with the measured rig.

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
OUT = ROOT / "docs" / "w01-design-cycle" / "figures" / "proportional-limit.png"

CURVE, OPEN, INK, RULE, GRID = "#b01c2e", "#1f6f8b", "#333333", "#8a8a8a", "#d9dcdb"

K, WN, ZETA = 3.4, 1.0, 0.06

# The gains drawn as step responses. Kept few, and spread over more than an
# order of magnitude, so the point is that nothing improves rather than that
# the lines are close together.
SHOWN = [0.5, 2.0, 10.0]


def closed_loop_poles(kp):
    """Roots of s^2 + 2*zeta*wn*s + wn^2*(1 + K*Kp)."""
    return np.roots([1.0, 2 * ZETA * WN, WN**2 * (1 + K * kp)])


def step_response(kp, t):
    """Unit step of the proportional loop, in closed form.

    Solved rather than simulated: the closed loop is a standard second order,
    and scipy is not a dependency of this repository.
    """
    wc = WN * np.sqrt(1 + K * kp)
    zc = ZETA / np.sqrt(1 + K * kp)
    dc = K * kp / (1 + K * kp)
    wd = wc * np.sqrt(1 - zc**2)
    envelope = np.exp(-zc * wc * t)
    return dc * (1 - envelope * (np.cos(wd * t) + (zc * wc / wd) * np.sin(wd * t)))


def main():
    fig, (ax_s, ax_t) = plt.subplots(1, 2, figsize=(10.4, 4.3))

    # --- left: where the poles go ---------------------------------------
    gains = np.concatenate([[0.0], np.logspace(-1.3, 1.4, 240)])
    poles = np.array([closed_loop_poles(g)[0] for g in gains])
    ax_s.plot(poles.real, poles.imag, color=CURVE, lw=2, zorder=3)
    ax_s.plot(poles.real, -poles.imag, color=CURVE, lw=2, zorder=3)

    op = closed_loop_poles(0.0)
    ax_s.plot(op.real, op.imag, "x", color=OPEN, ms=10, mew=2.2, zorder=4,
              label="open loop, $K_\\mathrm{p}=0$")

    ax_s.axvline(-ZETA * WN, color=RULE, ls=":", lw=1.4, zorder=2)
    ax_s.annotate(f"$\\mathrm{{Re}} = -\\zeta\\omega_\\mathrm{{n}} = {-ZETA * WN:.2f}$,\nwhatever the gain",
                  xy=(-ZETA * WN, 4.4), xytext=(-0.055, 4.2),
                  fontsize=10.5, color=INK, ha="left", va="top")

    ax_s.axhline(0, color=GRID, lw=1, zorder=1)
    ax_s.axvline(0, color=GRID, lw=1, zorder=1)
    ax_s.set_xlim(-0.30, 0.10)
    ax_s.set_ylim(-6.2, 6.2)
    ax_s.set_xlabel("Real")
    ax_s.set_ylabel("Imaginary")
    ax_s.set_title("The poles slide straight up", fontsize=12, color=INK)
    ax_s.legend(loc="lower left", fontsize=10, frameon=False)
    ax_s.grid(color=GRID, lw=0.6, alpha=0.6)

    # --- right: what that looks like ------------------------------------
    t = np.linspace(0, 80, 3000)
    for kp, style in zip(SHOWN, ["-", "--", ":"]):
        zc = ZETA / np.sqrt(1 + K * kp)
        ax_t.plot(t, step_response(kp, t), style, color=CURVE, lw=1.6,
                  label=f"$K_\\mathrm{{p}}={kp:g}$,  $\\zeta={zc:.3f}$")

    ax_t.axhline(1.0, color=RULE, ls="-", lw=1.0)
    ax_t.annotate("demand", xy=(78, 1.0), xytext=(78, 1.08),
                  fontsize=10, color=INK, ha="right")
    # The curves are not normalised, on purpose. None of them reaches the
    # demand, and the gap is the proportional loop's steady-state error:
    # K*Kp/(1 + K*Kp) of what was asked for. It shrinks as the gain rises,
    # which is the one thing more gain does buy here, and it is the argument
    # for integral action.
    ax_t.annotate("none of them gets there:\nthat gap is what $K_\\mathrm{i}$ is for",
                  xy=(64, 0.64), xytext=(26, 0.26),
                  fontsize=10.5, color=INK, ha="left",
                  arrowprops=dict(arrowstyle="->", color=RULE, lw=1.1))
    ax_t.set_xlim(0, 80)
    ax_t.set_ylim(0, 2.05)
    ax_t.set_xlabel("Time (s)")
    ax_t.set_ylabel("Elevation, for a demand of 1")
    ax_t.set_title("More gain, more overshoot, same 65 s", fontsize=12, color=INK)
    # Upper right: the only corner the decaying curves leave alone.
    ax_t.legend(loc="upper right", fontsize=10, frameon=False)
    ax_t.grid(color=GRID, lw=0.6, alpha=0.6)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200)
    plt.close(fig)

    # Numbers quoted in the handout, printed so they are checked rather than
    # remembered. Settling time is the 2% band, from the envelope.
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"{'Kp':>6}  {'zeta':>7}  {'wn':>6}  {'overshoot %':>12}  {'ts 2% (s)':>10}"
          f"  {'ss error %':>11}")
    for kp in [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]:
        zc = ZETA / np.sqrt(1 + K * kp)
        wc = WN * np.sqrt(1 + K * kp)
        os_pct = 100 * np.exp(-np.pi * zc / np.sqrt(1 - zc**2))
        ts = -np.log(0.02 * np.sqrt(1 - zc**2)) / (zc * wc)
        sse = 100 * (1 - K * kp / (1 + K * kp)) if kp else 100.0
        print(f"{kp:6.1f}  {zc:7.4f}  {wc:6.3f}  {os_pct:12.1f}  {ts:10.1f}  {sse:11.1f}")


if __name__ == "__main__":
    main()

# tracking: status=draft version=0 assisted=true
