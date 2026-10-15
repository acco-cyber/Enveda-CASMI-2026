# Rank-2 insertion experiment plan

Status: preparation only. No launch, new submission, or measured improvement. The public source title contains “LB 0.443”; fetched source does not independently establish that score. Its upstream v7c describes author-reported 0.441, E006 author-reported 0.440. Our CPU E006 score and CPU/GPU equivalence remain unmeasured.

Source: https://www.kaggle.com/code/antriksharya/casmi26-lb-0-443-v7c-engine-2-rank-2-insert — local reference/new/casmi26-lb-0-443-v7c-engine-2-rank-2-insert.ipynb, cell 34. Inherited upstream attribution and component licences must remain.

## Proposed single change

After the complete CPU E006 pipeline and its checks succeed, take the existing Engine2 first candidate and move or insert it at rank 2 when its official metric identity differs from rank 1. Leave rank 1 unchanged. Reuse the same-run Engine2 candidate list and final submission; no model inference, candidate retrieval, external data, or GPU allocation is added. Do not add rank2e1 or fragment reranking in this experiment.

The source applies the rank-2 overlay to v7c (E006 plus no-forward-evidence fragment fallback). Applying it to our E006 is a different baseline, so neither its stated score nor its delta can be transferred.

## Official identity requirement

The source `_keyi` validates RDKit parsing and calls `chem.score_key`. It removes equivalent copies of the inserted candidate under that function, but does not prove that this equals the official tautomer-canonical InChIKey14 identity. The source also never asserts full final-row identity uniqueness. Therefore official metric uniqueness is not established by this overlay alone.

Use the already loaded `metric_identity` (RDKit 2026.03.3, tautomer-canonical, connectivity block) for every comparison. Require all baseline candidates to be valid and identity-unique first. If the inserted candidate matches rank 1, do nothing. Remove its existing equivalent tail representative, insert the Engine2 representative at rank 2, truncate at 25, then assert validity, unique official identities, and exactly unchanged rank-1 identity AND string. No raw-SMILES-only duplicate comparison.

The source excludes `CCO`, an inherited fallback marker that is also valid ethanol. Preserve the source eligibility policy for a faithful comparison; report skipped fallback rows. An experiment changing fallback policy is separate.

## Acceptance and paired audit

- Freeze the successful E006 notebook version and dataset versions before making a derivative.
- Keep the exact same-run baseline CSV bytes and SHA256.
- Verify hidden input IDs dynamically; no hardcoded molecule IDs or predictions.
- Assert output IDs, order, row count, valid candidate lists of length 1–25, unique official identities, and zero changed top-1 strings/identities.
- Audit each row: original Engine2 rank under official identity; whether insertion happened; old/new candidate count; dropped final candidate; baseline and treatment hashes.
- Distinguish no-op (already rank 1/2), move from rank 3–25, and new candidate insertion.
- Do not spend a submission if final bytes or official ranked identities are unchanged.
- Submit only after CPU smoke health passes; the 1800-second ICE smoke fix and full hidden runtime are not yet verified.

Preserving top 1 does not preserve MRR@25: shifting the existing rank-2 truth to rank 3 changes its contribution from 1/2 to 1/3; inserting a previously absent correct candidate could improve a zero contribution to 1/2. Rank-25 removal can lose a correct tail candidate. Evaluate paired molecule-level reciprocal ranks on a held-out natural-product split where labels exist; visible placeholder smoke is only mechanical validation.

## Exact inherited source cell (reference, not launched)

```python
# ---- engine insert overlay, MODE = 'rank2' ----
import shutil as _shi
from rdkit import Chem as _Chi
MODE = 'rank2'
_shi.copyfile('submission.csv', 'submission_base.csv')
_sub = pd.read_csv('submission_base.csv')
def _keyi(s):
    if not isinstance(s, str) or not s or s == 'CCO':
        return None
    try:
        return (chem.score_key(s) or None) if _Chi.MolFromSmiles(s) is not None else None
    except Exception:
        return None
_B = {str(k): v for k, v in BASE.items()} if isinstance(BASE, dict) else {}
def _top(lst):
    l = [x for x in (lst or []) if x and x != 'CCO']
    return l[0] if l and _keyi(l[0]) else None
def _insert(toks, x, pos):
    kx = _keyi(x)
    keys = [_keyi(t) or t for t in toks]
    if kx in keys[:pos]:
        return toks, False
    rest = [t for t, k in zip(toks, keys) if k != kx]
    return (rest[:pos] + [x] + rest[pos:])[:25], True
_st = dict(rows=0, e2_ins=0, e1_ins=0)
_rows = []
for m, s in zip(_sub.molecule_id, _sub.smiles):
    _st['rows'] += 1
    toks = [t for t in str(s).split(';') if t]
    if toks and toks[0] != 'CCO':
        e = ENG.get(str(m)) if isinstance(ENG, dict) else None
        x2 = _top(e.get('smiles')) if e else None
        if x2 and _keyi(x2) != _keyi(toks[0]):
            toks, ch = _insert(toks, x2, 1); _st['e2_ins'] += int(ch)
        if MODE == 'rank2e1':
            b = _B.get(str(m))
            x1 = _top(list(b[0])) if b else None
            if x1:
                toks, ch = _insert(toks, x1, 2); _st['e1_ins'] += int(ch)
    _rows.append((m, ';'.join(toks) if toks else str(s)))
_fs = pd.DataFrame(_rows, columns=['molecule_id', 'smiles'])
_samp = pd.read_csv(os.path.join(COMP, 'sample_submission.csv'))
assert len(_fs) == len(_sub) == len(_samp) and _fs.molecule_id.is_unique and _fs.smiles.notna().all()
assert set(_fs.molecule_id.astype(str)) == set(_samp.molecule_id.astype(str))
assert _fs.smiles.map(lambda x: len(x.split(';'))).max() <= 25
_fs.to_csv('submission.csv', index=False)
open('probe_applied.txt', 'w').write(json.dumps(_st))
print(f'ENGINE INSERT APPLIED mode={MODE}:', json.dumps(_st), flush=True)
```
