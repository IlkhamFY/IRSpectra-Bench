#!/usr/bin/env python3
"""Re-score the n=500 headline as thinking-tier 200 vs earlier no-thinking 300.

Generation uses the deposited candidate lists and the InChIKey-14 contract
(first 14 characters of the RDKit InChIKey). Expansion gold is reconstructed
in memory by a unique (formula, IR band tuple, 13C string) match against
irexp_resolved. Nothing in the answer key is written.

Locked 194 answers and raw predictions live on spectro-agent main.
Expansion questions and predictions live on
spectro-agent cursor/expand-bench-500-b78b (not on main).

  python scripts/exp_split_thinking.py \
      --spectro /path/to/spectro-agent \
      --expand /path/to/expand-extract \
      --out-dir results
"""
from __future__ import annotations

import argparse
import csv
import glob
import gzip
import json
import sys
from pathlib import Path

from rdkit import Chem, RDLogger
from rdkit.Chem import rdMolDescriptors

RDLogger.DisableLog("rdApp.*")

# Deposited fverify arm counts (spectro-agent data/fverify_n500/wall.json,
# branch cursor/fverify-n500-unify-629c @ 473030fb). Not recomputed here:
# committed candidates.jsonl still omit is_true, and this script does not
# re-run the chamfer ranker.
FVERIFY_ARMS = {
    "locked_194": {"n": 194, "verified": 58, "misranked": 7, "never": 129},
    "plus_106": {"n": 106, "verified": 56, "misranked": 12, "never": 38},
    "thinking_200": {"n": 200, "verified": 90, "misranked": 26, "never": 84},
    "headline_500": {"n": 500, "verified": 204, "misranked": 45, "never": 251},
}


def ik14(smiles: str | None) -> str | None:
    mol = Chem.MolFromSmiles(smiles) if smiles else None
    if mol is None:
        return None
    return Chem.MolToInchiKey(mol)[:14]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def gold_index(path: Path) -> tuple[dict, set]:
    index: dict[tuple, dict] = {}
    dups: set = set()
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
                dups.add(key)
            else:
                index[key] = rec
    return index, dups


def score_cands(true_smiles: str, cands: list) -> tuple[bool, bool, str | None]:
    truth = ik14(true_smiles)
    ranked = list(cands or [])[:3]
    top1 = bool(ranked) and truth is not None and ik14(ranked[0]) == truth
    recall = truth is not None and any(ik14(s) == truth for s in ranked)
    return top1, recall, truth


def load_locked(spectro: Path) -> list[dict]:
    answers = {
        json.loads(line)["qid"]: json.loads(line)
        for line in open(spectro / "data/benchmark_main/answers2.jsonl")
    }
    clean = set(json.loads((spectro / "data/benchmark_main/clean_qids.json").read_text()))
    pred: dict = {}
    for path in glob.glob(str(spectro / "data/benchmark_main/raw/*.json")):
        try:
            pred.update(json.loads(Path(path).read_text()))
        except Exception:
            continue
    rows = []
    for qid, ans in answers.items():
        if qid not in clean:
            continue
        cands = pred.get(f"M-{qid}")
        if cands is None:
            sys.exit(f"locked main missing prediction M-{qid}")
        top1, recall, key = score_cands(ans["smiles"], cands)
        rows.append(
            {
                "slice": "locked_194",
                "qid": qid,
                "difficulty": ans.get("difficulty"),
                "top1": int(top1),
                "recall": int(recall),
                "ik14": key,
            }
        )
    for sub, tag in (("benchmark_v3", "v3"), ("benchmark_v2_ctrl", "v2ctrl")):
        ans_map = {
            json.loads(line)["qid"]: json.loads(line)
            for line in open(spectro / f"data/{sub}/answers2.jsonl")
        }
        pred_map = {
            json.loads(line)["qid"]: json.loads(line)
            for line in open(spectro / f"data/{sub}/predictions2.jsonl")
        }
        for qid, ans in ans_map.items():
            top1, recall, key = score_cands(ans["smiles"], pred_map[qid].get("candidates", []))
            rows.append(
                {
                    "slice": "locked_194",
                    "qid": f"{tag}:{qid}",
                    "difficulty": ans.get("difficulty"),
                    "top1": int(top1),
                    "recall": int(recall),
                    "ik14": key,
                }
            )
    if len(rows) != 194:
        sys.exit(f"locked cohort is {len(rows)}, expected 194")
    return rows


def load_expansion(expand: Path, round_name: str, slice_name: str, index: dict, dups: set) -> list[dict]:
    questions = load_jsonl(expand / round_name / "questions2.jsonl")
    predictions = {row["qid"]: row for row in load_jsonl(expand / round_name / "predictions2.jsonl")}
    rows = []
    for question in questions:
        qid = question["qid"]
        key = (
            question["formula"],
            tuple(question.get("ir_bands_cm-1") or []),
            question.get("c_nmr") or "",
        )
        if key in dups:
            sys.exit(f"ambiguous gold match {slice_name} {qid}")
        rec = index.get(key)
        if rec is None:
            sys.exit(f"no gold match {slice_name} {qid}")
        if qid not in predictions:
            sys.exit(f"missing prediction {slice_name} {qid}")
        top1, recall, ik = score_cands(rec["smiles"], predictions[qid].get("candidates", []))
        rows.append(
            {
                "slice": slice_name,
                "qid": qid,
                "difficulty": question.get("difficulty"),
                "top1": int(top1),
                "recall": int(recall),
                "ik14": ik,
            }
        )
    return rows


def summarise(rows: list[dict]) -> dict:
    n = len(rows)
    top1 = sum(r["top1"] for r in rows)
    recall = sum(r["recall"] for r in rows)
    out = {
        "n": n,
        "top1": top1,
        "recall": recall,
        "top1_pct": round(100 * top1 / n, 1) if n else None,
        "recall_pct": round(100 * recall / n, 1) if n else None,
        "gen_top1": top1,
        "gen_recalled_not_top1": recall - top1,
        "gen_never": n - recall,
        "self_rank": f"{top1}/{recall}" if recall else None,
    }
    for diff in ("simple", "complex"):
        sub = [r for r in rows if r["difficulty"] == diff]
        out[f"{diff}_n"] = len(sub)
        out[f"{diff}_top1"] = sum(r["top1"] for r in sub)
        out[f"{diff}_recall"] = sum(r["recall"] for r in sub)
    return out


def attach_fverify(name: str, stats: dict) -> dict:
    arm = FVERIFY_ARMS.get(name)
    stats = dict(stats)
    if arm is None:
        stats["fverify_source"] = "not_recomputed"
        return stats
    if arm["n"] != stats["n"]:
        sys.exit(f"fverify n mismatch for {name}: {arm['n']} vs {stats['n']}")
    if arm["verified"] + arm["misranked"] != stats["recall"]:
        sys.exit(
            f"fverify recall mismatch for {name}: "
            f"{arm['verified']}+{arm['misranked']} vs generation {stats['recall']}"
        )
    if arm["never"] != stats["gen_never"]:
        sys.exit(f"fverify never mismatch for {name}")
    stats["fverify_verified"] = arm["verified"]
    stats["fverify_misranked"] = arm["misranked"]
    stats["fverify_never"] = arm["never"]
    stats["fverify_source"] = "summed_from_deposited_wall_json_not_rerun"
    return stats


def earlier_fverify() -> dict:
    a, b = FVERIFY_ARMS["locked_194"], FVERIFY_ARMS["plus_106"]
    return {
        "n": a["n"] + b["n"],
        "verified": a["verified"] + b["verified"],
        "misranked": a["misranked"] + b["misranked"],
        "never": a["never"] + b["never"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spectro", type=Path, default=Path("/tmp/spectro-agent"))
    parser.add_argument("--expand", type=Path, default=Path("/tmp/deposits/data"))
    parser.add_argument("--qids", type=Path, default=Path("docs/headline500_expand200_qids.json"))
    parser.add_argument("--out-dir", type=Path, default=Path("results"))
    args = parser.parse_args()

    index, dups = gold_index(args.spectro / "data/irexp_resolved/irexp_resolved.jsonl.gz")
    locked = load_locked(args.spectro)
    plus = load_expansion(args.expand, "benchmark_expand", "plus_106", index, dups)
    expand = load_expansion(args.expand, "benchmark_expand_500", "expand500", index, dups)
    if len(plus) != 106:
        sys.exit(f"+106 is {len(plus)}, expected 106")
    if len(expand) != 230:
        sys.exit(f"expand-500 is {len(expand)}, expected 230")

    cut_qids = json.loads(args.qids.read_text())
    if len(cut_qids) != 200 or len(set(cut_qids)) != 200:
        sys.exit("headline 200 qid list is not 200 unique ids")
    clean = json.loads((args.expand / "benchmark_expand_500/clean_qids.json").read_text())
    if cut_qids != sorted(clean)[:200]:
        sys.exit("qid file is not the validate-clean string-sort prefix of 200")
    thinking = []
    have = {row["qid"]: row for row in expand}
    for qid in cut_qids:
        if qid not in have:
            sys.exit(f"thinking cut missing {qid}")
        row = dict(have[qid])
        row["slice"] = "thinking_200"
        thinking.append(row)

    ik_locked = {r["ik14"] for r in locked}
    ik_plus = {r["ik14"] for r in plus}
    ik_expand = {r["ik14"] for r in expand}
    if None in ik_locked or None in ik_plus or None in ik_expand:
        sys.exit("null InChIKey-14 in a gold structure")
    collisions = {
        "locked_vs_plus": len(ik_locked & ik_plus),
        "locked_vs_expand500": len(ik_locked & ik_expand),
        "plus_vs_expand500": len(ik_plus & ik_expand),
    }
    if any(collisions.values()):
        sys.exit(f"InChIKey-14 collisions: {collisions}")

    earlier = locked + plus
    headline = earlier + thinking
    slices = {
        "locked_194": summarise(locked),
        "plus_106": summarise(plus),
        "earlier_300": summarise(earlier),
        "thinking_200": summarise(thinking),
        "headline_500": summarise(headline),
        "expand500_all_230": summarise(expand),
        "expand500_clean_224": summarise([r for r in expand if r["qid"] in set(clean)]),
    }
    for name in ("locked_194", "plus_106", "thinking_200", "headline_500"):
        slices[name] = attach_fverify(name, slices[name])
    fw = earlier_fverify()
    if fw["n"] != slices["earlier_300"]["n"]:
        sys.exit("earlier-300 fverify n mismatch")
    if fw["verified"] + fw["misranked"] != slices["earlier_300"]["recall"]:
        sys.exit("earlier-300 fverify recall does not match recomputed generation")
    if fw["never"] != slices["earlier_300"]["gen_never"]:
        sys.exit("earlier-300 fverify never does not match recomputed generation")
    slices["earlier_300"]["fverify_verified"] = fw["verified"]
    slices["earlier_300"]["fverify_misranked"] = fw["misranked"]
    slices["earlier_300"]["fverify_never"] = fw["never"]
    slices["earlier_300"]["fverify_source"] = "sum_of_deposited_locked_194_and_plus_106_arms"

    # Locked headline identity. Do not publish a split that fails this check.
    h = slices["headline_500"]
    if (h["top1"], h["recall"], h["n"]) != (227, 249, 500):
        sys.exit(f"headline drifted: {h['top1']}/{h['n']} top-1, {h['recall']}/{h['n']} recall")
    if slices["earlier_300"]["top1"] + slices["thinking_200"]["top1"] != 227:
        sys.exit("200+300 top-1 does not add to 227")
    if slices["earlier_300"]["recall"] + slices["thinking_200"]["recall"] != 249:
        sys.exit("200+300 recall does not add to 249")

    payload = {
        "scoring": "RDKit InChIKey first 14 characters; up to 3 ranked candidates",
        "gold": (
            "locked 194 from committed answers2.jsonl; "
            "expansion gold reconstructed in memory by unique "
            "(formula, ir_bands_cm-1, c_nmr) match to irexp_resolved.jsonl.gz; "
            "answers not written"
        ),
        "match": {
            "plus_106": "106/106 unique",
            "expand500": "230/230 unique",
            "duplicate_keys_hit": 0,
            "inchikey14_collisions": collisions,
        },
        "thinking_cut": "validate-clean expand-500 qids, Python sorted(), first 200 (R01–R75)",
        "protocol": {
            "earlier_300": "locked 194 + all 106; no-thinking consumer",
            "thinking_200": "expand-500 cut; thinking-tier consumer",
        },
        "fverify_note": (
            "Forward-verify counts are the deposited arm table, summed. "
            "Chamfer was not re-run. Generation top-1 / recall were re-run."
        ),
        "slices": slices,
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "exp_split_thinking.json").write_text(json.dumps(payload, indent=2) + "\n")

    fields = [
        "slice", "n", "top1", "top1_pct", "recall", "recall_pct",
        "gen_top1", "gen_recalled_not_top1", "gen_never",
        "fverify_verified", "fverify_misranked", "fverify_never",
        "simple_n", "simple_top1", "simple_recall",
        "complex_n", "complex_top1", "complex_recall",
    ]
    with (args.out_dir / "exp_split_thinking.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for name, stats in slices.items():
            writer.writerow({"slice": name, **stats})

    with (args.out_dir / "exp_split_thinking_per_qid.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["slice", "qid", "difficulty", "top1", "recall"]
        )
        writer.writeheader()
        for row in earlier + thinking:
            writer.writerow({k: row[k] for k in writer.fieldnames})

    e, t = slices["earlier_300"], slices["thinking_200"]
    print(
        f"earlier_300 top1 {e['top1']}/{e['n']} recall {e['recall']}/{e['n']} "
        f"gen {e['gen_top1']}/{e['gen_recalled_not_top1']}/{e['gen_never']} "
        f"fverify {e['fverify_verified']}/{e['fverify_misranked']}/{e['fverify_never']}"
    )
    print(
        f"thinking_200 top1 {t['top1']}/{t['n']} recall {t['recall']}/{t['n']} "
        f"gen {t['gen_top1']}/{t['gen_recalled_not_top1']}/{t['gen_never']} "
        f"fverify {t['fverify_verified']}/{t['fverify_misranked']}/{t['fverify_never']}"
    )
    print(f"headline check {h['top1']}/{h['n']} {h['recall']}/{h['n']}")


if __name__ == "__main__":
    main()
