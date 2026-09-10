#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_policy.py — LGD-III 有门禁（GATED）权限策略生成器
=====================================================
把"凡自治之物：有籍·有证·有门禁"的第三律，落成一份可挂载到
agent 的权限门禁策略（policy-as-code）。

痛点映射：agent 越权 / 误删误发 / 失控循环 / 无权限边界
三律映射：LGD-III 有门禁 —— 触发门禁 · 评审门禁 · 放行门禁 · 复盘门禁

与 tool-call-guard 的区别：
  - tool-call-guard = 运行时「单次调用」闸门（执行器）
  - 本工具          = 「策略生成」层（治理配置），产出整套路权限边界

零依赖：仅标准库。

用法：
  # 用内置 preset 直接看示例策略
  python gate_policy.py --preset default --json

  # 从能力清单生成（manifest 是 agent 可用工具 + 风险标注）
  python gate_policy.py --manifest agent_manifest.json --out policy.json

  # 反向校验一份已生成的 policy 是否含 LGD-III 四道门禁
  python gate_policy.py --check policy.json
"""
import argparse
import json
import sys
from datetime import datetime, timezone

LGD_VERSION = "LGD-v1.0"

# 内置 preset：决定 risk 如何映射到 allow/review/deny
PRESETS = {
    "default":  {"mid": "review", "high": "deny",  "sensitive": "deny",  "max_loop": 20, "max_tokens": 200000},
    "paranoid": {"mid": "deny",   "high": "deny",  "sensitive": "deny",  "max_loop": 5,  "max_tokens": 50000},
    "open":     {"mid": "allow",  "high": "review", "sensitive": "deny",  "max_loop": 50, "max_tokens": 500000},
}


def _norm_risk(r):
    r = (r or "").lower()
    return r if r in ("low", "mid", "high") else "low"


def build_policy(manifest, preset_name):
    preset = PRESETS[preset_name]
    tools = manifest.get("tools", []) if isinstance(manifest, dict) else []
    scenario = manifest.get("scenario", "未声明场景") if isinstance(manifest, dict) else "未声明场景"

    allow, review, deny = [], [], []
    for t in tools:
        if not isinstance(t, dict):
            continue
        name = t.get("name")
        if not name:
            continue
        risk = _norm_risk(t.get("risk"))
        sensitive = bool(t.get("sensitive"))
        if sensitive:
            bucket = preset["sensitive"]
        elif risk == "high":
            bucket = preset["high"]
        elif risk == "mid":
            bucket = preset["mid"]
        else:
            bucket = "allow"
        if bucket == "deny":
            deny.append(name)
        elif bucket == "review":
            review.append(name)
        else:
            allow.append(name)

    policy = {
        "lgd_version": LGD_VERSION,
        "law": "LGD-III 有门禁 (GATED)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "preset": preset_name,
        "scenario": scenario,
        "tool_allow": sorted(set(allow)),
        "tool_review": sorted(set(review)),
        "tool_deny": sorted(set(deny)),
        "gates": {
            # 四道门禁：触发 / 评审 / 放行 / 复盘
            "trigger":  {"enabled": True, "desc": "调用敏感/高危工具前必须先过闸"},
            "review":   {"enabled": True, "desc": "tool_review 清单内的工具需人工评审放行"},
            "release":  {"enabled": True, "desc": "外部发送/写库/删除类动作需二次确认"},
            "retro":    {"enabled": True, "desc": "每次越权尝试留痕，定期复盘"},
        },
        "budget": {
            "max_loop_iterations": preset["max_loop"],
            "max_tokens": preset["max_tokens"],
            "note": "超过上限即中止，防止失控循环烧 token",
        },
        "note": "本策略由 gate-policy-generator 生成，非法律建议；实际边界以你的 SOW/合同为准。",
    }
    return policy


def check_policy(policy):
    """反向校验：是否含 LGD-III 四道门禁 + 预算闸。"""
    issues = []
    if not isinstance(policy, dict):
        return False, ["策略不是合法 JSON 对象"]
    gates = policy.get("gates", {})
    for g in ("trigger", "review", "release", "retro"):
        if not isinstance(gates.get(g), dict) or not gates[g].get("enabled"):
            issues.append(f"缺少门禁: {g}")
    budget = policy.get("budget", {})
    if not budget.get("max_loop_iterations") or not budget.get("max_tokens"):
        issues.append("缺少预算闸(max_loop_iterations / max_tokens)")
    ok = len(issues) == 0
    return ok, issues


def main():
    ap = argparse.ArgumentParser(description="LGD-III 有门禁 权限策略生成器")
    ap.add_argument("--manifest", help="agent 能力清单 JSON 路径（含 tools:[{name,risk,sensitive}] + scenario）")
    ap.add_argument("--preset", default="default", choices=list(PRESETS.keys()),
                    help="内置策略档：default(平衡)/paranoid(严苛)/open(宽松)")
    ap.add_argument("--out", help="输出 policy JSON 路径（不指定则打印到 stdout）")
    ap.add_argument("--check", help="反向校验某 policy JSON 是否满足 LGD-III 四道门禁")
    ap.add_argument("--json", action="store_true", help="强制以 JSON 输出（check 模式默认 JSON）")
    a = ap.parse_args()

    # ---- check 模式 ----
    if a.check:
        try:
            with open(a.check, "r", encoding="utf-8") as f:
                policy = json.load(f)
        except FileNotFoundError:
            print(f"[错误] 找不到文件: {a.check}", file=sys.stderr)
            return 2
        except json.JSONDecodeError as e:
            print(f"[错误] JSON 解析失败: {e}", file=sys.stderr)
            return 2
        ok, issues = check_policy(policy)
        if a.json:
            print(json.dumps({"compliant": ok, "issues": issues}, ensure_ascii=False, indent=2))
        else:
            print("LGD-III 合规校验:", "通过 ✅" if ok else "不通过 ❌")
            for i in issues:
                print("  -", i)
        return 0 if ok else 1

    # ---- 生成模式 ----
    manifest = None
    if a.manifest:
        try:
            with open(a.manifest, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except FileNotFoundError:
            print(f"[错误] 找不到 manifest 文件: {a.manifest}", file=sys.stderr)
            print("       提示：用 --preset default 可不带 manifest 直接生成示例策略。", file=sys.stderr)
            return 2
        except json.JSONDecodeError as e:
            print(f"[错误] manifest JSON 解析失败: {e}", file=sys.stderr)
            return 2
    else:
        # 无 manifest：给一份演示用 manifest，避免"无输入即崩"
        manifest = {
            "scenario": "通用客服 agent（演示）",
            "tools": [
                {"name": "read_file", "risk": "low"},
                {"name": "send_email", "risk": "mid"},
                {"name": "delete_file", "risk": "high", "sensitive": True},
                {"name": "sql_write", "risk": "high"},
                {"name": "web_search", "risk": "low"},
            ],
        }

    policy = build_policy(manifest, a.preset)
    out = json.dumps(policy, ensure_ascii=False, indent=2)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
        print(f"[ok] 策略已写入: {a.out}（{len(policy['tool_allow'])} allow / "
              f"{len(policy['tool_review'])} review / {len(policy['tool_deny'])} deny）")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
