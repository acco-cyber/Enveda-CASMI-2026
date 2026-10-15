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

## CPU validation and second submission (2026-10-15)

CPU E006 v2 completed: core2451.5seconds, observer2469.75seconds. ICE/GLstatusok onCPU,11coveredmolecules scored each.400row keys/hash/candidatebounds passed. Visible12-molecule smoke differs from GPU in9rawtail rows,0top1rows; not an equivalence proof or independent validation. Submitted exactCPUv2:57216989. GPU57202348 andCPU57216989 remainpending at inspection;2used,3slotsremain.

Three distinctCPU-only version1 trials are running: `gwey1025/casmi26-cpu-window30` (kernel138790133), `gwey1025/casmi26-cpu-window80` (138790146), `gwey1025/casmi26-cpu-e006-engine2-rank2` (138790158). Compare conservative/expanded candidate windows and top1-preserving official-identity rank2insertion. No newinferencepass or GPUallocation beyond sharedCPUparent. Window30 guard expansion is documented. Preserve strictchecks and reject genuinely identical predictions/no-oprank2. Do not duplicate these runs.

See evidence/20261015_1400, notebookbuildmanifests and generators. Fullhidden CPUruntime and scoregains remainunverified. Freshpublicsourceaudit identifies Dmitriiv47 CPUfragment/ICEevidence as a separate future experiment, not adopted here.

## Measured improvement and third/fourth submissions (2026-10-15)

GPU E006 receipt57202348 completed with public0.440, improving the recorded0.421 best by0.019. CPU E00657216989 remainspending. Exactversion1 CPUwindow30 submitted57222276; CPUwindow80 submitted57222283. Live limit4used/1remaining. Both are validated400-row/keyset/hash/CPU-simulator healthy outputs. LocalRDKit2026.03.3 officialidentity validity/uniqueness passed; both differ in10officialrankedrows from CPUv2 and their own same-run controls, no top1changes in12visible molecules. Scores and fullhiddenCPUtiming remainunverified. Window30sourcecontroldiffersslightly; paired same-run comparisons are authoritative.

Rank2trial completed but equals CPUv2 byte-for-byte:0changedrows,11alreadyrank1+1alreadyrank2;submission_eligiblefalse. It was not submitted. Replacement `gwey1025/casmi26-cpu-e006-fragment-gap` version1 (kernel138815528) is accepted and runningCPU-only. It appends noGL fragment+ICE reranking, preserves exactcandidate universe/formulaslots, boundsworker900s hidden/120s smoke, and retains baseline on optional failures. Independent review fixed NaN/launch/checkpointfail-open handling and atomicCSVwrites; baselineintegritychecksremainmandatory. No score claim, and no-op outputs must not spend lastslot. Inspect exactversion1 before further launch/submission.

Evidence: evidence/20261015_1700. All reference/code files retain upstream attribution. Source titles claiming0.442/0.443 do not establish measuredscores. The first-place publicscore was0.495 at inspection; rank1goalnotachieved.

## CPU score and fifth-slot candidate (2026-10-15 11:06 UTC)

CPU E006 v2 receipt57216989 completed with public **0.433**; GPU best remains **0.440**. Window30/80 are still pending. Fragment-gap completed with zero eligible rows and identical output, so it was not submitted. Four daily slots used, one remains.

Independently reviewed CPU_ALPHA075 version1 is running: https://www.kaggle.com/code/gwey1025/casmi26-cpu-e006-engine2-alpha075 (kernel138840608). It appends one final RRF weight experiment, Engine2 alpha0.6→0.75, with all35 parent cells unchanged. Exact same-run E006 reconstruction is mandatory before treatment; changed ranked official identities, chemistry/keyset/hash and inherited stage health must pass before submission. No added GPU allocation, inference pass or simulator pass. No score gain is claimed; top1 may change and score may worsen. Do not duplicate this pending run.

See evidence/20261015_2000/handoff.md and updated run-ledger. Rank1 remains unachieved; dataset version resolution and hidden-test generalization remain uncertain.

## Daily quota completed (2026-10-15 14:03 UTC)

CPU window30 receipt57222276 completed **0.433**, matching CPU control. GPU E006 remains best **0.440**. Window80 is pending.

CPU_ALPHA075 exactversion1 completed and passed independent acceptance: exact E006 same-run reconstruction;12official ranked rows changed,0top1changes;388visible placeholders unchanged; bothCPU ICE/GL stages healthy with0predictionfailures. Paired hashes and schema/keyset checks passed. Core smoke2145.56s plus overlay19.87s; full export2210.51s. NoGPUallocation. These smoke timings are not hidden-test timings.

Submitted https://www.kaggle.com/code/gwey1025/casmi26-cpu-e006-engine2-alpha075 version1, receipt **57233074**, pending. Post-submit limit confirms **5used /0remaining**,18total submissions. No further submissions today. Use the notebook hidden rerun, never the visible placeholder CSV directly.

Evidence and acceptance: evidence/20261015_2300. Next reconcile two pending scores, then choose an independently documented lowGPU hypothesis; rank1 remains unachieved. Keep this existing repository for all further versions.

## Window80 result and zero-inference comparison (2026-10-16 KST)

Window80 receipt57222283 completed **0.431**, below CPU control/window30 **0.433**. GPU best remains **0.440**. Alpha07557233074 is pending. Live daily limit still5used/0available despite KSTdatechange. No new notebook runs, submissions or GPU allocation in this check.

Downloaded exact GPUv1/CPUv2 candidate snapshots and verified both original hashes. Engine2 lists differ8/12visiblemolecules; PubChem ranked lists match despite numeric record differences. Some downstream differences remain despite identical saved upstream lists. These smoke observations do not establish the hidden0.007score-gap cause. See research/cpu-gpu-comparison-plan.md.

Prepared a threshold-only PubChemrel250→150 specification with paired downstream replay, truthful derivative provenance and mandatory retained integrity/health checks; not launched or scored. Fresh DmitriiV49 source adoptsrel150 but has no measured V49 score; external results remain authorclaims. See current source audit and evidence/20261016_0200. Preserve best0.440 and reconcile pending score before further trials.
