#!/usr/bin/env python3
"""Fetch Listing 1 molecule art from PubChem 3D (not RDKit 2D, not a baked plate).

Commercial-DoR record: `docs/figma-pack/listing1_exact_record.json`
(ILJNJJNKEOAREX-UHFFFAOYSA-N; CID 57398578). The ICLR float is live
lstlisting + framed minipages in `main.tex`; this script only writes
`figures/listing1_mol_pubchem3d.png` (PubChem PUG 3D conformer, canvas
punched to alpha).
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "docs/figma-pack/listing1_exact_record.json"
FIG = ROOT / "figures"
OUT_PNG = FIG / "listing1_mol_pubchem3d.png"

PUG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
UA = "IRSpectra-Bench/listing1 (manuscript figure; mailto:yabbaroi@mcmaster.ca)"
# Official PUG 3D image is 300x300 (`image_size=large`); arbitrary 3D sizes 501.
PNG_QUERY = "record/PNG?record_type=3d&image_size=large"
UREA = "NTJIYHYWVZYBEX-UHFFFAOYSA-N"


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def resolve_cid(inchikey: str) -> int:
    url = f"{PUG}/compound/inchikey/{inchikey}/cids/JSON"
    payload = json.loads(_get(url).decode("utf-8"))
    cids = payload["IdentifierList"]["CID"]
    if not cids:
        raise SystemExit(f"no PubChem CID for {inchikey}")
    return int(cids[0])


def confirm_3d(cid: int) -> list[str]:
    url = f"{PUG}/compound/cid/{cid}/conformers/JSON"
    payload = json.loads(_get(url).decode("utf-8"))
    ids = payload["InformationList"]["Information"][0]["ConformerID"]
    if not ids:
        raise SystemExit(f"CID {cid} has no PubChem 3D conformer")
    return [str(x) for x in ids]


def punch_canvas(img: Image.Image, thresh: int = 248) -> Image.Image:
    """Punch border-connected near-white canvas to alpha (labels stay)."""
    arr = img.convert("RGBA")
    px = arr.load()
    w, h = arr.size
    vis = [[False] * w for _ in range(h)]
    stack: list[tuple[int, int]] = []

    def is_white(x: int, y: int) -> bool:
        r, g, b, _a = px[x, y]
        return min(r, g, b) >= thresh

    def push(x: int, y: int) -> None:
        if 0 <= x < w and 0 <= y < h and not vis[y][x] and is_white(x, y):
            vis[y][x] = True
            stack.append((x, y))

    for x in range(w):
        push(x, 0)
        push(x, h - 1)
    for y in range(h):
        push(0, y)
        push(w - 1, y)
    while stack:
        x, y = stack.pop()
        r, g, b, _a = px[x, y]
        px[x, y] = (r, g, b, 0)
        push(x + 1, y)
        push(x - 1, y)
        push(x, y + 1)
        push(x, y - 1)
    return arr


def crop_visible(img: Image.Image, pad: int = 8) -> Image.Image:
    bbox = img.getbbox()
    if bbox is None:
        return img
    l, t, r, b = bbox
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(img.width, r + pad)
    b = min(img.height, b + pad)
    return img.crop((l, t, r, b))


def main() -> int:
    rec = json.loads(RECORD_PATH.read_text())
    inchikey = rec["inchikey"]
    if inchikey == UREA:
        raise SystemExit("refusing Sci Data urea clone; pick another commercial-DoR record")
    try:
        cid = resolve_cid(inchikey)
        conformers = confirm_3d(cid)
        png = _get(f"{PUG}/compound/cid/{cid}/{PNG_QUERY}")
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as exc:
        raise SystemExit(f"PubChem PUG 3D fetch failed: {exc}") from exc
    if png[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"PUG 3D response is not a PNG ({png[:40]!r})")
    raw = Image.open(BytesIO(png))
    if raw.size[0] < 100 or raw.size[1] < 100:
        raise SystemExit(f"unexpected 3D PNG size {raw.size}")
    # Keep a little canvas so the planar 3D conformer is not a razor strip.
    mol = crop_visible(punch_canvas(raw), pad=16)
    FIG.mkdir(exist_ok=True)
    mol.save(OUT_PNG, "PNG")
    print(
        f"wrote {OUT_PNG} {mol.size[0]}x{mol.size[1]} "
        f"inchikey={inchikey} cid={cid} conformers={','.join(conformers[:4])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
