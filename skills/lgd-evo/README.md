# lgd-evo — LGD 演化中枢（EVO phase hub）

Thin dispatcher for the **EVO** phase of [GovernanceOS](https://github.com/zhaoxinghua09-cell/governanceos): routes the evolution sub-skill by slug, probes its real availability, never vendors its internals.

## Nodes (1)

`agent-evolution` — self-improvement loop (registered/evidenced; since 2026-11-04 ships a runnable checker `scripts/evolution_check.py` for its capability-card evolution records — graded LIVE by `--verify` when the probe runs it clean).

## Usage

```bash
python scripts/lgd_evo.py --list              # show EVO nodes
python scripts/lgd_evo.py --route agent-evolution
python scripts/lgd_evo.py --verify --json-out evidence.json
```

`--verify` honestly grades each node: **LIVE** (script runs rc=0) / **DOC-ONLY** (dir exists, no runnable script → NOT VERIFIED: present on disk, never executed or validated) / **ECOSYSTEM** (install via `openclaw plugins install clawhub:<slug>`) / **ERROR**. Hollow-hub rule: if no node is LIVE, `--verify` prints a `HOLLOW` warning and exits rc=1 — a hub that verified zero runnable nodes never reports green.

## Install

`openclaw plugins install clawhub:governanceos` (GovernanceOS wires this hub into the full SPEC → PLAN → GATE → AUDIT → EVO lifecycle).

License: MIT (code) / CC BY 4.0 (methodology text).
