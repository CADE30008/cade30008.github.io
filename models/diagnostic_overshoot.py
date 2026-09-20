"""The overshoot-against-damping figure for the prerequisite diagnostic.

Writes diagnostics/figures/overshoot-vs-damping.png, which the quiz embeds.

The question's feedback makes three claims, and a curve can show all three at
once where prose can only assert them:

  * the pairing worth carrying: zeta = 0.4 gives about a quarter overshoot;
  * three anchors to interpolate between, because nobody evaluates the
    exponential in a design meeting;
  * that the curve is steep, so a small change in damping moves the overshoot
    a lot. Near zeta = 0.4 it runs at about 104 percentage points of overshoot
    per unit zeta, which is the reason phase margin is worth watching later.

Only the overshoot curve is drawn. Dorf's figure 5.7 puts normalised peak time
on a second axis beside it, which is useful in a design chapter and clutter
here, where the question is only about overshoot.

Run with `npm run models`, or directly.
"""

from __future__ import annotations

import base64
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "cade30008"
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "diagnostics" / "figures" / "overshoot-vs-damping.png"

CURVE, ANSWER, INK, RULE, GRID = "#b01c2e", "#1f6f8b", "#333333", "#8a8a8a", "#d9dcdb"

# The three anchors the feedback asks students to carry. The middle one is the
# question's own answer, so it is drawn differently.
ANCHORS = [0.2, 0.4, 0.7]
ANSWER_ZETA = 0.4


def overshoot(zeta):
    """Percent overshoot of a second-order step response. Underdamped only."""
    return 100 * np.exp(-np.pi * zeta / np.sqrt(1 - zeta**2))


def main() -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    z = np.linspace(0.02, 0.95, 800)
    ax.plot(z, overshoot(z), lw=2.4, color=CURVE, zorder=3)

    for zeta in ANCHORS:
        mp = overshoot(zeta)
        is_answer = zeta == ANSWER_ZETA
        colour = ANSWER if is_answer else INK
        ax.plot([zeta, zeta], [0, mp], lw=1.0, ls=(0, (3, 3)), color=colour, alpha=0.75, zorder=2)
        ax.plot([0, zeta], [mp, mp], lw=1.0, ls=(0, (3, 3)), color=colour, alpha=0.75, zorder=2)
        ax.plot([zeta], [mp], "o", ms=8 if is_answer else 6,
                color=colour, mec="white", mew=1.4, zorder=5)
        ax.annotate(f"$\\zeta$ = {zeta}\n{mp:.0f}%",
                    xy=(zeta, mp), xytext=(zeta + 0.045, mp + (7 if is_answer else 5)),
                    color=colour, fontsize=10,
                    fontweight="bold" if is_answer else "normal", linespacing=1.35)

    # How steep it is, at the point the question asks about.
    lo, hi = ANSWER_ZETA - 0.05, ANSWER_ZETA + 0.05
    ax.fill_between([lo, hi], 0, 100, color=ANSWER, alpha=0.07, zorder=0)
    ax.annotate("", xy=(hi, overshoot(hi)), xytext=(lo, overshoot(lo)),
                arrowprops=dict(arrowstyle="<|-|>", color=ANSWER, lw=1.2,
                                shrinkA=0, shrinkB=0))
    # Upper right is the only large clear area; anything nearer the curve
    # collided with an anchor label.
    ax.annotate(f"$\\pm$0.05 in $\\zeta$ is\n{abs(overshoot(hi) - overshoot(lo)) / 2:.0f} points of overshoot",
                xy=(0.452, 23), xytext=(0.545, 58), color=ANSWER, fontsize=9.5,
                linespacing=1.4, ha="left",
                arrowprops=dict(arrowstyle="-", color=ANSWER, lw=0.9, alpha=0.7))

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Damping ratio, $\\zeta$", fontsize=11, color=INK)
    ax.set_ylabel("Overshoot (%)", fontsize=11, color=INK)
    ax.set_xticks(np.arange(0, 1.01, 0.1))
    ax.set_yticks(np.arange(0, 101, 20))
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_color(RULE)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=130, metadata={"Software": None})
    plt.close(fig)

    kb = len(base64.b64encode(OUT.read_bytes())) / 1024
    pairs = ", ".join(f"{z}->{overshoot(z):.1f}%" for z in ANCHORS)
    slope = (overshoot(ANSWER_ZETA + 0.01) - overshoot(ANSWER_ZETA - 0.01)) / 0.02
    print(f"{OUT.relative_to(ROOT)}: anchors {pairs}; "
          f"slope at zeta={ANSWER_ZETA} is {slope:.0f} points per unit zeta; {kb:.0f} kB base64")


if __name__ == "__main__":
    main()
