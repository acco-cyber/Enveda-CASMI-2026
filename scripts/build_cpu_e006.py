"""Build a credential-free CPU E006 experiment. No launching or score claims."""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'reference/public_v90.ipynb'
OUTPUT = ROOT / 'notebooks/cpu-e006-v2/cpu_e006_v2.ipynb'
SMOKE_ICE_BUDGET = 1800
CPU_SETUP = "# CPU E006 candidate: no GPU allocation; ranking logic retained from E006.\n# CPU vs CUDA numerical equivalence and full hidden runtime are not yet verified.\nimport os as _cpu_os, signal as _cpu_signal\n_cpu_os.environ['CUDA_VISIBLE_DEVICES'] = ''\nCPU_THREADS = min(4, len(_cpu_os.sched_getaffinity(0)))\nfor _cpu_name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):\n    _cpu_os.environ[_cpu_name] = str(CPU_THREADS)\n_cpu_os.environ['NUMBA_NUM_THREADS'] = str(CPU_THREADS)\ndef _cpu_deadline(signum, frame):\n    raise SystemExit('CPU E006 exceeded the 8h30m execution budget; do not submit an incomplete run')\n_cpu_signal.signal(_cpu_signal.SIGALRM, _cpu_deadline)\n_cpu_signal.alarm(8 * 3600 + 30 * 60)\nprint('CPU_E006: all model and simulator inference uses CPU; execution budget 8h30m')\n"

def patch(text):
    return (text.replace('"cuda" if torch.cuda.is_available() else "cpu"', '"cpu"')
            .replace("'cuda' if torch.cuda.is_available() else 'cpu'", "'cpu'")
            .replace("device='cuda', budget_s=", "device='cpu', budget_s=")
            .replace('torch.cuda.empty_cache()', 'None'))

def patch_cell(source):
    edits = []
    for node in ast.parse(source).body:
        if not isinstance(node, ast.Assign):
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
        if isinstance(value, str):
            replacement = patch(value)
        elif isinstance(value, dict):
            replacement = {k: patch(v) if isinstance(v, str) else v for k, v in value.items()}
        else:
            continue
        if replacement != value:
            edits.append((node.value, repr(replacement)))
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    for node, replacement in reversed(edits):
        a = offsets[node.lineno - 1] + node.col_offset
        b = offsets[node.end_lineno - 1] + node.end_col_offset
        source = source[:a] + replacement + source[b:]
    return patch(source)

def validate(notebook):
    for cell in notebook['cells']:
        source = ''.join(cell['source'])
        tree = ast.parse(source)
        assert "device='cuda'" not in source
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            if isinstance(value, dict):
                for name, content in value.items():
                    if isinstance(content, str) and str(name).endswith('.py'):
                        ast.parse(content)
                        assert '"cuda" if torch.cuda.is_available()' not in content
            if isinstance(value, str) and any(getattr(t, 'id', '') in ('CORE', 'RUNNER') for t in node.targets):
                ast.parse(value)
                assert "'cuda' if torch.cuda.is_available()" not in value

if __name__ == '__main__':
    notebook = json.loads(SOURCE.read_text())
    notebook['cells'] = notebook['cells'][:34]
    for cell in notebook['cells']:
        cell['outputs'] = []
        cell['execution_count'] = None
        source = patch_cell(''.join(cell['source']))
        source = source.replace("gpu = subprocess.check_output(\n        ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], text=True).strip()\n    assert 'T4' in gpu, gpu", "gpu = None\n    import torch\n    assert not torch.cuda.is_available(), 'CPU candidate requires CUDA to remain disabled'\n    torch.set_num_threads(CPU_THREADS)")
        source = source.replace("meta['device'].startswith('cuda')", "meta['device'].startswith('cpu')")
        # Only the visible smoke budget changes; hidden ICE budget remains 5400 seconds.
        if 'if not IS_RERUN:' in source and 'ICE_BUDGET = 300' in source:
            source = source.replace('ICE_BUDGET = 300', f'ICE_BUDGET = {SMOKE_ICE_BUDGET}')
        cell['source'] = source.splitlines(keepends=True)
    notebook['cells'].insert(0, dict(cell_type='code', execution_count=None, metadata={}, outputs=[], source=CPU_SETUP.splitlines(keepends=True)))
    notebook['metadata']['cpu_e006_notes'] = dict(source='public_v90.ipynb cells0:34', removed_overlay='joint common-evidence cell34', runtime_status='unverified CPU candidate', simulator_budgets='v2 smoke ICE1800s; hidden ICE5400s unchanged; GL4000s unchanged', cpu_smoke_status='v1 ICE300s scored0 after420predictions; v2 expanded budget unverified', hidden_runtime='full CPU timing unverified; watchdog8h30m unchanged')
    validate(notebook)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(notebook, indent=1) + '\n')
    print(OUTPUT)
