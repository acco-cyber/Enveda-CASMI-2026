"""Build the bounded CPU fragment experiment without launching it."""
import ast
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'notebooks/cpu-e006-v2/cpu_e006_v2.ipynb'
REFERENCE = ROOT / 'reference/20261015_1400/dmitriigluzdov__casmi-26-from-spectra-to-structures.ipynb'
ADAPTER = ROOT / 'scripts/fragment_gap_overlay.py'
OUTPUT = ROOT / 'notebooks/cpu-fragment-gap/cpu_fragment_gap.ipynb'

reference = json.loads(REFERENCE.read_text())
fragment_cell = ''.join(reference['cells'][118]['source'])
assignment = next(node for node in ast.walk(ast.parse(fragment_cell))
                  if isinstance(node, ast.Assign)
                  and any(getattr(target, 'id', '') == 'FRAG_SRC' for target in node.targets))
fragment_source = ast.literal_eval(assignment.value)
ast.parse(fragment_source)
adapter = ADAPTER.read_text()
tree = ast.parse(adapter)
worker = next(ast.literal_eval(node.value) for node in tree.body
              if isinstance(node, ast.Assign)
              and any(getattr(target, 'id', '') == 'FRAGMENT_WORKER' for target in node.targets))
ast.parse(worker)

base = json.loads(BASE.read_text())
notebook = copy.deepcopy(base)
source = 'FRAGMENT_SOURCE = ' + repr(fragment_source) + '\n\n' + adapter
notebook['cells'].append(dict(cell_type='code', execution_count=None, metadata={}, outputs=[],
                              source=source.splitlines(keepends=True)))
assert notebook['cells'][:-1] == base['cells']
for cell in notebook['cells']:
    ast.parse(''.join(cell['source']))
notebook['metadata']['bounded_fragment_experiment'] = dict(
    base=str(BASE.relative_to(ROOT)), base_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
    reference=str(REFERENCE.relative_to(ROOT)), reference_version=47,
    fragment_source_sha256=hashlib.sha256(fragment_source.encode()).hexdigest(),
    adapter_sha256=hashlib.sha256(adapter.encode()).hexdigest(),
    score='unmeasured; upstream author-reported V46 0.441 is not this derivative',
    changes='one appended CPU overlay; original35 cells unchanged',
    bounds='900s hidden/120s smoke subprocess; complete molecule checkpoints only',
    candidate_universe='same final25 metric identities; noGL rows only; preserve formula slots',
    hidden_runtime='unverified; original8h30 watchdog remains active')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(notebook, indent=1) + '\n')
print(OUTPUT)
print('SHA256', hashlib.sha256(OUTPUT.read_bytes()).hexdigest())
