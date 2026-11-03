# lgd-audit — LGD 审计中枢（AUDIT phase hub）

Thin dispatcher for the **AUDIT** phase of [GovernanceOS](https://github.com/zhaoxinghua09-cell/governanceos): routes 10 audit sub-skills by slug, probes their real availability, never vendors their internals.

## Nodes (10)

`lgd-badge-issuer` · `lgd-badge-verify` · `lgd-three-laws-auditor` · `agent-trace-audit` · `bias-auditor` · `env-var-audit` · `ai-governance-audit-chain` · `audit-trail-keeper` · `expert-package-compliance-audit` · `traceability-audit-team`

## Usage

```bash
python scripts/lgd_audit_dispatcher.py --list              # show 10 nodes
python scripts/lgd_audit_dispatcher.py --route lgd-badge-verify
python scripts/lgd_audit_dispatcher.py --verify --json-out evidence.json
```

`--verify` honestly grades each node: **LIVE** (script runs rc=0) / **PRESENT** (dir exists, doc-only) / **ECOSYSTEM** (install via `openclaw plugins install clawhub:<slug>`) / **ERROR**.

## Install

`openclaw plugins install clawhub:governanceos` (GovernanceOS wires this hub into the full SPEC → PLAN → GATE → AUDIT → EVO lifecycle).

License: MIT (code) / CC BY 4.0 (methodology text).
