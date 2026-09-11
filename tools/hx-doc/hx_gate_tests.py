"""Prove each repository gate fails on the case it is meant to catch.

Every check here enforces a written rule. A check that cannot fail looks like
coverage and is not, so each gate gets one test that breaks the thing it
guards and asserts a non-zero exit.

Runs against a throwaway copy of the repository, never the working tree.

Usage:
  hx-gate-tests
"""
import io, os, re, shutil, subprocess, sys, tempfile

SRC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_TMP = tempfile.mkdtemp(prefix='hx-gate-')
WORK = os.path.join(_TMP, 'repo')
PY = sys.executable

passed = failed = 0

def run(*args, cwd=WORK):
    r = subprocess.run([PY] + list(args), cwd=cwd, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')

def check(label, cond, detail=''):
    global passed, failed
    if cond:
        passed += 1
        print('ok    %s' % label)
    else:
        failed += 1
        print('FAIL  %s\n%s' % (label, detail[:800]))

def fresh():
    if os.path.isdir(WORK):
        shutil.rmtree(WORK, ignore_errors=True)
    shutil.copytree(SRC, WORK, ignore=shutil.ignore_patterns('.git'))

def edit(rel, fn):
    p = os.path.join(WORK, rel.replace('/', os.sep))
    s = io.open(p, encoding='utf-8').read()
    io.open(p, 'w', encoding='utf-8', newline='\n').write(fn(s))

# ---------------------------------------------------------------- baseline --
fresh()
rc, out = run('tools/hx-doc/hx_fleet.py', '--check')
check('baseline: hx-fleet --check passes', rc == 0, out)

# ------------------------------------------- hx_fleet: unclosed marker ------
fresh()
edit('README.md', lambda s: s + '\n<!-- HX-FLEET:TABLE columns=id,ip -->\n')
rc, out = run('tools/hx-doc/hx_fleet.py', '--check')
check('hx-fleet: unclosed marker is drift',
      rc != 0 and 'marker' in out.lower(), out)

# ------------------------------------------- hx_fleet: unknown column -------
fresh()
edit('README.md', lambda s: s.replace('<!-- HX-FLEET:TABLE columns=id,ip',
                                      '<!-- HX-FLEET:TABLE columns=id,bogus', 1))
rc, out = run('tools/hx-doc/hx_fleet.py', '--check')
check('hx-fleet: unknown column is drift',
      rc != 0 and 'bogus' in out, out)

# ------------------------------------ hx_record_check: template option list -
fresh()
edit('docs/02-server-records/HX-10.md',
     lambda s: s.replace('**Build state:** NOT STARTED',
                         '**Build state:** NOT STARTED | IN PROGRESS | PASS', 1))
rc, out = run('tools/hx-doc/hx_record_check.py')
check('hx-record-check: option list is drift',
      rc != 0 and 'DRIFT' in out, out)

# ------------------------------------ hx_record_check: near-miss state ------
fresh()
edit('docs/02-server-records/HX-10.md',
     lambda s: s.replace('**Build state:** NOT STARTED',
                         '**Build state:** NOT APPLICABLE', 1))
rc, out = run('tools/hx-doc/hx_record_check.py')
check('hx-record-check: NOT APPLICABLE no longer satisfies NOT STARTED',
      rc != 0 and 'DRIFT' in out, out)

# ------------------------------------ hx_record_check: missing State line ---
fresh()
edit('docs/02-server-records/HX-10.md',
     lambda s: s.replace('**Build state:** NOT STARTED\n', '', 1))
rc, out = run('tools/hx-doc/hx_record_check.py')
check('hx-record-check: a missing State line is drift',
      rc != 0 and 'State' in out, out)

# ------------------------------------------ hx_doc_check: link traversal ----
fresh()
edit('docs/03-runbooks/README.md',
     lambda s: s + '\n\nSee [outside](../../../../../../Windows/System32/drivers/etc/hosts).\n')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a target outside the repository is broken',
      rc != 0 and 'broken' in out, out)

# ------------------------------ hx_upstream_drift: unpaired provenance ------
fresh()
def unpair(s):
    m = re.search(r'^(Repository:\s*[\w.-]+/[\w.-]+)\s*$', s, re.M)
    assert m, 'no Repository line in SKILL-REGISTRY.md'
    return s[:m.end()] + '\n' + m.group(1) + s[m.end():]
edit('skills/SKILL-REGISTRY.md', unpair)
rc, out = run('tools/hx-doc/hx_upstream_drift.py', '--markdown')
check('hx-upstream-drift: unpaired repo/sha lines are refused',
      rc != 0 and 'pair up' in out, out)

# --------------------------------------- hx_preflight: a missing pin --------
fresh()
edit('docs/03-runbooks/common/hx-base.env',
     lambda s: s.replace('HX_N8N_VERSION="2.38.6"', 'HX_N8N_VERSION=""', 1))
rc, out = run('tools/hx-doc/hx_preflight.py', '--quiet')
check('hx-preflight: an empty pin fails instead of being skipped',
      rc != 0 and 'no version pinned' in out, out)

# --------------------------------------- hx_new_server: unknown option ------
fresh()
rc, out = run('tools/hx-doc/hx_new_server.py', 'hx-17', '--no-olama')
check('hx-new-server: a misspelled flag is refused',
      rc == 2 and 'unknown option' in out, out)

# --------------------------------------- hx_new_server: template drift ------
fresh()
edit('docs/02-server-records/_TEMPLATE.md',
     lambda s: s.replace('**IP:** `192.168.50.2NN`', '**IP:** `TBD`', 1))
rc, out = run('tools/hx-doc/hx_new_server.py', 'hx-17', '--force')
check('hx-new-server: a missing template placeholder is refused',
      rc != 0 and 'placeholder' in out, out)

# ------------------------------------------ hx_proof: duplicate marker ------
fresh()
edit('docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md',
     lambda s: s + '\n<!-- HX-PROOF:TABLE phase=A -->\n<!-- /HX-PROOF -->\n')
rc, out = run('tools/hx-doc/hx_proof.py', '--check')
check('hx-proof: a duplicate phase marker is drift',
      rc != 0 and 'phase=A' in out, out)

# -------------------------------------- hx_proof: dependency on nothing -----
fresh()
edit('docs/00-control/hx-proof.tsv',
     lambda s: s.replace('\tB5,A2,P0\t', '\tB5,A2,Z9\t', 1))
rc, out = run('tools/hx-doc/hx_proof.py', '--check')
check('hx-proof: a dependency on an unknown step is refused',
      rc != 0 and 'Z9' in out, out)

# ------------------------------------- hx_render_html: source without mirror -
fresh()
edit('docs/03-runbooks/README.md', lambda s: s + '\nA line the mirror does not have.\n')
rc, out = run('tools/hx-doc/hx_render_html.py', '--check')
check('hx-render-html: an edited source with a stale mirror fails',
      rc != 0 and 'stale' in out.lower(), out)

# ------------------------------------ hx_smoke_lint: no known answer --------
fresh()
def strip_known(s):
    s = re.sub(r'(?i)known.answer', 'REMOVED', s)
    s = re.sub(r'(?i)expected output', 'REMOVED', s)
    s = re.sub(r'(?i)reply with exactly', 'REMOVED', s)
    return re.sub(r'(?i)exactly:', 'REMOVED', s)
edit('smoke-tests/redis-smoke-test.md', strip_known)
rc, out = run('tools/hx-doc/hx_smoke_lint.py')
check('hx-smoke-lint: an authority with no known answer fails',
      rc != 0 and 'known answer' in out, out)

# --------------------------------------- hx_version_pins: numeric sort ------
# Exercise the shipped comparator, not a copy of it: a test that reimplements
# the logic it is checking proves only that the test is self-consistent.
vers = ['595.9.05-0ubuntu0.24.04.1', '595.71.05-0ubuntu0.24.04.1']
src = io.open(os.path.join(SRC, 'tools', 'hx-doc', 'hx_version_pins.py'),
              encoding='utf-8').read()
m = re.search(r'( *)def vkey\(.*?return max\(set\(versions\), key=vkey\)',
              src, re.S)
check('hx-version-pins: the shipped comparator was found', bool(m), src[:400])
if m:
    ns = {'re': re}
    body = '\n'.join(line[len(m.group(1)):] if line.strip() else line
                     for line in m.group(0).splitlines()[:-1])
    exec(body, ns)
    check('hx-version-pins: 595.71.05 sorts above 595.9.05',
          max(set(vers), key=ns['vkey']).startswith('595.71.05'),
          'lexicographic would pick ' + sorted(vers)[-1])

# Not ignore_errors: a workspace that cannot be removed is worth saying out
# loud, but it is not a gate failure, so it does not change the exit status.
try:
    shutil.rmtree(_TMP)
except OSError as exc:
    print(f"warning: could not remove {_TMP}: {exc}")
print('\npassed=%d failed=%d' % (passed, failed))
raise SystemExit(1 if failed else 0)
