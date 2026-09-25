# Agent Teams — Team Specs

Team specifications published in the [Agent Teams Market](https://www.teamsmarket.com) Team Spec format: a self-contained Markdown document describing a multi-agent team, its members, its operating principles, its workflow, and the artifacts it produces.

Each spec is standalone — no runtime dependency, no bundled scripts. A team spec describes *what the team is and how it works*, so it can be read, reviewed, and reproduced by anyone.

## Teams

| Slug | Team | Members | Category | What it governs |
|---|---|---|---|---|
| [`symbiosis-expert-team`](symbiosis-expert-team.md) | Symbiosis Expert Team / 共生专家团 | 5 | Security & Compliance | Governance embedded in every member: agent identity, portable AI passports, AI-to-AI liaison, hardware extension, capability infusion |
| [`wb-safe-team`](wb-safe-team.md) | Safe Ops Team / 安全稳定运行专家团 | 6 | DevOps & Infrastructure | The AI assistant runtime itself: credentials and encryption, cost governance, runtime health, config drift, risk readiness, recovery |
| [`traceability-audit-team`](traceability-audit-team.md) | Traceability Audit Team / 溯源审计团 | 3 | Security & Compliance | Provenance and identity claims: standards grounding, three-anchor verification, reproducible evidence-chained audit reports |
| [`device-market-access-team`](device-market-access-team.md) | Device Market Access Team / 医械国际准入专家团 | 6 | Security & Compliance | Multi-market medical-device registration: EU MDR, US FDA, Japan PMDA, Southeast Asia, Gulf and Latin America, as one sequenced roadmap |
| [`content-publish-ops-team`](content-publish-ops-team.md) | Content Publishing Ops Team / 内容发布运营团 | 6 | Content Marketing | External publishing for regulated industries: material provenance, de-identification, channel-native drafting, single-veto pre-publish review, confirmation-gated release, and a publishing ledger |

### Teams deliberately not listed here

Some internal teams carry a charter restriction that prohibits publishing their operating method on any public remote. Those teams are omitted from this directory by design, not by oversight — a spec in this format necessarily describes a team's roles, workflow and review mechanism, which is exactly what such a charter withholds. Where a team's charter and this directory conflict, the charter governs.

## What a Team Spec contains

Every spec in this directory follows the same structure:

- **Frontmatter** — name, slug, category, description, long description, agent count, difficulty, tags, author, version
- **Overview** — the problem the team addresses and where it sits relative to neighbouring teams
- **Team Members** — per member: role, expertise, responsibilities (each naming a concrete tool, technique, or metric), and boundaries
- **Key Principles** — the positions the team takes, including what it rules out
- **Boundaries** — what the team will not do, and where those requests are routed instead
- **Workflow** — the operating steps, each with an owner and a stated success criterion
- **Output Artifacts** — the deliverables a run produces
- **Ideal For** — the situations the team is built for
- **Integration Points** — how the team hands off to adjacent functions

## Reading and using these specs

A team spec is a description, not an executable artifact. To run a team in this format on a supported host, the team is reconstituted from the member definitions in the spec — each member's role, responsibilities, and boundaries become that member's instruction set, and the workflow becomes the orchestration order.

Where the same team is also shipped as a host-specific package, the spec remains the authoritative description of *intent*; the package is one implementation of it. Where the two diverge, the divergence is a defect in the package, not in the spec.

## Related

- **Skills** — see [`../skills/`](../skills/) for the standalone, runnable skill library.
- **Theory** — the governance model these teams operate under is described in the [LGD theory stack](https://github.com/zhaoxinghua09-cell/lgd-theory).

## License

MIT — see [`../LICENSE`](../LICENSE). Specs authored by SynomosAI.
