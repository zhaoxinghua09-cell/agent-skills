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

© LGD / SynomosAI 2026 · MIT · 理论 CC BY 4.0
