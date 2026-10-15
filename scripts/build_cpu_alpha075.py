"""Build append-only CPU_ALPHA075 derivative, without launching it."""
import ast
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'notebooks/cpu-e006-v2/cpu_e006_v2.ipynb'
ADAPTER = ROOT / 'scripts/alpha075_overlay.py'
OUTPUT = ROOT / 'notebooks/cpu-alpha075/cpu_alpha075.ipynb'

base = json.loads(BASE.read_text())
tree = ast.parse(''.join(base['cells'][-1]['source']))
original_factory = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                        and n.name == '_factorial_entry')
original_row = next(n for n in original_factory.body if isinstance(n, ast.FunctionDef)
                    and n.name == 'rerank_row')
factory = copy.deepcopy(original_factory)
factory.name = '_alpha075_row_factory'
assert isinstance(factory.body[-1], ast.Return)
factory.body[-1] = ast.Return(value=ast.Name(id='rerank_row', ctx=ast.Load()))
factory_source = ast.unparse(ast.fix_missing_locations(factory)) + '\n'
rebuilt = ast.parse(factory_source).body[0]
rebuilt_row = next(n for n in rebuilt.body if isinstance(n, ast.FunctionDef)
                   and n.name == 'rerank_row')
assert ast.dump(rebuilt_row, include_attributes=False) == ast.dump(original_row, include_attributes=False)
assert isinstance(rebuilt.body[-1].value, ast.Name) and rebuilt.body[-1].value.id == 'rerank_row'
adapter = ADAPTER.read_text()
ast.parse(adapter)
notebook = copy.deepcopy(base)
source = 'ALPHA075_FACTORY_SOURCE = ' + repr(factory_source) + '\n\n' + adapter
notebook['cells'].append(dict(cell_type='code', execution_count=None, metadata={}, outputs=[],
                              source=source.splitlines(keepends=True)))
assert notebook['cells'][:-1] == base['cells']
for cell in notebook['cells']:
    ast.parse(''.join(cell['source']))
notebook['metadata']['alpha075_experiment'] = dict(
    source=str(BASE.relative_to(ROOT)), source_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
    factory_sha256=hashlib.sha256(factory_source.encode()).hexdigest(),
    adapter_sha256=hashlib.sha256(adapter.encode()).hexdigest(),
    hypothesis='Increase Engine2 RRF contribution by25percent, alpha0.6->0.75; no improvement claimed',
    scope='one appended overlay; original35cells unchanged; model/retrieval/window40/budgets unchanged',
    control='reconstruct exact same-run E006alpha0.6 with ICEfallbackTrue, not E004',
    score_status='unmeasured', top1_changes='allowed; audit required',
    submission_eligibility='changed ranked official identities; no-op retains baseline bytes')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(notebook, indent=1) + '\n')
print(OUTPUT)
print('SHA256', hashlib.sha256(OUTPUT.read_bytes()).hexdigest())
