"""The first-order lag Bode plot for the prerequisite diagnostic's Q8.

Writes diagnostics/figures/first-order-lag.png.

Q8 asks for the magnitude and phase of a first-order lag at its own corner
frequency. The three landmarks are worth seeing on one picture rather than
read as a list, because the whole point is that they travel together: every
first-order lag looks exactly like this, whatever its corner.

  * well below the corner: 0 dB and 0 degrees, the signal passes through;
  * at the corner: -3 dB and -45 degrees, half the phase it will ever lose;
  * well above: falling at 20 dB/decade, phase heading to -90 degrees.

The straight-line asymptotes are drawn alongside the true curve, because the
gap between them *is* the 3 dB, and a student who has only seen the asymptotic
sketch often expects 0 dB at the corner.

The plotted system is Q8's own, G = 10/(s+10), so the figure and the question
cannot drift apart.

Run with `npm run models`, or directly.
"""

from __future__ import annotations

import base64
from pathlib import Path

import control as ct
import matplotlib
import numpy as np

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "cade30008"
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "diagnostics" / "figures" / "first-order-lag.png"

CURVE, MARK, INK, RULE, GRID = "#b01c2e", "#1f6f8b", "#333333", "#8a8a8a", "#d9dcdb"
WC = 10.0                                   # rad/s, Q8's corner


def main() -> None:
    G = ct.tf([WC], [1, WC])
    w = np.geomspace(WC / 100, WC * 100, 2000)
    mag, ph, w = ct.frequency_response(G, w)
    db, deg = 20 * np.log10(mag), ph * 180 / np.pi

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 5.4), sharex=True)

    # Magnitude, with the asymptotes that meet at the corner.
    ax1.semilogx(w, db, lw=2.2, color=CURVE, zorder=4)
    ax1.semilogx([w[0], WC], [0, 0], lw=1.1, ls=(0, (4, 3)), color=INK, alpha=0.65)
    ax1.semilogx([WC, w[-1]], [0, -20 * np.log10(w[-1] / WC)], lw=1.1, ls=(0, (4, 3)),
                 color=INK, alpha=0.65)
    ax1.plot([WC], [-3.01], "o", ms=8, color=MARK, mec="white", mew=1.5, zorder=6)
    ax1.annotate("−3 dB at the corner,\nnot 0 dB", xy=(WC, -3.01), xytext=(WC * 2.3, 1.5),
                 fontsize=9, color=MARK, linespacing=1.4,
                 arrowprops=dict(arrowstyle="-", color=MARK, lw=1.0))
    ax1.text(WC * 8, -13, "−20 dB/decade", fontsize=9, color=INK, alpha=0.9, rotation=-25)
    ax1.set_ylabel("Magnitude (dB)", color=INK)
    ax1.set_ylim(-45, 14)
    ax1.set_yticks([-40, -30, -20, -10, 0, 10])

    # Phase, with the decade-either-side rule made visible.
    ax2.semilogx(w, deg, lw=2.2, color=CURVE, zorder=4)
    ax2.axvspan(WC / 10, WC * 10, color=MARK, alpha=0.07, zorder=0)
    ax2.plot([WC], [-45], "o", ms=8, color=MARK, mec="white", mew=1.5, zorder=6)
    ax2.annotate("−45°, exactly half way", xy=(WC, -45), xytext=(WC * 1.7, -24),
                 fontsize=9, color=MARK,
                 arrowprops=dict(arrowstyle="-", color=MARK, lw=1.0))
    ax2.text(WC / 9.5, -84, "almost all the phase turns\nwithin a decade either side",
             fontsize=8.6, color=INK, alpha=0.9, linespacing=1.4)
    ax2.set_ylabel("Phase (deg)", color=INK)
    ax2.set_xlabel("Frequency (rad/s)", color=INK)
    ax2.set_ylim(-100, 10)
    ax2.set_yticks([-90, -45, 0])

    for ax in (ax1, ax2):
        ax.axvline(WC, lw=1.0, ls=(0, (2, 3)), color=MARK, alpha=0.8, zorder=1)
        ax.grid(True, which="both", color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        for s in ax.spines.values():
            s.set_color(RULE)
    ax1.text(WC * 1.06, 10.5, r"$\omega_\mathrm{c}$", fontsize=12, color=MARK)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=130, metadata={"Software": None})
    plt.close(fig)

    i = int(np.argmin(abs(w - WC)))
    kb = len(base64.b64encode(OUT.read_bytes())) / 1024
    print(f"{OUT.relative_to(ROOT)}: at w={WC:g} rad/s, {db[i]:.2f} dB and {deg[i]:.2f} deg; "
          f"{kb:.0f} kB base64")


if __name__ == "__main__":
    main()

# tracking: status=draft version=0
