#!/usr/bin/env python3
"""Compile si/supplement.tex → si/supplement.pdf."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SI_DIR = os.path.join(ROOT, "si")
TEX = os.path.join(SI_DIR, "supplement.tex")
OUT = os.path.join(SI_DIR, "supplement.pdf")


def main() -> int:
    engine = os.environ.get("PDF_ENGINE") or shutil.which("tectonic") or "/tmp/tectonic"
    if not os.path.isfile(engine) and not shutil.which(engine):
        print("no tectonic", file=sys.stderr)
        return 3
    if engine == "tectonic" or engine.endswith("/tectonic"):
        rc = subprocess.call(
            [engine, "--keep-logs", "--keep-intermediates", "-o", SI_DIR, TEX],
            cwd=SI_DIR,
        )
    else:
        rc = subprocess.call([engine, "-interaction=nonstopmode", "supplement.tex"], cwd=SI_DIR)
    if not os.path.isfile(OUT):
        print("SI build produced no PDF", file=sys.stderr)
        return 4
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
