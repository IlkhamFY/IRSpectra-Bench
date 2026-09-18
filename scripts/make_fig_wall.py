#!/usr/bin/env python3
"""Figure 1 — forward-verify wall (n=194 instrumented slice). Blue-forward palette."""
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figstyle as fs

# Counts (locked instrumented slice; do not invent pooled fverify)
N = 194
VERIFIED = 58
MISRANKED = 7
NEVER = 129  # 58+7+129 == 194
RECALLED = VERIFIED + MISRANKED  # 65

# Blue-forward semantic (Ilkham: prefer blue; Fukasawa/Rams — quiet, honest)
C_VERIFIED = "#0077BB"   # Tol vibrant blue — correct after verify
C_MIS = "#6BAFD4"        # same-hue light — proposed, wrong rank
C_NEVER = "#3D4F61"      # blue-charcoal wall — never proposed
C_NOTE = "#5c636a"


def main() -> None:
    fs.apply()
    fig, ax = plt.subplots(figsize=(6.3, 1.55))
    ax.set_xlim(0, N)
    ax.set_ylim(0, 1)
    ax.axis("off")

    segs = [
        (0, VERIFIED, C_VERIFIED, str(VERIFIED)),
        (VERIFIED, MISRANKED, C_MIS, str(MISRANKED)),
        (VERIFIED + MISRANKED, NEVER, C_NEVER, str(NEVER)),
    ]
    y0, h = 0.28, 0.42
    for x0, w, color, label in segs:
        ax.add_patch(
            FancyBboxPatch(
                (x0, y0),
                w,
                h,
                boxstyle="square,pad=0",
                linewidth=0,
                facecolor=color,
                mutation_aspect=None,
                clip_on=False,
            )
        )
        if w >= 6:
            ax.text(
                x0 + w / 2,
                y0 + h / 2,
                label,
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                color="white",
                zorder=5,
            )

    # Bracket over recalled (verified + mis-ranked)
    bx0, bx1 = 0.0, float(RECALLED)
    by = y0 + h + 0.08
    ax.plot([bx0, bx0, bx1, bx1], [by - 0.04, by, by, by - 0.04], color=fs.INK, lw=0.7, solid_capstyle="butt")
    ax.text(
        RECALLED / 2,
        by + 0.06,
        f"{RECALLED} recalled ({100 * RECALLED / N:.0f}%)",
        ha="center",
        va="bottom",
        fontsize=8,
        color=fs.INK,
    )

    # Column labels under segments (centered on each)
    labels = [
        (VERIFIED / 2, "verified"),
        (VERIFIED + MISRANKED / 2, "mis-ranked"),
        (VERIFIED + MISRANKED + NEVER / 2, "never proposed"),
    ]
    for x, lab in labels:
        ax.text(x, y0 - 0.12, lab, ha="center", va="top", fontsize=8, color=C_NOTE)

    # Quiet n=194 cue, right
    ax.text(
        N,
        y0 + h + 0.08,
        f"n = {N}",
        ha="right",
        va="bottom",
        fontsize=7.5,
        color=C_NOTE,
    )

    out = Path(__file__).resolve().parents[1] / "figures" / "fig_wall"
    fig.savefig(str(out) + ".png", dpi=600, facecolor="white", bbox_inches="tight", pad_inches=0.08)
    fig.savefig(str(out) + ".pdf", facecolor="white", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    print(f"wrote {out}.png/.pdf")


if __name__ == "__main__":
    main()
