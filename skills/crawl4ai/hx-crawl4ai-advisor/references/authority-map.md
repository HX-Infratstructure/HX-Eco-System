# Crawl4AI authority map

## Decision hierarchy

| Question | Primary authority | Role of this skill/upstream |
|---|---|---|
| Where Crawl4AI runs | HX architecture / owner | No authority to move HX-17 |
| Deployment form | HX native-deployment rule / future HX-17 runbook | Reject container defaults |
| Current build state | `CURRENT-STATE.md`, `BUILD-STATE.md`, live evidence | Skill approval does not change state |
| Package/version/environment | future HX-17 runbook + current official package/release facts | Recommend, do not silently select |
| Browser/runtime placement | future HX-17 runbook | Product docs inform requirements only |
| Crawl/SDK/CLI behavior | current official Crawl4AI docs/source | Community skill may supplement after verification |
| LLM provider/model | HX owner/model/provider authority | Tutorials/community defaults cannot select provider |
| Network/proxy/auth/session controls | owner/HX security-network authority | Upstream defaults are advisory only |
| Crawl4AI MCP implementation | future HX-17 runbook + `MCP-STANDARD.md` | Official bridge is source evidence, not automatic deployment |
| Core PASS | `smoke-tests/crawl4ai-smoke-test.md` | Skill may prepare/troubleshoot, not redefine PASS |
| MCP PASS | `smoke-tests/mcp-companion-smoke-test.md` | Companion must independently pass after core |
| Permanent RAG ingestion | later owner-approved integration design | Not part of BASE |

## Upstream trust classes

### Official product — `VENDOR_OFFICIAL`

`unclecode/crawl4ai`, official docs, package metadata, release notes.

Use as primary upstream product authority after HX authority.

### Official assistant skill — `VENDOR_OFFICIAL / REFERENCE_ONLY`

The official docs publish an AI-assistant skill ZIP but label it compatible with Crawl4AI 0.7.4 while the reviewed product release is 0.9.3. Use for historical/structural ideas only unless its content is revalidated against the installed product version.

### Brett Davies skill — `COMMUNITY / EXPERT REFERENCE`

`brettdavies/crawl4ai-skill` is a strong portable skill bundle, current release 2.0.1, verified by its own metadata against Crawl4AI 0.8.9. It is useful for patterns, examples, and troubleshooting, but must be checked against official 0.9.x behavior before material use.

### ExplainX — `SECONDARY / DISCOVERY ONLY`

ExplainX is useful for finding the Brett skill and agent-host install instructions. It is not product/version/provenance/trust authority. At review, its displayed update/review chronology did not reconcile with the repository's own release history; do not use ratings or timestamps as admission evidence.

## Recommendation mapping

- Current official SDK/CLI behavior compatible with HX -> `ACCEPT`
- Useful upstream/community pattern needing HX shaping -> `ADAPT`
- Valuable but outside BASE/current role -> `REFERENCE_ONLY`
- Container/cloud/direct community installation or hard-coded unapproved provider -> `REJECT_FOR_HX`
- Unresolved package/service/MCP/network/session/provider choice -> `OWNER_DECISION_REQUIRED`
