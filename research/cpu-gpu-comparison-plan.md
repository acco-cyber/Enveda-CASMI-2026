# CPU/GPU comparison: bounded causal-localization plan

Checked 2026-10-16 02:00 KST run. No new launch or submission performed. Source notebook SHA for Alpha075 remains `082eb2d8daca785f1c5c4fcd1aedda74755738b25b89583b4b60bf46db4cf232`.

## Measured results

Latest API snapshot: `evidence/20261016_0200/submissions.json`. GPU E006 ref 57202348 is 0.440; CPU E006 v2 ref 57216989 is 0.433; CPU window30 ref 57222276 is 0.433; CPU window80 ref 57222283 is now complete at 0.431; Alpha075 ref 57233074 remains pending. These are reported leaderboard values, not independent held-out estimates.

Existing downloaded artifacts describe visible smoke, not the hidden scoring rerun:

| Observation | GPU E006 | CPU E006 v2 |
|---|---:|---:|
| Input / processed molecules | 400 / 12 | 400 / 12 |
| Python / main RDKit | 3.12.13 / 2026.03.3 | 3.12.13 / 2026.03.3 |
| Simulator RDKit | 2025.03.6 | 2025.03.6 |
| ICE status / covered / scored molecules | ok / 11 / 11 | ok / 11 / 11 |
| ICE candidate / scored counts | 773 / 755 | 774 / 756 |
| ICE spectrum predictions | 1526 | 1529 |
| ICE seconds | 70.25 | 1055.42 |
| GL status / covered / scored molecules | ok / 11 / 11 | ok / 11 / 11 |
| GL seconds | 39.12 | 196.91 |
| Stage prediction errors | 0 | 0 |
| E004 observer elapsed_seconds | 1063.17 | 2469.75 |

Runtime table values are the exact `elapsed_seconds` fields of `evidence/20261015/gpu_files/e004_verification.json` and `evidence/20261015_1400/cpu_files/e004_verification.json`. These are observer timestamps, not whole notebook export durations or hidden scoring runtime.

Both logs show 2,539,608 library spectra, a 774,943-structure Engine2 pool, 710,701 Engine1 pool structures, 41 visible spectra, and the same named `fpnet_full1.pt` asset. Equal names and counts are not byte-level proof of equal dataset versions.

Independent CSV comparison found nine differing smoke rows and zero differing top-1 strings. Candidate counts already differ at simulator input, so downstream simulator numeric differences alone cannot account for all observed differences. These measurements do not identify the cause of the 0.007 hidden leaderboard gap. Neither hidden stage timing nor per-molecule hidden ranks have been downloaded. Do not describe a timeout, precision effect, or dataset drift as the established cause.

The frozen final pass rejects ICE `status='budget'`, and also rejects a non-ok GL status when protonated spectra exist. Both observed smoke stages completed normally. Hidden partial-coverage claims require actual hidden metadata and the runner's status semantics.

## Cheapest next comparison: existing artifacts, zero inference

1. Download `e004_candidate_inputs.json` from both already completed exact notebook versions. Their report-pinned hashes are GPU `920f4fff4de56744ba82a594262d0ac7e246f7689a70c2eb8b7b7db5620b1b33` and CPU `564201cb3211926a4f35c7e9aac261b0f416a98b0ddeb5d7bb1cc9f4564a7817`. Verify hashes before comparing.
2. Compare identical molecule IDs stage by stage: `engine2`, `pubchem`, `base_tail`, `prefusion`, `fusion_overflow`. Report exact strings, ordered metric identities where the exact official RDKit environment is available, additions/removals, and earliest observed divergence. Main- vs Engine2-specific differences localize the branch; they do not yet identify its computational cause.
3. If available from the same runs, download BASE/PC score caches, Engine2 candidate lists and both simulator score JSONs. Pair only candidates present in both runs; quantify rank flips and raw score differences. Retrieve relevant resolved dataset versions or source-file hashes before attributing any discrepancy to hardware.
4. Recompute only the final pure-ranking overlay from the saved evidence as needed. This requires no neural inference, retrieval, simulator passes, submission, or GPU allocation. Reconstruct each control exactly before any cross-device evidence swap. Swap one cached branch at a time to test whether that branch is sufficient to reproduce the observed smoke row differences.

If required caches were not retained, stop causal attribution at the earliest available differing artifact. A later tiny matched-input CPU/GPU replay can target that branch when GPU quota is available; do not rerun the full competition pipeline merely to recover this information. Visible smoke is not suitable for estimating leaderboard improvement.

## Alpha075 output acceptance remains supported

`evidence/20261015_2300/alpha075_audit.json` and downloaded CSVs agree: 400 ordered unique IDs, 12 active rows changed, all 388 inactive placeholders unchanged, zero top-1 changes, and 11 added/dropped official identities. Runtime assertions establish 12 ranked-identity changes. Baseline SHA `d137914c7542d666b1f89cf30650d10e632fa74f632fd17f75a41110088f1939`; treatment SHA `08d70e7a04f1f2ca60b74bdcbec95c373e0434739beb75461ed992cdb1505000`. Both hashes were independently checked and both CPU simulator stages were healthy. This supports a distinct scoring experiment, not a score-gain claim. The visible CSV contains placeholders and is not a direct competition submission.

## Resource priority

Preserve GPU best 0.440. Reconcile already submitted pending work before launching another version. Do not force CSV changes, resubmit observed no-ops, or change simulator budgets without evidence of a relevant limitation. In E006, `if ice and gl` uses GL-only score arguments but depends on a truthy ICE dictionary; dropping ICE or requiring finite ICE can inadvertently disable GL. A budget reallocation would therefore require a separate, auditable gate-preservation design.


## Downloaded candidate snapshots: independent bounded comparison

Both candidate-input files have now been downloaded and their SHA256 hashes match the report-pinned values above. They cover the same 12 visible molecules. Findings distinguish raw numeric changes from ranked structures:

| Saved stage | Rows with ranked-list changes | Rows with set changes | Top-1 changes |
|---|---:|---:|---:|
| Prefusion, raw SMILES strings | 1 / 12 | 0 / 12 | 0 |
| Engine2, stored key lists | 8 / 12 | 5 / 12 | 0 |
| PubChem, raw SMILES strings | 0 / 12 | 0 / 12 | 0 |
| Base top-60 tail, raw SMILES strings | 4 / 12 | 1 / 12 | 0 |
| Fusion overflow tail, raw SMILES strings | 10 / 12 | 8 / 12 | 4 first-overflow changes |

Overflow top-1 means the first overflow-tail candidate, not final submission top-1. Engine2 comparisons use its stored keys; their equivalence to the final official identity is not re-established locally. Other set/rank counts use exact strings; they must not be advertised as independently recomputed official metric identities.

Engine2 changes include seven aggregate stored-key additions and seven removals across five molecules; three more molecules only reorder the same stored-key set. The sole prefusion change is a three-position reorder in `m_006153`, with the same 25 exact strings. Base-tail membership differs only in `m_006153` (one addition/removal); three other base-tail rows have ordering changes only.

All 12 PubChem records differ numerically, but their candidate lists and recorded keys are unchanged. Maximum absolute deltas across paired records: standardized `pc_fz` 0.0019720116452854874; `fz_top` 0.078521728515625; `S` 0.0019720116452854874; `best_pool_fz` 0.4349430985748768. These are different fields/scales; do not compare their magnitudes as a common quality measure. Observed numeric differences do not establish precision or hardware as the sole cause.

Two molecules (`m_00b5aa`, `m_01e922`) have identical saved prefusion and Engine2 lists but different fusion overflow. Thus differences occur both upstream of simulators and later in the pipeline; attributing every difference to Engine2 alone is unsupported. The next zero-inference artifact to request is paired simulator score JSON, followed by deterministic replay of final fusion with one evidence channel swapped at a time. Existing snapshots are insufficient to quantify which branch causes the hidden score difference.

No new GPU time, inference, launch, or submission was used in this comparison.
