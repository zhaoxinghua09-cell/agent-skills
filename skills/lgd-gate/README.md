# lgd-gate — LGD 门禁中枢（GATE Phase Umbrella）

One-stop entry to the **GATE phase** of [GovernanceOS](https://github.com/zhaoxinghua09-cell/governanceos): the 8 release-gate nodes that decide whether a skill/agent is allowed to ship.

## What it does

- `--list` — show all 8 GATE nodes with when-to-use and expected output.
- `--route <slug>` — print the exact call note for one node.
- `--verify` — **honest availability probe**: runs each node's script with `--help` and grades it LIVE / PRESENT / ECOSYSTEM / ERROR. Never fakes green.
- `--verify --json-out evidence.json` — machine-readable evidence.

## The 8 GATE nodes

skill-quality-gate · publish-quality-gate · skill-admission-gate · publish-review-gate · release-gate-check · skill-release-gate · human-oversight-gate · gate-policy-generator

## Design

Thin dispatcher only — routes by slug, zero vendored code, fully pluggable. Nodes live as independent skills and version independently.

## Part of GovernanceOS

🛡️ **Part of [GovernanceOS](https://github.com/zhaoxinghua09-cell/governanceos)** — the 24-node AI-agent governance lifecycle (SPEC → PLAN → GATE → AUDIT → EVO).
One-command install: `openclaw plugins install clawhub:governanceos`

Sister hubs: [`lgd-audit`](../lgd-audit/) (AUDIT phase, 10 nodes) · [`lgd-evo`](../lgd-evo/) (EVO phase)
