# Promotion150 implementation specification

Status: planning only; no notebook edits, launch or submission in this task.
Frozen baseline: `notebooks/cpu-e006-v2/cpu_e006_v2.ipynb`.
Baseline SHA256: `dd658f132d5c21d352e38428d32785ade9cffa1082c87f86182ba432be852fc4`.

## Hypothesis and exact numerical edit

In zero-based cell25, replace exactly one executable predicate:

```python
if (S is not None and float(S) > S_TAU and pop_top >= POP_TAU) or (rel > 250.0):
```

with:

```python
if (S is not None and float(S) > S_TAU and pop_top >= POP_TAU) or (rel > 150.0):
```

Do not change S_TAU6, POP_TAU5, LIB_TAU0.9, REL_TH600, insertion slots,
alpha0.6, KRR3, window40, ICE fallbackTrue, candidate resources, model weights,
CPU device/thread settings, budgets, watchdog, or metric rules. No Engine2rank2
hedge is added. On this baseline it is a threshold-only derivative, not an exact
reproduction of the author's0.446 parent, which includes a rank2 hedge.

The newly eligible set is150<rel<=250, except rows already satisfying the
popularity-and-S alternative. Exact150 does not promote; exact250 is newly
promoted. Rows without usable PubChem proposals and strong-library rows remain
ineligible. Changing the threshold must occur before subsequent fusion;
appending a finaltop1 override is not equivalent.

## Why an isolated last-cell override is wrong

Cell25 emits the merged list and promotion choice. Cell27 captures that list
into PREFUSION_LISTS and runs original fusion. Cells29–31 perform metric-safe
cleanup and metric-identity fusion. Cell34 rebuilds E006 from the captured
prefusion list. Setting a new threshold only in cell34 or moving a candidate to
finalrank1 skips these dependencies. Instead patch the actual merge stage and
replay all downstream ranking/audit stages.

## Paired same-run implementation

Prefer one unchanged CPU inference/simulator run, then two isolated downstream
ranking branches. Reuse identical BASE, PC, ENG, ICE_SCORES, GL_SCORES, te and
metric code for both. No new model, simulator or retrieval pass is required.

1. Capture original upstream context immediately before cell25. Make branch
   copies of mutable BASE/PC/ENG proposal lists and stage-local dictionaries;
   retain large read-only library/pool arrays by reference. Never copy or mutate
   the completed original control objects in place.
2. Execute source cells25–34 with rel250 in a dedicated branch working directory,
   resolving any read-only assets by their original absolute paths. Require
   exact IDs/order and CSV string equality against the completed original CPU
   E006 control. If any replay dependency cannot be isolated or reconstructed,
   abort preparation rather than bypassing an assertion.
3. Execute those same stages with the single numerical rel150 edit in a second
   branch directory. Audit/provenance labels must identify this derivative as
   described below. No original E004/E006 receipts are overwritten.
4. Validate all outputs and write a separate promotion150 CSV atomically. Only
   select it as the final submission after paired validation succeeds. An
   unchanged ranked metric-identity output is a no-op and not a new submission.

A simpler full derivative can patch cell25 and rerun the whole notebook, but
then CPU inference variation is a confounder. It still needs the truthful audit
labels and mandatory checks below; do not call an unpaired score difference a
threshold-only causal estimate.

## Inherited receipt/provenance updates, without disabling checks

The existing report names describe the upstream exactE004 recipe and must not
be reused as proof that rel150 is byte-identical to it.

- Cell32 `_e004_postflight` currently emits `experiment='E004'`, sourceversion80,
  sourceversionID356740494, and fixed `source_code_sha256=eee496...`. Retain
  those values explicitly as upstream lineage fields. Add derivative recipe
  `CPU_PROMOTION150_PRE_FUSION` and a builder-computed derivative stage-pack
  SHA256. Never replace the upstream hash with a false hash claim or claim this
  modified prefix is exactE004. A stage-pack hash can cover cells25–31 while
  excluding the receipt cell that embeds that digest, avoiding a circular hash.
- Cell34 `run_overlay` has `assert base_report['experiment']=='E004'`. In the
  treatment branch change the expected recipe to exactly
  `CPU_PROMOTION150_PRE_FUSION` (or retain the upstream experiment field and
  additionally assert the derivative_recipe and expected stage-pack digest).
  Keep an explicit equality assertion: do not delete, weaken to membership, or
  catch-and-ignore it.
- Cell34 must still assert the actual branch CSV hash equals the hash recorded
  by that branch's pre-E006 receipt. Its window40, ice_fallbackFalse control
  reconstruction must still reproduce that branch's actual pre-E006 CSV.
  These are within-branch invariants; they are not comparisons to the rel250
  branch. The final comparison is between paired E006 outputs, both with
  ice_fallbackTrue.
- Update final report `source_experiment` and `base_report_file` to the truthful
  derivative receipt. Use isolated directories or distinct filenames so the
  original control's e004_verification.json, experiment_verification.json,
  submission_reference.csv, and candidate audits are immutable.
- Keep runtime input checks, pinned RDKit2026.03.3, CPU assertions, complete
  active-input coverage, n_err0, simulator health assertions, row IDs/order,
  candidate validity and official-identity uniqueness, and every source
  reconstruction/hash assertion. Only expected recipe identities/digests and
  branch-specific receipt paths change.
- Preserve the unchanged upstream source links/licences. Label author0.446 as an
  unverified external claim, not this derivative's score. Index and pull API
  timestamps conflict; neither establishes a score measured today.

## Required audit and tests

Record branch recipe hashes, exact common inference-input hashes, paired CSV
hashes, all eligible rows and their rel/S/pop/lib values, threshold-only versus
already-popularity-promoted actions, original/proposed PubChem leaders,
prefusion list changes, final ranked-identity changes, top1 changes, added/dropped
identities, simulator health, and branch execution times. No hardcoded molecule
IDs, hidden labels, previous hidden predictions, or final-candidate forcing.

Meaningful boundary fixtures: rel149.999,150,150.001,250,250.001; popularity
alternative true/false; lib_max0.9 protection; absent PubChem list; missing-pool
mass leading to inherited rel1e9 (already promoted in both, not a new activation).
Require unaffected eligibility branches to match exactly. Require full rel250
replay to reconstruct completed E006 byte/string identity before accepting any
rel150 result. Assert final IDs/order and1–25 valid unique metric identities;
write with temp+os.replace only after validation.

If visible smoke never enters150<rel<=250 and produces no ranked changes,
record that result without spending a duplicate slot or changing IDs/gates to
force activation. Evaluate a separate labelled, structure-disjoint natural-product
validation panel before making further threshold claims.
