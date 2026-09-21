#!/usr/bin/env python3
"""Rebuild Listing 1 IRexp record plate (JSON + molecule).

Commercial-DoR example is `docs/figma-pack/listing1_exact_record.json`
(ILJNJJNKEOAREX; not the Sci Data NTJIYHYWVZYBEX urea clone).

Layout (no in-artwork "Listing 1" title — LaTeX already captions the float):
  framed two-column, JSON left / RDKit mol right, tight crop under the JSON.
Molecule canvas is transparent (border flood-fill); heteroatom knockouts stay.
"""
from __future__ import annotations

import base64
import io
import json
import sys
from pathlib import Path

from PIL import Image
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawmol import mol_image  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "docs/figma-pack/listing1_exact_record.json"
FIG = ROOT / "figures"

# Print frame (pt). Height is derived from JSON line count — no phantom strip.
W = 504.0
FRAME_X = 8.0
FRAME_Y = 8.0
FRAME_W = 488.0
LEFT_FRAC = 0.62
GAP_FRAC = 0.04
JSON_SIZE = 6.2
JSON_LH = 9.2
INNER = 8.0
COL_WRAP = 76


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _comma_tokens(value: str) -> list[str]:
    """Split on commas that are not inside parentheses (NMR J-lists)."""
    tokens: list[str] = []
    buf = ""
    depth = 0
    i = 0
    while i < len(value):
        ch = value[i]
        if ch == "(":
            depth += 1
            buf += ch
        elif ch == ")":
            depth = max(0, depth - 1)
            buf += ch
        elif ch == "," and depth == 0:
            buf += ","
            if i + 1 < len(value) and value[i + 1] == " ":
                buf += " "
                i += 1
            tokens.append(buf)
            buf = ""
        else:
            buf += ch
        i += 1
    if buf:
        tokens.append(buf)
    return tokens


def _wrap_value(prefix: str, value: str, width: int, cont_indent: int) -> list[str]:
    """Keep ``prefix`` on the first content line; break on ``, `` when present."""
    indent = " " * cont_indent
    if ", " in value:
        tokens = _comma_tokens(value)
    else:
        words = value.split(" ")
        tokens = [words[0]] + [f" {w}" for w in words[1:]] if words else [""]
    lines: list[str] = []
    lead = prefix
    buf = ""
    for tok in tokens:
        piece = buf + tok
        if len(lead + piece) <= width:
            buf = piece
            continue
        if buf:
            lines.append(lead + buf.rstrip())
        elif lead.strip():
            lines.append(lead.rstrip())
        lead = indent
        buf = tok.lstrip()
    if buf:
        lines.append(lead + buf)
    return lines or [prefix + value]


def json_lines(rec: dict) -> list[str]:
    bands = rec["ir_bands_cm-1"]
    band_str = ", ".join(f"{float(x):.1f}" for x in bands)
    h_nmr = rec["h_nmr"]
    c_nmr = rec["c_nmr"]
    lines = ["{"]
    lines.append(f'  "id": "{rec["id"]}",')
    if rec.get("formula"):
        lines.append(f'  "formula": "{rec["formula"]}",')
    lines.extend(
        _wrap_value('  "ir_bands_cm-1": [', band_str + "],", COL_WRAP, 20)
    )
    lines.append(f'  "ir_source": "{rec["ir_source"]}",')
    lines.append(f'  "source_doi": "{rec["source_doi"]}",')
    lines.append(f'  "pmcid": "{rec["pmcid"]}",')
    lines.extend(_wrap_value('  "h_nmr": "', h_nmr + '",', COL_WRAP, 11))
    lines.extend(_wrap_value('  "c_nmr": "', c_nmr + '",', COL_WRAP, 11))
    lines.append(f'  "smiles": "{rec["smiles"]}",')
    lines.append(f'  "inchikey": "{rec["inchikey"]}",')
    lines.append(f'  "has_structure": {str(rec["has_structure"]).lower()},')
    lines.append(f'  "license": "{rec["license"]}",')
    lines.append(f'  "license_pool": "{rec["license_pool"]}"')
    lines.append("}")
    return lines


def save_mol(smiles: str) -> Image.Image:
    img = mol_image(smiles, 720, 720, transparent=True)
    png_path = FIG / "listing1_mol_rdkit.png"
    img.save(png_path, "PNG")
    # Vector twin: embed the RGBA raster with a fully transparent page.
    iw, ih = img.size
    max_in = 3.0
    if iw >= ih:
        win, hin = max_in, max_in * ih / iw
    else:
        hin, win = max_in, max_in * iw / ih
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(win, hin), facecolor="none")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img)
    ax.axis("off")
    fig.savefig(
        FIG / "listing1_mol_rdkit.pdf",
        facecolor="none",
        edgecolor="none",
        transparent=True,
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close(fig)
    return img


def write_svg(rec: dict, mol: Image.Image) -> Path:
    lines = json_lines(rec)
    json_h = len(lines) * JSON_LH
    frame_h = INNER + json_h + INNER
    height = FRAME_Y + frame_h + FRAME_Y

    left_w = FRAME_W * LEFT_FRAC
    gap_w = FRAME_W * GAP_FRAC
    right_w = FRAME_W - left_w - gap_w
    mol_pad = 8.0
    box = min(right_w - 2 * mol_pad, frame_h - 2 * mol_pad)
    iw, ih = mol.size
    aspect = iw / float(ih)
    if aspect >= 1:
        mw, mh = box, box / aspect
    else:
        mh, mw = box, box * aspect
    mx = FRAME_X + left_w + gap_w + (right_w - mw) / 2
    my = FRAME_Y + (frame_h - mh) / 2

    buf = io.BytesIO()
    mol.save(buf, format="PNG")
    href = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{W:.1f}" height="{height:.1f}" viewBox="0 0 {W:.1f} {height:.1f}">',
        # Page is white for print; molecule itself has no opaque canvas.
        f'<rect width="{W:.1f}" height="{height:.1f}" fill="#FFFFFF"/>',
        '<defs><style type="text/css">'
        '@font-face { font-family: DejaVuSans; src: local("DejaVu Sans"); }'
        '@font-face { font-family: DejaVuSansMono; src: local("DejaVu Sans Mono"); }'
        "text { font-family: DejaVuSans, Helvetica, Arial, sans-serif; fill: #1A1A1A; }"
        '.mono { font-family: DejaVuSansMono, "Courier New", monospace; }'
        "</style></defs>",
        f'<rect x="{FRAME_X:.1f}" y="{FRAME_Y:.1f}" width="{FRAME_W:.1f}" '
        f'height="{frame_h:.1f}" rx="4" ry="4" fill="#F7F7F5" stroke="#E5E5E0" stroke-width="1"/>',
    ]
    x_json = FRAME_X + INNER
    y0 = FRAME_Y + INNER + JSON_SIZE
    for i, line in enumerate(lines):
        y = y0 + i * JSON_LH
        parts.append(
            f'<text x="{x_json:.1f}" y="{y:.1f}" class="mono" '
            f'font-size="{JSON_SIZE}" fill="#1A1A1A">{_esc(line)}</text>'
        )
    parts.append(
        f'<image x="{mx:.1f}" y="{my:.1f}" width="{mw:.1f}" height="{mh:.1f}" '
        f'href="{href}"/>'
    )
    parts.append("</svg>")
    path = FIG / "listing1_irexp_record.svg"
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    return path


def export_svg(svg_path: Path) -> None:
    try:
        import cairosvg
    except ImportError:
        print(f"wrote {svg_path} (no cairosvg; skip pdf/png)", file=sys.stderr)
        return
    pdf = svg_path.with_suffix(".pdf")
    png = svg_path.with_suffix(".png")
    cairosvg.svg2pdf(url=str(svg_path), write_to=str(pdf))
    width = float(svg_path.read_text().split('width="')[1].split('"')[0])
    cairosvg.svg2png(url=str(svg_path), write_to=str(png), output_width=int(width * 2))


def attach_formula(rec: dict) -> dict:
    """RDKit formula from the record SMILES (solver-visible; not stored in IRexp dump)."""
    mol = Chem.MolFromSmiles(rec["smiles"])
    if mol is None:
        raise ValueError(rec["smiles"])
    rec = dict(rec)
    rec["formula"] = rdMolDescriptors.CalcMolFormula(mol)
    return rec


def main() -> int:
    rec = json.loads(RECORD_PATH.read_text())
    rec = attach_formula(rec)
    if rec["inchikey"] == "NTJIYHYWVZYBEX-UHFFFAOYSA-N":
        raise SystemExit("refusing Sci Data urea clone; pick another commercial-DoR record")
    FIG.mkdir(exist_ok=True)
    mol = save_mol(rec["smiles"])
    svg = write_svg(rec, mol)
    export_svg(svg)
    text = svg.read_text()
    if "Listing 1" in text:
        raise SystemExit("in-artwork Listing 1 label leaked into SVG")
    h = float(text.split('height="')[1].split('"')[0])
    if h >= 260:
        raise SystemExit(f"plate height {h:.1f} still has phantom strip")
    print(f"wrote {svg} height={h:.1f}pt formula={rec['formula']} {rec['inchikey']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
