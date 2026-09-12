---
type: operations
title: Version pins and upstream drift
description: How software provenance is controlled — the package-source rule with its allowed, driver-only and forbidden sources, where every pin and checksum lives, the pre-build fetchability check, the pin-currency audit, and the reviewed-commit drift report for governed skills.
tags: [pins, versions, provenance, package-sources, drift, preflight, supply-chain]
verified:
  - by: openwiki/0.5.1
    at: 2026-09-12T03:13:20.331Z
sources:
  - id: openwiki-source-8adfdcfda59f3105449a5918
    resource: repo://docs/00-control/DECISIONS.md
  - id: openwiki-source-667355bbf619c0e53d4f76d4
    resource: repo://docs/03-runbooks/common/hx-base.env
  - id: openwiki-source-3edf0d2c56c6b02f0e70353e
    resource: repo://tools/hx-doc/hx_preflight.py
  - id: openwiki-source-1b6936d3e99ab8243153e1c6
    resource: repo://tools/hx-doc/hx_upstream_drift.py
  - id: openwiki-source-66d9417f03ff09c95f5bfe2d
    resource: repo://tools/hx-doc/hx_version_pins.py
  - id: openwiki-source-26d8089dce8fb91d7e894258
    resource: repo://tools/hx-smoke-runner/requirements.txt
generated: { by: "claude-code", at: "2026-09-12T03:13:20.331Z" }
---

# Version pins and upstream drift

Nothing on this fleet installs "the current version". Every application, model
and driver is pinned, most artifacts are checksummed, and three tools watch
whether those pins are still fetchable, still current and still what was
reviewed.

## The package-source rule

Application software comes from PyPI, npm, a GitHub release, an upstream source
tarball, a direct binary, or Hugging Face.

The Ubuntu archive is permitted for the NVIDIA driver, build toolchains and
library headers, and nothing else. **Snap is never permitted, for anything, the
driver included** — a ratified decision taken because two rules in the
repository disagreed: the review configuration said Snap was never permitted
while the runbook environment and the pin auditor treated it as acceptable for
drivers. The owner ratified the stricter wording and the auditor was changed to
match.

The auditor encodes the rule as three sets — approved application sources,
driver-only sources, and never-permitted sources — and reports a violation as
`REVIEW` with a migration note rather than a bare failure. A Snap pin is refused
whatever it is for; an Ubuntu-archive pin is refused for anything that is not a
driver. The rule check is deliberately factored out of the reporting loop so it
can be exercised without touching the network, which is what makes it cheap to
test — see [enforcement gate tests](../testing/enforcement-gate-tests.md), which
holds five checks on this rule alone.

## Where pins live

`docs/03-runbooks/common/hx-base.env` is the single place a version changes for
every server not yet built. It carries the Ollama version and its archive
SHA-256, the NVIDIA branch and exact package version, the reranker checkpoint
with an immutable commit revision plus its serving runtime and port, and one
pin per remaining fleet application — OmniRoute, NGINX, Open WebUI, PostgreSQL,
Redis, Qdrant, LightRAG, Deep Agents, Mem0, Node.js, n8n, FastMCP, Docling with
Granite-Docling, and Crawl4AI with Playwright.

Two secondary locations hold pins as well: the smoke runner's
`requirements.txt`, and inline pins inside the HX-12 runbook. The auditor
collects from all three.

Several pins carry a note explaining what the pin is actually fixing, which
matters when the pin cannot mean the obvious thing:

- The NGINX hash was computed from the published tarball because nginx.org signs
  releases with PGP and publishes no checksum file, so the pin fixes the
  artifact this repository reviewed rather than restating an upstream hash.
- The Redis pin moved to the published release tarball because a GitHub tag
  archive is generated on request and its bytes are not guaranteed stable, so it
  cannot be pinned at all.
- Playwright is pinned rather than Chromium, because Playwright decides which
  browser build lands and verifies that download itself; there is no stable
  archive URL for this repository to checksum.
- The reranker and Granite-Docling models are pinned to immutable commit
  revisions so a later upstream edit cannot change the model under a stable
  name.

Changing a pin does not retroactively change a closed server record; if a closed
server is upgraded, its record is updated and it is re-validated.

The runner's `requirements.txt` goes further, documenting the gap between direct
pins and a supply-chain-verified install: it records the exact command to
generate a fully hashed lock file, notes that the bootstrap installs from that
lock with `--require-hashes` when it exists and warns loudly when it does not,
and includes reference hashes for the two direct wheels.

## Before build day: is it still there?

```bash
tools/hx-doc/hx-preflight
```

A 404 discovered on a lab machine costs lab time. Preflight asks, from anywhere
and in about thirty seconds, whether every pinned artifact is still fetchable.
It downloads nothing.

It checks each direct download URL the install blocks use; each pinned PyPI
version, failing on a missing distribution **or a yanked one**; each pinned npm
version; each pinned Hugging Face model revision; and whether the pinned NVIDIA
driver is still published for noble/amd64, paged through the Ubuntu archive API
and filtered to the right series, architecture and pocket.

Two details show the care taken over false results. Some content delivery
networks refuse a `HEAD`, so the URL check falls back to a one-byte ranged `GET`
rather than reporting the artifact missing. And the guard at the start tests the
*input*, not the output: an empty environment file is the real failure case,
since it would make every pin read as missing, whereas a guard on the result
list could never fire because a result is always recorded.

## Are the pins still current?

```bash
tools/hx-doc/hx-version-pins       # products, models, drivers, Python deps
tools/hx-doc/hx-upstream-drift     # reviewed skill commits
```

The first compares each product pin with what upstream currently ships, across
PyPI, npm, GitHub releases, Hugging Face, the Ubuntu archive, PostgreSQL and the
Node.js and NGINX release listings. It exists because Ollama 0.34.0 shipped four
days before the documents were written and nobody knew.

The second reads the reviewed commits **out of the skill registry itself**,
rather than keeping a second hard-coded list that could fall out of step with
the registry, then asks each upstream for its head and how far behind the pin
is. Its parser refuses an unbalanced provenance block: `zip()` silently drops a
surplus, so a block listing more repositories than reviewed commits would either
skip a pin or pair a repository with another entry's commit and report drift
against the wrong thing.

### Drift is information; unreachable is not

Both tools separate "the pin moved" from "we could not look". A drifted pin is
reported and, in the weekly job, opens or updates a single issue — the pin stays
valid until the owner decides to move it, and the response is to re-review the
source and update both the reviewed commit and the last-reviewed date.

An unreachable upstream is a different thing entirely: nothing was compared.
`--fail-on-drift` therefore exits non-zero on errors as well as drift, because
returning success for a network failure made the flag pass on nothing, and the
weekly workflow raises an explicit error when the report mentions an unreachable
upstream. See
[continuous integration workflows](continuous-integration-workflows.md).

## Where verification actually bites

Pins are only half of it; the build path verifies what it downloads. The shared
runbook helper refuses to fetch anything without a recorded SHA-256, deletes an
artifact that fails its check so a later step cannot pick it up, and the Ollama
install keeps the previous installation until the new one is in place. That side
is covered in
[server base-build runbooks](../workflows/server-base-build-runbooks.md).
