#!/usr/bin/env python3
"""Chemistry-space plate for the pooled IRSpectra-Bench headline (n=295).

Panels: molecular weight, RDKit ring count, C–F bonds / molecule, N atoms / molecule.
Locked (194) vs validate-clean expansion (101), stacked. Five 13C-overread flags
(R12, R22, R25, R82, R91) are excluded. No accuracy metrics.

SMILES are read from spectro-agent (locked answers + unique (formula, IR, 13C)
match of the expansion questions against irexp_resolved). Expansion answers2.jsonl
is not written and is not required.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from rdkit import Chem, RDLogger
from rdkit.Chem import Descriptors, rdMolDescriptors

RDLogger.DisableLog("rdApp.*")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figstyle as fs  # noqa: E402

FLAGS = frozenset({"R12", "R22", "R25", "R82", "R91"})
LOCKED_N, EXPAND_N, POOL_N = 194, 101, 295


def _spectro_root(cli: str | None) -> Path:
    if cli:
        return Path(cli)
    env = os.environ.get("SPECTRO_AGENT")
    if env:
        return Path(env)
    for cand in (
        Path("/tmp/spectro-agent"),
        Path(__file__).resolve().parents[2] / "spectro-agent",
    ):
        if (cand / "data/benchmark_main/answers2.jsonl").is_file():
            return cand
    raise SystemExit(
        "spectro-agent checkout not found; pass --spectro or set SPECTRO_AGENT"
    )


def _cf_bonds(mol) -> int:
    n = 0
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 9:
            continue
        n += sum(1 for nb in atom.GetNeighbors() if nb.GetAtomicNum() == 6)
    return n


def _n_atoms(mol) -> int:
    return sum(1 for a in mol.GetAtoms() if a.GetAtomicNum() == 7)


def descriptors(smiles: str) -> dict:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("unparseable SMILES")
    return {
        "mw": float(Descriptors.MolWt(mol)),
        "hac": int(mol.GetNumHeavyAtoms()),
        "rings": int(mol.GetRingInfo().NumRings()),
        "arings": int(rdMolDescriptors.CalcNumAromaticRings(mol)),
        "cf": _cf_bonds(mol),
        "n": _n_atoms(mol),
    }


def load_locked(root: Path) -> list[dict]:
    rows = []
    clean = set(json.load(open(root / "data/benchmark_main/clean_qids.json")))
    answers = {
        json.loads(line)["qid"]: json.loads(line)
        for line in open(root / "data/benchmark_main/answers2.jsonl")
    }
    for qid, ans in answers.items():
        if qid not in clean:
            continue
        rows.append({"slice": "locked", "qid": qid, **descriptors(ans["smiles"])})
    for sub in ("benchmark_v3", "benchmark_v2_ctrl"):
        for line in open(root / f"data/{sub}/answers2.jsonl"):
            ans = json.loads(line)
            rows.append(
                {"slice": "locked", "qid": ans["qid"], **descriptors(ans["smiles"])}
            )
    return rows


def _match_key(formula, bands, c_nmr):
    return (formula, tuple(bands or []), c_nmr or "")


def load_expand_clean(root: Path) -> list[dict]:
    gold = root / "data/irexp_resolved/irexp_resolved.jsonl.gz"
    questions = [
        json.loads(line)
        for line in open(root / "data/benchmark_expand/questions2.jsonl")
    ]
    clean = set(json.load(open(root / "data/benchmark_expand/clean_qids.json")))
    assert FLAGS.isdisjoint(clean), FLAGS & clean
    assert len(clean) == EXPAND_N, len(clean)

    index: dict[tuple, dict] = {}
    duplicates = set()
    with gzip.open(gold, "rt") as fh:
        for line in fh:
            rec = json.loads(line)
            smi = rec.get("smiles")
            if not smi:
                continue
            mol = Chem.MolFromSmiles(smi)
            if mol is None:
                continue
            key = _match_key(
                rdMolDescriptors.CalcMolFormula(mol),
                rec.get("ir_bands_cm-1"),
                rec.get("c_nmr"),
            )
            if key in index:
                duplicates.add(key)
            else:
                index[key] = rec

    rows = []
    for q in questions:
        qid = q["qid"]
        key = _match_key(q["formula"], q["ir_bands_cm-1"], q["c_nmr"])
        if key in duplicates:
            raise SystemExit(f"ambiguous gold match for expansion {qid}")
        rec = index.get(key)
        if rec is None:
            raise SystemExit(f"no gold match for expansion {qid}")
        if qid not in clean:
            continue
        rows.append({"slice": "expand", "qid": qid, **descriptors(rec["smiles"])})
    return rows


def _vals(rows, key):
    return np.array([r[key] for r in rows], dtype=float)


def _stack_hist(ax, locked, expand, bins, **bar_kw):
    l_counts, edges = np.histogram(locked, bins=bins)
    e_counts, _ = np.histogram(expand, bins=bins)
    width = np.diff(edges)
    centres = edges[:-1]
    ax.bar(
        centres,
        l_counts,
        width=width,
        align="edge",
        color=fs.BLUE,
        edgecolor="white",
        linewidth=0.35,
        zorder=3,
        **bar_kw,
    )
    ax.bar(
        centres,
        e_counts,
        width=width,
        align="edge",
        bottom=l_counts,
        color=fs.SKY,
        edgecolor="white",
        linewidth=0.35,
        zorder=3,
        **bar_kw,
    )
    return int(l_counts.max() + e_counts.max())


def _stack_counts(ax, locked, expand, labels, edges):
    """Integer bins; last edge may be inf for a ≥k tail."""
    l_counts = np.array(
        [np.sum((locked >= lo) & (locked < hi)) for lo, hi in zip(edges[:-1], edges[1:])],
        dtype=int,
    )
    e_counts = np.array(
        [np.sum((expand >= lo) & (expand < hi)) for lo, hi in zip(edges[:-1], edges[1:])],
        dtype=int,
    )
    x = np.arange(len(labels))
    ax.bar(x, l_counts, color=fs.BLUE, width=0.72, zorder=3)
    ax.bar(x, e_counts, bottom=l_counts, color=fs.SKY, width=0.72, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    return x, l_counts + e_counts


def _clean_ax(ax, ylabel=None):
    ax.grid(False)
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    if ylabel:
        ax.set_ylabel(ylabel)


def caption_stats(locked, expand):
    pool = locked + expand
    def med(key):
        v = sorted(_vals(pool, key))
        return float(v[len(v) // 2])

    n_cf = int(sum(r["cf"] > 0 for r in pool))
    n_ali = int(sum(r["arings"] == 0 for r in pool))
    hac = _vals(pool, "hac")
    mw = _vals(pool, "mw")
    return {
        "n": len(pool),
        "n_locked": len(locked),
        "n_expand": len(expand),
        "mw_median": med("mw"),
        "mw_min": float(mw.min()),
        "mw_max": float(mw.max()),
        "hac_median": med("hac"),
        "hac_min": int(hac.min()),
        "hac_max": int(hac.max()),
        "rings_median": med("rings"),
        "arings_median": med("arings"),
        "n_aliphatic": n_ali,
        "n_with_cf": n_cf,
        "n_median": med("n"),
    }


def draw(locked, expand, out: Path):
    fs.apply()
    fig, axes = plt.subplots(1, 4, figsize=(fs.COL2, 2.22))
    ax_a, ax_b, ax_c, ax_d = axes

    l_mw, e_mw = _vals(locked, "mw"), _vals(expand, "mw")
    _stack_hist(ax_a, l_mw, e_mw, bins=np.arange(100, 900, 40))
    _clean_ax(ax_a, "compounds")
    ax_a.set_xlabel("molecular weight")
    ax_a.set_xlim(100, 860)
    ax_a.set_xticks([200, 400, 600, 800])
    fs.panel(ax_a, "a", x=-0.22, y=1.12)

    ring_edges = np.array([0, 1, 2, 3, 4, 5, 6, np.inf])
    ring_labels = ["0", "1", "2", "3", "4", "5", "\u22656"]
    _stack_counts(ax_b, _vals(locked, "rings"), _vals(expand, "rings"), ring_labels, ring_edges)
    _clean_ax(ax_b)
    ax_b.set_xlabel("rings")
    fs.panel(ax_b, "b", x=-0.14, y=1.12)

    # Observed C–F counts are {0,1,2,3,6}; the last bar is the single 6-bond molecule.
    cf_edges = np.array([0, 1, 2, 3, 4, np.inf])
    cf_labels = ["0", "1", "2", "3", "6"]
    _stack_counts(ax_c, _vals(locked, "cf"), _vals(expand, "cf"), cf_labels, cf_edges)
    _clean_ax(ax_c)
    ax_c.set_xlabel("C–F bonds")
    fs.panel(ax_c, "c", x=-0.14, y=1.12)

    n_edges = np.array([0, 1, 2, 3, 4, 5, np.inf])
    n_labels = ["0", "1", "2", "3", "4", "\u22655"]
    _stack_counts(ax_d, _vals(locked, "n"), _vals(expand, "n"), n_labels, n_edges)
    _clean_ax(ax_d)
    ax_d.set_xlabel("N atoms")
    fs.panel(ax_d, "d", x=-0.14, y=1.12)

    fig.legend(
        handles=[
            Patch(facecolor=fs.BLUE, edgecolor="none", label="locked"),
            Patch(facecolor=fs.SKY, edgecolor="none", label="expansion"),
        ],
        loc="upper center",
        ncol=2,
        bbox_to_anchor=(0.5, 1.06),
        frameon=False,
    )
    fs.finish(fig, pad=0.30, w_pad=0.70, h_pad=0.40, left=0.065, top=0.78)
    out.parent.mkdir(parents=True, exist_ok=True)
    fs.save(str(out), fig)
    plt.close(fig)
    print(f"wrote {out} and {out.with_suffix('.pdf')}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--spectro",
        default=None,
        help="spectro-agent checkout (default: SPECTRO_AGENT or /tmp/spectro-agent)",
    )
    ap.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parents[1] / "figures" / "fig_chemspace.png"),
    )
    args = ap.parse_args()
    root = _spectro_root(args.spectro)
    locked = load_locked(root)
    expand = load_expand_clean(root)
    if len(locked) != LOCKED_N or len(expand) != EXPAND_N:
        raise SystemExit(
            f"cohort size {len(locked)}+{len(expand)} != {LOCKED_N}+{EXPAND_N}"
        )
    if len(locked) + len(expand) != POOL_N:
        raise SystemExit("pooled n drifted")
    stats = caption_stats(locked, expand)
    print(json.dumps(stats, indent=2, sort_keys=True))
    draw(locked, expand, Path(args.out))


if __name__ == "__main__":
    main()
