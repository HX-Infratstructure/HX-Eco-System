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
    """Run a tool in the scratch copy; returns (exit status, combined output)."""
    r = subprocess.run([PY] + list(args), cwd=cwd, capture_output=True, text=True,
                       encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')

def check(label, cond, detail=''):
    """Record one test result and print it."""
    global passed, failed
    if cond:
        passed += 1
        print('ok    %s' % label)
    else:
        failed += 1
        print('FAIL  %s\n%s' % (label, detail[:800]))

def fresh():
    """Replace the scratch copy with a clean one, so tests cannot affect each other.

    The copy is made a git work tree. hx_doc_check runs `git check-ignore`
    against the repository root, and outside a work tree that exits 128, which
    it correctly treats as a failure. Every earlier test here expected a
    non-zero exit anyway, so the harness never noticed it was checking
    documents in an environment where one check could not pass.
    """
    if os.path.isdir(WORK):
        shutil.rmtree(WORK, ignore_errors=True)
    shutil.copytree(SRC, WORK, ignore=shutil.ignore_patterns('.git'))
    subprocess.run(['git', 'init', '-q'], cwd=WORK,
                   capture_output=True, check=True)

def edit(rel, fn):
    """Rewrite one file in the scratch copy through fn."""
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
    """Duplicate a Repository line so the repo and commit counts no longer match."""
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

# ----------------------- hx_doc_check: generated trees are not findings ------
# openwiki/ is written by the OpenWiki CLI and replaced wholesale on --init.
# A broken link there is a defect in the generator or the source it documents,
# never something to fix in the generated page. The skip has to actually skip.
fresh()
import pathlib
ow = pathlib.Path(WORK) / 'openwiki'
ow.mkdir(parents=True, exist_ok=True)
(ow / 'index.md').write_text(
    '# Generated' + chr(10) * 2 +
    'See [nothing](docs/this-does-not-exist.md).' + chr(10),
    encoding='utf-8')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a broken link inside openwiki/ is not a finding',
      rc == 0 and 'openwiki' not in out, out)

# The same broken link outside a generated tree must still fail, so the skip
# above is a skip and not a hole.
fresh()
edit('docs/03-runbooks/README.md',
     lambda s: s + chr(10) + 'See [nothing](this-does-not-exist.md).' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: the same broken link outside a generated tree fails',
      rc != 0 and 'broken' in out, out)

# ------------------------------------- hx_version_pins: package sources -----
# D-021: .coderabbit.yaml stands, so Snap is never permitted, driver included.
# The Ubuntu archive stays available for the driver, build toolchains and
# library headers. source_problem() is separate from the reporting loop so this
# runs without touching the network.
sys.path.insert(0, os.path.join(SRC, 'tools', 'hx-doc'))
import hx_version_pins as _pins  # noqa: E402

check('hx-version-pins: a Snap application is refused',
      'never permitted' in _pins.source_problem({'source': 'snap', 'kind': 'app'}))
check('hx-version-pins: a Snap driver is refused too',
      'never permitted' in _pins.source_problem({'source': 'snap', 'kind': 'driver'}))
check('hx-version-pins: the Ubuntu archive is allowed for a driver',
      _pins.source_problem({'source': 'ubuntu-archive', 'kind': 'driver'}) == '')
check('hx-version-pins: the Ubuntu archive is refused for an application',
      'migrate' in _pins.source_problem({'source': 'ubuntu-archive', 'kind': 'app'}))
check('hx-version-pins: PyPI is accepted',
      _pins.source_problem({'source': 'pypi', 'kind': 'app'}) == '')

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
    """Remove every phrase that declares a known answer."""
    s = re.sub(r'(?i)known.answer', 'REMOVED', s)
    s = re.sub(r'(?i)expected output', 'REMOVED', s)
    s = re.sub(r'(?i)reply with exactly', 'REMOVED', s)
    return re.sub(r'(?i)exactly:', 'REMOVED', s)
edit('smoke-tests/redis-smoke-test.md', strip_known)
rc, out = run('tools/hx-doc/hx_smoke_lint.py')
check('hx-smoke-lint: an authority with no known answer fails',
      rc != 0 and 'known answer' in out, out)

# ------------------------------ hx_smoke_lint: no retention statement -------
fresh()
def strip_retention(s):
    """Remove every phrase that states where evidence is retained."""
    s = re.sub(r'(?i)retention', 'REMOVED', s)
    s = re.sub(r'(?i)retain\w*', 'REMOVED', s)
    return s.replace('docs/05-evidence', 'docs/REMOVED')
edit('smoke-tests/qdrant-smoke-test.md', strip_retention)
rc, out = run('tools/hx-doc/hx_smoke_lint.py')
check('hx-smoke-lint: an authority with no retention statement fails',
      rc != 0 and 'evidence retention' in out, out)

# ------------------------- hx_smoke_lint: an empty Evidence heading fails ---
fresh()
def gut_evidence(s):
    """Cut the Evidence section down to a bare heading."""
    head = s.split('## Evidence')[0]
    return head + '## Evidence' + chr(10)
edit('smoke-tests/qdrant-smoke-test.md', gut_evidence)
rc, out = run('tools/hx-doc/hx_smoke_lint.py')
check('hx-smoke-lint: a bare Evidence heading does not satisfy the check',
      rc != 0 and 'evidence retention' in out, out)

# ------------------- hx_smoke_lint: a negated sentence does not satisfy it ---
# "do not retain credentials" contains retain. Matching that word was no
# better than matching evidence, which is why the check is anchored to the
# standard bundle path instead.
fresh()
NEGATED = 'Do not retain credentials in evidence, and do not retain secrets.'
def negate_evidence(s):
    """Replace the Evidence section with a sentence that only negates retention."""
    head = s.split('## Evidence')[0]
    return head + '## Evidence' + chr(10) * 2 + NEGATED + chr(10)
edit('smoke-tests/qdrant-smoke-test.md', negate_evidence)
rc, out = run('tools/hx-doc/hx_smoke_lint.py')
check('hx-smoke-lint: "do not retain credentials" does not satisfy the check',
      rc != 0 and 'evidence retention' in out, out)

# ---------------------------- hx_doc_check: a unit nothing creates ----------
fresh()
edit('docs/03-runbooks/common/10-crawl4ai.sh',
     lambda s: s.replace('hx_app_done NONE', 'hx_app_done hx-crawl4ai', 1))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a block reporting a unit nothing creates fails',
      rc != 0 and 'hx-crawl4ai' in out, out)

# ------------------- hx_doc_check: a mention is not a unit creation ---------
# A comment naming the unit path, or an rm of it, must not satisfy the check.
fresh()
def mention_only(s):
    """Report a unit, and mention its path without creating it."""
    s = s.replace('hx_app_done NONE', 'hx_app_done hx-crawl4ai', 1)
    return s + chr(10) + 'sudo rm -f /etc/systemd/system/hx-crawl4ai.service' + chr(10)
edit('docs/03-runbooks/common/10-crawl4ai.sh', mention_only)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: naming a unit path without creating it still fails',
      rc != 0 and 'hx-crawl4ai' in out, out)

# ---- hx-doc-check: the generated authority block ----------------------------
# A generated block may not amend the truth order. OpenWiki's first run wrote
# "Treat source code and tests as authoritative" into AGENTS.md, which
# contradicts section 2. That block is rewritten on every scheduled run, so the
# rule needs a check, not a memory. Both directions: the bad wording fails, and
# a claim that names the control Markdown passes.
fresh()
_ap = os.path.join(WORK, 'AGENTS.md')
_txt = io.open(_ap, encoding='utf-8').read()
_pat = r'<!-- OPENWIKI:START -->.*?<!-- OPENWIKI:END -->'
def _setblock(body):
    out = re.sub(_pat, '<!-- OPENWIKI:START -->' + chr(10) + body + chr(10) +
                 '<!-- OPENWIKI:END -->', _txt, flags=re.S)
    io.open(_ap, 'w', encoding='utf-8', newline=chr(10)).write(out)
    return out

check('gate-tests: the generated block was found in AGENTS.md',
      _setblock('placeholder') != _txt, _txt[-400:])

_setblock('Treat source code and tests as authoritative.')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a generated authority claim without docs/ is refused',
      rc != 0 and 'authority:' in out, out)

# Naming docs/ does not license the claim. Section 2 has no entry for source
# code, so this must still be refused - the first correction made here said
# 'source code, tests, and the authoritative Markdown', and was still wrong.
_setblock('Treat source code, tests and the control Markdown in docs/ as'
          ' authoritative.')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: naming docs/ does not license calling code authoritative',
      rc != 0 and 'authority:' in out, out)

# The same wrong claim, backwards. A pattern anchored on 'source code ...'
# authoritative' reads clean here, which is why the check works sentence by
# sentence instead.
_setblock('Authoritative sources include source code and tests.')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: the authority claim is refused in either word order',
      rc != 0 and 'authority:' in out, out)

# Capitalised, and with no mention of docs/. The second rule compared a
# raw string, so 'Authoritative' read clean.
_setblock('Authoritative material is listed in the run sheet.')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a capitalised authority claim is still refused',
      rc != 0 and 'authority:' in out, out)

# The noun form. 'authoritative' alone missed 'is the authority'.
_setblock('Source code is the authority for this repository.')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: the noun form of the claim is refused',
      rc != 0 and 'authority:' in out, out)

# And the denial must survive, or the repository's own correct wording
# would fail its own check.
_setblock('Source code and tests are evidence, not authority. The control'
          ' Markdown in docs/ is authoritative.')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: the negated wording is accepted', rc == 0, out)

# "attests" contains "tests". A substring match refused this sentence, which
# claims nothing about source code at all.
_setblock('The control Markdown in docs/ attests to the authority order.')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a word merely containing "tests" is not a claim',
      rc == 0, out)

# And the check is not simply refusing every block: a claim that names only
# the control Markdown passes.
_setblock('The control Markdown in docs/ stays authoritative.')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a claim naming only docs/ is accepted', rc == 0, out)

# ---- hx-doc-check: operational tooling documents ----------------------------
# CodeRabbit was adopted undocumented, then OpenWiki was adopted the same way.
# These three break the guard on purpose so a third repeat cannot pass quietly.
fresh()
_tool = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_body = io.open(_tool, encoding='utf-8').read()
io.open(_tool, 'w', encoding='utf-8', newline=chr(10)).write(
    _body.replace('## Upstream', '## Somewhere else', 1))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a tooling document missing a required section fails',
      rc != 0 and 'tooling:' in out and 'Upstream' in out, out)

fresh()
_idx = os.path.join(WORK, 'docs', '06-tooling', 'README.md')
_txt = io.open(_idx, encoding='utf-8').read()
# A table row, not prose. As prose the tooling check never saw it and
# check_links flagged the broken link instead, so this passed on the
# wrong gate entirely.
io.open(_idx, 'w', encoding='utf-8', newline=chr(10)).write(
    _txt.rstrip() + chr(10) +
    '| ghost | [ghost-tool.md](ghost-tool.md) | - | - |' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: an index row naming a missing file fails',
      rc != 0 and 'tooling:' in out and 'ghost-tool.md' in out, out)

# Prose after the table is still inside the Index section. Only rows count.
fresh()
_idx = os.path.join(WORK, 'docs', '06-tooling', 'README.md')
_txt = io.open(_idx, encoding='utf-8').read()
io.open(_idx, 'w', encoding='utf-8', newline=chr(10)).write(
    _txt.rstrip() + chr(10) * 2 + 'Also see [orphan](orphan.md).' + chr(10))
_orph = os.path.join(WORK, 'docs', '06-tooling', 'orphan.md')
io.open(_orph, 'w', encoding='utf-8', newline=chr(10)).write('# Orphan' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a prose link below the Index table is not an entry',
      rc != 0 and 'tooling:' in out and 'orphan.md' in out, out)

# A link in prose is not an index entry. Scanning the whole README would
# let a document pass by being mentioned anywhere.
fresh()
_idx = os.path.join(WORK, 'docs', '06-tooling', 'README.md')
_txt = io.open(_idx, encoding='utf-8').read()
_prose = _txt.replace('## Index',
    '## Aside' + chr(10) * 2 + 'See [openwiki](openwiki.md) and'
    ' [agents](openwiki-agents.md).' + chr(10) * 2 + '## Index', 1)
_prose = _prose.replace('| OpenWiki | [openwiki.md](openwiki.md) |'
                        ' [openwiki-agents.md](openwiki-agents.md) | D-023 |',
                        '| OpenWiki | not written yet | - | D-023 |', 1)
io.open(_idx, 'w', encoding='utf-8', newline=chr(10)).write(_prose)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a prose link outside the Index table is not an entry',
      rc != 0 and 'tooling:' in out and 'openwiki.md' in out, out)

# An Upstream heading with nothing under it is the heading without the
# point of it: the reader still has to go and find the product's docs.
fresh()
_tool = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_body = io.open(_tool, encoding='utf-8').read()
_cut = _body[:_body.index('## Upstream')] + '## Upstream' + chr(10) * 2 + 'None.' + chr(10)
io.open(_tool, 'w', encoding='utf-8', newline=chr(10)).write(_cut)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: an Upstream heading with no link fails',
      rc != 0 and 'tooling:' in out and 'Upstream' in out, out)

# The word, not a URL. 'http' alone used to satisfy the Upstream rule.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
_w = (_b[:_b.index('## Upstream')] + '## Upstream' + chr(10) * 2 +
      'There are no http links for this tool.' + chr(10))
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(_w)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: the word http is not an Upstream link',
      rc != 0 and 'tooling:' in out and 'Upstream' in out, out)

# Substring, not a link. 'wiki.md' occurs inside 'openwiki.md', so a
# substring test would call this file linked when nothing links to it.
fresh()
_sub = os.path.join(WORK, 'docs', '06-tooling', 'wiki.md')
io.open(_sub, 'w', encoding='utf-8', newline=chr(10)).write('# Wiki' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a filename that is only a substring of a link is unlinked',
      rc != 0 and 'tooling:' in out and 'wiki.md' in out, out)

# A heading inside a fenced example is an example, not a section.
fresh()
_tool = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_body = io.open(_tool, encoding='utf-8').read()
_fenced = _body.replace('## Upstream',
                        '```' + chr(10) + '## Upstream' + chr(10) + '```', 1)
io.open(_tool, 'w', encoding='utf-8', newline=chr(10)).write(_fenced)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a required heading inside a code fence does not count',
      rc != 0 and 'tooling:' in out and 'Upstream' in out, out)

fresh()
_orphan = os.path.join(WORK, 'docs', '06-tooling', 'orphan.md')
io.open(_orphan, 'w', encoding='utf-8', newline=chr(10)).write(
    '# Orphan' + chr(10) * 2 + '## What it is' + chr(10) * 2 + 'x' + chr(10) * 2 +
    '## Why we have it' + chr(10) * 2 + 'x' + chr(10) * 2 +
    '## When to use it' + chr(10) * 2 + 'x' + chr(10) * 2 +
    '## How to use it' + chr(10) * 2 + 'x' + chr(10) * 2 +
    '## Upstream' + chr(10) * 2 + '- <https://example.invalid/docs>' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
# The fixture is complete on purpose, including a real Upstream URL, so
# this can only fail on the linkage rule it names.
check('hx-doc-check: a complete document nobody links to still fails',
      rc != 0 and 'orphan.md is not linked from the' in out, out)

# ---- hx-version-pins: numeric sort ------------------------------------------
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
