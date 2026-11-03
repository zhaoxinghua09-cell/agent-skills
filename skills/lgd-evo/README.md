# lgd-evo — LGD 演化中枢（EVO phase hub）

Thin dispatcher for the **EVO** phase of [GovernanceOS](https://github.com/zhaoxinghua09-cell/governanceos): routes the evolution sub-skill by slug, probes its real availability, never vendors its internals.

## Nodes (1)

`agent-evolution` — self-improvement loop spec (registered/evidenced; doc-only PRESENT state, no executable yet — honesty-graded by `--verify`).

## Usage

```bash
python scripts/lgd_evo.py --list              # show EVO nodes
python scripts/lgd_evo.py --route agent-evolution
python scripts/lgd_evo.py --verify --json-out evidence.json
```

`--verify` honestly grades each node: **LIVE** (script runs rc=0) / **PRESENT** (dir exists, doc-only) / **ECOSYSTEM** (install via `openclaw plugins install clawhub:<slug>`) / **ERROR**.

## Install

`openclaw plugins install clawhub:governanceos` (GovernanceOS wires this hub into the full SPEC → PLAN → GATE → AUDIT → EVO lifecycle).

License: MIT (code) / CC BY 4.0 (methodology text).
