"""Create controlled CPU E006 final-fusion window variants; never launch."""
import ast
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'notebooks/cpu-e006-v2/cpu_e006_v2.ipynb'
base = json.loads(SOURCE.read_text())
source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
needle = "return run_overlay(scope, **{'experiment': 'E006', 'window': 40, 'ice_fallback': True"
original = ''.join(base['cells'][-1]['source'])
assert original.count(needle) == 1
hypotheses = {
    30: 'Conservative final fusion shortlist: restrict same-formula forward reranking to 30 candidates, reducing lower-support distractors. May exclude a correct candidate ranked 31–40.',
    80: 'Expanded final fusion shortlist: retain up to 80 candidates from the existing two-engine union before same-formula forward reranking. May recover lower-ranked answers but dilute strong candidates; no new simulator pass or retrieval.'
}
for window in (30, 80):
    label = f'CPU_WINDOW{window}'
    variant = copy.deepcopy(base)
    replacement = f"return run_overlay(scope, **{{'experiment': '{label}', 'window': {window}, 'ice_fallback': True"
    final = original.replace(needle, replacement)
    if window == 30:
        guard = 'if window not in (40, 80):'
        assert final.count(guard) == 1
        final = final.replace(guard, 'if window not in (30, 40, 80):').replace('Only the prespecified 40/80 candidate windows are supported', 'Only the prespecified 30/40/80 candidate windows are supported')
    normalized = final.replace(replacement, needle)
    if window == 30:
        normalized = normalized.replace('if window not in (30, 40, 80):', 'if window not in (40, 80):').replace('Only the prespecified 30/40/80 candidate windows are supported', 'Only the prespecified 40/80 candidate windows are supported')
    assert normalized == original
    variant['cells'][-1]['source'] = final.splitlines(keepends=True)
    for i, cell in enumerate(variant['cells']):
        ast.parse(''.join(cell['source']))
        assert cell['source'] == base['cells'][i]['source'] or i == len(base['cells']) - 1
    # No global configuration, model, simulator, CPU, or budget settings change.
    variant['metadata']['controlled_window_experiment'] = dict(
        experiment=label, source_notebook=str(SOURCE.relative_to(ROOT)), source_sha256=source_hash,
        only_parameter_change=f'final run_overlay window40 -> window{window}',
        validation_guard_change='allow30 in existing40/80 guard and update error text' if window == 30 else None,
        hypothesis=hypotheses[window], improvement_claim=None,
        validation='AST valid; exact source equality after normalizing final experiment label/window and required30 validation guard',
        runtime='CPUv2 visible smoke completed2469.75sec with ICE/GL ok; new variant and hidden run unmeasured')
    out = ROOT / f'notebooks/cpu-window{window}' / f'cpu_window{window}.ipynb'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(variant, indent=1) + '\n')
    print(out, hashlib.sha256(out.read_bytes()).hexdigest())
