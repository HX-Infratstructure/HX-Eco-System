# Qdrant Agent Skills — Upstream Source Record

- Vendor/project: Qdrant
- Classification: `VENDOR_OFFICIAL + META`
- Repository: `qdrant/skills`
- Official live catalog: `https://skills.qdrant.tech`
- Preferred official meta-skill: `meta/qdrant-advisor`
- Reviewed upstream branch: `main`
- Reviewed upstream commit: `b0941d03eddf88629306aa16588383400e68230b`
- Reviewed date: 2026-09-09
- HX consumption mode: live Advisor/contextual fetch; no full-tree vendoring
- HX wrapper: `../hx-qdrant-advisor/`

## Current official behavior

The Qdrant Advisor is designed to fetch the relevant Qdrant skill guidance live from `skills.qdrant.tech`, traverse only the branch needed for the current problem, and use canonical Qdrant documentation for implementation detail.

The upstream skill system covers areas including deployment choices, SDKs, scaling, performance, search quality, monitoring, model migration, and version upgrades.

## HX boundary

The upstream source is product expertise, not HX architecture authority.

Qdrant guidance that conflicts with owner-approved HX placement/deployment/network/model rules must be adapted, rejected for HX, or escalated for owner decision according to `../../SKILL-GOVERNANCE.md`.
