# HX Qdrant Skills

Qdrant is the first reference implementation of the governed HX skill architecture.

## HX placement

```text
HX-10 / 192.168.50.210
├── Qdrant
├── native Web UI
└── Qdrant MCP
```

Current state: `NOT STARTED` until HX-10 is built and evidence closes its base gates.

## Skill structure

```text
skills/qdrant/
├── README.md
├── upstream/
│   └── SOURCE.md
└── hx-qdrant-advisor/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── hx-context.md
        ├── authority-map.md
        └── upstream.md
```

## Design

`hx-qdrant-advisor` is an HX-native wrapper around current official Qdrant expertise.

The wrapper establishes HX context first, then uses Qdrant's official Advisor model to fetch only the current vendor skill branch relevant to the task.

```text
HX architecture / decisions
          ↓
HX-10 context + runbook
          ↓
hx-qdrant-advisor
          ↓
live Qdrant Advisor guidance
          ↓
reconcile vendor advice with HX
          ↓
execute from HX authority
          ↓
validate from HX smoke authority
```

## Why not vendor the entire Qdrant skill tree?

Qdrant's official Advisor is designed to load the current skill hierarchy live. Keeping a static full copy in HX would create unnecessary duplication and staleness risk.

HX therefore retains:

- stable HX-specific wrapper logic;
- explicit upstream provenance;
- current reviewed upstream commit;
- live vendor consumption as the default.

## Authority boundary

Qdrant expertise may influence Qdrant-specific configuration and diagnosis, but it cannot by itself:

- move Qdrant away from HX-10;
- switch HX to Docker/Cloud/embedded deployment;
- create an unapproved cluster;
- redesign DNS/routing/firewall/TLS;
- change embedding/model placement;
- change HX smoke-test acceptance criteria;
- create permanent integration during BASE stand-up.

See `../SKILL-GOVERNANCE.md` and `hx-qdrant-advisor/SKILL.md`.
