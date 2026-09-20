#!/usr/bin/env python3
"""Molecule drawing for ICLR plates (RDKit Cairo + optional vector bonds)."""
from __future__ import annotations

import io

import numpy as np
from matplotlib.patches import Circle
from PIL import Image
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import PrepareMolForDrawing, rdMolDraw2D

ATOM_COL = {7: "#0077BB", 8: "#CC3311", 9: "#009988", 16: "#EE7733", 15: "#EE7733"}
ATOM_LAB = {7: "N", 8: "O", 9: "F", 16: "S", 15: "P"}


def _trim(img: Image.Image, pad: int = 10) -> Image.Image:
    arr = np.asarray(img)
    if arr.ndim == 3 and arr.shape[2] == 4:
        ink = arr[:, :, 3] > 8
        ink |= arr[:, :, :3].min(axis=2) < 248
    else:
        ink = arr.min(axis=2) < 248 if arr.ndim == 3 else arr < 248
    ys, xs = np.where(ink)
    if xs.size == 0:
        return img
    l, r = max(0, int(xs.min()) - pad), min(img.width, int(xs.max()) + pad)
    t, b = max(0, int(ys.min()) - pad), min(img.height, int(ys.max()) + pad)
    return img.crop((l, t, r, b))


def mol_image(smiles: str, w: int = 560, h: int = 400) -> Image.Image:
    """High-res RDKit Cairo drawing (amide H, aromatic rings, heteroatom colors)."""
    mol = PrepareMolForDrawing(Chem.MolFromSmiles(smiles))
    d = rdMolDraw2D.MolDraw2DCairo(w, h)
    opt = d.drawOptions()
    opt.bondLineWidth = 1.8
    opt.additionalAtomLabelPadding = 0.08
    opt.fixedFontSize = 18
    d.DrawMolecule(mol)
    d.FinishDrawing()
    return _trim(Image.open(io.BytesIO(d.GetDrawingText())).convert("RGBA"))


def show_mol(ax, smiles: str, bbox: tuple[float, float, float, float], *, px=(560, 400)):
    """Place a Cairo molecule into ``bbox=(x0,y0,w,h)`` without stretching."""
    x0, y0, w, h = bbox
    img = mol_image(smiles, px[0], px[1])
    iw, ih = img.size
    aspect = iw / float(ih)
    if w / h > aspect:
        nw, nh = h * aspect, h
        x0 = x0 + (w - nw) / 2
        w = nw
    else:
        nw, nh = w, w / aspect
        y0 = y0 + (h - nh) / 2
        h = nh
    ax.imshow(
        img,
        extent=(x0, x0 + w, y0, y0 + h),
        aspect="auto",
        interpolation="lanczos",
        zorder=5,
        origin="upper",
    )


def prepare(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(smiles)
    mol = Chem.Mol(mol)
    Chem.Kekulize(mol, clearAromaticFlags=True)
    AllChem.Compute2DCoords(mol)
    return mol


def _scale(pts: np.ndarray, bbox: tuple[float, float, float, float], pad: float = 0.10):
    x0, y0, w, h = bbox
    xmin, xmax = float(pts[:, 0].min()), float(pts[:, 0].max())
    ymin, ymax = float(pts[:, 1].min()), float(pts[:, 1].max())
    sx = (w * (1 - 2 * pad)) / max(xmax - xmin, 1e-6)
    sy = (h * (1 - 2 * pad)) / max(ymax - ymin, 1e-6)
    s = min(sx, sy)
    cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
    mapped = np.column_stack(
        [x0 + w / 2 + (pts[:, 0] - cx) * s, y0 + h / 2 + (pts[:, 1] - cy) * s]
    )
    return mapped, s


def draw_mol(
    ax,
    smiles: str,
    bbox: tuple[float, float, float, float],
    *,
    bond_color: str = "#1a1a1a",
    lw: float = 1.15,
    font: float = 7.0,
    hetero_ms: float = 6.5,
    pad: float = 0.10,
):
    """Draw ``smiles`` into ``bbox=(x0,y0,w,h)`` in axes data coordinates."""
    mol = prepare(smiles)
    conf = mol.GetConformer()
    pts = np.array(
        [[conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y] for i in range(mol.GetNumAtoms())],
        dtype=float,
    )
    xy, s = _scale(pts, bbox, pad=pad)
    # Double-bond offset in data units (scales with the smaller box side).
    x0, y0, w, h = bbox
    off = 0.018 * min(w, h)

    for bond in mol.GetBonds():
        i, j = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        p1, p2 = xy[i], xy[j]
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            d = p2 - p1
            n = np.array([-d[1], d[0]], dtype=float)
            n = n / (np.linalg.norm(n) + 1e-9) * off
            ax.plot(
                [p1[0] + n[0], p2[0] + n[0]],
                [p1[1] + n[1], p2[1] + n[1]],
                color=bond_color,
                lw=lw * 0.92,
                solid_capstyle="round",
                zorder=3,
                clip_on=False,
            )
            ax.plot(
                [p1[0] - n[0], p2[0] - n[0]],
                [p1[1] - n[1], p2[1] - n[1]],
                color=bond_color,
                lw=lw * 0.92,
                solid_capstyle="round",
                zorder=3,
                clip_on=False,
            )
        else:
            ax.plot(
                [p1[0], p2[0]],
                [p1[1], p2[1]],
                color=bond_color,
                lw=lw,
                solid_capstyle="round",
                zorder=3,
                clip_on=False,
            )

    for atom in mol.GetAtoms():
        z = atom.GetAtomicNum()
        if z == 6:
            continue
        x, y = xy[atom.GetIdx()]
        col = ATOM_COL.get(z, bond_color)
        ax.add_patch(
            Circle(
                (x, y),
                radius=min(w, h) * 0.055,
                facecolor="white",
                edgecolor="none",
                zorder=4,
                clip_on=False,
            )
        )
        ax.text(
            x,
            y,
            ATOM_LAB.get(z, atom.GetSymbol()),
            ha="center",
            va="center",
            fontsize=font,
            fontweight="bold",
            color=col,
            zorder=5,
            clip_on=False,
        )
    return mol
