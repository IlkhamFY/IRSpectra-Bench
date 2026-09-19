# Expansion forward-verify (GNN-scripted; LLM campaign not run)

`diagnosis.json` is the **scripted GNN $^{13}$C chamfer** wall on the 106-compound
expansion. It is **not** an LLM forward-verify deposit.

| item | value |
|---|---|
| verifier | nmrshiftdb2 GNN (`scripts/gnn_predict.py`; same checkpoint as locked 59/65) |
| expansion wall | **45 verified / 23 mis-ranked / 38 never proposed** |
| generation recall | 68/106 (already known from `score2`) |
| GNN conditional | 45/68 (66.2%) vs self-rank 63/68 (92.6%) |
| locked LLM wall (unchanged) | 58 / 7 / 129 on $n{=}194$ |
| locked GNN calibration | 59/65 — matches the published number |
| LLM $^{13}$C overlap with locked `fverify*` | **0 / 301** unique SMILES |
| LLM campaign | **not run**; 18 Opus batches of 17 would close it |

Do not relabel these counts as LLM fverify. Do not draw a pooled wall from them.
Do not commit `answers2.jsonl` or a `candidates.jsonl` that carries `is_true`.

Reproduce (from spectro-agent with expansion data + GNN weights):

```
python scripts/forward_verify_expand.py          # GNN score + diagnosis.json
python scripts/forward_verify_expand.py score --llm
    # refuses until data/fverify_expand/raw/*.json exists
```
