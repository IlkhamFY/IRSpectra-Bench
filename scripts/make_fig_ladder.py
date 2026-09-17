#!/usr/bin/env python3
"""Compact wide-short inference ladder for ICLR (Fig 5 / fig3_method)."""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import figstyle as fs

def main() -> None:
    fs.apply()
    labels = ["solver self-rank", "+ forward-verify", "+ generate-wide"]
    vals = [23, 27, 30]
    colors = [fs.MUTED, fs.MUTED, fs.BLUE]
    fig, ax = plt.subplots(figsize=(5.2, 1.35))
    fs.ygrid(ax)
    bars = ax.bar(range(3), vals, width=0.62, color=colors, zorder=3)
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels)
    for b, v in zip(bars, vals):
        ax.text(
            b.get_x() + b.get_width() / 2,
            v / 2,
            f"{v}%",
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold",
            color="white",
            zorder=5,
        )
    ax.set_ylabel("exact top-1 (%)")
    ax.set_ylim(0, 32)
    ax.set_yticks([0, 10, 20, 30])
    ax.tick_params(axis="x", pad=2)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout(pad=0.15)
    out = Path(__file__).resolve().parents[1] / "figures" / "fig3_method"
    fig.savefig(str(out) + ".png", dpi=600, facecolor="white")
    fig.savefig(str(out) + ".pdf", facecolor="white")
    print(f"wrote {out}.png/.pdf")

if __name__ == "__main__":
    main()
