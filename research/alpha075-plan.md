# CPU_ALPHA075 controlled experiment

Accepted version1 and running CPU-only: `gwey1025/casmi26-cpu-e006-engine2-alpha075` (kernel138840608). Source: `notebooks/cpu-alpha075/cpu_alpha075.ipynb`.
Generator: `scripts/build_cpu_alpha075.py`; adapter: `scripts/alpha075_overlay.py`.

Hypothesis: increase Engine2's reciprocal-rank contribution by25percent,
alpha0.6→0.75, while holding offset3, window40, ICE fallback, learned models,
retrieval and simulator budgets fixed. Each engine contributes at most once per
official metric identity. Formula: `1/(3+main_rank)+alpha/(3+Engine2_rank)`.
No improvement or competition score is claimed. This can change top1, the
top40 shortlist boundary, final25 membership, and MRR in either direction.

All35 frozen CPU E006 v2 cells remain unchanged. The appended overlay embeds
the source `_factorial_entry` factory extracted by AST, renames it, and replaces
only its final return with `return rerank_row`. The nested row function's AST is
verified identical to the original. Defining the old nested `run_overlay` does
not execute it or write inherited audit files.

For every row, reconstruct E006alpha0.6 with ICE fallbackTrue and window40 from
the same-run `submission_reference.csv` and live candidate inputs; require exact
string equality against the completed baseline CSV. This is an E006 paired
control, not an E004 comparison. Pass a shallow scope copy with ALPHA0.75 only
for the treatment. Preserve placeholder rows. Validate official identities,
unique output identities,1–25 candidates, and exact input row IDs/order before
atomically replacing the CSV. Write separate `alpha075_audit` artifacts with
paired hashes, changed ranked identities, top1 changes, added/dropped identities,
and eligibility. If ranked identities are unchanged, retain original CSV bytes.

Checks completed: all36 cells and embedded factory AST parse; original35 cell
equality; exact nested row AST equality; source40/80 window guard retained;
positive boundary fixture that switches top1 at0.75; no-op byte preservation;
inactive-row preservation; paired-control mismatch failing closed without
changing the CSV. The boundary fixture uses main-rank1 support0.25 versus
main-rank10+Engine2-rank1 support1/13+alpha/4, which straddles0.25 between0.6
and0.75. These checks establish mechanics, not hidden-test benefit.
