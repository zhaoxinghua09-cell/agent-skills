# mcp-security-scan · MCP 安全扫描

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — An MCP server is a *third party to audit*. Before connecting, scan its tool list for command-exec / file-write / network-egress / credential-exposure risks, rate each tool and advise least-privilege. Ships a zero-dependency `mcp_scan.py`.

**中文** — 把 MCP server 当需审查的第三方：接前扫工具清单的命令执行/文件写/网络外联/凭证暴露四类风险，给评级与最小授权建议。零依赖 `mcp_scan.py`。

## Why it beats "connect and trust"

| Pain | This skill |
|---|---|
| MCP can run shell | Command-exec flagged 高 |
| Silent data exfil | Network-egress flagged |
| Token in tool desc | Credential-exposure flagged |
| "Just enable all tools" | Least-privilege, disable extras |

## What's inside

- `SKILL.md` — 4-risk model + 3-step audit flow + 铁律
- `scripts/mcp_scan.py` — zero-dependency CLI: scan a tools.json (name+desc), rate risk per tool + overall advice

```bash
python scripts/mcp_scan.py --tools tools.json
python scripts/mcp_scan.py --tools tools.json --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| MCP auth scopes | Pre-connect tool-level risk rating |
| Manual read of tools | Repeatable lexical scan |
| "It's official" | Explicit high-risk flag, not trust |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `tool-call-guard` and `prompt-injection-shield`.

---

© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237) · 代码 MIT · 理论文本保留所有权利

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : uibc-core = Apache-2.0 (see repo LICENSE)
                    本文本与理论表述不在 Apache-2.0 覆盖范围内
引用格式 (cite as)      : uibc-core/CITATION.cff · concept DOI 10.5281/zenodo.22821834
首次公开锚 (first public): 2026-09-17 13:31:45 UTC (commit cb6f11b)
                    外锚 (external anchor): Sigstore Rekor logIndex 2883389783
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
