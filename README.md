# Enveda CASMI 2026

Private experiment archive. No rank or score guarantee.

## Measured account history

13 submission records read on 2026-10-14 UTC. Best observed public score: 0.421 (submission 56869715, 2026-10-06). Live limits: 0 today; 5 allowed at inspection.

| Submission | UTC date | Score | Status |
|---|---|---:|---|
| 56869715 | 2026-10-06T04:03:21.08Z | 0.421 | complete |
| 56845607 | 2026-10-05T07:07:32.817Z | 0.420 | complete |
| 56826022 | 2026-10-04T14:09:20.99Z | 0.373 | complete |
| 56795627 | 2026-10-03T10:20:50.877Z | 0.392 | complete |
| 56790709 | 2026-10-03T05:53:20.833Z | 0.384 | complete |
| 56788656 | 2026-10-03T03:41:39.713Z | 0.343 | complete |
| 56788653 | 2026-10-03T03:41:18.237Z | 0.382 | complete |
| 56775173 | 2026-10-02T13:50:55.393Z | 0.396 | complete |
| 56775169 | 2026-10-02T13:50:30.083Z | 0.395 | complete |
| 56759564 | 2026-10-01T21:46:08.1Z | 0.388 | complete |
| 56759560 | 2026-10-01T21:45:52.59Z | 0.395 | complete |
| 56754118 | 2026-10-01T15:34:15.297Z | 0.398 | complete |
| 56753422 | 2026-10-01T14:55:18.62Z | 0.400 | complete |

## Source audit

The existing best-score notebook has a static 400-molecule-ID top1 dictionary and unconditionally indexes it. Do not reuse this override for a hidden-test rerun. Measured historical score remains 0.421; this audit does not invalidate that recorded receipt.

Next candidate: public flexonafft V90, remove only its final joint-evidence overlay (cell34), preserving the dynamically computed E006 control (window40, ICE fallback true). This avoids an extra two-model inference pass and PubChem scan. The source reports E006 score0.440; this candidate has NOT reproduced that score and exactV89 bytes were not retrieved. Do not label it a verifiedV89 reproduction.

## Sources

- https://www.kaggle.com/code/flexonafft/casmi26-public-baseline-adaptation-experiments
- https://www.kaggle.com/code/prvsiyan/analog-propagation-casmi-2026-baseline
- https://github.com/shiferaxa/casmi26

Visible test is a placeholder. Recompute all hidden-test predictions in the notebook. No cached visible-test predictions. Preserve upstream attribution embedded in notebooks. CPU-only equivalence remains unverified because simulators explicitly require CUDA. Actual GPU time and candidate score must be recorded after execution.

Credentials are never committed.

## Current execution handoff (2026-10-14 UTC)

Created repository acco-cyber/Enveda-CASMI-2026; reuse it for all future notebooks.

- GPU E006 kernel: `gwey1025/casmi26-e006-control-efficient`, version1, kernelId138751307; accepted, last observed running. No submission receipt.
- GPU quota is exhausted: 108079s used /108000s allowed; refresh2026-10-17 00:00UTC. Do not start additional GPU jobs.
- CPU experiment: `gwey1025/casmi26-cpu-e006-control`, source forces CPU for all models/simulators and8h30 watchdog; see exact push receipt. Compatibility and score unverified.
- Current first-place public score0.495. Public code index captures100 recent entries, not an exhaustive audit of every public source.
- Before any launch, inspect these exact jobs and reconcile status/version with latest submissions. Never duplicate pending launches. Before submission, inspect output schema, row keyset, chemistry checks, simulator health and live submission limits; record exact version and returned receipt. CPU/GPU differences must not be presented as equivalent.
- No new competition submission has been made in this run as of this handoff. Five submissions were available at initial inspection. Complete/verify a pending run before using a slot.

## Latest-source research

Authenticated index dated2026-10-14 led to inspection of three newer notebooks:

- `antriksharya/casmi26-lb-0-443-v7c-engine-2-rank-2-insert`: reuse Engine2 top1 at final rank2 when different, preserving finaltop1; no added inference. Title0.443 is a source claim, not independently reproduced. Best next cheap controlled experiment after a measured baseline.
- `ahmedberatozer/casmi26-v8b-native-treatment`: frozen A+B hard-negative FP checkpoint, 600update treatment; additional model provenance/dependency validation required.
- `flexonafft/casmi26-closing-the-evidence-gap` V15: latest CPU fragment-median overlay, >=3 informative spectra, >=2 discriminative peaks, candidate groups2–8,40-bond cap,lambda1.25,900s hidden budget. No verified higher score.

Do not infer measured improvements from titles or iteration numbers. Avoid blindly consuming remaining slots with equivalent predictions.

## 2026-10-15 execution update

GPU E006 version1 completed: smoke runtime1048.7seconds; full exported notebook1098.96seconds. CSV400unique input IDs/hash/1-25 candidate bounds and simulator health passed. This is12molecule smoke, not hidden validation. Submitted exactversion1: receipt57202348. Initial live limit5; after submission1used,4remaining. Score pending.

CPU version1 failed strictly: ICE budget300seconds expired with0molecules scored. CPU version2 increases only smoke ICE300->1800seconds and is running; hidden budgets and strict checks retained. No score/runtime equivalence claimed. Preserve failed version and do not submit it. See evidence/20261015 and updated run-ledger.
