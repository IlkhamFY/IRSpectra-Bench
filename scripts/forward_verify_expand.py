#!/usr/bin/env python3
"""Expansion-round forward-verify (scripted GNN 13C chamfer).

SNAPSHOT for the IRSpectra-Bench postcard repo. Run this from a spectro-agent
checkout that has data/benchmark_expand/ + data/nmrshiftdb/gnn_c13.pt +
scripts/gnn_predict.py (branches claude/funny-maxwell-u5S31 or
cursor/pooled-headline-b966). This postcard copy is for review; it does not
bundle the expansion key or candidate SMILES.

The locked n=194 LLM campaign (data/fverify + data/fverify_main) was never run
on the 106-compound expansion. This script does the feasible, training-free
substitute that already exists for the locked slice:

  * reconstruct the withheld expansion key under /tmp (same unique
    (formula, IR, 13C) match as scripts/score_pooled.py; never writes
    answers2.jsonl into the working tree)
  * build the candidate pool from committed predictions2.jsonl
  * re-rank by symmetric chamfer(GNN-predicted 13C, observed 13C)
  * emit diagnosis counts analogous to the 58/7/129 locked-slice wall

The GNN is the same nmrshiftdb2 checkpoint already reported as 59/65 (91%)
on the locked recall set vs the LLM verifier's 58/65 (89%). Those are
NOT interchangeable with an LLM expansion campaign. This script labels
every number as GNN-scripted.

  python scripts/forward_verify_expand.py           # reconstruct + GNN score
  python scripts/forward_verify_expand.py prep      # also write LLM batch stubs
  python scripts/forward_verify_expand.py score     # GNN score only (key must exist)
  python scripts/forward_verify_expand.py score --llm
        # score from data/fverify_expand/raw/*.json if an LLM campaign is deposited;
        # refuses (no invented numbers) when raw/ is empty

Public artefacts (no structures / no is_true):
  data/fverify_expand/diagnosis.json
  data/fverify_expand/fbatch_*.txt   (anon SMILES only; optional prep)
"""
from __future__ import annotations

import gzip
import json
import random
import re
import sys
from collections import defaultdict
from math import comb
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if not (_ROOT / "data" / "benchmark_expand" / "predictions2.jsonl").exists():
    _sidecar = _ROOT / "data" / "fverify_expand" / "diagnosis.json"
    raise SystemExit(
        "forward_verify_expand.py must be run from a spectro-agent checkout "
        "(data/benchmark_expand/ missing).\n"
        f"Frozen GNN-scripted counts are in {_sidecar} "
        "(45/23/38; not LLM fverify). See docs/EXPANSION_FVERIFY_2026-09-19.md.\n"
        "LLM campaign blocker: 301 unique SMILES, 0 locked-deposit overlap, "
        "18 Opus batches. Do not invent an LLM wall."
    )

from rdkit import Chem
from rdkit import RDLogger
from rdkit.Chem import rdMolDescriptors

RDLogger.DisableLog("rdApp.*")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gnn_predict  # noqa: E402

EXPAND = Path("data/benchmark_expand")
QUESTIONS = EXPAND / "questions2.jsonl"
PREDS = EXPAND / "predictions2.jsonl"
CLEAN = EXPAND / "clean_qids.json"
GOLD = Path("data/irexp_resolved/irexp_resolved.jsonl.gz")
VAULT = Path("/tmp/blind/_key/benchmark_expand.answers2.jsonl.withheld")
OUT = Path("data/fverify_expand")
SIDECAR = OUT / "diagnosis.json"
FLAGGED = ("R12", "R22", "R25", "R82", "R91")
BATCH = 17
SEED = 13  # distinct from locked-arm seeds (5, 11)


def obs_c13(c_nmr):
    return [float(x) for x in re.findall(r"(-?\d+\.?\d*)\s*\(", c_nmr or "")]


def ik14(smi):
    m = Chem.MolFromSmiles(smi) if smi else None
    return Chem.MolToInchiKey(m)[:14] if m else None


def canon(smi):
    m = Chem.MolFromSmiles(smi) if smi else None
    return Chem.MolToSmiles(m) if m else None


def chamfer(pred, obs):
    if not pred or not obs:
        return 999.0
    a = sum(min(abs(p - o) for o in obs) for p in pred) / len(pred)
    b = sum(min(abs(o - p) for p in pred) for o in obs) / len(obs)
    return (a + b) / 2


def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    lo = min(b, c)
    tail = sum(comb(n, k) for k in range(0, lo + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def _norm_bands(bands):
    return tuple(round(float(x), 4) for x in (bands or []))


def reconstruct_expand_key(dest: Path) -> list[dict]:
    """Unique match of each committed question against irexp_resolved."""
    qs = [json.loads(l) for l in QUESTIONS.open()]
    preds = {json.loads(l)["qid"] for l in PREDS.open()}
    if {q["qid"] for q in qs} != preds:
        raise SystemExit("questions2.jsonl qids do not match predictions2.jsonl")

    seen_prior = set()
    for af in Path("data").glob("benchmark*/answers*.jsonl"):
        if af.resolve() == dest.resolve():
            continue
        for line in af.open():
            seen_prior.add(json.loads(line)["inchikey"][:14])

    index = {}
    collisions = 0
    for line in gzip.open(GOLD, "rt"):
        r = json.loads(line)
        smi = r.get("smiles")
        if not (smi and r.get("c_nmr") and r.get("ir_bands_cm-1")):
            continue
        m = Chem.MolFromSmiles(smi)
        if m is None:
            continue
        formula = rdMolDescriptors.CalcMolFormula(m)
        key = (formula, _norm_bands(r["ir_bands_cm-1"]), r["c_nmr"])
        rec = {
            "smiles": Chem.MolToSmiles(m),
            "inchikey": r.get("inchikey") or Chem.MolToInchiKey(m),
            "heavy_atoms": m.GetNumHeavyAtoms(),
            "source_doi": r.get("source_doi"),
        }
        if key in index and index[key]["inchikey"][:14] != rec["inchikey"][:14]:
            collisions += 1
            index[key] = None
        elif key not in index:
            index[key] = rec

    rows = []
    unmatched, ambiguous = [], []
    for q in qs:
        key = (q["formula"], _norm_bands(q["ir_bands_cm-1"]), q["c_nmr"])
        rec = index.get(key)
        if rec is None:
            (ambiguous if key in index else unmatched).append(q["qid"])
            continue
        ik = rec["inchikey"][:14]
        if ik in seen_prior:
            raise SystemExit(f"{q['qid']}: reconstructed InChIKey-14 collides with a prior round")
        rows.append({
            "qid": q["qid"],
            "smiles": rec["smiles"],
            "inchikey": rec["inchikey"],
            "difficulty": q["difficulty"],
            "heavy_atoms": rec["heavy_atoms"],
            "source_doi": rec.get("source_doi"),
        })

    if unmatched or ambiguous:
        raise SystemExit(f"key reconstruction failed: unmatched={unmatched} ambiguous={ambiguous}")
    if len(rows) != 106:
        raise SystemExit(f"expected 106 reconstructed answers, got {len(rows)}")
    n_simple = sum(1 for r in rows if r["difficulty"] == "simple")
    if n_simple != 53:
        raise SystemExit(f"strata drifted: simple={n_simple} (want 53)")

    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"reconstructed {len(rows)} answers -> {dest}  "
          f"(gold-index collisions skipped: {collisions})")
    return rows


def load_key() -> list[dict]:
    if (EXPAND / "answers2.jsonl").exists():
        raise SystemExit("data/benchmark_expand/answers2.jsonl is in the working tree; "
                         "withhold it. This script reads the vault only.")
    if VAULT.exists():
        rows = [json.loads(l) for l in VAULT.open()]
        print(f"using existing key at {VAULT} ({len(rows)} rows)")
        return rows
    return reconstruct_expand_key(VAULT)


def build_candidates(answers: list[dict]) -> list[dict]:
    q = {json.loads(l)["qid"]: json.loads(l) for l in QUESTIONS.open()}
    p = {json.loads(l)["qid"]: json.loads(l) for l in PREDS.open()}
    a = {r["qid"]: r for r in answers}
    rows = []
    for qid, ans in a.items():
        tik = ans["inchikey"][:14]
        obs = obs_c13(q[qid].get("c_nmr"))
        seen = set()
        for rank, smi in enumerate(((p.get(qid) or {}).get("candidates") or [])[:3]):
            cs = canon(smi)
            if not cs or cs in seen:
                continue
            seen.add(cs)
            rows.append({
                "cid": f"expand:{qid}:{rank}",
                "dir": str(EXPAND),
                "qid": qid,
                "smiles": cs,
                "self_rank": rank,
                "is_true": ik14(cs) == tik,
                "obs_c13": obs,
                "difficulty": ans["difficulty"],
            })
    return rows


def llm_overlap(rows: list[dict]) -> dict:
    """How many expansion candidate SMILES already have a locked-arm LLM 13C."""
    locked = {}
    for arm in ("data/fverify", "data/fverify_main"):
        amap_p = Path(arm) / "anon_map.json"
        if not amap_p.exists():
            continue
        amap = json.load(amap_p.open())
        pred = {}
        for f in sorted(Path(arm).glob("raw/*.json")):
            pred.update(json.load(f.open()))
        for smi, anon in amap.items():
            if anon in pred:
                locked[canon(smi) or smi] = pred[anon]
    n_uniq = len({r["smiles"] for r in rows})
    hit = sum(1 for s in {r["smiles"] for r in rows} if s in locked)
    return {
        "locked_llm_unique_smiles_with_pred": len(locked),
        "expand_unique_smiles": n_uniq,
        "overlap_unique_smiles": hit,
        "overlap_frac": (hit / n_uniq) if n_uniq else 0.0,
    }


def write_llm_batches(rows: list[dict]) -> dict:
    """Anon SMILES batches for a future LLM campaign. No is_true, no key."""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "raw").mkdir(exist_ok=True)
    uniq = sorted({r["smiles"] for r in rows})
    rng = random.Random(SEED)
    rng.shuffle(uniq)
    amap = {s: f"E{i:03d}" for i, s in enumerate(uniq)}
    # public map is anon_id -> SMILES only (already in predictions2.jsonl)
    public = {amap[s]: s for s in uniq}
    json.dump(public, (OUT / "anon_map_public.json").open("w"), indent=1)
    n_batch = 0
    for bi in range((len(uniq) + BATCH - 1) // BATCH):
        chunk = uniq[bi * BATCH:(bi + 1) * BATCH]
        body = "\n".join(f"{amap[s]}  {s}" for s in chunk)
        (OUT / f"fbatch_{bi + 1}.txt").write_text(body + "\n")
        n_batch += 1
    readme = OUT / "README.md"
    readme.write_text(
        "# Expansion forward-verify deposits\n\n"
        "LLM 13C campaign was **not** run. `fbatch_*.txt` are anonymised candidate\n"
        "SMILES (already in `data/benchmark_expand/predictions2.jsonl`) for a future\n"
        "blind Opus forward-predict pass. Deposit `{anon_id: [shifts]}` JSON under\n"
        "`raw/` and re-score with `scripts/forward_verify_expand.py score --llm`.\n\n"
        "`diagnosis.json` is the **GNN-scripted** wall. Do not relabel it as LLM fverify.\n"
        "Do not commit `answers2.jsonl` or a candidates.jsonl that carries `is_true`.\n"
    )
    return {"unique_smiles": len(uniq), "n_batches": n_batch, "batch_size": BATCH}


def score_gnn(rows: list[dict], answers: list[dict]) -> tuple[list[dict], dict]:
    cache = {}
    comps = defaultdict(list)
    for r in rows:
        comps[r["qid"]].append(r)

    recs = []
    for qid, ans in ((r["qid"], r) for r in answers):
        cands = comps.get(qid, [])
        if not cands:
            recs.append({
                "qid": qid, "difficulty": ans["difficulty"],
                "n_cand": 0, "recall": False, "self": False, "verify": False,
                "dist": 999.0, "predicted": False,
            })
            continue
        obs = cands[0]["obs_c13"]
        for c in cands:
            if c["smiles"] not in cache:
                cache[c["smiles"]] = gnn_predict.predict_c13(c["smiles"])
            c["pred"] = cache[c["smiles"]]
            c["dist"] = chamfer(c["pred"], obs) if c["pred"] else 999.0
        best = min(cands, key=lambda c: c["dist"])
        recs.append({
            "qid": qid, "difficulty": cands[0]["difficulty"],
            "n_cand": len(cands),
            "recall": any(c["is_true"] for c in cands),
            "self": sorted(cands, key=lambda c: c["self_rank"])[0]["is_true"],
            "verify": best["is_true"],
            "dist": best["dist"],
            "predicted": any(c["pred"] for c in cands),
        })
    return recs, {"unique_predicted": sum(1 for v in cache.values() if v),
                  "unique_attempted": len(cache)}


def score_locked_gnn_calibration() -> dict:
    """Re-derive the published 59/65 GNN number on the locked n=194 candidate files."""
    comps = defaultdict(list)
    for arm in ("data/fverify/candidates.jsonl", "data/fverify_main/candidates.jsonl"):
        p = Path(arm)
        if not p.exists():
            return {"status": "skipped", "reason": f"missing {arm}"}
        for line in p.open():
            r = json.loads(line)
            comps[arm + r["qid"] + r.get("dir", "")].append(r)
    cache = {}
    recs = []
    for cands in comps.values():
        obs = cands[0]["obs_c13"]
        for c in cands:
            if c["smiles"] not in cache:
                cache[c["smiles"]] = gnn_predict.predict_c13(c["smiles"])
            c["pred"] = cache[c["smiles"]]
            c["dist"] = chamfer(c["pred"], obs) if c["pred"] else 999.0
        recs.append({
            "recall": any(c["is_true"] for c in cands),
            "self": sorted(cands, key=lambda c: c["self_rank"])[0]["is_true"],
            "verify": min(cands, key=lambda c: c["dist"])["is_true"],
            "n_cand": len(cands),
        })
    cond = [r for r in recs if r["recall"]]
    return {
        "status": "ok",
        "n_compounds_with_parseable_cands": len(recs),
        "recalled": sum(r["recall"] for r in recs),
        "self_ranked": sum(r["self"] for r in recs),
        "gnn_verified": sum(r["verify"] for r in recs),
        "conditional_gnn": [sum(r["verify"] for r in cond), len(cond)],
        "published_locked_gnn_conditional": [59, 65],
        "published_locked_llm_conditional": [58, 65],
        "matches_published_59_65": (
            sum(r["verify"] for r in cond) == 59 and len(cond) == 65
        ),
    }


def block(name: str, rec: list[dict]) -> dict:
    n = len(rec)
    ceil = sum(r["recall"] for r in rec)
    s1 = sum(r["self"] for r in rec)
    v1 = sum(r["verify"] for r in rec)
    never = n - ceil
    mis = ceil - v1
    cond = [r for r in rec if r["recall"]]
    multi = [r for r in cond if r["n_cand"] > 1]
    print(f"\n=== {name}  (n={n}) ===")
    print(f"  generation recall              {ceil}/{n} ({100 * ceil / n:.1f}%)")
    print(f"  top-1, solver self-ranking     {s1}/{n} ({100 * s1 / n:.1f}%)")
    print(f"  top-1, GNN-verified            {v1}/{n} ({100 * v1 / n:.1f}%)")
    print(f"  wall: verified / mis-ranked / never-proposed   "
          f"{v1} / {mis} / {never}")
    out = {
        "n": n,
        "recalled": ceil,
        "self_ranked": s1,
        "verified": v1,
        "misranked": mis,
        "wall": never,
        "conditional_verify": [sum(r["verify"] for r in cond), len(cond)] if cond else [0, 0],
        "conditional_self": [sum(r["self"] for r in cond), len(cond)] if cond else [0, 0],
    }
    if cond:
        cs = sum(r["self"] for r in cond)
        cv = sum(r["verify"] for r in cond)
        b = sum(1 for r in cond if r["self"] and not r["verify"])
        c = sum(1 for r in cond if r["verify"] and not r["self"])
        print(f"  CONDITIONAL ON RECALL (n={len(cond)}):")
        print(f"    self-ranking     {cs}/{len(cond)} ({100 * cs / len(cond):.1f}%)")
        print(f"    GNN-verify       {cv}/{len(cond)} ({100 * cv / len(cond):.1f}%)")
        print(f"    McNemar exact: b={b} (self only) c={c} (verify only) "
              f"p={mcnemar_exact(b, c):.3f}")
        out["mcnemar_cond"] = {"self_only": b, "verify_only": c,
                               "p": round(mcnemar_exact(b, c), 3)}
        out["single_candidate_on_recall"] = len(cond) - len(multi)
    if multi:
        ms = sum(r["self"] for r in multi)
        mv = sum(r["verify"] for r in multi)
        b = sum(1 for r in multi if r["self"] and not r["verify"])
        c = sum(1 for r in multi if r["verify"] and not r["self"])
        print(f"  MULTI-CANDIDATE ONLY (n={len(multi)}):")
        print(f"    self-ranking     {ms}/{len(multi)} ({100 * ms / len(multi):.1f}%)")
        print(f"    GNN-verify       {mv}/{len(multi)} ({100 * mv / len(multi):.1f}%)")
        print(f"    McNemar exact: b={b} c={c} p={mcnemar_exact(b, c):.3f}")
        out["multi"] = {
            "n": len(multi), "self": ms, "verify": mv,
            "mcnemar": {"self_only": b, "verify_only": c,
                        "p": round(mcnemar_exact(b, c), 3)},
        }
    return out


def score_llm(rows: list[dict], answers: list[dict]) -> tuple[list[dict], dict] | None:
    """Score from deposited LLM 13C JSON. Returns None if the campaign is absent."""
    raw = sorted((OUT / "raw").glob("*.json")) if (OUT / "raw").exists() else []
    if not raw:
        return None
    pred = {}
    for f in raw:
        pred.update(json.load(f.open()))
    public_p = OUT / "anon_map_public.json"
    if not public_p.exists():
        raise SystemExit("LLM raw/ present but anon_map_public.json missing; run prep")
    public = json.load(public_p.open())  # anon_id -> smiles
    smi_to_anon = {v: k for k, v in public.items()}
    comps = defaultdict(list)
    for r in rows:
        comps[r["qid"]].append(r)
    recs = []
    n_hit = 0
    for ans in answers:
        qid = ans["qid"]
        cands = comps.get(qid, [])
        if not cands:
            recs.append({
                "qid": qid, "difficulty": ans["difficulty"],
                "n_cand": 0, "recall": False, "self": False, "verify": False,
                "dist": 999.0, "predicted": False,
            })
            continue
        obs = cands[0]["obs_c13"]
        for c in cands:
            anon = smi_to_anon.get(c["smiles"])
            c["pred"] = pred.get(anon) if anon else None
            if c["pred"]:
                n_hit += 1
            c["dist"] = chamfer(c["pred"], obs) if c["pred"] else 999.0
        best = min(cands, key=lambda c: c["dist"])
        recs.append({
            "qid": qid, "difficulty": cands[0]["difficulty"],
            "n_cand": len(cands),
            "recall": any(c["is_true"] for c in cands),
            "self": sorted(cands, key=lambda c: c["self_rank"])[0]["is_true"],
            "verify": best["is_true"],
            "dist": best["dist"],
            "predicted": any(c["pred"] for c in cands),
        })
    info = {
        "raw_files": len(raw),
        "anon_ids_predicted": len(pred),
        "candidate_rows_with_pred": n_hit,
    }
    if n_hit == 0:
        return None
    return recs, info


def main():
    args = [a for a in sys.argv[1:] if a != "--llm"]
    want_llm = "--llm" in sys.argv[1:]
    do_prep = (not args) or ("prep" in args) or (args == ["all"])
    do_score = (not args) or ("score" in args) or (args == ["all"]) or want_llm
    if args and args[0] not in ("prep", "score", "all"):
        raise SystemExit("usage: forward_verify_expand.py [prep|score|all] [--llm]")

    answers = load_key()
    clean = set(json.load(CLEAN.open()))
    flagged = sorted(r["qid"] for r in answers if r["qid"] not in clean)
    if flagged != sorted(FLAGGED):
        raise SystemExit(f"flagged qids drifted: {flagged} vs {list(FLAGGED)}")

    rows = build_candidates(answers)
    print(f"{len(rows)} parseable candidates over {len({r['qid'] for r in rows})} "
          f"compounds; roster is 106")
    overlap = llm_overlap(rows)
    print(f"LLM 13C overlap with locked fverify deposits: "
          f"{overlap['overlap_unique_smiles']}/{overlap['expand_unique_smiles']} "
          f"unique SMILES ({100 * overlap['overlap_frac']:.1f}%)")

    batch_info = None
    if do_prep:
        batch_info = write_llm_batches(rows)
        print(f"wrote {batch_info['n_batches']} LLM batch stubs "
              f"({batch_info['unique_smiles']} unique SMILES) under {OUT}/")

    if not do_score:
        return

    if want_llm:
        llm_out = score_llm(rows, answers)
        if llm_out is None:
            raise SystemExit(
                "LLM expansion fverify blocked: data/fverify_expand/raw/*.json is empty. "
                f"{overlap['expand_unique_smiles']} unique SMILES, "
                f"{overlap['overlap_unique_smiles']} reusable from locked deposits, "
                f"≈{(overlap['expand_unique_smiles'] + BATCH - 1) // BATCH} Opus "
                "forward-predict jobs (batch size 17, SMILES only, no tools). "
                "Do not invent an LLM wall. GNN-scripted counts are in diagnosis.json."
            )
        recs, info = llm_out
        print(f"\n--- expansion LLM score ({info}) ---")
        block("expansion all (LLM deposits)", recs)
        block("expansion validate-clean (LLM deposits)",
              [r for r in recs if r["qid"] in clean])
        raise SystemExit("LLM deposits present; write a separate sidecar before mixing "
                         "with GNN diagnosis.json (not implemented: refuse to overwrite).")

    print("\n--- locked-slice GNN calibration (published 59/65) ---")
    cal = score_locked_gnn_calibration()
    if cal.get("status") == "ok":
        cv, cn = cal["conditional_gnn"]
        print(f"  locked parseable compounds: {cal['n_compounds_with_parseable_cands']}")
        print(f"  GNN conditional: {cv}/{cn}  "
              f"{'MATCHES published 59/65' if cal['matches_published_59_65'] else 'DOES NOT MATCH published 59/65'}")
    else:
        print(f"  skipped: {cal.get('reason')}")

    print("\n--- expansion GNN score ---")
    recs, pred_info = score_gnn(rows, answers)
    print(f"GNN predictions: {pred_info['unique_predicted']}/{pred_info['unique_attempted']} "
          f"unique SMILES")

    all106 = block("expansion all (GNN-scripted)", recs)
    clean_recs = [r for r in recs if r["qid"] in clean]
    clean101 = block("expansion validate-clean (GNN-scripted)", clean_recs)
    for d in ("simple", "complex"):
        block(f"expansion all — {d}", [r for r in recs if r["difficulty"] == d])

    cal_pred = sorted((r["dist"], r["verify"]) for r in recs if r["predicted"])
    print("\ncalibration (GNN pick correct vs chamfer):")
    cal_bins = {}
    for lo, hi in [(0, 2), (2, 4), (4, 8), (8, 999)]:
        b = [t for d, t in cal_pred if lo <= d < hi]
        if b:
            print(f"  {lo}-{hi} ppm: {sum(b)}/{len(b)} correct ({100 * sum(b) / len(b):.0f}%)")
            cal_bins[f"{lo}-{hi}"] = [sum(b), len(b)]

    OUT.mkdir(parents=True, exist_ok=True)
    sidecar = {
        "verifier": "gnn_scripted_13C_chamfer",
        "not_llm_fverify": True,
        "n": 106,
        "verified": all106["verified"],
        "misranked": all106["misranked"],
        "wall": all106["wall"],
        "recalled": all106["recalled"],
        "self_ranked": all106["self_ranked"],
        "conditional_verify": all106["conditional_verify"],
        "conditional_self": all106["conditional_self"],
        "mcnemar_cond": all106.get("mcnemar_cond"),
        "multi": all106.get("multi"),
        "clean101": clean101,
        "locked_llm_wall_unchanged": {
            "n": 194, "verified": 58, "misranked": 7, "wall": 129, "recalled": 65,
            "note": "LLM forward-verify; do not replace with expansion GNN counts",
        },
        "locked_gnn_calibration": cal,
        "llm_overlap": overlap,
        "llm_campaign": {
            "status": "not run",
            "blocker": "no data/fverify_expand/raw/*.json LLM 13C deposits",
            "unique_smiles_to_predict": overlap["expand_unique_smiles"],
            "already_have_locked_llm_pred": overlap["overlap_unique_smiles"],
            "batches_if_prep": batch_info,
            "protocol": "same as scripts/forward_verify_main.py: blind Opus, SMILES only, no tools",
            "approx_cost": (
                f"{overlap['expand_unique_smiles']} unique SMILES in batches of {BATCH} "
                f"≈ {(overlap['expand_unique_smiles'] + BATCH - 1) // BATCH} Opus forward-predict jobs; "
                "no new solver elucidation"
            ),
        },
        "calibration_ppm": cal_bins,
        "flagged_qids": list(FLAGGED),
        "key_handling": "reconstructed under /tmp/blind/_key/; answers2.jsonl not in tree",
    }
    SIDECAR.write_text(json.dumps(sidecar, indent=1) + "\n")
    print(f"\nwrote {SIDECAR}")
    if (EXPAND / "answers2.jsonl").exists():
        raise SystemExit("answers2.jsonl leaked into the tree")


if __name__ == "__main__":
    main()
