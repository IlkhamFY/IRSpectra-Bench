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


# Lead Fig 1 chrome — protocol dashboard matching the merged gen plate.
C_NAVY = "#1e40af"
C_SKY = "#bfdbfe"
C_GRAY = "#D1D5DB"
C_GRAY_DEEP = "#9AA0A6"
C_CARD = "#eff6ff"
C_PANEL = "#f8fafc"
C_DASH = "#93c5fd"
C_INK = "#0f172a"
C_MUTED = "#64748b"
C_LINE = "#cbd5e1"
C_ICON = "#94a3b8"


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


def _bars_icon(ax, cx, cy, color=C_ICON):
    for i, h in enumerate((8.0, 13.0, 10.0)):
        ax.add_patch(
            plt.Rectangle(
                (cx - 8.5 + i * 6.4, cy - 6.5),
                4.4,
                h,
                facecolor=color,
                edgecolor="none",
                lw=0,
                clip_on=False,
            )
        )


def _mol(ax, cx, cy, scale=1.0, color="#334155", selected=False):
    s = scale
    if selected:
        ax.add_patch(
            plt.Circle((cx, cy), 15.0 * s, facecolor=C_NAVY, edgecolor="none", clip_on=False, zorder=4)
        )
        ax.plot(
            [cx - 5.4 * s, cx - 1.6 * s, cx + 6.4 * s],
            [cy - 0.2 * s, cy - 4.8 * s, cy + 5.4 * s],
            color="white",
            lw=1.7,
            solid_capstyle="round",
            solid_joinstyle="round",
            zorder=6,
            clip_on=False,
        )
        return
    pts = [
        (cx - 7 * s, cy - 3 * s),
        (cx - 2 * s, cy + 5 * s),
        (cx + 6 * s, cy + 4 * s),
        (cx + 8 * s, cy - 4 * s),
        (cx + 1 * s, cy - 7 * s),
    ]
    xs, ys = zip(*pts)
    ax.plot(
        list(xs) + [xs[0]],
        list(ys) + [ys[0]],
        color=color,
        lw=1.15,
        solid_capstyle="round",
        solid_joinstyle="round",
        zorder=5,
        clip_on=False,
    )
    ax.plot(
        [cx - 2 * s, cx - 9 * s],
        [cy + 5 * s, cy + 8 * s],
        color=color,
        lw=1.15,
        solid_capstyle="round",
        zorder=5,
        clip_on=False,
    )


def write_fig1(path: Path) -> None:
    """Lead Fig 1 as true vector (PDF text/paths, real SVG, 600 dpi PNG).

    Generation-locked integers (same as merged main / PR #32; not fverify):
      recall 249/500 (49.8%); self-rank 227/249 (91.2%);
      top-1 227/500 (45.4%); 49.8% × 91.2% = 45.4%;
      wall 227 / 22 / 251.
    """
    fs.apply()
    plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42, "ps.fonttype": 42})

    # ~7.00 × 3.10 in matches the hi-res gen plate (3024×1329); 4200 px @ 600 dpi.
    fig, ax = plt.subplots(figsize=(7.00, 3.10))
    ax.set_xlim(0, 700)
    ax.set_ylim(0, 310)
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    y, h = 200, 94
    _round(ax, 16, y, 108, h, fc="white", ec=C_LINE, rs=8)
    ax.add_patch(plt.Circle((70, y + 70), 11, facecolor=C_CARD, edgecolor="none", clip_on=False))
    _bars_icon(ax, 70, y + 68)
    ax.text(70, y + 46, "Peak lists", ha="center", va="center", fontsize=8, fontweight="bold", color=C_INK)
    ax.text(70, y + 30, "IR  ·  \u00b9H  ·  \u00b9\u00b3C", ha="center", va="center", fontsize=6.5, color=C_MUTED)
    _arrow(ax, 128, 140, y + h / 2)

    _round(ax, 144, y, 118, h, fc=C_CARD, ec="none", rs=8)
    ax.text(203, y + 72, "Generate", ha="center", va="center", fontsize=8, fontweight="bold", color=C_INK)
    ax.text(203, y + 46, "249/500", ha="center", va="center", fontsize=13, fontweight="bold", color=C_INK)
    ax.text(203, y + 24, "recall in top 3", ha="center", va="center", fontsize=6.5, color=C_MUTED)
    _arrow(ax, 266, 278, y + h / 2)

    _round(ax, 282, y, 246, h, fc=C_PANEL, ec=C_DASH, lw=1.05, rs=8, linestyle=(0, (3.2, 2.0)))
    ax.text(405, y + 78, "candidate pool", ha="center", va="center", fontsize=7, color=C_MUTED)
    for i, xm in enumerate([318, 362, 405, 448, 492]):
        _mol(ax, xm, y + 40, scale=1.0 if i != 3 else 1.05, selected=(i == 3), color="#64748b")
    _arrow(ax, 532, 544, y + h / 2)

    _round(ax, 548, y, 136, h, fc="white", ec=C_LINE, rs=8)
    _mol(ax, 616, y + 74, scale=0.72, color=C_ICON)
    ax.text(616, y + 54, "Select", ha="center", va="center", fontsize=8, fontweight="bold", color=C_INK)
    ax.text(616, y + 34, "227/249", ha="center", va="center", fontsize=13, fontweight="bold", color=C_NAVY)
    ax.text(616, y + 16, "top-1 | recalled", ha="center", va="center", fontsize=6.5, color=C_MUTED)

    pills = [
        (118, "49.8%  recall in top 3", "white", C_INK, C_LINE),
        (350, "91.2%  top-1 | recalled", "white", C_INK, C_LINE),
        (575, "45.4%  top-1", C_NAVY, "white", C_NAVY),
    ]
    for x, lab, fc, tc, ec in pills:
        _round(ax, x - 88, 160, 176, 26, fc=fc, ec=ec, rs=13)
        ax.text(x, 173, lab, ha="center", va="center", fontsize=7, fontweight="bold", color=tc)
    ax.text(236, 173, "\u00d7", ha="center", va="center", fontsize=11, color=C_MUTED)
    ax.text(462, 173, "=", ha="center", va="center", fontsize=11, color=C_MUTED)

    _round(ax, 16, 10, 668, 136, fc=C_PANEL, ec="none", rs=9)
    ax.text(32, 128, "Where top-1 fails", ha="left", va="center", fontsize=8.5, fontweight="bold", color=C_INK)
    ax.text(64, 82, "500", ha="center", va="center", fontsize=18, fontweight="bold", color=C_INK)
    ax.text(64, 58, "n=500", ha="center", va="center", fontsize=6.5, color=C_MUTED)
    _arrow(ax, 96, 118, 80)

    def _funnel(x, y0, w, hbar, fc, title, n, dark=False):
        _round(ax, x, y0, w, hbar, fc=fc, ec="none", rs=5)
        tc = "white" if dark else C_INK
        ax.text(x + 10, y0 + hbar / 2, title, ha="left", va="center", fontsize=7, color=tc)
        ax.text(x + w - 10, y0 + hbar / 2, str(n), ha="right", va="center", fontsize=10, fontweight="bold", color=tc)

    _funnel(124, 72, 250, 28, C_SKY, "in pool", GEN_RECALL)
    _arrow(ax, 380, 400, 86)
    _funnel(406, 72, 250, 28, C_NAVY, "exact top-1", GEN_TOP1, dark=True)
    _funnel(124, 28, 250, 28, C_GRAY, "never proposed", GEN_NEVER)
    _arrow(ax, 380, 400, 42)
    _funnel(406, 28, 250, 28, C_GRAY_DEEP, "in pool, not top-1", GEN_NOT_TOP1)

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
