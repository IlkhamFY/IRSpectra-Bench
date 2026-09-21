#!/usr/bin/env python3
"""n=500 fverify wall — propose is the wall, not verify.

Locked integers from spectro-agent data/fverify_n500/WALL_n500.md (no CIs):
  verified:        204
  misranked:        45
  never-proposed:  251
  recalled:        249  (= 204 + 45)
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

# n=500 fverify wall. Do not use generation 227/22/251 here.
N = 500
VERIFIED = 204
MISRANKED = 45
NEVER = 251
RECALLED = VERIFIED + MISRANKED  # 249

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


def write_fig1_svg(path: Path) -> None:
    """Deprecated twin. Lead Fig 1 is the Wonder bake (PDF/PNG); TeX includes PDF."""
    width, height = 504.0, 288.0
    pad_x = 14.0
    usable = width - 2 * pad_x
    y_bar = 176.0
    h_bar = 28.0
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
<rect x="14.0" y="12.0" width="152.0" height="88.0" rx="6" ry="6" fill="#F7F7F5" stroke="#E5E5E0" stroke-width="1"/>
<text x="24.0" y="30.0" font-size="10" font-weight="700">1 · Input</text>
<text x="24.0" y="48.0" font-size="8.5" fill="#1A1A1A">Molecular formula + literature</text>
<text x="24.0" y="60.0" font-size="8.5" fill="#1A1A1A">peak lists (IR cm⁻¹, ¹H, ¹³C)</text>
<text x="24.0" y="88.0" font-size="7.5" font-weight="600" fill="#00897B">blind peak lists (not traces)</text>
<line x1="168.0" y1="56.0" x2="170.0" y2="56.0" stroke="#6B7280" stroke-width="1.2"/>
<polygon points="174.0,56.0 169.0,52.5 169.0,59.5" fill="#6B7280"/>
<rect x="176.0" y="12.0" width="152.0" height="88.0" rx="6" ry="6" fill="#F7F7F5" stroke="#E5E5E0" stroke-width="1"/>
<text x="186.0" y="30.0" font-size="10" font-weight="700">2 · Generation</text>
<text x="186.0" y="48.0" font-size="8.5" fill="#1A1A1A">LLM proposes ranked</text>
<text x="186.0" y="60.0" font-size="8.5" fill="#1A1A1A">candidate structures</text>
<text x="186.0" y="88.0" font-size="7.5" font-weight="600" fill="#00897B">true enters pool 249/500 (49.8%)</text>
<line x1="330.0" y1="56.0" x2="332.0" y2="56.0" stroke="#6B7280" stroke-width="1.2"/>
<polygon points="336.0,56.0 331.0,52.5 331.0,59.5" fill="#6B7280"/>
<rect x="338.0" y="12.0" width="152.0" height="88.0" rx="6" ry="6" fill="#F7F7F5" stroke="#E5E5E0" stroke-width="1"/>
<text x="348.0" y="30.0" font-size="10" font-weight="700">3 · Verification</text>
<text x="348.0" y="48.0" font-size="8.5" fill="#1A1A1A">Self-rank / optional</text>
<text x="348.0" y="60.0" font-size="8.5" fill="#1A1A1A">forward-verify re-rank</text>
<text x="348.0" y="88.0" font-size="7.5" font-weight="600" fill="#00897B">selects true 227/249 (91%) when present</text>
<text x="252.0" y="122.0" text-anchor="middle" font-size="11" font-weight="600" fill="#1A1A1A">top-1 = generation recall × verification precision|recall</text>
<text x="252.0" y="140.0" text-anchor="middle" font-size="12" font-weight="700" fill="#1A1A1A">45.4% ≈ 49.8% × 91.2%</text>
<text x="252.0" y="154.0" text-anchor="middle" font-size="7.5" fill="#6B7280">n=500 self-rank: 227/500 = 45.4%; precision|recall 227/249 = 91.2%</text>
<rect x="{x0:.2f}" y="{y_bar}" width="{w1 - gap:.2f}" height="{h_bar}" fill="{C_TOP1}"/>
<text x="{(x0 + x1 - gap) / 2:.2f}" y="{y_bar + 18.5}" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">{VERIFIED}</text>
<text x="{(x0 + x1) / 2:.2f}" y="218.0" text-anchor="middle" font-size="8" fill="#6B7280">verified</text>
<rect x="{x1:.2f}" y="{y_bar}" width="{max(w2 - gap, 8):.2f}" height="{h_bar}" fill="{C_INSET}"/>
<text x="{x1 + max(w2 - gap, 8) / 2:.2f}" y="{y_bar + 18.5}" text-anchor="middle" font-size="9" font-weight="700" fill="#FFFFFF">{MISRANKED}</text>
<text x="{x1 + w2 / 2:.2f}" y="218.0" text-anchor="middle" font-size="7.5" fill="#6B7280">misranked</text>
<rect x="{x2:.2f}" y="{y_bar}" width="{w3:.2f}" height="{h_bar}" fill="{C_NEVER}"/>
<text x="{(x2 + x3) / 2:.2f}" y="{y_bar + 18.5}" text-anchor="middle" font-size="11" font-weight="700" fill="#FFFFFF">{NEVER}</text>
<text x="{(x2 + x3) / 2:.2f}" y="218.0" text-anchor="middle" font-size="8" fill="#6B7280">never proposed</text>
<polyline points="{x0:.2f},174.0 {x0:.2f},170.0 {x2:.2f},170.0 {x2:.2f},174.0" fill="none" stroke="#1A1A1A" stroke-width="0.9"/>
<text x="{(x0 + x2) / 2:.2f}" y="167.5" text-anchor="middle" font-size="9" font-weight="600" fill="#1A1A1A">{RECALLED} recalled (49.8%)</text>
<text x="252.0" y="234.0" text-anchor="middle" font-size="9" font-weight="600" fill="#1A1A1A">No re-ranking repairs the 251 never proposed</text>
<text x="252.0" y="248.0" text-anchor="middle" font-size="7.5" fill="#6B7280">n=500 forward-verify wall — propose is the wall, not verify</text>
</svg>
'''
    path.write_text(svg, encoding="utf-8")


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

    # Matplotlib twin ( palettes / Overleaf preview )
    fig, ax = plt.subplots(figsize=(7.0, 1.42))
    ax.set_xlim(0, N)
    ax.set_ylim(0, 1)
    ax.axis("off")
    _bar(ax, N)
    out = root / "fig_wall"
    fig.savefig(str(out) + ".png", dpi=600, facecolor="white", bbox_inches="tight", pad_inches=0.08)
    fig.savefig(str(out) + ".pdf", facecolor="white", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)

    wall_svg = root / "fig_wall_diagnostic.svg"
    write_svg(wall_svg)
    _export_svg(wall_svg)

    # Lead Fig 1 is the Wonder ship bake (figures/fig1_lead_overview.pdf/png).
    # TeX includes the PDF; do not overwrite it from this matplotlib twin.
    print(f"wrote {wall_svg} and pdf/png twins")


if __name__ == "__main__":
    main()
