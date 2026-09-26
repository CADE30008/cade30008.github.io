"""The Bode plot for the prerequisite diagnostic's frequency-domain question.

Writes diagnostics/figures/second-order-bode.png, which the quiz embeds.

The system is a standard second-order low-pass with zeta = 0.2 and
omega_n = 5 rad/s, chosen so that two facts are readable and one of them is a
trap:

  * the phase passes through -90 degrees at exactly omega_n, for any zeta.
    That is the exact route to omega_n and it is the one worth teaching;
  * the gain peaks at omega_r = omega_n sqrt(1 - 2 zeta^2) = 4.80 rad/s, which
    is *not* omega_n. A student who reads the peak frequency as the natural
    frequency gets 4.8, and that is the misconception the question is for.

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
OUT = ROOT / "diagnostics" / "figures" / "second-order-bode.png"

ZETA, WN = 0.2, 5.0


def main() -> None:
    G = ct.tf([WN**2], [1, 2 * ZETA * WN, WN**2])
    w = np.geomspace(0.2, 60, 2000)
    mag, phase, w = ct.frequency_response(G, w)
    db, deg = 20 * np.log10(mag), phase * 180 / np.pi

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 5.0), sharex=True)
    ax1.semilogx(w, db, color="#b01c2e", lw=2)
    ax1.set_ylabel("Magnitude (dB)")
    ax1.set_ylim(-45, 15)
    ax1.set_yticks([-40, -30, -20, -10, 0, 10])

    ax2.semilogx(w, deg, color="#b01c2e", lw=2)
    ax2.set_ylabel("Phase (deg)")
    ax2.set_xlabel("Frequency (rad/s)")
    ax2.set_ylim(-185, 5)
    ax2.set_yticks([-180, -135, -90, -45, 0])

    for ax in (ax1, ax2):
        ax.grid(True, which="both", color="#d9dcdb", lw=0.6)
        ax.set_axisbelow(True)
        for s in ax.spines.values():
            s.set_color("#8a8a8a")

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=130, metadata={"Software": None})
    plt.close(fig)

    peak_db = float(db.max())
    w_peak = float(w[db.argmax()])
    w_90 = float(w[np.argmin(abs(deg + 90))])
    kb = len(base64.b64encode(OUT.read_bytes())) / 1024
    print(f"{OUT.relative_to(ROOT)}: peak {peak_db:.2f} dB at {w_peak:.2f} rad/s, "
          f"phase -90 deg at {w_90:.2f} rad/s, {kb:.0f} kB base64")


if __name__ == "__main__":
    main()

# tracking: status=draft version=0
