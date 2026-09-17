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

# ------------------------- hx_record_check: the Foundation section ----------
# Added 2026-09-16. Identity, time authority and fleet access were absent from
# every record because the template never asked for them, and a gate cannot
# require what the template does not declare.
fresh()
edit('docs/02-server-records/HX-10.md',
     lambda s: s.replace('## Foundation', '## Something Else', 1))
rc, out = run('tools/hx-doc/hx_record_check.py')
check('hx-record-check: a record with no Foundation section fails',
      rc != 0 and 'Foundation' in out, out)

# HX-1 is the domain controller, not a rebuilt application host. It declares
# the sections that do not apply and says why. That declaration has to work,
# or the gate forces a fiction onto the one host the standard is not about.
fresh()
rc, out = run('tools/hx-doc/hx_record_check.py')
check('hx-record-check: a declared not-applicable section is accepted',
      rc == 0, out)

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

# ------------------- hx_doc_check: a server path is not a repository path ----
# A server record has to name the file that holds a host's configuration. Those
# paths live on the server, not here, so the link gate must not read them as
# repository references. HX5-F04.
fresh()
edit('docs/03-runbooks/README.md',
     lambda s: s + chr(10) + 'Persistent network file: `/etc/netplan/50-cloud-init.yaml`' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a server path under /etc is not a repository reference',
      rc == 0 and 'netplan' not in out, out)

# The exemption above is for paths that are not ours. A repository path that
# does not resolve must still fail, so the skip is a skip and not a hole.
fresh()
edit('docs/03-runbooks/README.md',
     lambda s: s + chr(10) + 'See `docs/this-does-not-exist.md` for more.' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a repository path that does not resolve still fails',
      rc != 0 and 'broken' in out, out)

# A system root can be traversed out of. `/etc/../docs/x.md` starts with /etc/
# but names a repository path, so the exemption must classify it by where it
# resolves to, not by how it is spelt.
fresh()
edit('docs/03-runbooks/README.md',
     lambda s: s + chr(10) + 'See `/etc/../docs/this-does-not-exist.md` for more.' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a repository path spelt through a system root still fails',
      rc != 0 and 'broken' in out, out)

# ----------------------- hx_doc_check: a withdrawn path stays withdrawn ------
# D-025 deleted .github/workflows/openwiki-update.yml and withdrew scheduled
# generation. The OpenWiki scaffold restores that file on its own. HX5-F06.
fresh()
wf = pathlib.Path(WORK) / '.github' / 'workflows' / 'openwiki-update.yml'
wf.parent.mkdir(parents=True, exist_ok=True)
wf.write_text('name: OpenWiki Update' + chr(10), encoding='utf-8')
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a path a decision withdrew is refused if it comes back',
      rc != 0 and 'openwiki-update.yml' in out, out)

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

# The remediation messages must name every approved source. The expected
# phrases come from the module under test (_SOURCE_PHRASES), not a second
# copy here, so a legitimate policy change that keeps set, phrases and
# rendering in agreement still passes. What this catches is a phrase that
# exists but never reaches the message through the join rendering.
def _message_names(msg):
    """Every approved source's display phrase appears in the message."""
    return all(v in msg for v in _pins._SOURCE_PHRASES.values())

_snap_msg = _pins.source_problem({'source': 'snap', 'kind': 'app'})
_ubuntu_msg = _pins.source_problem({'source': 'ubuntu-archive', 'kind': 'app'})
check('hx-version-pins: the Snap message names every approved source',
      _message_names(_snap_msg), _snap_msg)
check('hx-version-pins: the Ubuntu-archive message names every approved source',
      _message_names(_ubuntu_msg), _ubuntu_msg)

# ------------------------------------------ hx_proof: duplicate marker ------
fresh()
edit('docs/00-control/HX-ECO-SYSTEM-SMOKE-TEST-ROADMAP.md',
     lambda s: s + '\n<!-- HX-PROOF:TABLE phase=A -->\n<!-- /HX-PROOF -->\n')
rc, out = run('tools/hx-doc/hx_proof.py', '--check')
check('hx-proof: a duplicate phase marker is drift',
      rc != 0 and 'phase=A' in out, out)

# -------------------------------------- hx_proof: dependency on nothing -----
fresh()
# Append a bogus dependency to the first step that has any, rather than
# naming one row's exact dependency string. Hardcoding 'B5,A2,P0' broke the
# moment a real step gained a new requirement, and the test then silently
# edited nothing - it reported a gate failure that was its own.
def _bogus_dep(text):
    out, done = [], False
    for line in text.split(chr(10)):
        cells = line.split(chr(9))
        if not done and len(cells) >= 6 and cells[5] not in ('NONE', 'requires', ''):
            cells[5] += ',Z9'
            line = chr(9).join(cells)
            done = True
        out.append(line)
    assert done, 'no step with dependencies in hx-proof.tsv'
    return chr(10).join(out)
edit('docs/00-control/hx-proof.tsv', _bogus_dep)
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
def _complete_doc(title):
    """A tooling document valid in every respect but the one under test.

    Title-only fixtures failed the heading rule as well as the rule a test
    names, and the filename appeared in both messages, so those tests could
    pass on the wrong gate.
    """
    parts = ['# ' + title, '']
    for heading in ('What it is', 'Why we have it', 'When to use it',
                    'How to use it'):
        parts += ['## ' + heading, '', 'Text.', '']
    parts += ['## Upstream', '', '- <https://example.invalid/docs>',
              '- <https://example.invalid/source>', '']
    return chr(10).join(parts)

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
io.open(_orph, 'w', encoding='utf-8', newline=chr(10)).write(_complete_doc('Orphan'))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a prose link below the Index table is not an entry',
      rc != 0 and 'orphan.md is not linked from the' in out, out)

# A link in prose is not an index entry. Scanning the whole README would
# let a document pass by being mentioned anywhere.
fresh()
_idx = os.path.join(WORK, 'docs', '06-tooling', 'README.md')
_txt = io.open(_idx, encoding='utf-8').read()
_prose = _txt.replace('## Index',
    '## Aside' + chr(10) * 2 + 'See [openwiki](openwiki.md) and'
    ' [agents](openwiki-agents.md).' + chr(10) * 2 + '## Index', 1)
_prose = _prose.replace('| OpenWiki | [openwiki.md](openwiki.md) |'
                        ' [openwiki-agents.md](openwiki-agents.md) | D-025 |',
                        '| OpenWiki | not written yet | - | D-025 |', 1)
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
      rc != 0 and "has an 'Upstream' heading with no link" in out, out)

# The word, not a URL. 'http' alone used to satisfy the Upstream rule.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
_w = (_b[:_b.index('## Upstream')] + '## Upstream' + chr(10) * 2 +
      'There are no http links for this tool.' + chr(10))
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(_w)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: the word http is not an Upstream link',
      rc != 0 and "has an 'Upstream' heading with no link" in out, out)

# Substring, not a link. 'wiki.md' occurs inside 'openwiki.md', so a
# substring test would call this file linked when nothing links to it.
fresh()
_sub = os.path.join(WORK, 'docs', '06-tooling', 'wiki.md')
io.open(_sub, 'w', encoding='utf-8', newline=chr(10)).write(_complete_doc('Wiki'))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a filename that is only a substring of a link is unlinked',
      rc != 0 and 'wiki.md is not linked from the' in out, out)

# A heading inside a fenced example is an example, not a section.
fresh()
_tool = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_body = io.open(_tool, encoding='utf-8').read()
_fenced = _body.replace('## Upstream',
                        '```' + chr(10) + '## Upstream' + chr(10) + '```', 1)
io.open(_tool, 'w', encoding='utf-8', newline=chr(10)).write(_fenced)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a required heading inside a code fence does not count',
      rc != 0 and "has no '## Upstream' heading" in out, out)

fresh()
_orphan = os.path.join(WORK, 'docs', '06-tooling', 'orphan.md')
io.open(_orphan, 'w', encoding='utf-8', newline=chr(10)).write(
    '# Orphan' + chr(10) * 2 + '## What it is' + chr(10) * 2 + 'x' + chr(10) * 2 +
    '## Why we have it' + chr(10) * 2 + 'x' + chr(10) * 2 +
    '## When to use it' + chr(10) * 2 + 'x' + chr(10) * 2 +
    '## How to use it' + chr(10) * 2 + 'x' + chr(10) * 2 +
    '## Upstream' + chr(10) * 2 + '- <https://example.invalid/docs>' + chr(10) +
    '- <https://example.invalid/source>' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
# The fixture is complete on purpose, including a real Upstream URL, so
# this can only fail on the linkage rule it names.
check('hx-doc-check: a complete document nobody links to still fails',
      rc != 0 and 'orphan.md is not linked from the' in out, out)

# Trailing text does not close a fence. Before, '```not-a-close' closed it, the
# Upstream heading below leaked out as structure, and the next fence line
# swallowed the rest - so the failure named the link, not the heading.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
_f = chr(96) * 3
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(_b.replace(
    '## Upstream',
    _f + chr(10) + _f + 'not-a-close' + chr(10) + '## Upstream' + chr(10) + _f, 1))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a fence line with trailing text does not close the fence',
      rc != 0 and "has no '## Upstream' heading" in out, out)

# A shorter run does not close a longer fence.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(_b.replace(
    '## Upstream',
    chr(96) * 4 + chr(10) + chr(96) * 3 + chr(10) + '## Upstream' + chr(10) +
    chr(96) * 4, 1))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a three-backtick line does not close a four-backtick fence',
      rc != 0 and "has no '## Upstream' heading" in out, out)

# A tilde fence is a fence. Only backticks were tracked, so a heading inside
# ~~~ supplied a required section that is not there.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(
    _b.replace('## Upstream', '~~~' + chr(10) + '## Upstream' + chr(10) + '~~~', 1))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a required heading inside a tilde fence does not count',
      rc != 0 and "has no '## Upstream' heading" in out, out)

# A table row inside a fenced example is an example, not an index entry.
fresh()
_idx = os.path.join(WORK, 'docs', '06-tooling', 'README.md')
_txt = io.open(_idx, encoding='utf-8').read()
_row = ('| OpenWiki | [openwiki.md](openwiki.md) |'
        ' [openwiki-agents.md](openwiki-agents.md) | D-025 |')
_txt = _txt.replace(_row, '| OpenWiki | not written yet | - | D-025 |', 1)
_txt = (_txt.rstrip() + chr(10) * 2 + '```' + chr(10) + _row + chr(10) +
        '```' + chr(10))
io.open(_idx, 'w', encoding='utf-8', newline=chr(10)).write(_txt)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: an index row inside a code fence is not an entry',
      rc != 0 and 'openwiki.md is not linked from the' in out, out)

# A scheme with no address. 'https:// yet' contains https:// and links nothing.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
_w = (_b[:_b.index('## Upstream')] + '## Upstream' + chr(10) * 2 +
      'No documentation is available at https:// yet.' + chr(10))
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(_w)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a bare scheme is not an Upstream link',
      rc != 0 and "has an 'Upstream' heading with no link" in out, out)

# All five headings, wrong order. The index says 'in this order'.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
_b = (_b.replace('## What it is', '@@SWAP@@', 1)
        .replace('## Why we have it', '## What it is', 1)
        .replace('@@SWAP@@', '## Why we have it', 1))
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(_b)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: required headings out of order fail',
      rc != 0 and 'out of order' in out, out)

# Four spaces make an indented code block, not a fence. Before, a four-space
# fence line opened a fence that never closed, hiding the Upstream heading and
# everything after it, so this valid document failed.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(_b.replace(
    '## Upstream', '    ' + chr(96) * 3 + chr(10) + chr(10) + '## Upstream', 1))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: a four-space indented fence line does not open a fence',
      rc == 0, out)

# The pending count reads Index rows only. The phrase in prose used to add one.
fresh()
_idx = os.path.join(WORK, 'docs', '06-tooling', 'README.md')
_txt = io.open(_idx, encoding='utf-8').read()
io.open(_idx, 'w', encoding='utf-8', newline=chr(10)).write(
    _txt.rstrip() + chr(10) * 2 + 'A tool that is not written yet is backlog.' + chr(10))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: the backlog phrase in prose is not a pending tool',
      rc == 0 and 'tooling: 2 tool(s) still undocumented' in out, out)

# The index promises the documentation and the source. One real link used to
# satisfy the Upstream rule, and so did the same URL written twice.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
_one = (_b[:_b.index('## Upstream')] + '## Upstream' + chr(10) * 2 +
        '- <https://docs.langchain.com/oss/openwiki/overview>' + chr(10))
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(_one)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: one Upstream link is not the documentation and the source',
      rc != 0 and "has only one link under 'Upstream'" in out, out)

fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
_dup = (_b[:_b.index('## Upstream')] + '## Upstream' + chr(10) * 2 +
        '- <https://docs.langchain.com/oss/openwiki/overview>' + chr(10) +
        '- [docs](https://docs.langchain.com/oss/openwiki/overview)' + chr(10))
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(_dup)
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: the same Upstream URL twice counts as one link',
      rc != 0 and "has only one link under 'Upstream'" in out, out)

# D-024 says the backlog is reported on every run. The count rode on the
# all-complete note, so a failure anywhere in this check made it disappear.
fresh()
_t = os.path.join(WORK, 'docs', '06-tooling', 'openwiki.md')
_b = io.open(_t, encoding='utf-8').read()
io.open(_t, 'w', encoding='utf-8', newline=chr(10)).write(
    _b.replace('## Upstream', '## Somewhere else', 1))
rc, out = run('tools/hx-doc/hx_doc_check.py')
check('hx-doc-check: the backlog count is still reported when the check fails',
      rc != 0 and "has no '## Upstream' heading" in out
      and 'tooling: 2 tool(s) still undocumented' in out, out)

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

# ------------------------- hx-base.env: the foundation gate helpers ---------
# The 2026-09-16 Layer 0/1 audit found that the base block validated only what
# it configured, so identity, time authority and fleet access were never
# checked on any host. The gate that closes that runs on a server, not here,
# so the checks take their inputs as arguments and are exercised directly.
def foundation(fn, *args):
    """Call one hx_require_* helper in a subshell; return its exit status."""
    env = os.path.join(SRC, 'docs', '03-runbooks', 'common', 'hx-base.env')
    quoted = ' '.join("'%s'" % a.replace("'", "'\\''") for a in args)
    r = subprocess.run(
        ['bash', '-c', '. "$1" 2>/dev/null; %s %s' % (fn, quoted), '_', env],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')

FLEET_FP = 'SHA256:fpIJEHjkhRYRqnhvRhtgSqggOAjkTU90vSGWbh0vsPk'

# Identity. HX-2, HX-3 and HX-4 all answered with the short name.
rc, out = foundation('hx_require_fqdn', 'hx-6', 'hx-6.hx.local.arpa')
check('foundation: a short hostname is not an FQDN', rc == 41, out)
rc, out = foundation('hx_require_fqdn', 'hx-6.hx.local.arpa', 'hx-6.hx.local.arpa')
check('foundation: the correct FQDN passes', rc == 0, out)

# Time. The subtle case: HX-1 present in the source list but not selected.
# Three of four hosts were synchronised to a public pool with chrony absent.
SELECTED = '^* 192.168.50.200   3  6  377  15  +22us[+27us] +/- 71ms'
NOT_SEL = ('^* 185.125.190.57   2 10  377 290 +912us[+915us] +/- 72ms\n'
           '^- 192.168.50.200   3  6  377  15  +22us[ +27us] +/- 71ms')
rc, out = foundation('hx_require_ntp_source', NOT_SEL, '192.168.50.200')
check('foundation: HX-1 configured but not selected is refused', rc == 42, out)
rc, out = foundation('hx_require_ntp_source', SELECTED, '192.168.50.200')
check('foundation: HX-1 selected passes', rc == 0, out)

# Fleet access. "authorized_keys has a key" would have passed HX-2 and HX-3.
_kd = os.path.join(_TMP, 'keys')
os.makedirs(_kd, exist_ok=True)
_good = os.path.join(_kd, 'good.keys')
io.open(_good, 'w', encoding='utf-8', newline='\n').write(
    io.open(os.path.join(SRC, 'docs', '03-runbooks', 'common', 'hx-fleet-key.pub'),
            encoding='utf-8').read())
_wrong = os.path.join(_kd, 'wrong.keys')
subprocess.run(['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-C', 'not-the-fleet-key',
                '-f', os.path.join(_kd, 'other')], capture_output=True)
io.open(_wrong, 'w', encoding='utf-8', newline='\n').write(
    io.open(os.path.join(_kd, 'other.pub'), encoding='utf-8').read())

rc, out = foundation('hx_require_fleet_key', os.path.join(_kd, 'absent.keys'), FLEET_FP)
check('foundation: a missing authorized_keys is refused', rc == 43, out)
rc, out = foundation('hx_require_fleet_key', _wrong, FLEET_FP)
check('foundation: some other key is not the approved fleet key', rc == 44, out)
rc, out = foundation('hx_require_fleet_key', _good, FLEET_FP)
check('foundation: the approved fleet key passes', rc == 0, out)

# The committed public key must be the approved one, or the bootstrap installs
# the wrong thing on every future server.
rc, out = foundation('hx_require_fleet_key',
                     os.path.join(SRC, 'docs', '03-runbooks', 'common', 'hx-fleet-key.pub'),
                     FLEET_FP)
check('foundation: the committed public key matches the approved fingerprint', rc == 0, out)

# Persistence. Ubuntu carries SSH on the socket; reading a disabled
# ssh.service as a failure would break every host in the fleet.
rc, out = foundation('hx_require_ssh_persistence', 'disabled', 'enabled')
check('foundation: socket activation counts as SSH persistence', rc == 0, out)
rc, out = foundation('hx_require_ssh_persistence', 'disabled', 'disabled')
check('foundation: neither ssh.service nor ssh.socket enabled is refused', rc == 45, out)

# 00-foundation.sh disables systemd-timesyncd before starting chrony. If it
# then stopped on a failed selection, the host would be left with no time
# source at all - and on a domain-joined host that is not a clock problem,
# it is Kerberos rejecting skewed tickets and SSSD losing identities. The
# script needs a predicate it can test and roll back from, not one that exits.
_SEL = '^* 192.168.50.200   3  6  377  15  +22us[+27us] +/- 71ms'
_NOT = ('^* 185.125.190.57   2 10  377 290 +912us +/- 72ms\n'
        '^- 192.168.50.200   3  6  377  15  +22us +/- 71ms')
rc, out = foundation('hx_ntp_selected', _SEL, '192.168.50.200')
check('foundation: hx_ntp_selected returns true for the selected source',
      rc == 0, out)
rc, out = foundation('hx_ntp_selected', _NOT, '192.168.50.200')
check('foundation: hx_ntp_selected returns false, it does not exit, when unselected',
      rc == 1, out)

# The rollback has to be in the script, not just in the intention.
_found = io.open(os.path.join(SRC, 'docs', '03-runbooks', 'common',
                              '00-foundation.sh'), encoding='utf-8').read()
# The chrony package removes systemd-timesyncd, so a failure path that stops
# chrony to "restore" it leaves the host with no time source at all. HX-4
# reached exactly that state for two minutes during the first live run.
_fail_branch = _found[_found.index('if [ "$HX_NTP_OK" -ne 1 ]'):]
_fail_branch = _fail_branch[:_fail_branch.index('fi')]
check('foundation: a failed time switch does not stop chrony',
      'disable --now chrony' not in _fail_branch, _fail_branch[:400])
check('foundation: the failure path says the host still keeps time',
      'still keeps time' in _fail_branch, _fail_branch[:400])

# chrony has to be running before the old source is touched, or there is a
# window with neither.
check('foundation: chrony is started before timesyncd is disabled',
      _found.index('enable --now chrony')
      < _found.index('disable --now systemd-timesyncd'),
      _found[_found.find('time authority'):][:400])

# Sixty seconds reported a false failure on HX-4, which reached HX-1 about a
# minute after chrony started.
check('foundation: cold-start selection is given more than a minute',
      'seq 1 36' in _found, _found[_found.find('HX_NTP_OK'):][:300])

# The package starts chrony before the drop-in is written, and `enable --now`
# does nothing to a running service, so without an explicit restart chrony
# keeps the configuration it booted with and never reads HX-1. This is what
# actually failed on HX-3 and HX-4; the polling window was a symptom.
check('foundation: chrony is restarted after the drop-in is written',
      _found.index('10-hx-fleet.conf') < _found.index('systemctl restart chrony')
      < _found.index('HX_NTP_OK'),
      _found[_found.find('time authority'):][:500])

# D-028: the hold picks the pinned branch and nothing else. A filter that
# caught every nvidia package would freeze branches this decision says nothing
# about, and one that caught none would let routine patching move the driver.
# The real installed set from HX-3, not an invented one. The four packages
# that are actually the driver carry a suffix after "-server", and an
# end-anchored pattern left every one of them free while holding the
# libraries - a hold that looked like twelve packages and protected nothing
# that matters.
_PKGS = '\n'.join([
    'libnvidia-cfg1-595-server',
    'libnvidia-common-595-server',
    'libnvidia-egl-wayland1',
    'libnvidia-gl-595-server',
    'linux-firmware-nvidia-graphics',
    'nvidia-compute-utils-595-server',
    'nvidia-dkms-595-server-open',
    'nvidia-driver-595-server-open',
    'nvidia-firmware-595-server-595.71.05',
    'nvidia-kernel-common-595-server',
    'nvidia-kernel-source-595-server-open',
    'nvidia-prime',
    'nvidia-settings',
    'nvidia-utils-595-server',
    'xserver-xorg-video-nvidia-595-server',
    'libnvidia-cfg1-580-server',
])
rc, out = foundation('hx_nvidia_hold_list', _PKGS, '595')
_held = sorted(ln for ln in out.splitlines() if ln.strip())

# The ones that carry the driver itself. If these are not held, the hold is
# decoration.
for _pkg in ('nvidia-dkms-595-server-open', 'nvidia-driver-595-server-open',
             'nvidia-kernel-source-595-server-open',
             'nvidia-firmware-595-server-595.71.05'):
    check('foundation: the driver hold covers %s' % _pkg, _pkg in _held, str(_held))

check('foundation: the driver hold covers the runtime libraries too',
      'libnvidia-gl-595-server' in _held and 'nvidia-utils-595-server' in _held,
      str(_held))
check('foundation: the driver hold leaves other branches alone',
      'libnvidia-cfg1-580-server' not in _held, str(_held))
check('foundation: the driver hold leaves unrelated packages alone',
      not any(p in _held for p in ('nvidia-prime', 'nvidia-settings',
                                   'libnvidia-egl-wayland1',
                                   'linux-firmware-nvidia-graphics')),
      str(_held))
rc, out = foundation('hx_nvidia_hold_list', _PKGS, '999')
check('foundation: a branch with nothing installed holds nothing',
      [ln for ln in out.splitlines() if ln.strip()] == [], out)

# And the hold must run before the upgrade, or it holds nothing that matters.
_base = io.open(os.path.join(SRC, 'docs', '03-runbooks', 'common',
                             '01-base-admin-network-updates.sh'),
                encoding='utf-8').read()
check('foundation: the driver hold is applied before apt upgrade runs',
      'apt-mark hold' in _base
      and _base.index('apt-mark hold') < _base.index('apt upgrade'),
      _base[_base.find('D-028'):][:300])

print()

# ------------------- hx_fleet_access: the external administration proof -----
# Every other Layer 0/1 control can be checked from inside a session that has
# already authenticated, which is why this one failed unnoticed: HX-2 and HX-3
# reported ssh active throughout, while the fleet could not log in to either.
# The ssh call needs a server; the verdict does not, so it is tested here.
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    'hx_fleet_access', os.path.join(SRC, 'tools', 'hx-doc', 'hx_fleet_access.py'))
_fa = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_fa)

GOOD = 'hx-5\nKEY+SUDO-PASS\n'
check('fleet-access: a login proving host and sudo passes',
      _fa.verdict(GOOD, 'hx-5') == [], _fa.verdict(GOOD, 'hx-5'))

# The key works but the account cannot act. Reporting this as PASS is exactly
# the half-proof the standard exists to refuse.
NO_SUDO = 'hx-5\n'
_p = _fa.verdict(NO_SUDO, 'hx-5')
check('fleet-access: a login without sudo proof is refused',
      len(_p) == 1 and 'KEY+SUDO-PASS' in _p[0], _p)

# Right key, wrong machine.
_p = _fa.verdict('hx-4\nKEY+SUDO-PASS\n', 'hx-5')
check('fleet-access: an answer from the wrong host is refused',
      len(_p) == 1 and 'hx-5' in _p[0], _p)

_p = _fa.verdict('', 'hx-5')
check('fleet-access: an empty response proves nothing', len(_p) == 2, _p)

# A key on a Windows mount reads as world-readable whatever Windows thinks, so
# ssh silently declines to offer it and the server's refusal looks like the
# key being rejected. The tool has to name the real cause.
_problem = _fa.key_permission_problem(
    '/mnt/c/Users/someone/.ssh/hx_fleet_ed25519', 0o100644)
check('fleet-access: a key on a Windows mount is explained, not just refused',
      _problem is not None and 'Windows mount' in _problem, str(_problem))

check('fleet-access: a key at 0600 on a real path is accepted',
      _fa.key_permission_problem('/home/op/.ssh/hx_fleet_ed25519', 0o100600) is None,
      str(_fa.key_permission_problem('/home/op/.ssh/hx_fleet_ed25519', 0o100600)))

_problem = _fa.key_permission_problem('/home/op/.ssh/hx_fleet_ed25519', 0o100644)
check('fleet-access: a world-readable key anywhere is refused',
      _problem is not None and 'chmod 600' in _problem, str(_problem))

_problem = _fa.key_problem(pathlib.Path(os.path.join(_TMP, 'no-such-key')))
check('fleet-access: a missing private key is refused before ssh runs',
      _problem is not None and 'does not exist' in _problem, _problem)

# The host must be resolvable from the fleet inventory, or the operator is
# typing addresses by hand on build day.
# Against an isolated inventory, not the real one. Asserting a production
# address here would turn a legitimate IP change into a parser failure, and
# report drift in the fleet as a bug in the tool.
_fixture = os.path.join(_TMP, 'fleet-fixture.tsv')
io.open(_fixture, 'w', encoding='utf-8', newline='\n').write(
    'name\tip\trole\n'
    'HX-42\t10.0.0.42\tfixture host\n')
_real_fleet = _fa.FLEET
try:
    _fa.FLEET = pathlib.Path(_fixture)
    check('fleet-access: the fleet inventory resolves a known host',
          _fa.fleet_ip('hx-42') == '10.0.0.42', str(_fa.fleet_ip('hx-42')))
    check('fleet-access: resolution is case-insensitive on the host name',
          _fa.fleet_ip('HX-42') == '10.0.0.42', str(_fa.fleet_ip('HX-42')))
    check('fleet-access: an unknown host does not resolve',
          _fa.fleet_ip('hx-99') is None, str(_fa.fleet_ip('hx-99')))
finally:
    _fa.FLEET = _real_fleet

# `sudo -n true` alone can be satisfied by a cached credential timestamp, so a
# host with no NOPASSWD policy could still emit the marker. That is a false
# PASS on the one control this tool exists to prove.
_probe = _fa.remote_probe()
check('fleet-access: the sudo proof ignores cached credentials',
      'sudo -k -n true' in _probe, _probe)

# The marker must be a line, not a substring of one. A login banner that
# quoted this document would otherwise satisfy the proof.
_p = _fa.verdict('hx-5\nxKEY+SUDO-PASSx\n', 'hx-5')
check('fleet-access: the marker embedded in another line is not the marker',
      len(_p) == 1 and 'as a line of its own' in _p[0], str(_p))

# The probe prints the hostname first. Output in the other order did not come
# from the probe, whatever it contains.
_p = _fa.verdict('KEY+SUDO-PASS\nhx-5\n', 'hx-5')
check('fleet-access: the marker before the hostname is refused',
      len(_p) == 1 and 'before the hostname' in _p[0], str(_p))

# A session that printed the right thing and then exited non-zero is a proof
# failure, not a pass. Output alone is not the proof.
check('fleet-access: a clean exit is required, not just the right output',
      _fa.exit_for_session(1, 'hx-5\nKEY+SUDO-PASS\n') == 48,
      str(_fa.exit_for_session(1, 'hx-5\nKEY+SUDO-PASS\n')))
check('fleet-access: a non-zero exit with no output is a failed login',
      _fa.exit_for_session(255, '') == 47, str(_fa.exit_for_session(255, '')))
check('fleet-access: a clean exit reaches the verdict',
      _fa.exit_for_session(0, 'hx-5\n') is None,
      str(_fa.exit_for_session(0, 'hx-5\n')))
check('fleet-access: the probe asks the host to name itself',
      _probe.startswith('hostname'), _probe)

# Mode 000 sets no group or other bits, so a permission-bit check passes and
# ssh then fails to load the key - reported as a failed login rather than an
# unusable key. Root can read it regardless, so only assert where it holds.
_unreadable = os.path.join(_TMP, 'unreadable.key')
io.open(_unreadable, 'w', encoding='utf-8').write('x')
os.chmod(_unreadable, 0)
if hasattr(os, 'geteuid') and os.geteuid() != 0:
    _problem = _fa.key_problem(pathlib.Path(_unreadable))
    check('fleet-access: an unreadable key is refused before ssh runs',
          _problem is not None and 'cannot be read' in _problem, str(_problem))
os.chmod(_unreadable, 0o600)

# ------------------------- hx-base.env: the GPU expectation ----------------
# Block 2 is shared by all seventeen hosts and installed a driver on every one
# of them. Only HX-2 through HX-5 carry a card. A list on its own would repeat
# the audit's own finding, so the list is checked against the hardware and both
# disagreements have to be shown to fail.
GPU_LIST = 'hx-2 hx-3 hx-4 hx-5'
NV_PRESENT = '0x1234\n0x10de\n0x8086'
NO_NV = '0x1234\n0x8086\n0x1af4'

rc, out = foundation('hx_require_gpu_expectation', 'hx-4', GPU_LIST, NV_PRESENT)
check('gpu: a listed host with a card installs', rc == 0 and out.strip() == 'install', out)
rc, out = foundation('hx_require_gpu_expectation', 'hx-7', GPU_LIST, NO_NV)
check('gpu: an unlisted host with no card skips', rc == 0 and out.strip() == 'skip', out)
rc, out = foundation('hx_require_gpu_expectation', 'hx-4', GPU_LIST, NO_NV)
check('gpu: a listed host with no card is refused', rc == 46, out)
rc, out = foundation('hx_require_gpu_expectation', 'hx-7', GPU_LIST, NV_PRESENT)
check('gpu: an unlisted host with a card is refused', rc == 46, out)

# hx-17 is not a prefix or suffix of any listed host, but hx-2 is a substring
# of nothing here by luck rather than design, so prove the match is word-wise.
rc, out = foundation('hx_require_gpu_expectation', 'hx-1', GPU_LIST, NO_NV)
check('gpu: hx-1 is not matched by hx-2..hx-5', rc == 0 and out.strip() == 'skip', out)

# ------------------------- hx-app-lib.sh: the HTTP answer ------------------
# HX4-F06 was a service that crash-looped and reported active between restarts.
# Its curl check ran, failed every time, and the loop simply ran out, so the
# block passed on the two systemd checks that finding proved unreliable.
def applib(fn, *args):
    """Call one hx-app-lib.sh helper in a subshell; return its exit status."""
    lib = os.path.join(SRC, 'docs', '03-runbooks', 'common', 'hx-app-lib.sh')
    quoted = ' '.join("'%s'" % a.replace("'", "'\\''") for a in args)
    r = subprocess.run(
        ['bash', '-c', '. "$1" 2>/dev/null; %s %s' % (fn, quoted), '_', lib],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')

_URL = 'http://127.0.0.1:7997/health'
rc, out = applib('hx_require_http_answer', 'hx-reranker', _URL, '1')
check('app-lib: an endpoint that never answered fails the block', rc == 32, out)
rc, out = applib('hx_require_http_answer', 'hx-reranker', _URL, '0')
check('app-lib: an endpoint that answered passes', rc == 0, out)
check('app-lib: the STOP names the finding it comes from',
      'HX4-F06' in applib('hx_require_http_answer', 'hx-n', _URL, '1')[1],
      applib('hx_require_http_answer', 'hx-n', _URL, '1')[1])

# ------------------------- hx-base.env: the loopback listener --------------
# HX-6's live-dashboard WebSocket must not be reachable from the LAN, and the
# runbook listed that as an operator check until it became a gate.
_LOOPBACK = ('LISTEN 0 511 127.0.0.1:20132 0.0.0.0:*\n'
             'LISTEN 0 511 0.0.0.0:20128 0.0.0.0:*')
_LOOPBACK6 = 'LISTEN 0 511 [::1]:20132 [::]:*'
_LAN = ('LISTEN 0 511 192.168.50.206:20132 0.0.0.0:*\n'
        'LISTEN 0 511 0.0.0.0:20128 0.0.0.0:*')
_WILDCARD = 'LISTEN 0 511 0.0.0.0:20132 0.0.0.0:*'
_ABSENT = 'LISTEN 0 511 0.0.0.0:20128 0.0.0.0:*'

rc, out = foundation('hx_require_loopback_listener', _LOOPBACK, '20132')
check('listener: 127.0.0.1 passes', rc == 0, out)
rc, out = foundation('hx_require_loopback_listener', _LOOPBACK6, '20132')
check('listener: [::1] passes', rc == 0, out)
rc, out = foundation('hx_require_loopback_listener', _LAN, '20132')
check('listener: a LAN address is refused', rc == 35, out)
rc, out = foundation('hx_require_loopback_listener', _WILDCARD, '20132')
check('listener: 0.0.0.0 is refused', rc == 35, out)
rc, out = foundation('hx_require_loopback_listener', _ABSENT, '20132')
check('listener: absent is refused, not treated as compliant', rc == 35, out)

# ------------------------- hx-base.env: the OmniRoute contract -------------
# HX-6 runbook 5.3 refuses a guessed bind variable, and the owner's initial
# password is never generated by the build.
rc, out = foundation('hx_require_bind_var', '')
check('omniroute: an unset bind variable is refused', rc == 36, out)
rc, out = foundation('hx_require_bind_var', 'HOSTNAME')
check('omniroute: an observed bind variable passes', rc == 0, out)
rc, out = foundation('hx_require_supplied_secret', 'HX_OMNIROUTE_INITIAL_PASSWORD', '')
check('omniroute: a missing owner secret is refused', rc == 37, out)
rc, out = foundation('hx_require_supplied_secret', 'HX_OMNIROUTE_INITIAL_PASSWORD', 'x')
check('omniroute: a supplied owner secret passes', rc == 0, out)

# A branch tip is not a pin: HX-6 builds a recorded commit, not release/v3.8.51.
rc, out = foundation('hx_require_source_pin', '')
check('source pin: an empty commit is refused', rc == 38, out)
rc, out = foundation('hx_require_source_pin', 'release/v3.8.51')
check('source pin: a branch name is refused', rc == 38, out)
rc, out = foundation('hx_require_source_pin', '3d5baf13f41bf0e35c8b1e57f1d5119dbdaaaf3f')
check('source pin: a resolved commit passes', rc == 0, out)

# npm 11 drops an optionalDependency whose install script it will not run, and
# exits 0. The repair is upstream's; this refuses to continue when it did not take.
rc, out = foundation('hx_require_native_dep', 'better-sqlite3', '1')
check('native dep: an unresolved addon is refused', rc == 39, out)
rc, out = foundation('hx_require_native_dep', 'better-sqlite3', '0')
check('native dep: a resolved addon passes', rc == 0, out)
rc, out = foundation('hx_require_native_dep', 'better-sqlite3', '1')
check('native dep: the STOP forbids the skip flag',
      'OMNIROUTE_SKIP_NATIVE_DEP_CHECK' in out, out)

# ------------------------- 10-omniroute.sh: identity on the app tree -------
# /srv/omniroute/app is mode 750 and omniroute-owned by design, so a filesystem
# test run as the calling user answers about permission rather than about the
# tree. That reported .git as absent on a rerun and the block tried to clone
# into a populated checkout. Five accesses had the same defect.
# Split a line into the commands it actually runs. `&&`, `||`, `;` and `|`
# each start a new one, and so does a command substitution, so the check sees
# `[ -f ... ]` in `sudo -u omniroute git ... && [ -f ... ]` as its own command.
# A regex split cannot see quoting: it would cut inside single quotes, where
# none of that is shell syntax any more, just text. The scanner below tracks
# quote state instead. Inside single quotes nothing runs. Inside double quotes
# the operators are literal too, but a substitution still executes, so it
# still opens a command.
def _read_substitution(text: str, i: int) -> tuple[str, int]:
    """text[i:i+2] == '$('. Return (inner text, index past the closing ')')."""
    depth = 1
    j = i + 2
    start = j
    quote = ""
    while j < len(text):
        ch = text[j]
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "'\"":
            quote = ch
        elif text[j:j+2] == "$(":
            depth += 1
            j += 1
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start:j], j + 1
        j += 1
    return text[start:], len(text)  # unterminated: the rest is the command


def shell_segments(line: str) -> list[str]:
    """The commands a shell line actually runs, one string each."""
    segments: list[str] = []
    buf: list[str] = []
    quote = ""
    i = 0
    n = len(line)

    def flush() -> None:
        segments.append("".join(buf))
        buf.clear()

    while i < n:
        ch = line[i]
        if quote == "'":
            buf.append(ch)
            if ch == "'":
                quote = ""
        elif quote == '"':
            if ch == '"':
                quote = ""
                buf.append(ch)
            elif ch == "\\" and i + 1 < n:
                buf.append(line[i:i+2])
                i += 1
            elif line[i:i+2] == "$(":
                # A substitution inside double quotes still runs.
                inner, i = _read_substitution(line, i)
                segments.extend(shell_segments(inner))
                continue
            else:
                buf.append(ch)
        elif ch == "'" or ch == '"':
            quote = ch
            buf.append(ch)
        elif ch == "\\" and i + 1 < n:
            buf.append(line[i:i+2])
            i += 1
        elif line[i:i+2] in ("&&", "||"):
            flush()
            i += 1
        elif ch in ";|&":
            flush()
        elif line[i:i+2] == "$(":
            inner, i = _read_substitution(line, i)
            segments.extend(shell_segments(inner))
            continue
        else:
            buf.append(ch)
        i += 1
    flush()
    return segments
_ACCESS = re.compile(r"^(\[|test|node)\s")
_PRIV = re.compile(r"^sudo\s+-u\s+omniroute\s+")
# Shell keywords and one-off environment assignments sit in front of the command
# without changing which command runs. Left in place they hide the access:
# `if [ -f "$APP/x" ]` and `HOME=/srv/omniroute node "$CLI"` both fail a match
# anchored on the command token, so the check would read them as harmless.
_LEAD = re.compile(
    r"^(?:(?:if|then|elif|else|while|until|do|!)\s+"
    r"|[A-Za-z_][A-Za-z0-9_]*=\S*\s+)+"
)
# `env` wraps the real command: its own options and the assignments it
# carries sit in front of the executable without changing what runs.
# `env HOME=/srv/omniroute node "$CLI"` is a node invocation and must be
# detected as one, not skipped because the body starts with `env`.
_ENV = re.compile(
    r"^env(?:\s+-\S+|\s+[A-Za-z_][A-Za-z0-9_]*=\S*)*\s+"
)


def unprivileged_app_reads(text: str) -> list[str]:
    """Commands that touch the OmniRoute app tree without assuming its identity.

    Checked per command, not per line. Asking whether the line contains
    "sudo -u omniroute" passes `sudo -u omniroute git ... && [ -f "$APP/x" ]`,
    where the sudo belongs to the git call and the bracket test still runs as
    the caller. That is the defect this exists to catch, so a chained command
    must carry the prefix itself.
    """
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#") or not line:
            continue
        if "HX_OMNIROUTE_APP_DIR" not in line and "OMNIROUTE_CLI" not in line:
            continue
        for seg in shell_segments(line):
            seg = seg.strip()
            if "HX_OMNIROUTE_APP_DIR" not in seg and "OMNIROUTE_CLI" not in seg:
                continue
            # Strip the prefix first, then ask what the command is. Testing the
            # other way round accepts a privileged form by never recognising it
            # as an access at all, which reads as a pass for the wrong reason.
            cmd = _LEAD.sub("", seg)
            privileged = bool(_PRIV.match(cmd))
            body = _PRIV.sub("", cmd, count=1) if privileged else cmd
            # An env wrapper does not change which executable runs; strip it
            # and its options/assignments so the real command is matched.
            body = _ENV.sub("", body)
            # Only filesystem access matters; --prefix and interpolation do not.
            if not _ACCESS.match(body):
                continue
            if privileged:
                continue
            out.append(seg)
    return out

_omni = io.open(os.path.join(SRC, "docs", "03-runbooks", "common", "10-omniroute.sh"),
                encoding="utf-8").read()
_bad = unprivileged_app_reads(_omni)
check("omniroute: every app-tree read assumes the omniroute identity",
      _bad == [], "\n".join(_bad))

# The checker must be able to fail, or it is decoration.
check("omniroute: the identity check catches an unprivileged read",
      unprivileged_app_reads('[ -f "$HX_OMNIROUTE_APP_DIR/dist/server.js" ] || exit 1') != [])
check("omniroute: the identity check accepts a privileged one",
      unprivileged_app_reads('sudo -u omniroute test -f "$HX_OMNIROUTE_APP_DIR/x"') == [])

# The prefix has to belong to the command that reads the tree. Here it belongs
# to the git call, and the bracket test still runs as the caller.
_chained = ('sudo -u omniroute git -C "$HX_OMNIROUTE_APP_DIR" fetch '
            '&& [ -f "$HX_OMNIROUTE_APP_DIR/dist/server.js" ]')
check("omniroute: sudo on an earlier command does not cover a chained test",
      unprivileged_app_reads(_chained) != [], _chained)

# Same shape with the other separators, so the fix is not one operator deep.
for _sep in ("||", ";"):
    _c = 'sudo -u omniroute git -C "$HX_OMNIROUTE_APP_DIR" fetch %s test -f "$OMNIROUTE_CLI"' % _sep
    check("omniroute: sudo does not cover a command chained with %s" % _sep,
          unprivileged_app_reads(_c) != [], _c)

# A command substitution is its own command too.
check("omniroute: an unprivileged read inside a substitution is caught",
      unprivileged_app_reads('V="$(node "$OMNIROUTE_CLI" --version)"') != [])
check("omniroute: a privileged read inside a substitution is accepted",
      unprivileged_app_reads('V="$(sudo -u omniroute node "$OMNIROUTE_CLI" --version)"') == [])

# A background separator starts a new command as surely as the others do.
_bg = 'sudo -u omniroute git -C "$HX_OMNIROUTE_APP_DIR" fetch & node "$OMNIROUTE_CLI" --version'
check("omniroute: sudo does not cover a command chained with &",
      unprivileged_app_reads(_bg) != [], _bg)

# Quoting changes what runs. Inside single quotes an operator or a
# substitution is text, so the scanner must not cut there; inside double
# quotes the operators are literal too, but a substitution still executes.
_sq = "echo '&& [ -f \"$HX_OMNIROUTE_APP_DIR/dist/server.js\" ] && $(node \"$OMNIROUTE_CLI\")'"
check("omniroute: operators and substitutions in single quotes are not commands",
      unprivileged_app_reads(_sq) == [], _sq)
check("omniroute: a substitution inside double quotes still runs",
      unprivileged_app_reads('msg="x $(node "$OMNIROUTE_CLI" --version)"') != [])
check("omniroute: an operator inside double quotes is literal",
      unprivileged_app_reads('msg="a && [ -f "$HX_OMNIROUTE_APP_DIR/x" ]"') == [])

# A shell keyword in front of the command does not change which command runs.
# Anchoring on the command token alone read these as harmless.
check("omniroute: an unprivileged test behind `if` is caught",
      unprivileged_app_reads('if [ -f "$HX_OMNIROUTE_APP_DIR/dist/server.js" ]; then') != [])
check("omniroute: a privileged test behind `if !` is still accepted",
      unprivileged_app_reads('if ! sudo -u omniroute test -d "$HX_OMNIROUTE_APP_DIR/.git"; then') == [])

# Same for a one-off environment assignment.
check("omniroute: an unprivileged node behind an env assignment is caught",
      unprivileged_app_reads('HOME=/srv/omniroute node "$OMNIROUTE_CLI" --version') != [])
check("omniroute: a privileged node behind an env assignment is accepted",
      unprivileged_app_reads('sudo -u omniroute env HOME=/srv/omniroute node "$OMNIROUTE_CLI" -v') == [])

# An env wrapper is not the command: its options and assignments must be
# stripped before the executable is matched, or the access hides behind it.
_env = 'env HOME=/srv/omniroute node "$OMNIROUTE_CLI" --version'
check("omniroute: an unprivileged node behind env is caught",
      unprivileged_app_reads(_env) != [], _env)
check("omniroute: a privileged node behind env is accepted",
      unprivileged_app_reads('sudo -u omniroute env HOME=/srv/omniroute node "$OMNIROUTE_CLI" -v') == [])
check("omniroute: env with options still exposes the command",
      unprivileged_app_reads('env -i HOME=/srv/omniroute node "$OMNIROUTE_CLI" --version') != [])

# The native-dependency probes run inside `bash -lc`, which the per-command
# identity check cannot see into. Their shape is gated directly instead: the
# probe must carry the service identity and must cd into the application tree
# before node runs, because a probe whose cwd is still the caller's home
# cannot traverse the 750 omniroute-owned tree and answers "module not found"
# about a package that is installed. HX-6 proved exactly that false negative.
_resolves_fn = re.search(
    r"^omniroute_resolves\(\) \{\n(.*?)^\}", _omni, re.S | re.M)
check("omniroute: the resolution probe exists", bool(_resolves_fn))
if _resolves_fn:
    _rf = _resolves_fn.group(0)
    check("omniroute: the resolution probe runs as the service identity",
          "sudo -u omniroute bash -lc" in _rf, _rf)
    # The cd must be guarded so a failed cd stops the probe: `cd ... || exit`
    # is required, and a `|| true` or semicolon fallback that would run node
    # from the wrong directory anyway is refused.
    check("omniroute: the resolution probe cds into the app tree before node",
          re.search(r"cd '\$HX_OMNIROUTE_APP_DIR' \|\| exit \d+", _rf) is not None
          and not re.search(r"cd '\$HX_OMNIROUTE_APP_DIR'[^\n]*(\|\| true|;\s*\n\s*node)", _rf),
          _rf)
_loads_fn = re.search(
    r"^omniroute_native_loads\(\) \{\n(.*?)^\}", _omni, re.S | re.M)
check("omniroute: the native-load probe exists", bool(_loads_fn))
if _loads_fn:
    _lf = _loads_fn.group(0)
    check("omniroute: the native-load probe runs as the service identity",
          "sudo -u omniroute bash -lc" in _lf, _lf)
    check("omniroute: the native-load probe cds into the app tree before node",
          re.search(r"cd '\$HX_OMNIROUTE_APP_DIR' \|\| exit \d+", _lf) is not None
          and not re.search(r"cd '\$HX_OMNIROUTE_APP_DIR'[^\n]*(\|\| true|;\s*\n\s*node)", _lf),
          _lf)
    # The runbook writes the JS inside a double-quoted shell string, so its
    # quotes are escaped. Unescape them, strip comments, and match the
    # executable require -> open -> close sequence, not substrings that a
    # comment or dead code could satisfy.
    _lf_js = "\n".join(
        line.split("#", 1)[0]
        for line in _lf.replace('\\"', '"').splitlines()
    )
    check("omniroute: the native-load probe loads better-sqlite3",
          re.search(r'require\("better-sqlite3"\)\(":memory:"\)', _lf_js) is not None,
          _lf_js)
    check("omniroute: the native-load probe closes the database after opening it",
          re.search(r'require\("better-sqlite3"\)\(":memory:"\).*db\.close\(\)',
                    _lf_js, re.S) is not None, _lf_js)
check("omniroute: the native load is gated, not just noted",
      re.search(
          r"omniroute_native_loads && _nl=0 \|\| _nl=1.*"
          r'hx_require_native_dep\s+"better-sqlite3 native addon"\s+"\$_nl"',
          _omni,
          re.S,
      ) is not None)

# The cwd mechanism itself, not just its shape. The HX-6 false negative was:
# node run as the service identity with its cwd still inside the caller's
# home, which the service identity cannot traverse, so Node cannot read the
# package configs along the resolution path and answers "Cannot read package
# config ... permission denied" about a package that is installed. The cd-first
# form fails loudly at the cd instead, which is detectable. Reproduced here
# with a 0750 agentzero-owned directory and the probe run as nobody.
_cwd = os.path.join(_TMP, 'cwd-check')
os.makedirs(_cwd, mode=0o750)
_r = subprocess.run(
    ['sudo', '-u', 'nobody', 'node', '-e', 'require.resolve("better-sqlite3")'],
    cwd=_cwd, capture_output=True, text=True)
check("cwd: a probe from an untraversable cwd misreads an installed package",
      _r.returncode != 0 and 'permission denied' in _r.stderr, _r.stderr[-300:])
_r = subprocess.run(
    ['sudo', '-u', 'nobody', 'bash', '-c',
     "cd '%s' && node -e 'require.resolve(\"better-sqlite3\")'" % _cwd],
    capture_output=True, text=True)
check("cwd: the cd-first probe fails loudly at the cd, not silently",
      _r.returncode != 0 and 'cd:' in _r.stderr, _r.stderr[-300:])
# The control needs a world-traversable path from the root down: a 0755 leaf
# under the 0700 mkdtemp parent is still unreachable for nobody.
_open = tempfile.mkdtemp(prefix='hx-gate-open-', dir='/tmp')
os.chmod(_open, 0o755)
_r = subprocess.run(
    ['sudo', '-u', 'nobody', 'node', '-e', 'require.resolve("better-sqlite3")'],
    cwd=_open, capture_output=True, text=True)
check("cwd: a traversable cwd gives the honest module-not-found",
      _r.returncode != 0 and "Cannot find module 'better-sqlite3'" in _r.stderr,
      _r.stderr[-300:])
os.chmod(_open, 0o700)
try:
    shutil.rmtree(_open)
except OSError as exc:
    print(f"warning: could not remove {_open}: {exc}")

# Not ignore_errors: a workspace that cannot be removed is worth saying out
# loud, but it is not a gate failure, so it does not change the exit status.
try:
    shutil.rmtree(_TMP)
except OSError as exc:
    print(f"warning: could not remove {_TMP}: {exc}")
print('\npassed=%d failed=%d' % (passed, failed))
raise SystemExit(1 if failed else 0)
