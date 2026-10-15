# Dmitrii V49 source update — 2026-10-16 02:00KST audit

Source: https://www.kaggle.com/code/dmitriigluzdov/casmi-26-from-spectra-to-structures
Fetched version49; SHA256 `646626ce028774af76dfe5addf0320e547e7f90408b493713efb487578e9201e`.
Read-only pull, no execution. The index and pull metadata timestamps conflict;
both are retained in `evidence/20261016_0200/dmitrii_source_audit.json`.
No new independently verified score is established by this pull.

Material code changes versus our saved V47:

- PubChem promotion threshold250→150 in cell110, following seyitkaangunes.
- Reverts the V47 fragment+ICEBERG mixture: fragment evidence is now computed
  only when neither GLACIER nor ICEBERG has scores. ICE-covered/noGL molecules
  retain the ordinary ICE fallback.
- Adds Engine2rank2 overlay, introduced in V48, with official metric identity
  checks, paired hashes and atomic replacement.
- Mounted-input inventory uses full hashes for files<=32MB and explicitly
  labelled size+4MBhead+4MBtail digests for larger files. Author says previous
  full inventory reads took>2hours. This is a receipt I/O optimization, not a
  prediction change or full-hash equivalence. A separate full train.parquet
  digest still remains in the receipt.

Author-reported outcomes, not independently verified:

- V46fragment-only-no-forward gate0.441; V47ICE+fragment0.440 (negative result).
- V48Engine2rank2 overlay0.443; V49rel150 result is not supplied.
- Other E0060.440 ablations: multi-CE GLACIER0.436; centroiding0.440;
  polarity/adduct-specific fingerprint merge0.424; JESTRfusion0.418;
  CFM-IDreranking0.440 at0.25weight and0.422 at1.0weight.

Implication: prioritize the separately specified controlled promotion150 test,
not the discarded ICE+fragment mixture or additional simulator passes. Do not
bundle V48rank2 with threshold changes if estimating the threshold effect on our
fixed CPU E006 baseline. No notebook launch or submission was performed here.
