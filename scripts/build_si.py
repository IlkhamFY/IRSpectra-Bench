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


def _engine() -> str | None:
    env = os.environ.get("PDF_ENGINE")
    if env and (os.path.isfile(env) or shutil.which(env)):
        return env if os.path.isfile(env) else shutil.which(env)
    for cand in ("/tmp/tectonic", "tectonic", "pdflatex", "xelatex"):
        if cand.startswith("/") and os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
        found = shutil.which(cand)
        if found:
            return found
    return None


def main() -> int:
    engine = _engine()
    if not engine:
        print("no PDF engine (tectonic/pdflatex/xelatex)", file=sys.stderr)
        return 3
    base = os.path.basename(engine)
    if base == "tectonic" or engine.endswith("/tectonic"):
        rc = subprocess.call(
            [engine, "--keep-logs", "--keep-intermediates", "-o", SI_DIR, TEX],
            cwd=SI_DIR,
        )
    else:
        rc = 0
        for _ in range(2):
            rc = subprocess.call(
                [engine, "-interaction=nonstopmode", "supplement.tex"], cwd=SI_DIR
            )
            if rc != 0:
                break
    if not os.path.isfile(OUT):
        print("SI build produced no PDF", file=sys.stderr)
        return 4
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
