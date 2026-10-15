"""CPU E006 rank-2 experiment. Reuses same-run predictions; no inference.
Adaptation of antriksharya/casmi26-lb-0-443-v7c-engine-2-rank-2-insert,
using the inherited official metric_identity for every comparison.
No score or CPU/GPU numerical equivalence is claimed.
"""

def rank2_transform(original, engine_candidates, identity):
    original = list(original)
    keys = [identity(s) for s in original]
    assert 1 <= len(original) <= 25
    assert all(k is not None for k in keys) and len(keys) == len(set(keys))
    audit = dict(action='no_engine_candidate', engine2_original_rank=None,
                 old_count=len(original), new_count=len(original), dropped_candidates=[])
    if original[0] == 'CCO':
        audit['action'] = 'skip_baseline_fallback'
        return original, audit
    eligible = [s for s in (engine_candidates or []) if s and s != 'CCO']
    if not eligible:
        return original, audit
    candidate = eligible[0]
    key = identity(candidate)
    if key is None:
        audit['action'] = 'skip_invalid_engine_candidate'
        return original, audit
    rank = keys.index(key) + 1 if key in keys else None
    audit['engine2_original_rank'] = rank
    if rank in (1, 2):
        audit['action'] = 'already_rank_' + str(rank)
        return original, audit
    tail = [s for s, k in zip(original[1:], keys[1:]) if k != key]
    revised = ([original[0], candidate] + tail)[:25]
    newkeys = [identity(s) for s in revised]
    assert revised[0] == original[0] and newkeys[0] == keys[0]
    assert all(k is not None for k in newkeys) and len(newkeys) == len(set(newkeys))
    assert 1 <= len(revised) <= 25
    assert newkeys[1] == key
    audit.update(action='move_existing' if rank else 'insert_new', new_count=len(revised),
                 dropped_candidates=[s for s, k in zip(original, keys) if k not in set(newkeys)])
    return revised, audit


def run_rank2_overlay(scope):
    import hashlib
    import io
    import json
    import os
    from collections import Counter
    from pathlib import Path
    import pandas as pd
    from rdkit import Chem

    identity = scope['metric_identity']
    original_identity = identity
    def checked_identity(smiles):
        if not isinstance(smiles, str) or not smiles or Chem.MolFromSmiles(smiles) is None:
            return None
        return original_identity(smiles)
    path = Path('submission.csv')
    baseline_bytes = path.read_bytes()
    Path('rank2_baseline_submission.csv').write_bytes(baseline_bytes)
    baseline = pd.read_csv(io.BytesIO(baseline_bytes), dtype=str, keep_default_na=False)
    sample = pd.read_csv(os.path.join(scope['COMP'], 'sample_submission.csv'), dtype=str)
    assert list(baseline.columns) == ['molecule_id', 'smiles']
    assert baseline.molecule_id.is_unique
    assert baseline.molecule_id.tolist() == sample.molecule_id.tolist()
    active = set(scope['te'].molecule_id.astype(str))
    expected = set(sample.molecule_id)
    assert active <= expected
    if scope['IS_RERUN']:
        assert active == expected
    engines = {str(k): v for k, v in scope['ENG'].items()}
    assert active <= set(engines)
    treatment = baseline.copy()
    audits = []
    identity_changes = string_changes = top1_string_changes = top1_identity_changes = 0
    for i, row in baseline.iterrows():
        original = row.smiles.split(';')
        oldkeys = [checked_identity(s) for s in original]
        assert 1 <= len(original) <= 25 and all(k is not None for k in oldkeys)
        assert len(oldkeys) == len(set(oldkeys))
        if row.molecule_id in active:
            revised, audit = rank2_transform(original, engines[row.molecule_id].get('smiles', []), checked_identity)
        else:
            revised = original
            audit = dict(action='skip_inactive_placeholder', engine2_original_rank=None,
                         old_count=len(original), new_count=len(original), dropped_candidates=[])
        newkeys = [checked_identity(s) for s in revised]
        assert all(k is not None for k in newkeys) and len(newkeys) == len(set(newkeys))
        assert original[0] == revised[0] and oldkeys[0] == newkeys[0]
        changed = original != revised
        string_changes += int(changed)
        identity_changes += int(oldkeys != newkeys)
        top1_string_changes += int(original[0] != revised[0])
        top1_identity_changes += int(oldkeys[0] != newkeys[0])
        audit.update(molecule_id=row.molecule_id, active=row.molecule_id in active,
                     changed=changed, ranked_identities_changed=oldkeys != newkeys)
        audits.append(audit)
        treatment.at[i, 'smiles'] = ';'.join(revised)
    assert treatment.molecule_id.tolist() == baseline.molecule_id.tolist()
    assert not top1_string_changes and not top1_identity_changes
    # Preserve exact original bytes when the transformation is a no-op.
    treatment_bytes = treatment.to_csv(index=False).encode() if string_changes else baseline_bytes
    path.write_bytes(treatment_bytes)
    report = dict(experiment='CPU_E006_Engine2_rank2', score_status='unmeasured',
                  source='https://www.kaggle.com/code/antriksharya/casmi26-lb-0-443-v7c-engine-2-rank-2-insert',
                  inference_added=False, rows=len(baseline), active_rows=len(active),
                  changed_rows=string_changes, ranked_identity_changed_rows=identity_changes,
                  top1_string_changes=top1_string_changes, top1_identity_changes=top1_identity_changes,
                  baseline_sha256=hashlib.sha256(baseline_bytes).hexdigest(),
                  treatment_sha256=hashlib.sha256(treatment_bytes).hexdigest(),
                  actions=dict(Counter(a['action'] for a in audits)),
                  submission_eligible=bool(string_changes and identity_changes and baseline_bytes != treatment_bytes),
                  limitation='Top-1 preservation does not preserve MRR; smoke is mechanical validation only.')
    pd.DataFrame(audits).to_csv('rank2_row_audit.csv', index=False)
    Path('rank2_audit.json').write_text(json.dumps(dict(report=report, rows=audits), indent=2) + '\n')
    print('RANK2_AUDIT', json.dumps(report))
    return report
