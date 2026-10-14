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
