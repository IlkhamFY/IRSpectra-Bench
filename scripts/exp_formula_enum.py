#!/usr/bin/env python3
"""Formula-constrained constitutional enumeration on a declared subset.

Generator: MAYGEN 1.8 (orderly generation). Input to the generator is the
question formula only. Top-1, when the set is small enough to rank, is the
isomer with the lowest symmetric chamfer between the deposited nmrshiftdb
GNN 13C predictor and the printed 13C peak list. Scoring of the true
structure is RDKit InChIKey-14, same contract as the headline.

Declared attempt, fixed before any hit/miss was read:
  heavy-atom count <= 12 on the n=500 headline.
Pilot (same VM, 30s, partial files discarded):
  C6H13NO2 (HA 9) and C9H16O (HA 10) exhausted.
  C7H10O4 (HA 11), C10H18O2 (HA 12), C9H9ClO3S (HA 14),
  C12H10FNO (HA 15), C10H8Br4O2 (HA 16) each passed 5e5 structures
  without exhausting. HA>12 is not attempted. That exclusion is the
  whole denominator statement, not a silent drop inside the attempt.

Timeouts inside HA<=12 stay in the denominator as misses.
Gold is rebuilt in memory and not written.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from rdkit import Chem, RDLogger
from rdkit.Chem import rdMolDescriptors

RDLogger.DisableLog("rdApp.*")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp_split_thinking import gold_index, ik14, load_jsonl  # noqa: E402

ELEM = re.compile(r"([A-Z][a-z]?)(\d*)")
MAX_HA = 12
TIMEOUT_S = 45
RANK_CAP = 80000


def heavy_atoms(formula: str) -> int | None:
    if any(ch in formula for ch in ".+-"):
        return None
    atoms: dict[str, int] = {}
    for el, n in ELEM.findall(formula):
        atoms[el] = atoms.get(el, 0) + (int(n) if n else 1)
    if not atoms:
        return None
    return sum(v for k, v in atoms.items() if k != "H")


def obs_c13(text: str | None) -> list[float]:
    hits = [float(x) for x in re.findall(r"(-?\d+\.?\d*)\s*\(", text or "")]
    if hits:
        return hits
    return [float(x) for x in re.findall(r"-?\d+\.\d+", text or "")]


def load_gnn(spectro: Path):
    spec = importlib.util.spec_from_file_location(
        "gnn_predict", spectro / "scripts" / "gnn_predict.py"
    )
    if spec is None or spec.loader is None:
        sys.exit(f"cannot load {spectro / 'scripts' / 'gnn_predict.py'}")
    module = importlib.util.module_from_spec(spec)
    # MODEL path inside gnn_predict is relative to the spectro checkout.
    sys.path.insert(0, str(spectro / "scripts"))
    cwd = Path.cwd()
    try:
        import os

        os.chdir(spectro)
        spec.loader.exec_module(module)
    finally:
        os.chdir(cwd)
    return module


def cohort(spectro: Path, expand: Path, qids: Path) -> list[dict]:
    index, dups = gold_index(spectro / "data/irexp_resolved/irexp_resolved.jsonl.gz")
    rows = []

    def add(slice_name: str, qid: str, question: dict, smiles: str, difficulty: str | None):
        rows.append(
            {
                "slice": slice_name,
                "qid": qid,
                "formula": question["formula"],
                "difficulty": difficulty or question.get("difficulty"),
                "obs": obs_c13(question.get("c_nmr")),
                "ik14": ik14(smiles),
                "ha": heavy_atoms(question["formula"]),
            }
        )

    answers = {
        json.loads(line)["qid"]: json.loads(line)
        for line in open(spectro / "data/benchmark_main/answers2.jsonl")
    }
    questions = {
        json.loads(line)["qid"]: json.loads(line)
        for line in open(spectro / "data/benchmark_main/questions2.jsonl")
    }
    clean = set(json.loads((spectro / "data/benchmark_main/clean_qids.json").read_text()))
    for qid, ans in answers.items():
        if qid not in clean:
            continue
        add("locked_194", qid, questions[qid], ans["smiles"], ans.get("difficulty"))
    for sub, tag in (("benchmark_v3", "v3"), ("benchmark_v2_ctrl", "v2ctrl")):
        amap = {
            json.loads(line)["qid"]: json.loads(line)
            for line in open(spectro / f"data/{sub}/answers2.jsonl")
        }
        qmap = {
            json.loads(line)["qid"]: json.loads(line)
            for line in open(spectro / f"data/{sub}/questions2.jsonl")
        }
        for qid, ans in amap.items():
            add("locked_194", f"{tag}:{qid}", qmap[qid], ans["smiles"], ans.get("difficulty"))

    def add_expansion(round_name: str, slice_name: str, keep: set[str] | None):
        qs = load_jsonl(expand / round_name / "questions2.jsonl")
        for question in qs:
            qid = question["qid"]
            if keep is not None and qid not in keep:
                continue
            key = (
                question["formula"],
                tuple(question.get("ir_bands_cm-1") or []),
                question.get("c_nmr") or "",
            )
            if key in dups or key not in index:
                sys.exit(f"gold match failed {slice_name} {qid}")
            add(slice_name, qid, question, index[key]["smiles"], question.get("difficulty"))

    add_expansion("benchmark_expand", "plus_106", None)
    cut = set(json.loads(qids.read_text()))
    add_expansion("benchmark_expand_500", "thinking_200", cut)
    if len(rows) != 500:
        sys.exit(f"cohort {len(rows)} != 500")
    if any(r["ik14"] is None for r in rows):
        sys.exit("null gold key")
    return rows


def run_maygen(jar: Path, formula: str, outdir: Path) -> tuple[str, Path | None, str]:
    outdir.mkdir(parents=True, exist_ok=True)
    smi = outdir / f"{formula}.smi"
    if smi.exists():
        smi.unlink()
    try:
        proc = subprocess.run(
            ["java", "-jar", str(jar), "-f", formula, "-smi", "-t", "-o", str(outdir)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        if smi.exists():
            smi.unlink()
        return "timeout", None, ""
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    if "does not represent" in text or "user defined element" in text or not smi.exists():
        if smi.exists():
            smi.unlink()
        return "unsupported", None, text.strip().splitlines()[-1] if text.strip() else ""
    if proc.returncode != 0:
        if smi.exists():
            smi.unlink()
        return "error", None, text[-300:]
    return "complete", smi, ""


def read_isomers(path: Path) -> dict:
    """Stream a finished MAYGEN file. Rank only when the unique set is small."""
    smiles_for_key: dict[str, str] = {}
    n_lines = 0
    n_bad = 0
    for line in path.open():
        smi = line.strip()
        if not smi:
            continue
        n_lines += 1
        if len(smiles_for_key) > RANK_CAP:
            # Still count the rest for the size, but do not keep structures.
            # Recall on an unread tail would be a silent subsample, so stop
            # and mark the formula unranked and unscored.
            for _ in path.open():
                pass
            return {
                "status": "complete_unranked",
                "n_smiles": n_lines,
                "n_unique_ik14": None,
                "note": f"unique InChIKey-14 exceeded {RANK_CAP}; not scored",
            }
        key = ik14(smi)
        if key is None:
            n_bad += 1
            continue
        smiles_for_key.setdefault(key, smi)
    return {
        "status": "complete",
        "n_smiles": n_lines,
        "n_unique_ik14": len(smiles_for_key),
        "n_unparsed": n_bad,
        "smiles_for_key": smiles_for_key,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spectro", type=Path, default=Path("/tmp/spectro-agent"))
    parser.add_argument("--expand", type=Path, default=Path("/tmp/deposits/data"))
    parser.add_argument("--qids", type=Path, default=Path("docs/headline500_expand200_qids.json"))
    parser.add_argument("--jar", type=Path, default=Path("/tmp/MAYGEN-1.8.jar"))
    parser.add_argument("--work", type=Path, default=Path("/tmp/maygen_bench"))
    parser.add_argument("--out-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    if not args.jar.is_file():
        sys.exit(f"missing MAYGEN jar: {args.jar}")
    if shutil.which("java") is None:
        sys.exit("java not on PATH")

    rows = cohort(args.spectro, args.expand, args.qids)
    attempted = [r for r in rows if r["ha"] is not None and r["ha"] <= MAX_HA]
    skipped = [r for r in rows if r not in attempted]
    print(
        f"declared attempt HA<={MAX_HA}: {len(attempted)} compounds, "
        f"{len({r['formula'] for r in attempted})} formulas; "
        f"not attempted {len(skipped)}",
        flush=True,
    )
    gnn = load_gnn(args.spectro)
    gnn.MODEL = str(args.spectro / "data/nmrshiftdb/gnn_c13.pt")
    by_formula: dict[str, list[dict]] = {}
    for row in attempted:
        by_formula.setdefault(row["formula"], []).append(row)

    cache: dict[str, dict] = {}
    for i, (formula, members) in enumerate(sorted(by_formula.items()), 1):
        status, smi, note = run_maygen(args.jar, formula, args.work)
        print(f"[{i}/{len(by_formula)}] {formula} gen={status} {note[:80]}", flush=True)
        if status != "complete" or smi is None:
            cache[formula] = {"status": status, "note": note[:200]}
            continue
        parsed = read_isomers(smi)
        smi.unlink()
        print(
            f"    unique={parsed.get('n_unique_ik14')} smiles={parsed.get('n_smiles')} "
            f"read={parsed['status']}",
            flush=True,
        )
        cache[formula] = parsed
        _ = members

    per_qid = []
    for row in attempted:
        info = cache[row["formula"]]
        status = info["status"]
        rec = {
            "slice": row["slice"],
            "qid": row["qid"],
            "formula": row["formula"],
            "ha": row["ha"],
            "difficulty": row["difficulty"],
            "n_obs_c13": len(row["obs"]),
            "status": status,
            "n_unique_ik14": info.get("n_unique_ik14"),
            "recall": 0,
            "top1": 0,
            "gnn_top3": 0,
            "ranked": 0,
        }
        smiles_for_key = info.get("smiles_for_key") or {}
        if status == "complete" and smiles_for_key:
            rec["recall"] = int(row["ik14"] in smiles_for_key)
            if row["obs"]:
                ranked = []
                for key, smi in smiles_for_key.items():
                    pred = gnn.predict_c13(smi)
                    ranked.append((gnn.chamfer(pred, row["obs"]), key))
                ranked.sort()
                rec["ranked"] = 1
                rec["top1"] = int(bool(ranked) and ranked[0][1] == row["ik14"])
                rec["gnn_top3"] = int(row["ik14"] in {k for _, k in ranked[:3]})
            else:
                rec["status"] = "complete_unranked"
                rec["top1"] = ""
                rec["gnn_top3"] = ""
        elif status == "complete":
            rec["recall"] = 0
            rec["top1"] = 0
        elif status == "complete_unranked":
            rec["recall"] = ""
            rec["top1"] = ""
            rec["gnn_top3"] = ""
        per_qid.append(rec)
        # Drop the heavy maps from being reused incorrectly — fine to keep.

    # Free SMILES before writing. Keys stay until summary.
    for info in cache.values():
        info.pop("smiles_for_key", None)
        info.pop("keys", None)

    def count(pred):
        return sum(1 for r in per_qid if pred(r))

    summary = {
        "generator": "MAYGEN 1.8",
        "jar_note": "github.com/MehmetAzizYirik/MAYGEN release V1.8",
        "ranker": "spectro-agent data/nmrshiftdb/gnn_c13.pt chamfer vs printed 13C",
        "scoring": "RDKit InChIKey-14",
        "max_heavy_atoms": MAX_HA,
        "timeout_s": TIMEOUT_S,
        "rank_cap": RANK_CAP,
        "headline_n": 500,
        "attempted_n": len(attempted),
        "not_attempted_n": len(skipped),
        "not_attempted_reason": (
            "HA>12 or charged formula. Pilots at HA 11–16 did not exhaust "
            "within 30s (each >5e5 structures). Not a scored subsample of those."
        ),
        "n_complete": count(lambda r: r["status"] == "complete"),
        "n_timeout": count(lambda r: r["status"] == "timeout"),
        "n_unsupported": count(lambda r: r["status"] == "unsupported"),
        "n_unscored": count(lambda r: r["status"] == "complete_unranked"),
        "n_ranked": count(lambda r: r["ranked"] == 1),
        "recall_hits": count(lambda r: r["recall"] == 1),
        "top1_hits": count(lambda r: r["top1"] == 1),
        "gnn_top3_hits": count(lambda r: r["gnn_top3"] == 1),
        "denominator": "attempted_n (timeouts and unsupported stay in)",
    }
    # complete-only recall, stated separately
    complete = [r for r in per_qid if r["status"] == "complete"]
    summary["complete_n"] = len(complete)
    summary["recall_on_complete"] = sum(r["recall"] == 1 for r in complete)
    summary["top1_on_ranked"] = summary["top1_hits"]
    summary["ranked_n"] = summary["n_ranked"]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "exp_formula_enum.json").write_text(json.dumps(summary, indent=2) + "\n")
    fields = [
        "slice", "qid", "formula", "ha", "difficulty", "n_obs_c13", "status",
        "n_unique_ik14", "recall", "top1", "gnn_top3", "ranked",
    ]
    with (args.out_dir / "exp_formula_enum_per_qid.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(per_qid)
    with (args.out_dir / "exp_formula_enum.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
