"""Append only a rank-2 overlay to the frozen successful CPU E006 v2."""
import ast
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'notebooks/cpu-e006-v2/cpu_e006_v2.ipynb'
helper = ROOT / 'scripts/rank2_overlay.py'
out = ROOT / 'notebooks/cpu-rank2'
out.mkdir(parents=True, exist_ok=True)
notebook = json.loads(source.read_bytes())
original_cells = len(notebook['cells'])
code = helper.read_text() + '\nRANK2_REPORT = run_rank2_overlay(globals())\n'
ast.parse(code)
notebook['cells'].append(dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=code.splitlines(keepends=True)))
assert notebook['cells'][:-1] == json.loads(source.read_bytes())['cells']
notebook['metadata']['cpu_rank2_notes'] = dict(source_notebook_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), source_cells=original_cells,
    overlay_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(), new_inference=False, score_status='unmeasured')
target = out / 'cpu_rank2.ipynb'
target.write_text(json.dumps(notebook, indent=1) + '\n')
metadata = json.loads((source.parent / 'kernel-metadata.json').read_text())
metadata.update(id='gwey1025/casmi26-cpu-e006-engine2-rank2', title='CASMI26 CPU E006 Engine2 Rank2', code_file=target.name)
assert metadata['enable_gpu'] is False and metadata['is_private'] is True
(out / 'kernel-metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
manifest = dict(source_notebook=str(source.relative_to(ROOT)), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    source_metadata_sha256=hashlib.sha256((source.parent / 'kernel-metadata.json').read_bytes()).hexdigest(),
    derivative_sha256=hashlib.sha256(target.read_bytes()).hexdigest(), overlay_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),
    inherited_cells_unchanged=True, additional_cells=1, score_status='unmeasured', launched=False,
    dataset_sources=metadata['dataset_sources'],
    dataset_version_note='Dataset source slugs inherited exactly; resolved versions require runtime evidence.')
(out / 'build_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))
