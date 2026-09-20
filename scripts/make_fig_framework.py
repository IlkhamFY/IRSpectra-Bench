#!/usr/bin/env python3
"""Fig. 1 — IRSpectra-Bench protocol + diagnosis (publication plate).

Panel (a) generate → candidates → forward-verify → top-1.
Panel (b) instrumented wall 58/7/129 on n=194 (not a pooled n=300 wall).
Panel (c) two scored cohorts: n=300 generation vs n=194 fverify.
No expand-500 accuracy is drawn here (appendix / SI only).
"""
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figstyle as fs

N, VERIFIED, MIS, NEVER = 194, 58, 7, 129
RECALLED = VERIFIED + MIS


def _box(ax, x, y, w, h, fc, ec, lw=0.9, r=0.018):
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.006,rounding_size={r}",
        linewidth=lw, facecolor=fc, edgecolor=ec, mutation_aspect=0.6,
        zorder=3, clip_on=False,
    )
    ax.add_patch(p)
    return p


def _txt(ax, x, y, s, *, size=8, weight="regular", color=None, ha="center", va="center", **kw):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, fontweight=weight,
            color=color or fs.INK, zorder=4, clip_on=False, **kw)


def _arrow(ax, x0, y0, x1, y1, color=None):
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0), (x1, y1),
            arrowstyle="-|>", mutation_scale=9,
            lw=1.05, color=color or fs.INK,
            shrinkA=0, shrinkB=0, zorder=2, clip_on=False,
        )
    )


def _panel_letter(ax, letter, x, y):
    ax.text(x, y, letter, fontsize=11, fontweight="bold", color=fs.INK,
            ha="left", va="top", zorder=6, clip_on=False)


def main() -> None:
    fs.apply()
    fig = plt.figure(figsize=(6.85, 3.72))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(Rectangle((0.012, 0.558), 0.976, 0.428,
                           facecolor="#F4F8FB", edgecolor="#D5DEE6",
                           lw=0.6, zorder=0, clip_on=False))
    ax.add_patch(Rectangle((0.012, 0.016), 0.598, 0.524,
                           facecolor="#F7F4EF", edgecolor="#E2D9CC",
                           lw=0.6, zorder=0, clip_on=False))
    ax.add_patch(Rectangle((0.624, 0.016), 0.364, 0.524,
                           facecolor="#F3F7F4", edgecolor="#D4E0D8",
                           lw=0.6, zorder=0, clip_on=False))

    _panel_letter(ax, "a", 0.020, 0.974)
    _txt(ax, 0.052, 0.962, "Protocol — literature peak lists, not traces",
         size=7.5, weight="bold", ha="left", va="top", color=fs.NOTE)
    _panel_letter(ax, "b", 0.020, 0.528)
    _txt(ax, 0.052, 0.516, "Instrumented wall (n=194 fverify only)",
         size=7.5, weight="bold", ha="left", va="top", color=fs.NOTE)
    _panel_letter(ax, "c", 0.634, 0.528)
    _txt(ax, 0.666, 0.516, "Two scored cohorts",
         size=7.5, weight="bold", ha="left", va="top", color=fs.NOTE)

    stages = [
        (0.030, "IRexp", "lit. IR / ¹H / ¹³C\nband lists",
         "#E8F1F8", fs.BLUE, "companion resource"),
        (0.220, "Blind payload", "formula + peak lists\nno name / SMILES",
         "#EEF3F7", "#3D4F61", "gold held out"),
        (0.410, "Generate", "≤3 ranked SMILES\nclosed-book LLM",
         "#DCEAF6", fs.BLUE, "n=300 generation"),
        (0.600, "Forward-verify", "pred. vs obs. ¹³C\nsym. chamfer",
         "#D8EFEA", fs.GREEN, "n=194 only"),
        (0.790, "Top-1", "InChIKey-14\nconstitution",
         "#F3E4D8", fs.ORANGE, "mechanical score"),
    ]
    yb, h, w = 0.675, 0.228, 0.164
    for i, (x, title, body, fc, ec, foot) in enumerate(stages):
        _box(ax, x, yb, w, h, fc, ec, lw=1.05)
        _txt(ax, x + w / 2, yb + h - 0.036, title, size=8.0, weight="bold", color=ec)
        _txt(ax, x + w / 2, yb + 0.100, body, size=6.6, color=fs.INK, linespacing=1.28)
        _txt(ax, x + w / 2, yb - 0.026, foot, size=6.2, color=fs.NOTE)
        if i < len(stages) - 1:
            _arrow(ax, x + w + 0.003, yb + h / 2, stages[i + 1][0] - 0.003, yb + h / 2)

    _txt(ax, 0.50, 0.578,
         "propose >> verify: a missing candidate cannot be recovered by re-ranking",
         size=6.9, color=fs.INK, style="italic")

    x0, bar_w, bar_y, bar_h = 0.050, 0.520, 0.195, 0.155
    segs = [
        (VERIFIED, fs.BLUE, "58", "verified"),
        (MIS, fs.SKY, "7", "mis-ranked"),
        (NEVER, "#3D4F61", "129", "never proposed"),
    ]
    cursor = 0.0
    for w_n, color, lab, name in segs:
        ww = bar_w * (w_n / N)
        ax.add_patch(Rectangle((x0 + cursor, bar_y), ww, bar_h,
                               facecolor=color, edgecolor="none", zorder=3))
        if w_n >= 6:
            _txt(ax, x0 + cursor + ww / 2, bar_y + bar_h / 2, lab,
                 size=9, weight="bold", color="white")
        _txt(ax, x0 + cursor + ww / 2, bar_y - 0.030, name, size=6.5, color=fs.NOTE)
        cursor += ww

    rec_w = bar_w * (RECALLED / N)
    by = bar_y + bar_h + 0.016
    ax.plot([x0, x0, x0 + rec_w, x0 + rec_w],
            [by - 0.012, by, by, by - 0.012],
            color=fs.INK, lw=0.7, solid_capstyle="butt", zorder=4)
    _txt(ax, x0 + rec_w / 2 + 0.04, by + 0.026,
         "65 recalled (34%)  ·  58/65 = 89% if proposed",
         size=6.6, color=fs.INK, ha="center")

    _txt(ax, 0.310, 0.055,
         "Not a pooled n=300 wall. No fverify precision on 106 or 230.",
         size=6.2, color=fs.NOTE)

    cards = [
        (0.318, fs.BLUE, "#E8F1F8",
         "Generation  n = 300",
         "118/300  (39.3%)",
         "top-1  ·  133/300 recall"),
        (0.122, fs.GREEN, "#E4F3EF",
         "Forward-verify  n = 194",
         "58/65  (89%)",
         "precision | recall  ·  129 never"),
    ]
    for y, ec, fc, head, hero, sub in cards:
        _box(ax, 0.644, y, 0.326, 0.168, fc, ec, lw=1.0)
        _txt(ax, 0.807, y + 0.140, head, size=6.5, weight="bold", color=ec)
        _txt(ax, 0.807, y + 0.090, hero, size=9.6, weight="bold", color=fs.INK)
        _txt(ax, 0.807, y + 0.038, sub, size=6.2, color=fs.NOTE)

    _txt(ax, 0.807, 0.048,
         "Headline is n=300 generation.\nLarger blind round: appendix / SI.",
         size=6.2, color=fs.NOTE, linespacing=1.28)

    out = Path(__file__).resolve().parents[1] / "figures" / "fig_framework"
    fig.savefig(str(out) + ".pdf", facecolor="white")
    fig.savefig(str(out) + ".png", dpi=600, facecolor="white")
    # SVG twin for editability
    fig.savefig(str(out) + ".svg", facecolor="white")
    plt.close(fig)
    print(f"wrote {out}.pdf/.png/.svg")


if __name__ == "__main__":
    main()
