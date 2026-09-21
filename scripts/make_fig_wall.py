#!/usr/bin/env python3
"""Lead Fig 1 (generation) + separate fverify diagnostic wall.

Fig 1 (`fig1_lead_overview`) — generation-locked n=500:
  top-1:           227/500 (45.4%)
  recall@3:        249/500 (49.8%)
  self-rank:       227/249 (91.2%)
  wall:            227 | 22 | 251
  identity:        45.4% ≈ 49.8% × 91.2%

Diagnostic only (`fig_wall_diagnostic`) — n=500 fverify:
  verified:        204
  misranked:        45
  never-proposed:  251
  recalled:        249  (= 204 + 45)

Do not draw fverify 204/45/251 on Fig 1.
"""
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figstyle as fs

N = 500

# Diagnostic wall (fig_wall_diagnostic only). Not the lead plate.
FV_VERIFIED = 204
FV_MISRANKED = 45
FV_NEVER = 251
FV_RECALLED = FV_VERIFIED + FV_MISRANKED  # 249

# Lead Fig 1 generation wall.
GEN_TOP1 = 227
GEN_NOT_TOP1 = 22
GEN_NEVER = 251
GEN_RECALL = GEN_TOP1 + GEN_NOT_TOP1  # 249

# Back-compat aliases for the diagnostic bar helpers.
VERIFIED = FV_VERIFIED
MISRANKED = FV_MISRANKED
NEVER = FV_NEVER
RECALLED = FV_RECALLED

# Lead-plate teal / vermil / grey
C_TOP1 = "#00897B"
C_INSET = "#E53935"
C_NEVER = "#5F6368"
C_NOTE = "#5c636a"


def _bar(ax, n: int, y0: float = 0.30, h: float = 0.40, gap: float = 1.4) -> None:
    segs = [
        (0, VERIFIED, C_TOP1, str(VERIFIED), 11),
        (VERIFIED, MISRANKED, C_INSET, str(MISRANKED), 9),
        (VERIFIED + MISRANKED, NEVER, C_NEVER, str(NEVER), 11),
    ]
    for x0, w, color, label, fs_n in segs:
        ax.add_patch(
            FancyBboxPatch(
                (x0 + gap / 2, y0),
                max(w - gap, 0.8),
                h,
                boxstyle="square,pad=0",
                linewidth=0,
                facecolor=color,
                clip_on=False,
            )
        )
        ax.text(
            x0 + w / 2,
            y0 + h / 2,
            label,
            ha="center",
            va="center",
            fontsize=fs_n,
            fontweight="bold",
            color="white",
            zorder=5,
        )

    bx0, bx1 = 0.0, float(RECALLED)
    by = y0 + h + 0.10
    ax.plot(
        [bx0, bx0, bx1, bx1],
        [by - 0.05, by, by, by - 0.05],
        color=fs.INK,
        lw=0.8,
        solid_capstyle="butt",
    )
    ax.text(
        RECALLED / 2,
        by + 0.07,
        f"{RECALLED} recalled ({100 * RECALLED / n:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=8,
        color=fs.INK,
        fontweight="bold",
    )

    labels = [
        (VERIFIED / 2, "verified"),
        (VERIFIED + MISRANKED / 2, "misranked"),
        (VERIFIED + MISRANKED + NEVER / 2, "never proposed"),
    ]
    for x, lab in labels:
        ax.text(x, y0 - 0.14, lab, ha="center", va="top", fontsize=8, color=C_NOTE)


def write_svg(path: Path, width: float = 504.0, height: float = 102.0) -> None:
    """Vector wall matching the lead-plate frame (print pt)."""
    pad_x = 12.0
    usable = width - 2 * pad_x
    y_bar = 38.0
    h_bar = 34.0
    gap = 1.5

    def x_of(count: float) -> float:
        return pad_x + usable * (count / N)

    x0 = x_of(0)
    x1 = x_of(VERIFIED)
    x2 = x_of(VERIFIED + MISRANKED)
    x3 = x_of(N)
    w1, w2, w3 = x1 - x0, x2 - x1, x3 - x2

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="{width}" height="{height}" fill="#FFFFFF"/>
<defs><style type="text/css">@font-face {{ font-family: DejaVuSans; src: local("DejaVu Sans"); }}text {{ font-family: DejaVuSans, Helvetica, Arial, sans-serif; fill: #1A1A1A; }}</style></defs>
<rect x="{x0:.2f}" y="{y_bar}" width="{w1 - gap:.2f}" height="{h_bar}" fill="{C_TOP1}"/>
<text x="{(x0 + x1 - gap) / 2:.2f}" y="{y_bar + 21.5}" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">{VERIFIED}</text>
<text x="{(x0 + x1) / 2:.2f}" y="88.0" text-anchor="middle" font-size="8.5" fill="#6B7280">verified</text>
<rect x="{x1:.2f}" y="{y_bar}" width="{max(w2 - gap, 8):.2f}" height="{h_bar}" fill="{C_INSET}"/>
<text x="{x1 + max(w2 - gap, 8) / 2:.2f}" y="{y_bar + 21.5}" text-anchor="middle" font-size="10" font-weight="700" fill="#FFFFFF">{MISRANKED}</text>
<text x="{x1 + w2 / 2:.2f}" y="88.0" text-anchor="middle" font-size="8" fill="#6B7280">misranked</text>
<rect x="{x2:.2f}" y="{y_bar}" width="{w3:.2f}" height="{h_bar}" fill="{C_NEVER}"/>
<text x="{(x2 + x3) / 2:.2f}" y="{y_bar + 21.5}" text-anchor="middle" font-size="12" font-weight="700" fill="#FFFFFF">{NEVER}</text>
<text x="{(x2 + x3) / 2:.2f}" y="88.0" text-anchor="middle" font-size="8.5" fill="#6B7280">never proposed</text>
<polyline points="{x0:.2f},35.0 {x0:.2f},30.0 {x2:.2f},30.0 {x2:.2f},35.0" fill="none" stroke="#1A1A1A" stroke-width="1"/>
<text x="{(x0 + x2) / 2:.2f}" y="25.0" text-anchor="middle" font-size="10" font-weight="600">{RECALLED} recalled (49.8%)</text>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


# Lead Fig 1 chrome. Wall fills from FIG1_BUILD_SPEC (not the fverify funnel).
C_CARD = "#F7F7F5"
C_STROKE = "#E5E5E0"
C_TEAL = "#00897B"
C_INK = "#1A1A1A"
C_MUTED = "#6B7280"
C_LINE = "#D1D5DB"
C_ICON = "#6B7280"


def _round(ax, x, y, w, h, fc="white", ec=None, lw=0.6, rs=7, **kw):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle=f"round,pad=0,rounding_size={rs}",
            linewidth=lw,
            facecolor=fc,
            edgecolor=ec or "none",
            mutation_aspect=1,
            clip_on=False,
            **kw,
        )
    )


def _arrow(ax, x0, x1, y, color=C_ICON):
    ax.annotate(
        "",
        xy=(x1, y),
        xytext=(x0, y),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=1.05,
            mutation_scale=8,
            shrinkA=0,
            shrinkB=0,
        ),
        clip_on=False,
    )


def write_fig1(path: Path) -> None:
    """Lead Fig 1 as true vector (PDF text/paths, real SVG, 600 dpi PNG).

    Generation-locked integers (FIG1_BUILD_SPEC; not fverify 204/45/251):
      recall 249/500 (49.8%); self-rank 227/249 (91.2%);
      top-1 227/500 (45.4%); 45.4% ≈ 49.8% × 91.2%;
      wall 227 / 22 / 251.
    """
    fs.apply()
    plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42, "ps.fonttype": 42})

    # SPEC frame 7.00 × 4.00 in → 4200 px wide at 600 dpi.
    W, H = 700.0, 400.0
    fig, ax = plt.subplots(figsize=(7.00, 4.00))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # ---- Row A: three protocol cards ----
    pad, gap, y, h = 16.0, 14.0, 286.0, 98.0
    cw = (W - 2 * pad - 2 * gap) / 3.0
    cards = [
        (
            "1  ·  Input",
            "Molecular formula + literature",
            "peak lists (IR, \u00b9H, \u00b9\u00b3C)",
            "blind peak lists (not traces)",
        ),
        (
            "2  ·  Generation",
            "LLM proposes ranked",
            "candidate structures",
            "true enters pool 249/500 (49.8%)",
        ),
        (
            "3  ·  Verification",
            "Self-rank / optional",
            "forward-verify re-rank",
            "selects true 227/249 (91%) when present",
        ),
    ]
    for i, (title, l1, l2, annot) in enumerate(cards):
        x = pad + i * (cw + gap)
        _round(ax, x, y, cw, h, fc=C_CARD, ec=C_STROKE, rs=7)
        ax.text(x + 12, y + 80, title, ha="left", va="center", fontsize=9, fontweight="bold", color=C_INK)
        ax.text(x + 12, y + 56, l1, ha="left", va="center", fontsize=7.5, color=C_INK)
        ax.text(x + 12, y + 40, l2, ha="left", va="center", fontsize=7.5, color=C_INK)
        ax.text(x + 12, y + 16, annot, ha="left", va="center", fontsize=6.8, fontweight="bold", color=C_TEAL)
        if i < 2:
            _arrow(ax, x + cw + 1.5, x + cw + gap - 1.5, y + h / 2)

    # ---- Row B: decomposition equation ----
    ax.text(
        W / 2,
        258,
        "top-1  =  generation recall  \u00d7  verification precision|recall",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="normal",
        color=C_INK,
    )
    ax.text(
        W / 2,
        236,
        "45.4%  \u2248  49.8%  \u00d7  91.2%",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color=C_INK,
    )
    ax.text(
        W / 2,
        218,
        "n=500 self-rank:  227/500 = 45.4%;   precision|recall  227/249 = 91.2%",
        ha="center",
        va="center",
        fontsize=7,
        color=C_MUTED,
    )

    # ---- Row C: generation wall 227 | 22 | 251 ----
    bx0, bx1 = pad, W - pad
    usable = bx1 - bx0
    yb, hb, gap_pt = 118.0, 36.0, 1.8

    def x_of(count: float) -> float:
        return bx0 + usable * (count / N)

    x1 = x_of(GEN_TOP1)
    x2 = x_of(GEN_TOP1 + GEN_NOT_TOP1)
    x3 = x_of(N)
    segs = [
        (bx0, x1, C_TOP1, str(GEN_TOP1), 12, "top-1"),
        (x1, x2, C_INSET, str(GEN_NOT_TOP1), 9, "not top-1"),
        (x2, x3, C_NEVER, str(GEN_NEVER), 12, "never proposed"),
    ]
    for xa, xb, color, lab, fs_n, under in segs:
        w = max(xb - xa - gap_pt, 8.0)
        ax.add_patch(
            plt.Rectangle((xa, yb), w, hb, facecolor=color, edgecolor="none", lw=0, clip_on=False)
        )
        ax.text(
            xa + w / 2,
            yb + hb / 2,
            lab,
            ha="center",
            va="center",
            fontsize=fs_n,
            fontweight="bold",
            color="white",
            zorder=5,
        )
        ax.text(xa + (xb - xa) / 2, yb - 16, under, ha="center", va="top", fontsize=7.5, color=C_MUTED)

    # Bracket over first two segments (249 recalled).
    rec_x1 = x_of(GEN_RECALL)
    ax.plot(
        [bx0, bx0, rec_x1, rec_x1],
        [yb + hb + 8, yb + hb + 14, yb + hb + 14, yb + hb + 8],
        color=C_INK,
        lw=0.85,
        solid_capstyle="butt",
        clip_on=False,
    )
    ax.text(
        (bx0 + rec_x1) / 2,
        yb + hb + 18,
        "249 recalled (49.8%)",
        ha="center",
        va="bottom",
        fontsize=8.5,
        fontweight="bold",
        color=C_INK,
    )

    ax.text(
        W / 2,
        58,
        "No re-ranking repairs the 251 never proposed",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color=C_INK,
    )
    ax.text(
        W / 2,
        36,
        "Generation decomposition on n=500 \u2014 propose is the wall, not verify",
        ha="center",
        va="center",
        fontsize=7.5,
        color=C_MUTED,
    )

    out = path.with_suffix("")
    fig.savefig(str(out) + ".pdf", facecolor="white")
    fig.savefig(str(out) + ".svg", facecolor="white")
    fig.savefig(str(out) + ".png", dpi=600, facecolor="white")
    plt.close(fig)


def _export_svg(svg_path: Path) -> None:
    try:
        import cairosvg
    except ImportError:
        print(f"wrote {svg_path} (no cairosvg; skip pdf/png)", file=sys.stderr)
        return
    cairosvg.svg2pdf(url=str(svg_path), write_to=str(svg_path.with_suffix(".pdf")))
    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(svg_path.with_suffix(".png")),
        output_width=int(float(svg_path.read_text().split('width="')[1].split('"')[0]) * 2),
    )


def main() -> None:
    fs.apply()
    root = Path(__file__).resolve().parents[1] / "figures"

    # Diagnostic SVG only (fverify 204/45/251). Do not overwrite fig_wall.pdf.
    wall_svg = root / "fig_wall_diagnostic.svg"
    write_svg(wall_svg)
    _export_svg(wall_svg)

    fig1 = root / "fig1_lead_overview"
    write_fig1(fig1)
    print(f"wrote {wall_svg} and {fig1}.{{pdf,png,svg}}")


if __name__ == "__main__":
    main()
