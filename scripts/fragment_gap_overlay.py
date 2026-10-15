"""Bounded CPU fragment evidence for E006's existing final candidate universe.

Adapted evidence kernel: dmitriigluzdov/casmi-26-from-spectra-to-structures v47,
cell 118, attributed there to Ahmed Berat Özer's v7c and Huseyin Emre Aksoy
(Apache-2.0). The kernel is embedded verbatim by build_cpu_fragment_gap.py.
Our adapter preserves the final25 candidate identity set, applies only without
GLACIER coverage, and bounds CPU scoring in a checkpointed subprocess.
Author-reported V46 0.441 does not establish this derivative's score.
"""
import math


def finite_scores(values):
    return any(v is not None and math.isfinite(float(v)) for v in values.values())


def checked_reorder(candidates, identities, order):
    """Require a true permutation; no candidate insertion, omission or duplication."""
    if sorted(order) != list(range(len(candidates))):
        raise ValueError('Reranker returned a non-permutation')
    revised = [candidates[i] for i in order]
    new_ids = [identities[i] for i in order]
    assert len(new_ids) == len(set(new_ids)) and set(new_ids) == set(identities)
    return revised


FRAGMENT_WORKER = r'''
import json, os, sys, time
import numpy as np
os.environ['CUDA_VISIBLE_DEVICES'] = ''
from rdkit import rdBase
assert rdBase.rdkitVersion == '2026.03.3'
import bounded_frag_rescore as frag

def save(value, path):
    temp = path + '.tmp'
    with open(temp, 'w') as handle:
        json.dump(value, handle, allow_nan=False)
    os.replace(temp, path)

if __name__ == '__main__':
    inp, out = sys.argv[1:]
    tasks = json.load(open(inp))
    result = {'complete': {}, 'errors': {}, 'warmup': False}
    save(result, out)
    frag.warmup()
    result['warmup'] = True
    save(result, out)
    cache = {}
    for mid, task in tasks.items():
        try:
            spectra = [dict(s, mz=np.asarray(s['mz'], np.float64), it=np.asarray(s['it'], np.float64))
                       for s in task['spectra']]
            values = frag.score_molecule(spectra, task['candidates'], cache=cache)
            if len(values) != len(task['candidates']) or any(v is None for v in values):
                raise ValueError('Missing fragment coverage')
            values = [float(v) for v in values]
            if not np.isfinite(values).all():
                raise ValueError('Nonfinite fragment coverage')
            result['complete'][mid] = dict(candidates=task['candidates'], scores=values)
        except Exception as error:
            result['errors'][mid] = repr(error)
        save(result, out)
    print('CPU_FRAGMENT_WORKER_COMPLETE', len(result['complete']), flush=True)
'''


def run_bounded_fragment_overlay(scope, fragment_source, workdir='/kaggle/working'):
    import hashlib
    import json
    import os
    from pathlib import Path
    import signal
    import subprocess
    import sys
    import time
    import numpy as np
    import pandas as pd

    started = time.monotonic()
    root = Path(workdir)
    path = root / 'submission.csv'
    baseline_bytes = path.read_bytes()
    (root / 'submission_fragment_control.csv').write_bytes(baseline_bytes)
    baseline = pd.read_csv(path, dtype=str, keep_default_na=False)
    identity = scope['metric_identity']
    active = set(scope['te'].molecule_id.astype(str))
    groups = {str(mid): sub for mid, sub in scope['te'].groupby('molecule_id', sort=False)}
    tasks, supports, audit, optional_errors = {}, {}, {}, []
    for row in baseline.itertuples(index=False):
        mid = str(row.molecule_id)
        audit[mid] = dict(molecule_id=mid, branch='inactive_placeholder', changed=False,
                          changed_top1=False, ice_used=False)
        if mid not in active:
            continue
        candidates = row.smiles.split(';')
        ids = [identity(s) for s in candidates]
        assert None not in ids and len(ids) == len(set(ids)), mid
        audit[mid]['branch'] = 'glacier_covered'
        try:
            glacier_covered = bool(scope['gl_of'](mid))
        except Exception as error:
            audit[mid].update(branch='task_preparation_failed_preserve_baseline', error=repr(error))
            optional_errors.append(dict(stage='task_preparation', molecule_id=mid, error=repr(error)))
            continue
        if glacier_covered:
            continue
        audit[mid]['branch'] = 'insufficient_candidates'
        if len(candidates) < 2:
            continue
        try:
            engine = scope['ENG'].get(mid, {})
            first = [s for s in scope['PREFUSION_LISTS'].get(mid, []) if s and s != 'CCO']
            union, scores, _ = scope['metric_fusion'](
                first, engine.get('smiles', []), identity,
                alpha=scope['ALPHA'], offset=scope['KRR'], limit=1000)
            by_id = dict(zip(map(identity, union), map(float, scores)))
            audit[mid]['branch'] = 'missing_fusion_support'
            if any(k not in by_id for k in ids):
                continue
            spectra = [dict(mz=np.asarray(r.ms2_mzs, np.float64).tolist(),
                            it=np.asarray(r.ms2_normalized_intensities, np.float64).tolist(),
                            adduct=str(r.adduct), prec=float(r.precursor_mz),
                            mode=1 if r.ionization_mode == 'positive' else -1)
                       for r in groups[mid].itertuples(index=False)][:16]
            if not spectra:
                audit[mid]['branch'] = 'missing_spectra'
                continue
            support = [by_id[k] for k in ids]
            if not np.isfinite(support).all():
                raise ValueError('Nonfinite fusion support')
            task = dict(candidates=candidates, spectra=spectra)
            # Detect NaN/Infinity and serialization errors per molecule, before
            # adding anything to the shared optional worker payload.
            json.dumps(task, allow_nan=False)
            supports[mid], tasks[mid] = support, task
            audit[mid]['branch'] = 'no_complete_fragment_checkpoint'
        except Exception as error:
            audit[mid].update(branch='task_preparation_failed_preserve_baseline', error=repr(error))
            optional_errors.append(dict(stage='task_preparation', molecule_id=mid, error=repr(error)))

    budget = 900 if scope['IS_RERUN'] else 120
    # Retain the enclosing 8h30 watchdog and reserve time for final assertions/write.
    remaining = signal.getitimer(signal.ITIMER_REAL)[0]
    if remaining > 0:
        budget = min(budget, max(0, remaining - 30))
    worker_result = {'complete': {}, 'errors': {}, 'warmup': False}
    timed_out, worker_rc = False, None
    output = root / 'fragment_worker_output.json'
    if tasks and budget >= 1:
        launch_attempted = False
        try:
            (root / 'bounded_frag_rescore.py').write_text(fragment_source)
            (root / 'bounded_fragment_worker.py').write_text(FRAGMENT_WORKER)
            inp = root / 'fragment_worker_input.json'
            inp.write_text(json.dumps(tasks, allow_nan=False))
            output.unlink(missing_ok=True)
            env = dict(os.environ, CUDA_VISIBLE_DEVICES='')
            launch_attempted = True
            proc = subprocess.run([sys.executable, str(root / 'bounded_fragment_worker.py'),
                                   str(inp), str(output)], env=env, cwd=str(root),
                                  capture_output=True, text=True, timeout=budget)
            worker_rc = proc.returncode
            print(proc.stdout[-1500:], proc.stderr[-1500:])
            if worker_rc != 0:
                optional_errors.append(dict(stage='worker_exit', returncode=worker_rc,
                                            stderr=proc.stderr[-1500:]))
        except subprocess.TimeoutExpired:
            timed_out = True
            print('CPU fragment deadline: preserve baseline for every unfinished molecule')
        except Exception as error:
            optional_errors.append(dict(stage='worker_setup_or_launch', error=repr(error)))
        if launch_attempted:
            try:
                if output.is_file():
                    result = json.loads(output.read_text())
                    if not isinstance(result, dict) or not isinstance(result.get('complete'), dict) or not isinstance(result.get('errors'), dict) or not isinstance(result.get('warmup'), bool):
                        raise ValueError('Malformed worker checkpoint schema')
                    # Validate the entire checkpoint before accepting its contents.
                    for mid, entry in result['complete'].items():
                        if mid not in tasks or not isinstance(entry, dict) or entry.get('candidates') != tasks[mid]['candidates']:
                            raise ValueError('Checkpoint candidate universe mismatch')
                        values = entry.get('scores')
                        if not isinstance(values, list) or len(values) != len(tasks[mid]['candidates']) or not np.isfinite(np.asarray(values, float)).all():
                            raise ValueError('Incomplete or nonfinite checkpoint scores')
                    json.dumps(result, allow_nan=False)
                    worker_result = result
            except Exception as error:
                optional_errors.append(dict(stage='checkpoint_read', error=repr(error)))

    rows = []
    for row in baseline.itertuples(index=False):
        mid, original = str(row.molecule_id), row.smiles.split(';')
        revised = list(original)
        evidence = worker_result['complete'].get(mid)
        if mid in tasks and evidence and evidence.get('candidates') == original:
            try:
                frag = dict(zip(original, evidence['scores']))
                ice = scope['ICE_SCORES'].get(mid, {}) or {}
                if finite_scores(ice):
                    channels, weights = [ice, frag], [scope['ICE_LAM'], 0.5]
                    audit[mid]['ice_used'] = True
                else:
                    channels, weights = [frag], [0.5]
                keys = [scope['chem'].score_key(s) or s for s in original]
                forms = [scope['_form2'](s) for s in original]
                order = scope['gl_fuse'].rerank_multi(original, keys, supports[mid], forms,
                                                     channels, weights, top_n=len(original))
                revised = checked_reorder(original, [identity(s) for s in original], list(order))
                # The upstream function must preserve formula slots, too.
                assert [scope['_form2'](s) for s in revised] == forms
                audit[mid]['branch'] = 'ice_plus_fragment' if audit[mid]['ice_used'] else 'fragment_only'
            except Exception as error:
                revised = list(original)
                audit[mid].update(branch='rerank_failed_preserve_baseline', error=repr(error))
        if mid not in tasks:
            assert revised == original
        if mid in active:
            ids = [identity(s) for s in revised]
            assert None not in ids and len(ids) == len(set(ids))
            assert set(ids) == set(map(identity, original)), mid
        audit[mid].update(changed=revised != original, changed_top1=revised[:1] != original[:1])
        rows.append((row.molecule_id, ';'.join(revised)))
    frame = pd.DataFrame(rows, columns=['molecule_id', 'smiles'])
    assert list(frame.molecule_id) == list(baseline.molecule_id) and frame.molecule_id.is_unique
    assert frame.smiles.map(lambda s: 1 <= len(s.split(';')) <= 25).all()
    # A no-op retains the original byte sequence exactly.
    if any(a['changed'] for a in audit.values()):
        temporary_submission = root / 'submission.fragment.tmp.csv'
        frame.to_csv(temporary_submission, index=False)
        os.replace(temporary_submission, path)
    else:
        assert path.read_bytes() == baseline_bytes
    report = dict(experiment='CPU_E006_bounded_fragment_noGL', score_status='unmeasured',
                  inference_added='CPU two-cleavage fragment scoring only; no learned model/retrieval',
                  candidate_universe='same final25 metric identities; formula slots preserved',
                  source='https://www.kaggle.com/code/dmitriigluzdov/casmi-26-from-spectra-to-structures',
                  source_version=47, upstream_v46_score='author-reported0.441; not this derivative',
                  fragment_source_sha256=hashlib.sha256(fragment_source.encode()).hexdigest(),
                  eligible=len(tasks), complete=len(worker_result['complete']),
                  worker_errors=worker_result['errors'], worker_returncode=worker_rc,
                  optional_errors=optional_errors,
                  worker_warmup=worker_result['warmup'], worker_timed_out=timed_out,
                  budget_seconds=budget, elapsed_seconds=time.monotonic()-started,
                  rows=len(frame), active_rows=len(active),
                  changed_rows=sum(a['changed'] for a in audit.values()),
                  top1_changes=sum(a['changed_top1'] for a in audit.values()),
                  baseline_sha256=hashlib.sha256(baseline_bytes).hexdigest(),
                  treatment_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  limitations=['Visible smoke is mechanical validation only.',
                               'Final25 universe restriction differs from upstream40 fusion.',
                               'Timeout keeps only completed whole-molecule checkpoints.'])
    report['submission_eligible'] = report['baseline_sha256'] != report['treatment_sha256']
    pd.DataFrame(audit.values()).to_csv(root / 'fragment_overlay_audit.csv', index=False)
    (root / 'fragment_overlay_audit.json').write_text(json.dumps(dict(report=report, rows=list(audit.values())), indent=2, allow_nan=False))
    print('CPU_FRAGMENT_OVERLAY', json.dumps(report, allow_nan=False))
    return report


if __name__ == '__main__':
    FRAGMENT_OVERLAY_REPORT = run_bounded_fragment_overlay(globals(), FRAGMENT_SOURCE)
