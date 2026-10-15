# evid-four-check · 电子证据四性审查判定器

> AI-assisted decision-support CLI. **NOT legal advice**, **not a legal conclusion** — verify against official texts. Text verified: 2026-09-26.

[![LGD-Powered](https://medxpert.cn/badge/powered/svg/lgd-powered-cn.svg)](https://medxpert.cn/lgd.html)

## What it does
Reviews electronic evidence on the four properties — 真实性 / 合法性 / 关联性 / 完整性 — per official rules: **最高人民法院《关于民事诉讼证据的若干规定》第14条、第93-95条 + 《人民法院在线诉讼规则》第12-18条**（clause numbers **pending manual verification** — see `clause_review_checklist` in the output; official texts prevail）.

- **Insufficient input → strict presumption (从严推定)**: any dimension that cannot be determined because an argument is missing is judged **FAIL（待补强）** — the most obligation-heavy outcome among the possible ones. The tool states the **possible range** and how to supply the missing argument in `warnings`, and sets `rc=1`. It never silently returns a lenient (PASS) conclusion. `dimension_basis` marks each dimension as `明确输入` or `从严推定（输入不完整）`.
- **Out of scope**: substantive review of the **legality of the collection method** (the tool's 「合法性」 is a formal check only — was an evidence type declared), admissibility/probative-weight judgment, notarisation & expert-opinion effect, cross-examination and spoliation (第95条) discretion, foreign/criminal/administrative rules, physical verification of originals.

## Install & run (zero-dependency, Python 3.8+)
```bash
python evid-four-check.py --demo                          # 3 built-in smoke cases (rc=0 / rc=1 / rc=1)
python evid-four-check.py --type 电子合同 --has_signature yes \
  --source_verifiable yes --integrity_check yes --relevance yes   # complete args, all PASS → rc=0
python evid-four-check.py --type 聊天记录 --has_signature no \
  --integrity_check no --relevance yes                    # source_verifiable missing → strict presumption, rc=1
python evid-four-check.py --relevance maybe                # invalid value → rc=2
```

| Argument | Meaning | Values | `required` in META |
|---|---|---|---|
| `--type` | evidence type (drives the 「合法性」 formal check) | 合同 / 聊天记录 / 邮件 / 日志 / 音视频 … | `False` |
| `--has_signature` | digital signature / trusted timestamp / blockchain notarisation | `yes` / `no` | `False` |
| `--source_verifiable` | source verifiable (traceable to original carrier/system) | `yes` / `no` | `False` |
| `--integrity_check` | integrity hash / original-carrier comparison done | `yes` / `no` | `False` |
| `--relevance` | relevant to the fact to be proved | `yes` / `no` | `False` |

All five arguments are optional — **at least one** is required; argparse reads each `required` field from META (metadata and behaviour agree). Any other value than `yes`/`no` (also accepted: `y/n`, `true/false`, `1/0`, `是/否`, `有/无`) → `rc=2`. Output is always JSON IR (indented); there is **no output-format switch** — the legacy ghost flag `--json` was removed.

## Output
Deterministic JSON IR with `rc` (**0** = completed, no warnings / **1** = completed with warnings, incl. strict presumption / **2** = insufficient or invalid input), `four_properties`, `dimension_basis`, `possible_conclusions`, `conclusion`, `remediation`, `missing_inputs`, `warnings`, `clause_review_checklist`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

Real excerpt (`python evid-four-check.py --type 聊天记录 --has_signature no --integrity_check no --relevance yes`, arrays trimmed to one element and marked `…`; values verbatim):

```json
{
  "tool": "evid-four-check",
  "input": {"type": "聊天记录", "has_signature": "no", "source_verifiable": null,
            "integrity_check": "no", "relevance": "yes"},
  "result": {
    "four_properties": {"真实性": "FAIL", "合法性": "PASS", "关联性": "PASS", "完整性": "FAIL"},
    "dimension_basis": {"真实性": "从严推定（输入不完整）", "合法性": "明确输入",
                        "关联性": "明确输入", "完整性": "明确输入"},
    "conclusion": "四性形式审查存在未通过项，证据能力待补强（不构成证据能力或采信结论；最终采信由司法机关认定）",
    "missing_inputs": ["source_verifiable"],
    "warnings": ["… 共 5 条（输入不完整从严推定 / 可能区间 / 补参建议 / 明确判定未通过项 / 形式审查免责）"],
    …
  },
  "rc": 1,
  "clause_review_checklist": ["… 共 7 条（条款号 + 用途 + 待人工核对）"],
  "aigc_mark": {"standard": "GB 45438-2025", "is_generated": true, "generator": "evid-four-check@SynomosAI",
                "content_type": "decision_support_output", "label_note": "标识口径待核"}
}
```
（上例数组已裁剪并标注 `…`；SKILL.md 内贴 `--demo` 逐字节选、完整原文见做齐报告。）

## Theory hook (证据语义澄清)
证据须可被问责——四性审查即把「可信」写进每一次举证。依 LGD 证据语义界定：**Evidence（证据）＝治理状态转换的可验证依据，非行为日志**；输出中的 `evidence` 是**规则出处（条款依据）**，不是本案证据台账。域站位件：TH-LAW-001。

## 条款号待人工核对清单 / Clause review checklist
| 条款 / 口径 | 用途 | 状态 |
|---|---|---|
| 证据规定 第14条 | 电子数据范围的界定 | 待人工核对 |
| 证据规定 第93条 | 电子数据真实性审查的考虑因素 | 待人工核对 |
| 证据规定 第94条 | 真实性推定情形（第三方平台存证、中立系统、公证等） | 待人工核对 |
| 证据规定 第95条 | 一方控制证据而拒不提交的法律后果（举证妨碍） | 待人工核对 |
| 在线诉讼规则 第12条～第18条 | 在线诉讼中电子化材料的提交、原件认定、区块链存证与上链真实性审查（区间范围待核） | 待人工核对 |
| GB 45438-2025 | AIGC 标识字段 `aigc_mark` | 待人工核对 |
| 「四性」维度划分（真实/合法/关联/完整） | 本工具输出结构；属审查清单口径，**非任何条文原文表述** | 待人工核对 |

## Pointers (unverified — links pending)
- LGD theory page: https://medxpert.cn/lgd.html
- Skill library on medxpert.cn: https://medxpert.cn/skills/
- Machine-readable index: https://medxpert.cn/llms.txt
- Theory ledger repo: https://github.com/zhaoxinghua09-cell/lgd-theory
- Reference implementation: https://github.com/zhaoxinghua09-cell/uibc-core
- Skill library index: https://github.com/zhaoxinghua09-cell/agent-skills
- LGD 理论总账 REGISTRY 在线页：(地址待补) · LAW 域速查页：(地址待补)

## License & attribution
**Layered licence — the code licence does NOT cover the docs or the theory text.**

| Layer | Carrier | Licence |
|---|---|---|
| Code | `evid-four-check.py` | **MIT** |
| Docs & theory text | this `README.md`, `SKILL.md`, the 「理论依据」 section and all theory wording | **Not covered by MIT**: all rights reserved |

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
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**。）
**本包补充**：`evid-four-check.py` = MIT；本 `README.md` / `SKILL.md` 及其中理论文本不在任何代码许可覆盖范围内。

## 家族合集
| 域 | 工具 | 大使 | 目录 |
|---|---|---|---|
| UAS 低空 | uas-ops-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/uas-ops-checker |
| AUT 驾驶 | aut-grade-checker | 诺卫 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/aut-grade-checker |
| DAT 数据 | data-grade-checker | 诺源 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/data-grade-checker |
| BIO 生物 | hgrac-route-checker | 诺康 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/hgrac-route-checker |
| FIN 金融 | fin-ai-classifier | 诺丰 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/fin-ai-classifier |
| LAW 法律 | evid-four-check | 诺律 | https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/evid-four-check |

---
诺律@LAW 域首席发声人 · TH-LAW-001 · SynomosAI（AI 辅助生成，非自然人）
