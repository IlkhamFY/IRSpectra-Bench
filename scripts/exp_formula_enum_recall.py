#!/usr/bin/env python3
"""Fill recall for MAYGEN runs that finished above the rank cap.

The main enumerator keeps a top-1 ranker only when the unique
connectivity set is at most 80,000. Larger finished files were marked
complete_unranked and not scored. This pass regenerates those formulas
and tests InChIKey-14 membership only. It does not rank them, and it
does not treat an unfinished scan as a miss.
"""
from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exp_formula_enum import TIMEOUT_S, cohort, run_maygen  # noqa: E402
from exp_split_thinking import ik14  # noqa: E402

SCAN_S = 480


def main() -> None:
    root = Path("/tmp/maygen_out")
    rows = list(csv.DictReader(open(root / "exp_formula_enum_per_qid.csv")))
    pending = [r for r in rows if r["status"] == "complete_unranked"]
    if not pending:
        print("nothing to rescan")
        return
    members = {
        (r["slice"], r["qid"]): r
        for r in cohort(Path("/tmp/spectro-agent"), Path("/tmp/deposits/data"), Path("docs/headline500_expand200_qids.json"))
    }
    work = Path("/tmp/maygen_recall")
    by_formula: dict[str, list[dict]] = {}
    for row in pending:
        by_formula.setdefault(row["formula"], []).append(row)
    print(f"rescan {len(by_formula)} formulas / {len(pending)} compounds", flush=True)
    for formula, group in sorted(by_formula.items()):
        golds = {}
        for row in group:
            src = members[(row["slice"], row["qid"])]
            golds[row["qid"]] = src["ik14"]
        t0 = time.time()
        status, smi, note = run_maygen(Path("/tmp/MAYGEN-1.8.jar"), formula, work)
        print(f"{formula} gen={status} in {time.time()-t0:.1f}s {note[:60]}", flush=True)
        found = {qid: False for qid in golds}
        n_lines = 0
        scan = "not_started"
        if status == "complete" and smi is not None:
            scan = "eof"
            t1 = time.time()
            for line in smi.open():
                text = line.strip()
                if not text:
                    continue
                n_lines += 1
                key = ik14(text)
                if key in golds.values():
                    for qid, g in golds.items():
                        if key == g:
                            found[qid] = True
                if all(found.values()):
                    scan = "hit"
                    break
                if time.time() - t1 > SCAN_S:
                    scan = "scan_timeout"
                    break
                if n_lines % 100000 == 0:
                    print(f"  {formula} scanned {n_lines}", flush=True)
            smi.unlink()
        for row in group:
            row["n_smiles_scanned"] = n_lines
            row["recall_scan"] = scan
            if scan == "hit" and found[row["qid"]]:
                row["recall"] = 1
                row["status"] = "complete_unranked"
            elif scan == "eof":
                row["recall"] = 0
                row["status"] = "complete_unranked"
            else:
                row["recall"] = ""
                row["status"] = "complete_unranked_unscanned"
            row["top1"] = ""
            row["gnn_top3"] = ""
            row["ranked"] = 0
            print(
                f"  {row['qid']} recall={row['recall']} scan={scan} lines={n_lines}",
                flush=True,
            )
    # merge back
    updated = { (r["slice"], r["qid"]): r for r in rows }
    for row in pending:
        updated[(row["slice"], row["qid"])] = row
    # pending rows were the same objects as in rows, already mutated
    fields = list(rows[0].keys())
    for extra in ("n_smiles_scanned", "recall_scan"):
        if extra not in fields:
            fields.append(extra)
    with (root / "exp_formula_enum_per_qid.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    summary = json.loads((root / "exp_formula_enum.json").read_text())
    summary["recall_pass"] = {
        "scan_timeout_s": SCAN_S,
        "maygen_timeout_s": TIMEOUT_S,
        "n_rescanned_compounds": len(pending),
        "recall_hits_on_unranked": sum(r.get("recall") == 1 or r.get("recall") == "1" for r in pending),
        "recall_miss_on_unranked": sum(str(r.get("recall")) == "0" for r in pending),
        "still_unscanned": sum(r["status"] == "complete_unranked_unscanned" for r in pending),
    }
    (root / "exp_formula_enum.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["recall_pass"], indent=2), flush=True)


if __name__ == "__main__":
    main()
