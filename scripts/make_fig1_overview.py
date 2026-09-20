#!/usr/bin/env python3
"""Fig 1 — IRSpectra-Bench protocol + closed-book reasoning + n=194 wall.

Publication plate for the ICLR lead figure. Honest to the method:
  peak lists → closed-book LLM propose (top-k SMILES) → forward 13C verify
  → ranked constitution. No peak-table tool, no spectral retrieval.

Locked wall counts (instrumented slice only; do not invent a pooled wall):
  n=194; 58 verified / 7 mis-ranked / 129 never proposed; 65 recalled.
Running example v3-R25 is already disclosed (IR 1679; chamfer 0.42 vs 1.30).
"""
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drawmol
import figstyle as fs

N, VERIFIED, MISRANKED, NEVER = 194, 58, 7, 129
RECALLED = VERIFIED + MISRANKED  # 65

SMI_TRUE = "CC(C)(C)NC(=O)c1ccccn1"  # 2-pyridyl picolinamide
SMI_ISO = "CC(C)(C)NC(=O)c1cccnc1"  # 3-pyridyl nicotinamide

C_VERIFIED = "#0077BB"
C_MIS = "#6BAFD4"
C_NEVER = "#3D4F61"
FILL_BLUE = "#E8F3FA"
FILL_TEAL = "#E4F4F2"
FILL_INK = "#F3F4F5"
FILL_RED = "#F8EBE8"
HDR_BLUE = fs.BLUE
HDR_TEAL = fs.GREEN
HDR_INK = "#2C3A47"
EDGE = "#C5CDD4"


def card(ax, x, y, w, h, *, fc="white", ec=EDGE, lw=0.70, r=0.010, z=2):
    p = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        zorder=z,
        clip_on=False,
    )
    ax.add_patch(p)
    return p


def arrow(ax, x0, y0, x1, y1, color=fs.INK):
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            arrowstyle="-|>",
            mutation_scale=8.0,
            lw=0.80,
            color=color,
            zorder=4,
            clip_on=False,
        )
    )


def sticks(ax, xs, ys, *, color=fs.INK, h=0.07, lw=1.15):
    for x, y in zip(xs, ys):
        ax.plot([x, x], [y, y + h], color=color, lw=lw, solid_capstyle="butt", zorder=4, clip_on=False)


def header(ax, x, y, w, h_bar, color, num, title):
    """Full-width header with inline step number."""
    ax.add_patch(Rectangle((x, y), w, h_bar, facecolor=color, edgecolor="none", zorder=3, clip_on=False))
    # number badge
    ax.plot(x + 0.016, y + h_bar / 2, "o", ms=8.5, color="white", zorder=5, clip_on=False)
    ax.text(
        x + 0.016,
        y + h_bar / 2,
        str(num),
        ha="center",
        va="center",
        fontsize=6.4,
        fontweight="bold",
        color=color,
        zorder=6,
        clip_on=False,
    )
    ax.text(
        x + 0.050,
        y + h_bar / 2,
        title,
        ha="left",
        va="center",
        fontsize=6.6,
        fontweight="bold",
        color="white",
        zorder=5,
        clip_on=False,
    )


def panel_a(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fs.panel(ax, "a", x=-0.012, y=1.02)

    specs = [
        (0.000, 0.228, HDR_BLUE, FILL_BLUE, "1", "Blind peak lists"),
        (0.258, 0.228, HDR_BLUE, FILL_BLUE, "2", "LLM propose"),
        (0.516, 0.228, HDR_TEAL, FILL_TEAL, "3", r"Forward $^{13}$C verify"),
        (0.774, 0.226, HDR_INK, FILL_INK, "4", "Ranked constitution"),
    ]
    y, h, hb = 0.04, 0.90, 0.155
    for x, w, hdr, fill, num, title in specs:
        card(ax, x, y, w, h, fc=fill, ec=EDGE, lw=0.65, r=0.008)
        header(ax, x, y + h - hb, w, hb, hdr, num, title)

    for x0, x1 in ((0.228, 0.258), (0.486, 0.516), (0.744, 0.774)):
        arrow(ax, x0, 0.49, x1, 0.49)

    # 1 — inputs
    x = 0.000
    lines = [
        (0.72, "formula   (as from HRMS)", fs.INK, 6.5),
        (0.62, r"IR band list   (cm$^{-1}$)", fs.INK, 6.5),
        (0.52, r"$^{1}$H / $^{13}$C printed lists", fs.INK, 6.5),
        (0.42, "no name / SMILES / scaffold", fs.NOTE, 6.1),
    ]
    for yy, txt, col, sz in lines:
        ax.text(x + 0.012, yy, txt, fontsize=sz, color=col, zorder=4)
    sticks(ax, [x + 0.020 + i * 0.028 for i in range(7)], [0.16] * 7, color=fs.BLUE, h=0.14, lw=1.30)
    ax.text(x + 0.114, 0.105, "lists, not traces", ha="center", fontsize=5.8, color=fs.NOTE, zorder=4)

    # 2 — propose
    x = 0.258
    ax.text(x + 0.012, 0.72, "closed-book frontier LLM", fontsize=6.5, color=fs.INK, zorder=4)
    ax.text(x + 0.012, 0.62, r"top-$k$ SMILES   ($k\leq 3$)", fontsize=6.5, color=fs.INK, zorder=4)
    ax.text(x + 0.012, 0.52, "RDKit formula check only", fontsize=6.5, color=fs.INK, zorder=4)
    for i, (lab, col) in enumerate(
        (("candidate 1", fs.BLUE), ("candidate 2", fs.SKY), ("candidate 3", fs.MUTED))
    ):
        yy = 0.36 - i * 0.095
        card(ax, x + 0.016, yy, 0.196, 0.080, fc="white", ec=col, lw=0.70, r=0.008, z=4)
        ax.text(x + 0.114, yy + 0.040, lab, ha="center", va="center", fontsize=6.3, color=col, zorder=5)

    # 3 — verify
    x = 0.516
    ax.text(x + 0.012, 0.72, r"predict $^{13}$C  (blind to obs.)", fontsize=6.5, color=fs.INK, zorder=4)
    ax.text(x + 0.012, 0.62, "symmetric chamfer on", fontsize=6.5, color=fs.INK, zorder=4)
    ax.text(x + 0.012, 0.52, r"$^{13}$C peak sets  $\rightarrow$  re-rank", fontsize=6.5, color=fs.INK, zorder=4)
    xs = [x + 0.028 + i * 0.030 for i in range(6)]
    sticks(ax, xs, [0.22] * 6, color=fs.INK, h=0.14, lw=1.20)
    sticks(ax, [u + 0.007 for u in xs], [0.22] * 6, color=fs.GREEN, h=0.10, lw=1.05)
    ax.text(x + 0.028, 0.145, "obs", fontsize=5.8, color=fs.INK, zorder=4)
    ax.text(x + 0.072, 0.145, "pred", fontsize=5.8, color=fs.GREEN, zorder=4)
    ax.text(x + 0.125, 0.145, r"$d_{\mathrm{chamfer}}$", fontsize=6.2, color=fs.NOTE, zorder=4)

    # 4 — score
    x = 0.774
    ax.text(x + 0.012, 0.72, "InChIKey-14 connectivity", fontsize=6.5, color=fs.INK, zorder=4)
    ax.text(x + 0.012, 0.62, "constitution, not stereo", fontsize=6.5, color=fs.INK, zorder=4)
    ax.text(x + 0.012, 0.50, r"top-1 $=$ recall $\times$ prec.", fontsize=6.6, color=fs.INK, zorder=4)
    card(ax, x + 0.014, 0.14, 0.198, 0.26, fc="white", ec=HDR_INK, lw=0.75, r=0.008, z=4)
    ax.text(x + 0.113, 0.32, "rank-1 constitution", ha="center", fontsize=6.3, fontweight="bold", color=HDR_INK, zorder=5)
    ax.text(x + 0.113, 0.22, "scored offline", ha="center", fontsize=6.1, color=fs.NOTE, zorder=5)


def panel_b(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fs.panel(ax, "b", x=-0.025, y=1.03)

    ax.text(0.00, 0.965, "Closed-book peak reasoning", fontsize=8.0, fontweight="bold", color=fs.INK, zorder=4)
    ax.text(0.00, 0.900, "printed lists only  ·  no table tool  ·  no retrieval", fontsize=6.2, color=fs.NOTE, zorder=4)

    chips = [
        (0.00, FILL_BLUE, HDR_BLUE, r"IR 1679 cm$^{-1}$", "amide C=O"),
        (0.34, FILL_BLUE, HDR_BLUE, r"$^{1}$H / $^{13}$C lists", "H / C environments"),
        (0.68, FILL_INK, HDR_INK, r"C$_{10}$H$_{14}$N$_{2}$O", "composition"),
    ]
    for x, fill, hdr, top, bot in chips:
        card(ax, x, 0.72, 0.315, 0.155, fc=fill, ec=EDGE, lw=0.60, r=0.010)
        ax.add_patch(Rectangle((x, 0.72), 0.012, 0.155, facecolor=hdr, edgecolor="none", zorder=4, clip_on=False))
        ax.text(x + 0.028, 0.815, top, fontsize=6.2, color=fs.INK, zorder=5)
        ax.text(x + 0.028, 0.755, bot, fontsize=6.0, color=fs.NOTE, zorder=5)

    # isomer pair at readable size (same structures as fig_mechanism)
    pair = [
        (0.00, SMI_TRUE, fs.GREEN, FILL_TEAL, "2-pyridyl  ·  selected", "0.42 ppm"),
        (0.515, SMI_ISO, fs.VERMIL, FILL_RED, "3-pyridyl  ·  rejected", "1.30 ppm"),
    ]
    for x, smi, ec, fc, name, ch in pair:
        card(ax, x, 0.02, 0.485, 0.675, fc=fc, ec=ec, lw=0.90, r=0.012)
        ax.text(x + 0.242, 0.630, name, ha="center", va="center", fontsize=6.4, fontweight="bold", color=ec, zorder=6)
        drawmol.show_mol(ax, smi, (x + 0.02, 0.14, 0.445, 0.46), px=(560, 400))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.text(x + 0.242, 0.075, ch, ha="center", fontsize=6.1, color=fs.NOTE, zorder=6)

    ax.text(0.00, -0.015, "v3-R25 verify-save  ·  disclosed running example", fontsize=5.8, color=fs.NOTE, zorder=4)


def panel_c(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fs.panel(ax, "c", x=-0.02, y=1.03)

    ax.text(0.00, 0.965, r"Wall  ·  $n{=}194$ instrumented slice", fontsize=8.0, fontweight="bold", color=fs.INK, zorder=4)
    ax.text(0.00, 0.900, "forward-verify only  ·  not the $n{=}300$ headline", fontsize=6.2, color=fs.NOTE, zorder=4)

    segs = [
        (0, VERIFIED, C_VERIFIED, str(VERIFIED), "verified"),
        (VERIFIED, MISRANKED, C_MIS, str(MISRANKED), "mis-ranked"),
        (VERIFIED + MISRANKED, NEVER, C_NEVER, str(NEVER), "never proposed"),
    ]
    y0, h = 0.52, 0.175
    for x0, w, color, lab, name in segs:
        xx, ww = x0 / N, w / N
        ax.add_patch(Rectangle((xx, y0), ww, h, facecolor=color, edgecolor="none", zorder=3, clip_on=False))
        if w >= 6:
            ax.text(xx + ww / 2, y0 + h / 2, lab, ha="center", va="center", fontsize=8, fontweight="bold", color="white", zorder=5)
        ax.text(xx + ww / 2, y0 - 0.050, name, ha="center", va="top", fontsize=6.2, color=fs.NOTE, zorder=4)

    bx0, bx1 = 0.0, RECALLED / N
    by = y0 + h + 0.035
    ax.plot([bx0, bx0, bx1, bx1], [by - 0.018, by, by, by - 0.018], color=fs.INK, lw=0.70, solid_capstyle="butt", zorder=4)
    ax.text(
        RECALLED / (2 * N),
        by + 0.012,
        f"{RECALLED} recalled ({100 * RECALLED / N:.0f}%)",
        ha="center",
        va="bottom",
        fontsize=6.6,
        color=fs.INK,
        zorder=4,
    )

    chips = [
        (0.22, C_VERIFIED, FILL_BLUE, r"58/65 selected once proposed  (89%)"),
        (0.04, C_NEVER, FILL_INK, r"129/194 never enter the pool  —  binds top-1"),
    ]
    for y, edge, fill, txt in chips:
        card(ax, 0.00, y, 1.00, 0.145, fc=fill, ec=edge, lw=0.70, r=0.010)
        ax.text(0.03, y + 0.072, txt, ha="left", va="center", fontsize=6.5, color=fs.INK, zorder=5)


def main() -> None:
    fs.apply()
    fig = plt.figure(figsize=(6.30, 3.38))
    ax_a = fig.add_axes([0.026, 0.530, 0.960, 0.435])
    ax_b = fig.add_axes([0.026, 0.040, 0.548, 0.455])
    ax_c = fig.add_axes([0.600, 0.040, 0.386, 0.455])
    panel_a(ax_a)
    panel_b(ax_b)
    panel_c(ax_c)

    out = Path(__file__).resolve().parents[1] / "figures" / "fig1_overview"
    fig.savefig(str(out) + ".png", dpi=600, facecolor="white")
    fig.savefig(str(out) + ".pdf", facecolor="white")
    fig.savefig(str(out) + "@2x.png", dpi=600, facecolor="white")
    plt.close(fig)
    print(f"wrote {out}.png/.pdf and {out}@2x.png")


if __name__ == "__main__":
    main()
