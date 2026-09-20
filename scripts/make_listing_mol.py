#!/usr/bin/env python3
"""Listing 1 molecule — gold held-out constitution for v3-R25.

Disclosed running example (N-tert-butylpicolinamide / 2-pyridyl).
The solver never sees this structure; it is scored offline.
"""
from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drawmol
import figstyle as fs

SMILES = "CC(C)(C)NC(=O)c1ccccn1"


def main() -> None:
    fs.apply()
    fig, ax = plt.subplots(figsize=(2.20, 1.55))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    drawmol.show_mol(ax, SMILES, (0.00, 0.00, 1.00, 1.00), px=(640, 440))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    out = Path(__file__).resolve().parents[1] / "figures" / "fig_listing_mol"
    fig.savefig(str(out) + ".png", dpi=600, facecolor="white", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(str(out) + ".pdf", facecolor="white", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"wrote {out}.png/.pdf")


if __name__ == "__main__":
    main()
