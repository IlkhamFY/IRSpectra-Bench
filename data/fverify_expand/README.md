# OUT OF SCOPE — not a paper claim

This directory is a **diagnostic proxy sidecar**. It is **not** IRSpectra-Bench
forward-verify.

- Paper fverify = training-free **LLM** ¹³C on locked **n=194** only (58/7/129, 58/65).
- Expansion LLM ¹³C dumps **do not exist**. See `docs/FVERIFY106_BLOCKER.md`.
- `diagnosis.json` records a nmrshiftdb2 **GNN** chamfer run on this VM. Different
  method. Do not cite in `iclr_paper.tex`, Figure 1, the leaderboard, or the 89%
  sentence. Do not draw a pooled 45+58 wall.

Do not commit `answers2.jsonl` or a `candidates.jsonl` that carries `is_true`.
