# Bounded CPU fragment derivative

Prepared notebook: `notebooks/cpu-fragment-gap/cpu_fragment_gap.ipynb`.
Generator: `scripts/build_cpu_fragment_gap.py`; adapter: `scripts/fragment_gap_overlay.py`.
No launch or score claim was made while preparing these files.

The original 35 CPU E006 v2 cells remain unchanged. One appended cell embeds the
fragment scoring kernel verbatim from Dmitrii Gluzdov's V47 cell118, which credits
Ahmed Berat Özer's v7c and Huseyin Emre Aksoy (Apache-2.0). Upstream V46's
author-reported0.441 does not measure this derivative; V47's score is unverified.

Only active molecules without GLACIER coverage are eligible. The adapter reuses
same-run Engine2/prefusion lists to recover the existing reciprocal-rank support
for each final candidate; it never retrieves additional candidates. It preserves
the exact final25 candidate identity set, reconstructs support scores before any
ICE reranking (avoiding double-counting), and combines that support with existing
ICE scores when finite and fragment evidence at weight0.5. Formula positions must
remain identical. Missing support, scoring failure, incomplete checkpoints, or
reranker validation failure preserve the original molecule list.

CPU fragment scoring runs in an isolated subprocess capped at900seconds hidden
or120seconds smoke, including import/compilation. Only completed, finite,
whole-molecule checkpoints are usable. The enclosing8h30 watchdog remains active;
the subprocess timeout is shortened when necessary to reserve30seconds. All
learned models, retrieval, and simulator settings remain unchanged. The final25
universe restriction intentionally differs from V47's40candidate rebuild.

Validation completed: AST parsing of all36cells and embedded worker/kernel;
original35cell equality; synthetic eligible-molecule reorder; GL-covered and
inactive-row preservation; rejection of malformed permutations; unchanged
candidate identity sets; timeout fallback preserving exact CSV bytes. These are
mechanical fixture checks, not measured competition predictions.

Review repairs also verified: NaN precursor/serialization failures are recorded
per molecule; worker setup/launch OSError, nonzero exit, malformed checkpoint
JSON/schema, and mismatched checkpoint candidate universes preserve exact baseline
bytes. Final candidate identity and key-set assertions remain mandatory. A changed
CSV is written to a temporary file and atomically replaced only after validation.
Fixtures cover all those failure paths, successful atomic replacement, and a
duplicate-identity baseline failing closed.

The latest12molecule smoke has11GL-covered molecules, so actual eligibility may
be only one molecule. No local measured spectra or detailed same-run candidate
inputs were available for an honest replay. The notebook writes
`fragment_overlay_audit.json` and sets `submission_eligible=False` if output bytes
do not change. A no-op should not consume a fifth slot. Do not broaden the gate,
insert candidates, choose IDs, or tune against test labels to force a change.
If it is a no-op, collect a separate structure-disjoint natural-product validation
panel with labels and evaluate the same gate there before another experiment.
