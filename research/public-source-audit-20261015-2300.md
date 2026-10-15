# Public source audit — 2026-10-15 23:00 KST

Read-only authenticated Kaggle index:100 public notebooks, sorted by run time.
Six references pulled, no source executed. No table timestamps are used to imply execution or a score measured today. Sanitized metadata and source hashes:
`evidence/20261015_2300/source_audit.json`. Reference snapshots are in
`reference/20261015_2300`. No new notebook or submission was launched.

## Timestamp limitation

The index `lastRunTime` field contains2026-10-15timestamps, but fetched kernel metadata's `lastRunTime`
values are2026-10-12around14:02UTC. For promotion150,V2 metadata explicitly
reports `2026-10-12T14:02:03.0146004Z`, whereas its index field says `2026-10-15T10:51:08.03Z`. Treat these as separate source fields;
this audit does not resolve the discrepancy or claim a newly measured result
today. The machine-readable receipt retains both timestamps.

## Findings

| Source / fetched version | Fresh change | Score evidence | Recommendation |
|---|---|---|---|
| [seyitkaangunes promotion150](https://www.kaggle.com/code/seyitkaangunes/casmi26-e006-pubchem-promo-rel-150-lb-0-446),V2 | PubChem structure-evidence promotion threshold250→150 before fusion, inherited Engine2 rank2 hedge | Author reports0.446 versus0.442 parent; siblingrel100 reported0.444. Pull contains no independently verified leaderboard score or stored execution outputs | Strongest bounded next hypothesis; isolate threshold only on a fixed evaluated baseline |
| [Closing the Evidence Gap](https://www.kaggle.com/code/flexonafft/casmi26-closing-the-evidence-gap),V19 | Replaces previous fragment iteration with Engine2 rank3 hedge onrel100 recipe, protects first two candidates | Explicitly unmeasured; no improvement claimed | Cheap postprocessing, but bundles a differentrel100 parent; avoid stacking with currentalpha/window tests |
| [rajrajak99 V420](https://www.kaggle.com/code/rajrajak99/casmi26-apex-v420-sovereign-rank2-vanguard),V2 | rel100+rank2+library override+mass-only tail fill | Target0.445–0.448+, not measured proof | Avoid combined change and faulty mass-index backfill |
| [rajrajak99 V440](https://www.kaggle.com/code/rajrajak99/casmi26-apex-v440-sovereign-multi-ce-rank2),V1 | Patches GLACIER runner for multi-collision-energy mean similarity; adds rank2/library override/backfill | Target0.446–0.450+, not measured proof | More simulator work and multiple confounders; poor immediate low-GPU choice |
| [rajrajak99 V450](https://www.kaggle.com/code/rajrajak99/casmi26-apex-v450-sovereign-sodiated-rank2),V1 | Shifts every sodium-adduct fragment peak−21.98194Da and relabels proton adduct for additional GLACIER pass; rank2/library override/backfill | Target0.446–0.452+, not measured proof | No measured validation of adduct transformation; additional simulator pass; avoid immediate adoption |
| [juna1013 train/submission](https://www.kaggle.com/code/juna1013/casmi-2026-train-submission),V15 | Batch-normalizes assembled CSR matrix instead of normalizing each spectrum individually; intensity floor0.01→0.02, weights change to intensity^0.375 withoutm/z weighting | No new score or execution timings in pulled source | CSR batch-normalization is a useful CPU optimization pattern; remain with stronger current engine |

The promotion150 source is included
because its explicit author-reported experiment is more useful than recently listed target
claims. None of these pulls independently establishes a measured gain over our
account's0.440. Public web search remains stale for these new notebook versions.

## Concrete source correctness issue

All three rajrajak99 variants sort `_gm_compounds.nm.values` into a separate
`_gm_mz_sorted` array, but later use searchsorted positions against
`_gm_compounds.iloc[...]` without sorting that dataframe by neutral mass. The
mass index and structure rows need not align, so tail candidates can correspond
to different masses. Do not copy that backfill. Their library-match “zero
regression” statement is also not established merely by a high similarity score.

## Best next controlled experiment after pending scores resolve

Keep one fixed baseline's models, simulator settings, candidate resources,
Engine2weight, window and metric logic unchanged. Change only the earlier
PubChem promotion predicate from `rel > 250` to `rel > 150` while retaining the
existing `(S >6 and popularity>=5)` alternative. The author reports gains on two
parents, but our account must measure its own result. It adds no learned
inference or retrieval, making it preferable to extra GLACIER passes.

This must be implemented at the original promotion stage before subsequent
fusion, not by appending a finaltop1 override. A future derivative needs new
provenance and same-run paired receipt because inherited E004 byte/hash/control
observers describe the250recipe. Do not disable their assertions or falsely
label changed pre-fusion outputs as an exact E004 reproduction. Audit eligible
rows in150<rel<=250, promotionchanges, candidateidentity changes, top1changes,
and GL/ICEhealth; skip duplicate outputs. Do not run more experiments today:
root reports quota5/5 and has pending controlled submissions to assess first.
