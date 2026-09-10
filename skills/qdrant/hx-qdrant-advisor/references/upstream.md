# Official Qdrant Skill Source

## Trust classification

- Provider: Qdrant
- Classification: Vendor Official / Meta-skill
- Repository: `qdrant/skills`
- Preferred skill: `meta/qdrant-advisor`
- Live catalog: `https://skills.qdrant.tech`
- Live search: `https://skills.qdrant.tech/search?query=<encoded query>`
- Review date: 2026-09-09
- Reviewed upstream commit: `b0941d03eddf88629306aa16588383400e68230b`

The reviewed official Advisor instructs agents to fetch current skill guidance live rather than answer Qdrant questions from memory. The Qdrant documentation also recommends the Advisor as the preferred entry point because it traverses only the relevant branch of Qdrant's evolving skill hierarchy.

## HX consumption policy

Prefer live consumption over vendoring the full Qdrant skill tree into HX.

Reason:

- Qdrant skills evolve independently of HX;
- a static full copy can become stale;
- live contextual loading keeps agent context smaller;
- HX needs Qdrant expertise, not Qdrant ownership of HX architecture.

This HX wrapper therefore carries HX-specific context and governance, then consults the live official Advisor for product expertise.

## Current official hub areas observed at review

The Qdrant skill catalog includes hub guidance for areas such as:

- client SDKs;
- scaling;
- performance optimization;
- search quality;
- monitoring;
- deployment options;
- edge;
- model migration;
- version upgrades.

Do not treat this list as complete or frozen. Search the live catalog for the actual task.

## Deployment-choice warning

Official Qdrant guidance legitimately covers Docker, self-hosted, Cloud, embedded, and other deployment patterns. HX has already chosen native self-hosted Qdrant on HX-10 unless the infrastructure owner changes that decision.

Use vendor deployment skills to understand Qdrant constraints and best practices, not to override HX placement or introduce a different deployment architecture automatically.
