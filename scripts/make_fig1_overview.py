#!/usr/bin/env python3
"""Fig 1 — IRSpectra-Bench overview (IR-Agent layout density, our story).

Three full-width strips, not a 4-box PowerPoint row:
  (a) overall framework with the propose fork (verify vs never-proposed)
  (b) peak-list reasoning on disclosed v3-R25
  (c) instrumented wall n=194

Honest method only: printed lists, closed-book LLM, RDKit formula check,
forward 13C chamfer. No peak-table tool, no retrieval, no IR-Agent icons.

Locked counts: 58 verified / 7 mis-ranked / 129 never proposed (n=194).
v3-R25 disclosed: IR 1679; chamfer 0.42 vs 1.30 ppm.
"""
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drawmol
import figstyle as fs

N, VERIFIED, MISRANKED, NEVER = 194, 58, 7, 129
RECALLED = VERIFIED + MISRANKED

SMI_TRUE = "CC(C)(C)NC(=O)c1ccccn1"
SMI_ISO = "CC(C)(C)NC(=O)c1cccnc1"

C_VERIFIED = "#0077BB"
C_MIS = "#6BAFD4"
C_NEVER = "#3D4F61"
FILL_TEAL = "#EEF7F6"
FILL_BLUE = "#F3F8FC"
FILL_RED = "#FBF0EE"
FILL_INK = "#F4F5F6"
EDGE = "#B8C0C7"
MONO = FontProperties(family="Liberation Mono", size=5.6)


def card(ax, x, y, w, h, *, fc="white", ec=EDGE, lw=0.85, r=0.012, z=2):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, clip_on=False,
    )
    ax.add_patch(p)
    return p


def left_rail(ax, x, y, h, color):
    ax.add_patch(Rectangle((x, y), 0.010, h, facecolor=color, edgecolor="none", zorder=4, clip_on=False))


def arrow(ax, x0, y0, x1, y1, color=fs.INK, lw=0.85, ms=8.5, ls="-"):
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0), (x1, y1),
            arrowstyle="-|>", mutation_scale=ms, lw=lw, color=color,
            linestyle=ls, zorder=5, clip_on=False,
        )
    )


def title(ax, letter, text, x=0.0, y=1.0):
    ax.text(
        x, y, f"({letter})  {text}",
        transform=ax.transAxes,
        fontsize=8.0, fontweight="bold", ha="left", va="bottom",
        color=fs.INK, clip_on=False, zorder=10,
    )


def blank(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def panel_a(ax):
    blank(ax)
    title(ax, "a", "Overall framework", x=-0.008, y=1.02)

    # nodes: input | propose | (verify → rank) / (never → wall)
    inp = (0.000, 0.10, 0.195, 0.80)
    pro = (0.250, 0.10, 0.195, 0.80)
    ver = (0.510, 0.52, 0.215, 0.38)
    ran = (0.785, 0.52, 0.215, 0.38)
    nev = (0.510, 0.10, 0.215, 0.32)
    wal = (0.785, 0.10, 0.215, 0.32)

    card(ax, *inp, fc=FILL_BLUE, ec=fs.BLUE, lw=1.05)
    left_rail(ax, inp[0], inp[1], inp[3], fs.BLUE)
    card(ax, *pro, fc=FILL_BLUE, ec=fs.BLUE, lw=1.05)
    left_rail(ax, pro[0], pro[1], pro[3], fs.BLUE)
    card(ax, *ver, fc=FILL_TEAL, ec=fs.GREEN, lw=1.05)
    left_rail(ax, ver[0], ver[1], ver[3], fs.GREEN)
    card(ax, *ran, fc=FILL_TEAL, ec=fs.GREEN, lw=1.05)
    left_rail(ax, ran[0], ran[1], ran[3], fs.GREEN)
    card(ax, *nev, fc=FILL_INK, ec=C_NEVER, lw=1.05)
    left_rail(ax, nev[0], nev[1], nev[3], C_NEVER)
    card(ax, *wal, fc=FILL_INK, ec=C_NEVER, lw=1.05)
    left_rail(ax, wal[0], wal[1], wal[3], C_NEVER)

    # arrows
    arrow(ax, 0.195, 0.50, 0.250, 0.50, fs.INK)
    arrow(ax, 0.445, 0.68, 0.510, 0.68, fs.GREEN)
    arrow(ax, 0.725, 0.71, 0.785, 0.71, fs.GREEN)
    arrow(ax, 0.445, 0.26, 0.510, 0.26, C_NEVER, ls=(0, (2.2, 1.4)))
    arrow(ax, 0.725, 0.26, 0.785, 0.26, C_NEVER, ls=(0, (2.2, 1.4)))

    # INPUT
    x, y = inp[0], inp[1]
    ax.text(x + 0.020, 0.82, "Blind peak lists", fontsize=6.8, fontweight="bold", color=fs.BLUE, zorder=6)
    for yy, t in (
        (0.70, r"formula   (as from HRMS)"),
        (0.58, r"IR band list   (cm$^{-1}$)"),
        (0.46, r"$^{1}$H printed list"),
        (0.34, r"$^{13}$C printed list"),
    ):
        ax.text(x + 0.020, yy, t, fontsize=6.3, color=fs.INK, zorder=6)
    ax.text(x + 0.020, 0.20, "no name / SMILES / scaffold", fontsize=5.8, color=fs.NOTE, style="italic", zorder=6)

    # PROPOSE
    x = pro[0]
    ax.text(x + 0.020, 0.82, "LLM propose", fontsize=6.8, fontweight="bold", color=fs.BLUE, zorder=6)
    ax.text(x + 0.020, 0.70, "closed-book frontier LLM", fontsize=6.3, color=fs.INK, zorder=6)
    ax.text(x + 0.020, 0.59, r"top-$k$ SMILES   ($k\leq 3$)", fontsize=6.3, color=fs.INK, zorder=6)
    ax.text(x + 0.020, 0.48, "RDKit formula check only", fontsize=6.3, color=fs.INK, zorder=6)
    for i, lab in enumerate(("candidate 1", "candidate 2", "candidate 3")):
        yy = 0.34 - i * 0.075
        card(ax, x + 0.018, yy, 0.160, 0.062, fc="white", ec=fs.SKY, lw=0.55, r=0.008, z=6)
        ax.text(x + 0.098, yy + 0.031, lab, ha="center", va="center", fontsize=5.8, color=fs.BLUE, zorder=7)

    # VERIFY
    x, y, w, h = ver
    ax.text(x + 0.020, 0.82, r"Forward $^{13}$C verify", fontsize=6.6, fontweight="bold", color=fs.GREEN, zorder=6)
    ax.text(x + 0.020, 0.70, r"predict $^{13}$C  (blind to obs.)", fontsize=6.1, color=fs.INK, zorder=6)
    ax.text(x + 0.020, 0.60, "symmetric chamfer  →  re-rank", fontsize=6.1, color=fs.INK, zorder=6)

    # RANK
    x = ran[0]
    ax.text(x + 0.020, 0.82, "Ranked constitution", fontsize=6.6, fontweight="bold", color=fs.GREEN, zorder=6)
    ax.text(x + 0.020, 0.71, "InChIKey-14 connectivity", fontsize=6.1, color=fs.INK, zorder=6)
    ax.text(x + 0.020, 0.62, r"top-1  $=$  recall $\times$ prec.", fontsize=6.2, color=fs.INK, zorder=6)
    ax.text(x + 0.020, 0.555, "training-free ranking", fontsize=5.9, color=fs.NOTE, zorder=6)

    # NEVER
    x = nev[0]
    ax.text(x + 0.020, 0.34, r"Never proposed", fontsize=6.6, fontweight="bold", color=C_NEVER, zorder=6)
    ax.text(x + 0.020, 0.24, r"true $\notin$ pool", fontsize=6.2, color=fs.INK, zorder=6)
    ax.text(x + 0.020, 0.155, "129 / 194 on this slice", fontsize=6.1, color=fs.NOTE, zorder=6)

    # WALL pointer
    x = wal[0]
    ax.text(x + 0.020, 0.34, "Binds top-1", fontsize=6.6, fontweight="bold", color=C_NEVER, zorder=6)
    ax.text(x + 0.020, 0.24, "re-ranking cannot recover", fontsize=6.1, color=fs.INK, zorder=6)
    ax.text(x + 0.020, 0.155, "proposal wall  (below)", fontsize=6.1, color=fs.NOTE, zorder=6)


def panel_b(ax):
    blank(ax)
    title(ax, "b", "Peak-list reasoning", x=-0.008, y=1.02)
    ax.text(0.268, 1.02, "closed-book  ·  no table tool  ·  no retrieval  ·  v3-R25",
            fontsize=6.2, color=fs.NOTE, va="bottom", zorder=6)

    # process card
    card(ax, 0.000, 0.02, 0.268, 0.90, fc=FILL_BLUE, ec=fs.BLUE, lw=0.95)
    left_rail(ax, 0.000, 0.02, 0.90, fs.BLUE)
    ax.text(0.020, 0.84, "What the solver reads", fontsize=6.7, fontweight="bold", color=fs.BLUE, zorder=6)
    steps = (
        (0.70, "1", r"IR 1679 cm$^{-1}$", "amide C=O hypothesis"),
        (0.46, "2", r"$^{1}$H / $^{13}$C printed lists", "H / C environments"),
        (0.22, "3", r"formula  C$_{10}$H$_{14}$N$_{2}$O", "composition constraint"),
    )
    for yy, n, head, sub in steps:
        ax.plot(0.028, yy + 0.055, "o", ms=8.0, color=fs.BLUE, zorder=7)
        ax.text(0.028, yy + 0.055, n, ha="center", va="center", fontsize=5.8,
                fontweight="bold", color="white", zorder=8)
        ax.text(0.048, yy + 0.078, head, fontsize=6.3, color=fs.INK, zorder=6)
        ax.text(0.048, yy + 0.018, sub, fontsize=5.9, color=fs.NOTE, zorder=6)

    # IR card — only disclosed 1679 is labelled
    card(ax, 0.282, 0.02, 0.248, 0.90, fc="white", ec=EDGE, lw=0.80)
    ax.text(0.406, 0.84, r"IR  (printed list)", ha="center", fontsize=6.6,
            fontweight="bold", color=fs.INK, zorder=6)
    # schematic axis + single disclosed stick
    x0, x1, yb = 0.300, 0.512, 0.28
    ax.plot([x0, x1], [yb, yb], color=fs.INK, lw=0.70, zorder=6)
    # ghost ticks (not data)
    for t in (0.08, 0.22, 0.55, 0.78):
        xx = x0 + t * (x1 - x0)
        ax.plot([xx, xx], [yb, yb + 0.10], color=fs.GHOST, lw=1.15, zorder=5)
    # 1679 — disclosed, placed mid-high like a carbonyl stretch
    x1679 = x0 + 0.38 * (x1 - x0)
    ax.plot([x1679, x1679], [yb, yb + 0.36], color=fs.BLUE, lw=1.70, zorder=7)
    ax.text(x1679, yb + 0.40, "1679", ha="center", fontsize=6.2, fontweight="bold", color=fs.BLUE, zorder=7)
    ax.text(x1679, 0.18, r"amide C=O", ha="center", fontsize=6.0, color=fs.NOTE, zorder=7)
    ax.text(0.406, 0.08, r"cm$^{-1}$  ·  abridged", ha="center", fontsize=5.7, color=fs.NOTE, zorder=6)

    # isomer pair
    pair = [
        (0.544, SMI_TRUE, fs.GREEN, FILL_TEAL, "2-pyridyl  ·  selected", "0.42 ppm"),
        (0.772, SMI_ISO, fs.VERMIL, FILL_RED, "3-pyridyl  ·  rejected", "1.30 ppm"),
    ]
    for x, smi, ec, fc, name, ch in pair:
        card(ax, x, 0.02, 0.220, 0.90, fc=fc, ec=ec, lw=1.00, r=0.012)
        ax.text(x + 0.110, 0.84, name, ha="center", fontsize=6.2, fontweight="bold", color=ec, zorder=7)
        drawmol.show_mol(ax, smi, (x + 0.012, 0.20, 0.196, 0.58), px=(720, 480))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.text(x + 0.110, 0.12, ch, ha="center", fontsize=6.3, color=fs.NOTE, zorder=7)


def panel_c(ax):
    blank(ax)
    title(ax, "c", r"Proposal wall   ·   $n{=}194$ instrumented slice", x=-0.008, y=1.02)
    ax.text(0.455, 1.02, r"forward-verify only   ·   not the $n{=}300$ headline",
            fontsize=6.2, color=fs.NOTE, va="bottom", zorder=6)

    segs = [
        (0, VERIFIED, C_VERIFIED, str(VERIFIED), "verified"),
        (VERIFIED, MISRANKED, C_MIS, str(MISRANKED), "mis-ranked"),
        (VERIFIED + MISRANKED, NEVER, C_NEVER, str(NEVER), "never proposed"),
    ]
    y0, h = 0.58, 0.22
    for x0, w, color, lab, name in segs:
        xx, ww = x0 / N, w / N
        ax.add_patch(Rectangle((xx, y0), ww, h, facecolor=color, edgecolor="none", zorder=3, clip_on=False))
        if w >= 6:
            ax.text(xx + ww / 2, y0 + h / 2, lab, ha="center", va="center",
                    fontsize=8.5, fontweight="bold", color="white", zorder=5)
        ax.text(xx + ww / 2, y0 - 0.055, name, ha="center", va="top", fontsize=6.4, color=fs.NOTE, zorder=4)

    bx0, bx1 = 0.0, RECALLED / N
    by = y0 + h + 0.04
    ax.plot([bx0, bx0, bx1, bx1], [by - 0.02, by, by, by - 0.02],
            color=fs.INK, lw=0.70, solid_capstyle="butt", zorder=4)
    ax.text(RECALLED / (2 * N), by + 0.012,
            f"{RECALLED} recalled ({100 * RECALLED / N:.0f}%)",
            ha="center", va="bottom", fontsize=6.6, color=fs.INK, zorder=4)

    chips = [
        (0.000, C_VERIFIED, FILL_BLUE, "58/65 selected once proposed", "89% conditional precision"),
        (0.340, C_MIS, "#EAF4FA", "7 mis-ranked", "true in pool, wrong top-1"),
        (0.680, C_NEVER, FILL_INK, "129/194 never proposed", "binds top-1; re-ranking unused"),
    ]
    for x, edge, fill, head, sub in chips:
        card(ax, x, 0.02, 0.320, 0.32, fc=fill, ec=edge, lw=0.90, r=0.012)
        left_rail(ax, x, 0.02, 0.32, edge)
        ax.text(x + 0.024, 0.24, head, fontsize=6.4, fontweight="bold", color=fs.INK, zorder=6)
        ax.text(x + 0.024, 0.10, sub, fontsize=6.0, color=fs.NOTE, zorder=6)


def main() -> None:
    fs.apply()
    fig = plt.figure(figsize=(6.30, 4.72), facecolor="white")
    ax_a = fig.add_axes([0.030, 0.655, 0.955, 0.300])
    ax_b = fig.add_axes([0.030, 0.300, 0.955, 0.310])
    ax_c = fig.add_axes([0.030, 0.028, 0.955, 0.230])
    panel_a(ax_a)
    panel_b(ax_b)
    panel_c(ax_c)

    out = Path(__file__).resolve().parents[1] / "figures" / "fig1_overview"
    fig.savefig(str(out) + ".png", dpi=600, facecolor="white")
    fig.savefig(str(out) + ".pdf", facecolor="white")
    fig.savefig(str(out) + "@2x.png", dpi=600, facecolor="white")
    fig.savefig(str(out) + ".svg", facecolor="white")
    plt.close(fig)
    print(f"wrote {out}.png/.pdf/.svg and {out}@2x.png")


if __name__ == "__main__":
    main()
