#!/usr/bin/env python3
"""Offline NMRTrans baseline on the IRSpectra-Bench n=500 roster.

Same problems: molecular formula + printed 1H and 13C peak lists.
IR bands are not an NMRTrans input and are not converted into a spectrum.
No paid LLM API. Integrals, J values, carbon counts, and shift ranges are
taken only from the printed lists. Missing integrals stay 0 (not imputed
to 1H). 13C intensity inside NMRTrans is the repeat count of a shift,
using a printed nC annotation when the list gives one.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")

ROOT = Path("/tmp/bench")
NMRTRANS = Path("/tmp/NMRTrans")
ALL_ATOMS = ["B", "Br", "C", "Cl", "F", "H", "I", "N", "O", "P", "S", "Si"]
SPLIT_VOCAB = [
    "<unk>", "m", "d", "s", "dd", "t", "ddd", "q",
    "dt", "td", "br", "ddt", "dq", "tt", "quint",
    "dddd", "qd", "sept", "ddp", "ddq", "bd", "dqd",
]
SPLIT_TO_IDX = {tok: i for i, tok in enumerate(SPLIT_VOCAB)}
SPLIT_TOKENS = sorted((t for t in SPLIT_VOCAB if t != "<unk>"), key=len, reverse=True)
WORD_TO_SPLIT = {
    "multiplet": "m",
    "doublet": "d",
    "singlet": "s",
    "triplet": "t",
    "quartet": "q",
    "quintet": "quint",
    "broad": "br",
}


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def roster() -> list[dict]:
    main_clean = set(json.loads((ROOT / "data/benchmark_main/clean_qids.json").read_text()))
    cut = json.loads(
        (ROOT / "data/benchmark_expand_500/headline500_expand200_qids.json").read_text()
    )
    rows = []
    for cohort, path, keep in (
        ("locked-main", ROOT / "data/benchmark_main/questions2.jsonl", main_clean),
        ("locked-v3", ROOT / "data/benchmark_v3/questions2.jsonl", None),
        ("locked-v2ctrl", ROOT / "data/benchmark_v2_ctrl/questions2.jsonl", None),
        ("expand", ROOT / "data/benchmark_expand/questions2.jsonl", None),
        ("expand500", ROOT / "data/benchmark_expand_500/questions2.jsonl", set(cut)),
    ):
        for question in load_jsonl(path):
            if keep is not None and question["qid"] not in keep:
                continue
            item = dict(question)
            item["cohort"] = cohort
            item["uid"] = f"{cohort}:{question['qid']}"
            rows.append(item)
    if len(rows) != 500:
        raise SystemExit(f"expected 500 problems, got {len(rows)}")
    uids = [row["uid"] for row in rows]
    if len(set(uids)) != 500:
        raise SystemExit("uid collision")
    return rows


def _split_top_level(text: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    for char in text:
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        if char == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(char)
    if buf:
        parts.append("".join(buf))
    return parts


def _split_index(body: str) -> int:
    text = body.lower()
    if re.search(r"\b(?:broad|brs|bs)\b", text) or re.search(r"(?<![a-z])br(?![a-z])", text):
        return SPLIT_TO_IDX["br"]
    for word, tok in WORD_TO_SPLIT.items():
        if re.search(rf"\b{word}\b", text):
            return SPLIT_TO_IDX[tok]
    for tok in SPLIT_TOKENS:
        if re.search(rf"(?<![a-z]){re.escape(tok)}(?![a-z])", text):
            return SPLIT_TO_IDX[tok]
    return 0


def parse_h_nmr(text: str, stats: Counter) -> list[list]:
    if not isinstance(text, str):
        stats["h_nonstring"] += 1
        return []
    text = re.split(r"(?i)(?:;|\.)?\s*13\s*C\b", text, maxsplit=1)[0]
    peaks = []
    for chunk in _split_top_level(text):
        match = re.search(
            r"(-?\d+(?:\.\d+)?)\s*(?:[-–]\s*(-?\d+(?:\.\d+)?))?",
            chunk,
        )
        if not match:
            continue
        left = float(match.group(1))
        right = float(match.group(2)) if match.group(2) else None
        if right is None:
            shift, width = left, 0.0
        else:
            shift = (left + right) / 2.0
            width = abs(left - right) / 2.0
            stats["h_ranges"] += 1
        body = chunk[match.end():]
        paren = re.search(r"\((.*)\)", chunk)
        if paren:
            body = paren.group(1)
        integral_match = re.search(r"(\d+)\s*H\b", body, flags=re.I)
        if integral_match:
            integral = float(integral_match.group(1))
        else:
            integral = 0.0
            stats["h_integral_missing"] += 1
        j_match = re.search(r"J(?:CF)?\s*=\s*([^);]+)", body, flags=re.I)
        couplings = []
        if j_match:
            couplings = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", j_match.group(1))]
        if len(couplings) > 6:
            stats["h_j_truncated"] += 1
            couplings = couplings[:6]
        split_idx = _split_index(body)
        if split_idx == 0:
            stats["h_split_unk"] += 1
        peaks.append([shift, width, split_idx, integral, couplings])
        stats["h_peaks"] += 1
    if not peaks:
        stats["h_empty"] += 1
    return peaks


def parse_c_nmr(text: str, stats: Counter) -> list[float]:
    if not isinstance(text, str):
        stats["c_nonstring"] += 1
        return []
    shifts: list[float] = []
    pattern = re.compile(
        r"(-?\d+(?:\.\d+)?)\s*\(\s*(\d+)\s*C\b[^)]*\)"
        r"|(-?\d+(?:\.\d+)?)\s*\([^)]*\)"
        r"|(-?\d+(?:\.\d+)?)"
    )
    for match in pattern.finditer(text):
        if match.group(1) is not None:
            shift = float(match.group(1))
            count = int(match.group(2))
            stats["c_annotated"] += 1
            if count < 1 or count > 12:
                stats["c_count_capped"] += 1
                count = 1
            elif count > 1:
                stats["c_count_gt1"] += 1
        elif match.group(3) is not None:
            shift = float(match.group(3))
            count = 1
            stats["c_other_paren"] += 1
        else:
            shift = float(match.group(4))
            count = 1
            stats["c_bare"] += 1
        if shift < 0 or shift > 220:
            stats["c_clamped"] += 1
        shifts.extend([shift] * count)
        stats["c_lines"] += 1
    if not shifts:
        stats["c_empty"] += 1
    return shifts


def formula_vector(formula: str, stats: Counter):
    import torch

    counts: Counter = Counter()
    for atom, count in re.findall(r"([A-Z][a-z]?)(\d*)", formula or ""):
        counts[atom] += int(count) if count else 1
    outside = [atom for atom in counts if atom not in ALL_ATOMS]
    if outside:
        stats["formula_outside"] += 1
        stats["formula_outside_atoms"] += len(outside)
    vec = torch.zeros(len(ALL_ATOMS), dtype=torch.float)
    for atom, count in counts.items():
        if atom in ALL_ATOMS:
            vec[ALL_ATOMS.index(atom)] = float(count)
    return vec


def check_parse(rows: list[dict]) -> None:
    stats: Counter = Counter()
    for row in rows:
        h = parse_h_nmr(row.get("h_nmr") or "", stats)
        c = parse_c_nmr(row.get("c_nmr") or "", stats)
        formula_vector(row["formula"], stats)
        if len(h) > 60:
            stats["h_over_60"] += 1
        if len(c) > 60:
            stats["c_over_60"] += 1
    print(json.dumps(stats, indent=2, sort_keys=True))


def _pad_j(values: list[float]) -> list[float]:
    padded = [0.0] * 6
    for i, value in enumerate(values[:6]):
        padded[i] = float(value)
    return padded


def featurize(rows: list[dict]):
    import torch

    stats: Counter = Counter()
    batch = []
    for row in rows:
        h_peaks = parse_h_nmr(row.get("h_nmr") or "", stats)
        c_shifts = parse_c_nmr(row.get("c_nmr") or "", stats)
        h_feat = []
        for shift, width, split_idx, integral, couplings in h_peaks[:60]:
            h_feat.append([shift, width, split_idx, integral] + _pad_j(couplings))
        c_norm = []
        for shift in c_shifts[:60]:
            c_norm.append(min(1.0, max(0.0, shift / 220.0)))
        batch.append(
            {
                "uid": row["uid"],
                "qid": row["qid"],
                "cohort": row["cohort"],
                "formula": row["formula"],
                "difficulty": row.get("difficulty"),
                "h": h_feat,
                "c": c_norm,
                "formula_vector": formula_vector(row["formula"], stats),
                "n_h": len(h_peaks),
                "n_c": len(c_shifts),
            }
        )
    return batch, stats


def load_model():
    import torch

    sys.path.insert(0, str(NMRTRANS / "src"))
    from config import load_training_config, prepare_tokenizer
    from test import load_model as load_nmr_model
    import logging

    logging.basicConfig(level=logging.INFO)
    config = load_training_config(NMRTRANS / "configs/experiment_c_h_formula.yaml")
    tokenizer = prepare_tokenizer(config, logging.getLogger("nmrtrans"))
    ckpt = NMRTRANS / "checkpoints/pretrained/nmrtrans-c-h-nmr-formula.ckpt"
    model = load_nmr_model(config, tokenizer, str(ckpt), device=torch.device("cpu"), use_data_parallel=False)
    model.eval()
    return model, tokenizer


def tokens_to_smiles(model, tokenizer, tokens) -> str:
    text = model.tokens_to_smiles(tokens)
    return text.replace(" ", "")


def predict(rows: list[dict], out_path: Path, limit: int | None) -> None:
    import torch

    if limit is not None:
        rows = rows[:limit]
    feats, stats = featurize(rows)
    print("parse", json.dumps(stats, sort_keys=True), flush=True)
    model, tokenizer = load_model()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = 0
    t0 = time.time()
    with out_path.open("w") as handle, torch.inference_mode():
        for item in feats:
            c = item["c"]
            h = item["h"]
            c_tensor = torch.tensor(c, dtype=torch.float).view(1, -1, 1) if c else torch.zeros(1, 1, 1)
            c_mask = torch.ones(1, len(c), dtype=torch.long) if c else torch.zeros(1, 1, dtype=torch.long)
            if h:
                h_tensor = torch.tensor(h, dtype=torch.float).unsqueeze(0)
                h_mask = torch.ones(1, len(h), dtype=torch.long)
            else:
                h_tensor = torch.zeros(1, 1, 10)
                h_mask = torch.zeros(1, 1, dtype=torch.long)
            formula = item["formula_vector"].unsqueeze(0)
            started = time.time()
            beam_ids = model.generate(
                c_peaks=c_tensor,
                h_features=h_tensor,
                formula_vector=formula,
                c_nmr_mask=c_mask,
                h_nmr_mask=h_mask,
                num_beams=3,
                num_return_sequences=3,
                do_sample=False,
                max_length=82,
            )
            beam_ids = beam_ids.view(3, -1)
            candidates = []
            for seq in beam_ids:
                smiles = tokens_to_smiles(model, tokenizer, seq)
                if smiles and smiles not in candidates:
                    candidates.append(smiles)
            while len(candidates) < 3:
                candidates.append("")
            record = {
                "uid": item["uid"],
                "qid": item["qid"],
                "cohort": item["cohort"],
                "difficulty": item["difficulty"],
                "formula": item["formula"],
                "candidates": candidates[:3],
                "n_h_peaks": item["n_h"],
                "n_c_shifts": item["n_c"],
            }
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            done += 1
            elapsed = time.time() - started
            print(f"{done}/{len(feats)} {item['uid']} {elapsed:.1f}s {candidates[0][:80]}", flush=True)
    print(f"wrote {out_path} in {time.time()-t0:.1f}s", flush=True)


def ik14(smiles: str) -> str | None:
    if not smiles:
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return Chem.MolToInchiKey(mol)[:14]


def gold_index():
    import gzip
    from rdkit.Chem import rdMolDescriptors

    index = {}
    duplicates = set()
    path = ROOT / "data/irexp_resolved/irexp_resolved.jsonl.gz"
    with gzip.open(path, "rt") as handle:
        for line in handle:
            rec = json.loads(line)
            smiles = rec.get("smiles")
            if not smiles:
                continue
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                continue
            key = (
                rdMolDescriptors.CalcMolFormula(mol),
                tuple(rec.get("ir_bands_cm-1") or []),
                rec.get("c_nmr") or "",
            )
            if key in index:
                duplicates.add(key)
            else:
                index[key] = smiles
    return index, duplicates


def score(pred_path: Path, question_rows: list[dict], out_path: Path) -> None:
    preds = {row["uid"]: row for row in load_jsonl(pred_path)}
    index, duplicates = gold_index()
    cohorts = Counter()
    top1 = Counter()
    recall = Counter()
    invalid_top = Counter()
    formula_ok = Counter()
    missing_gold = []
    per = []
    for question in question_rows:
        uid = question["uid"]
        if uid not in preds:
            missing_gold.append(uid)
            continue
        key = (
            question["formula"],
            tuple(question.get("ir_bands_cm-1") or []),
            question.get("c_nmr") or "",
        )
        if key in duplicates or key not in index:
            missing_gold.append(uid)
            continue
        truth = ik14(index[key])
        cands = preds[uid].get("candidates") or []
        keys = [ik14(s) for s in cands[:3]]
        hit1 = bool(keys) and truth is not None and keys[0] == truth
        hitk = truth is not None and any(k == truth for k in keys if k)
        cohort = question["cohort"]
        group = "locked" if cohort.startswith("locked") else cohort
        for name in (group, "all"):
            cohorts[name] += 1
            top1[name] += int(hit1)
            recall[name] += int(hitk)
            invalid_top[name] += int(keys[0] is None) if keys else 1
            pred_mol = Chem.MolFromSmiles(cands[0]) if cands and cands[0] else None
            if pred_mol is not None:
                from rdkit.Chem import rdMolDescriptors
                formula_ok[name] += int(rdMolDescriptors.CalcMolFormula(pred_mol) == question["formula"])
        per.append({"uid": uid, "cohort": cohort, "top1": hit1, "recall": hitk})
    summary = {
        "n": cohorts["all"],
        "missing": missing_gold,
        "top1": dict(top1),
        "recall": dict(recall),
        "n_by": dict(cohorts),
        "invalid_top1": dict(invalid_top),
        "top1_formula_match": dict(formula_ok),
        "scoring": "RDKit InChIKey first 14 characters",
        "k": 3,
        "decoder": "beam search num_beams=3 num_return_sequences=3 do_sample=False",
        "checkpoint": "little1d/C-H-Formula nmrtrans-c-h-nmr-formula.ckpt",
        "code": "https://github.com/little1d/NMRTrans 9a72756532e60d540f05eafa93d31aecd1cb4362",
        "inputs": "formula + printed 1H (shift, range, multiplicity, integral, J) + 13C shifts; IR unused",
    }
    out_path.write_text(json.dumps(summary, indent=2) + "\n")
    (out_path.with_suffix(".hits.jsonl")).write_text("".join(json.dumps(row) + "\n" for row in per))
    print(json.dumps(summary, indent=2))


def main() -> None:
    global ROOT, NMRTRANS
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench-root", type=Path, default=ROOT)
    parser.add_argument("--nmrtrans-root", type=Path, default=NMRTRANS)
    parser.add_argument("--check-parse", action="store_true")
    parser.add_argument("--predict", type=Path)
    parser.add_argument("--score", type=Path)
    parser.add_argument("--scores-out", type=Path, default=Path("/tmp/bench/scores.json"))
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    ROOT = args.bench_root
    NMRTRANS = args.nmrtrans_root
    rows = roster()
    if args.check_parse:
        check_parse(rows)
        return
    if args.predict:
        predict(rows, args.predict, args.limit)
        return
    if args.score:
        score(args.score, rows, args.scores_out)
        return
    parser.error("choose --check-parse, --predict, or --score")


if __name__ == "__main__":
    main()
