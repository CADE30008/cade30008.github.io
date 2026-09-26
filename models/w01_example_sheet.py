"""The measured-response figure for week 1's example sheet, and its answers.

Writes docs/w01-design-cycle/figures/example-response.png and prints every
number the solutions quote, so the solutions are transcribed from a run of
this file rather than worked out by hand and hoped over.

The system is not the rig. It is a second order with different numbers, so
that a student who remembers the rig's 3.4 / 1.0 / 0.06 cannot pattern-match
their way to the answer.

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
OUT = ROOT / "docs" / "w01-design-cycle" / "figures" / "example-response.png"

CURVE, INK, RULE, GRID = "#b01c2e", "#333333", "#8a8a8a", "#d9dcdb"

# The truth the figure is drawn from. Chosen so the peaks land near enough to
# gridlines to be readable with a ruler, and so zeta is not a round number.
K, WN, ZETA = 2.5, 1.4, 0.12
STEP_V = 2.0
TRIM = 3.0          # deg, where it sat before the step


def response(t):
    wd = WN * np.sqrt(1 - ZETA**2)
    env = np.exp(-ZETA * WN * t)
    return TRIM + K * STEP_V * (1 - env * (np.cos(wd * t) + (ZETA * WN / wd) * np.sin(wd * t)))


def main():
    t = np.linspace(0, 25, 4000)
    y = response(t)

    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    ax.plot(t, y, color=CURVE, lw=1.8)
    ax.axhline(TRIM + K * STEP_V, color=RULE, ls="--", lw=1.1)
    ax.axhline(TRIM, color=RULE, ls=":", lw=1.1)
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 12)
    ax.set_xticks(np.arange(0, 26, 1), minor=True)
    ax.set_xticks(np.arange(0, 26, 5))
    ax.set_yticks(np.arange(0, 12.5, 0.5), minor=True)
    ax.set_yticks(np.arange(0, 13, 2))
    ax.grid(which="major", color=GRID, lw=0.9)
    ax.grid(which="minor", color=GRID, lw=0.4, alpha=0.7)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Angle (deg)")
    ax.set_title("Measured response to a 2.0 V step, applied at t = 0",
                 fontsize=12, color=INK)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200)
    plt.close(fig)
    print(f"wrote {OUT.relative_to(ROOT)}")

    # ---- the answers -----------------------------------------------------
    wd = WN * np.sqrt(1 - ZETA**2)
    period = 2 * np.pi / wd
    final = TRIM + K * STEP_V

    print(f"\ntruth:        K = {K}, wn = {WN}, zeta = {ZETA}, step = {STEP_V} V")
    print(f"trim before   {TRIM:.2f} deg")
    print(f"final value   {final:.2f} deg")
    print(f"K measured    ({final:.2f} - {TRIM:.2f}) / {STEP_V} = {(final-TRIM)/STEP_V:.3f} deg/V")
    print(f"wd            {wd:.4f} rad/s,  period {period:.3f} s")

    # Peaks, as a student would read them.
    peaks = []
    for n in range(1, 6):
        tp = n * np.pi / wd if n % 2 == 1 else n * np.pi / wd
        peaks.append((tp, response(np.array([tp]))[0]))
    print("\nturning points (odd are overshoots, even are undershoots):")
    for i, (tp, yp) in enumerate(peaks, 1):
        print(f"  {i}: t = {tp:6.3f} s,  y = {yp:6.3f} deg,  "
              f"deviation {yp - final:+.3f}")

    a1 = peaks[0][1] - final
    a3 = peaks[2][1] - final
    delta_adj = np.log(a1 / a3)              # one full cycle apart
    zeta_adj = delta_adj / np.sqrt(4 * np.pi**2 + delta_adj**2)
    print(f"\nfirst and second overshoot: {a1:.4f}, {a3:.4f}")
    print(f"log decrement (one cycle)  = ln({a1:.4f}/{a3:.4f}) = {delta_adj:.4f}")
    print(f"zeta from it               = {zeta_adj:.4f}")
    print(f"wn = wd/sqrt(1-zeta^2)     = {wd/np.sqrt(1-zeta_adj**2):.4f} rad/s")

    os_pct = 100 * np.exp(-np.pi * ZETA / np.sqrt(1 - ZETA**2))
    ts = -np.log(0.02 * np.sqrt(1 - ZETA**2)) / (ZETA * WN)
    print(f"\novershoot     {os_pct:.1f}%")
    print(f"settling 2%   {ts:.2f} s")

    # ---- Q3: what proportional gain does to this plant -------------------
    print("\nproportional loop on this plant:")
    print(f"{'Kp':>6}{'zeta_cl':>10}{'wn_cl':>9}{'OS %':>8}{'ts 2%':>8}{'ss err %':>10}")
    for kp in (0.0, 1.0, 4.0):
        zc = ZETA / np.sqrt(1 + K * kp)
        wc = WN * np.sqrt(1 + K * kp)
        o = 100 * np.exp(-np.pi * zc / np.sqrt(1 - zc**2))
        s = -np.log(0.02 * np.sqrt(1 - zc**2)) / (zc * wc)
        e = 100 / (1 + K * kp)
        print(f"{kp:6.1f}{zc:10.4f}{wc:9.3f}{o:8.1f}{s:8.2f}{e:10.1f}")


if __name__ == "__main__":
    main()

# tracking: status=draft version=0
