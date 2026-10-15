"""Paired append-only E006 experiment: Engine2 RRF contribution +25%.

The builder embeds the original row routine from frozen CPU E006 v2. The factory
defines its nested helpers and returns rerank_row without calling old run_overlay.
No learned model, retrieval, simulator budget or original source cell is changed.
"""


def load_row_routine(factory_source, scope):
    namespace = {}
    exec(compile(factory_source, 'frozen_e006_row_factory', 'exec'), namespace)
    return namespace['_alpha075_row_factory'](scope)


def run_alpha075_overlay(scope, factory_source, workdir='/kaggle/working'):
    import hashlib
    import json
    import os
    from pathlib import Path
    import time
    import pandas as pd

    started = time.monotonic()
    root = Path(workdir)
    path = root / 'submission.csv'
    baseline_bytes = path.read_bytes()
    baseline = pd.read_csv(path, dtype=str, keep_default_na=False)
    reference = pd.read_csv(root / 'submission_reference.csv', dtype=str, keep_default_na=False)
    assert list(baseline.columns) == list(reference.columns) == ['molecule_id', 'smiles']
    assert baseline.molecule_id.is_unique and reference.molecule_id.is_unique
    assert list(baseline.molecule_id) == list(reference.molecule_id)
    assert float(scope['ALPHA']) == 0.6 and float(scope['KRR']) == 3.0
    active = set(scope['te'].molecule_id.astype(str))
    assert active <= set(baseline.molecule_id)
    identity = scope['metric_identity']
    rerank_row = load_row_routine(factory_source, scope)
    treatment_scope = dict(scope, ALPHA=0.75)
    baseline_rows = dict(zip(baseline.molecule_id, baseline.smiles))
    output, audits = [], []
    for row in reference.itertuples(index=False):
        mid = str(row.molecule_id)
        original = row.smiles.split(';')
        processed = mid in active
        control, _ = rerank_row(scope, mid, original, window=40,
                                ice_fallback=True, processed=processed)
        # Always fail closed if source extraction or same-run inputs cannot
        # reproduce the completed E006 CSV exactly, including representatives.
        assert ';'.join(control) == baseline_rows[mid], f'E006 paired control mismatch: {mid}'
        revised, branch = rerank_row(treatment_scope, mid, original, window=40,
                                    ice_fallback=True, processed=processed)
        assert 1 <= len(control) <= 25 and 1 <= len(revised) <= 25
        old_keys, new_keys = [identity(s) for s in control], [identity(s) for s in revised]
        if processed:
            assert None not in old_keys and len(old_keys) == len(set(old_keys)), mid
            assert None not in new_keys and len(new_keys) == len(set(new_keys)), mid
        else:
            assert revised == control and ';'.join(revised) == baseline_rows[mid], mid
        audits.append(dict(molecule_id=mid, processed=processed, branch=branch['branch'],
                           changed_strings=revised != control,
                           ranked_identity_changed=new_keys != old_keys,
                           top1_string_changed=revised[:1] != control[:1],
                           top1_identity_changed=new_keys[:1] != old_keys[:1],
                           added_identities=len(set(new_keys)-set(old_keys)),
                           dropped_identities=len(set(old_keys)-set(new_keys)),
                           candidate_count=branch['candidate_count']))
        output.append((row.molecule_id, ';'.join(revised)))
    frame = pd.DataFrame(output, columns=['molecule_id', 'smiles'])
    assert list(frame.molecule_id) == list(baseline.molecule_id)
    assert frame.molecule_id.is_unique and set(frame.molecule_id) == set(baseline.molecule_id)
    assert frame.smiles.map(lambda s: 1 <= len(s.split(';')) <= 25).all()
    identity_changes = sum(a['ranked_identity_changed'] for a in audits)
    # Preserve inherited E004/E006 audit files; keep our own exact paired control.
    (root / 'submission_alpha075_control.csv').write_bytes(baseline_bytes)
    if identity_changes:
        temporary = root / 'submission.alpha075.tmp.csv'
        frame.to_csv(temporary, index=False)
        os.replace(temporary, path)
    else:
        # Representative-only changes are not a distinct scored experiment.
        assert path.read_bytes() == baseline_bytes
    report = dict(experiment='CPU_ALPHA075', score_status='unmeasured',
                  base='frozen CPU E006 v2', control_alpha=0.6, treatment_alpha=0.75,
                  engine2_contribution_multiplier=1.25, offset=3.0, window=40,
                  ice_fallback=True, source_row_routine_preserved=True,
                  paired_e006_control_reconstructed=True,
                  factory_sha256=hashlib.sha256(factory_source.encode()).hexdigest(),
                  rows=len(frame), active_rows=len(active),
                  changed_rows=sum(a['changed_strings'] for a in audits),
                  ranked_identity_changed_rows=identity_changes,
                  top1_string_changes=sum(a['top1_string_changed'] for a in audits),
                  top1_identity_changes=sum(a['top1_identity_changed'] for a in audits),
                  added_identities=sum(a['added_identities'] for a in audits),
                  dropped_identities=sum(a['dropped_identities'] for a in audits),
                  baseline_sha256=hashlib.sha256(baseline_bytes).hexdigest(),
                  treatment_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  elapsed_seconds=time.monotonic()-started,
                  submission_eligible=bool(identity_changes),
                  limitations=['Visible smoke is mechanical validation only.',
                               'More Engine2 support can worsen MRR and change top1.',
                               'Top40 membership may change within the existing two-engine union.',
                               'No new inference, retrieval, model or simulator pass.'])
    pd.DataFrame(audits).to_csv(root / 'alpha075_audit.csv', index=False)
    (root / 'alpha075_audit.json').write_text(json.dumps(dict(report=report, rows=audits),
                                                       indent=2, allow_nan=False))
    print('CPU_ALPHA075_AUDIT', json.dumps(report, allow_nan=False))
    return report


if __name__ == '__main__':
    ALPHA075_REPORT = run_alpha075_overlay(globals(), ALPHA075_FACTORY_SOURCE)
