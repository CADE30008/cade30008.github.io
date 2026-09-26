"""The s-plane figure for the prerequisite diagnostic's pole question.

Writes diagnostics/figures/pole-locations.png, which the quiz embeds.

The figure answers three questions at once, because students routinely have one
of them and not the others:

  * what the left and right halves mean. Real part negative and the response
    decays, positive and it grows. The halves are shaded rather than only
    labelled, so that much is legible before any text is read;
  * what the vertical axis does. Height off the axis is the oscillation frequency,
    and a pair sitting *on* the axis oscillates for ever, which is the case students
    most often miss because it is neither stable nor unstable;
  * that the two are independent, which is the real idea. Cases 1 and 2 share
    a real part and differ only in the imaginary part, so they decay at exactly
    the same rate and only one of them oscillates. Putting them at the same sigma is
    the whole reason the figure is laid out this way.

Four cases, one for each option in the question, so the figure doubles as a key
to the four answers. Conjugate pairs are drawn as pairs: the second root is
what makes the response a real oscillation rather than a complex one, and
dropping it invites the idea that a lone complex pole is a thing you can have.

Each response is drawn over whatever window shows its shape, and with its own
vertical scale, so neither axis carries numbers: the figure is about what shape
each location produces, not how fast. A growing exponential in particular
dwarfs its own first cycle if you give it long enough, so case 4 gets a shorter
window than the rest.

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
OUT = ROOT / "diagnostics" / "figures" / "pole-locations.png"

DECAY, MARGINAL, GROW = "#1f6f8b", "#c98a00", "#b01c2e"
SHADE_L, SHADE_R = "#edf3f6", "#fbeef0"
INK, RULE = "#333333", "#8a8a8a"

# sigma, omega, colour, label offset for the number, time window, caption.
# omega = 0 is a single real pole rather than a conjugate pair. Cases 1 and 2
# share a sigma on purpose: same envelope, and only the imaginary part differs.
CASES = [
    (-1.2, 3.6, DECAY,    (-0.62, 0.42), 4.0, "decays while oscillating"),
    (-1.2, 0.0, DECAY,    (-0.62, 0.42), 4.0, "decays, no oscillation"),
    (0.0,  4.3, MARGINAL, (0.46, 0.36),  4.0, "oscillates for ever"),
    (1.2,  3.6, GROW,     (0.46, 0.42),  2.0, "grows while oscillating"),
]


def response(sigma: float, omega: float, t: np.ndarray) -> np.ndarray:
    """The shape of the response a pole at sigma +/- j*omega produces."""
    env = np.exp(sigma * t)
    return env if omega == 0 else env * np.cos(omega * t)


def plane(ax) -> None:
    xlim, ylim = (-4.0, 4.0), (-5.4, 5.4)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    mid = (0 - xlim[0]) / (xlim[1] - xlim[0])
    ax.axhspan(*ylim, xmin=0, xmax=mid, color=SHADE_L, zorder=0)
    ax.axhspan(*ylim, xmin=mid, xmax=1, color=SHADE_R, zorder=0)

    ax.annotate("", xy=(xlim[1], 0), xytext=(xlim[0], 0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3))
    ax.annotate("", xy=(0, ylim[1]), xytext=(0, ylim[0]),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3))
    ax.text(xlim[1] - 0.10, -0.95, r"$\sigma$", color=INK, fontsize=14, ha="right")
    ax.text(0.14, ylim[1] - 0.06, r"$j\omega$", color=INK, fontsize=14, va="top")

    ax.text(xlim[0] + 0.18, ylim[1] - 0.22, "LEFT HALF\nresponse decays",
            color=DECAY, fontsize=10, fontweight="bold", va="top", linespacing=1.4)
    ax.text(xlim[1] - 0.18, ylim[1] - 0.22, "RIGHT HALF\nresponse grows",
            color=GROW, fontsize=10, fontweight="bold", va="top", ha="right",
            linespacing=1.4)

    for n, (sigma, omega, colour, (dx, dy), _, _) in enumerate(CASES, 1):
        roots = [(sigma, omega)] if omega == 0 else [(sigma, omega), (sigma, -omega)]
        for x, y in roots:
            ax.plot([x], [y], marker="x", ms=11, mew=2.6, color=colour, zorder=5)
        x, y = roots[0]
        ax.text(x + dx, y + dy, str(n), color="white", fontsize=8.5, fontweight="bold",
                ha="center", va="center", zorder=6,
                bbox=dict(boxstyle="circle,pad=0.28", fc=colour, ec="none"))

    ax.annotate("", xy=(-3.15, -4.55), xytext=(-0.4, -4.55),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0, alpha=0.8))
    ax.text(-1.78, -4.30, "further left, faster decay", color=INK, fontsize=8.6,
            ha="center", alpha=0.9)
    ax.annotate("", xy=(-3.15, 3.75), xytext=(-3.15, 1.0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0, alpha=0.8))
    ax.text(-3.0, 2.35, "higher up,\noscillates faster", color=INK, fontsize=8.6,
            ha="left", va="center", alpha=0.9, linespacing=1.35)
    ax.text(0.18, -4.55, "on the axis: neither", color=MARGINAL, fontsize=8.8,
            fontweight="bold", va="center")

    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def main() -> None:
    fig = plt.figure(figsize=(7.8, 6.2))
    gs = fig.add_gridspec(2, 4, height_ratios=[2.2, 1], hspace=0.30, wspace=0.20,
                          left=0.03, right=0.97, top=0.97, bottom=0.04)
    plane(fig.add_subplot(gs[0, :]))

    for i, (sigma, omega, colour, _, t_max, caption) in enumerate(CASES):
        box = fig.add_subplot(gs[1, i])
        t = np.linspace(0, t_max, 700)
        y = response(sigma, omega, t)
        if omega:
            env = np.exp(sigma * t)
            box.plot(t, env, ls=(0, (3, 3)), lw=0.9, color=colour, alpha=0.6)
            box.plot(t, -env, ls=(0, (3, 3)), lw=0.9, color=colour, alpha=0.6)
        box.plot(t, y, lw=1.7, color=colour)
        box.axhline(0, lw=0.8, color=INK, zorder=1)
        lim = float(np.abs(y).max()) * 1.12
        box.set_ylim(-lim, lim); box.set_xlim(0, t_max)
        box.set_xticks([]); box.set_yticks([])
        for s in box.spines.values():
            s.set_color(RULE); s.set_linewidth(0.7)
        box.set_title(f"{i + 1}.  {caption}", fontsize=9, color=colour, pad=4)
        box.set_xlabel("time", fontsize=8, color=INK, labelpad=2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=130, metadata={"Software": None})
    plt.close(fig)

    kb = len(base64.b64encode(OUT.read_bytes())) / 1024
    cases = ", ".join(f"{s:+g}{'' if w == 0 else f'±{w:g}j'}" for s, w, *_ in CASES)
    print(f"{OUT.relative_to(ROOT)}: poles at {cases}; "
          f"cases 1 and 2 share sigma={CASES[0][0]:+g}; {kb:.0f} kB base64")


if __name__ == "__main__":
    main()

# tracking: status=draft version=0 assisted=true
