#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lgd_gate.py — LGD 门禁中枢（meta 薄分发器 · GATE 阶段）

薄分发器：只按 slug 路由到 GATE 阶段的具体子技能，不搬运、不重实现任何子技能代码。
所有真实门禁由被引用的子技能完成。

诚实纪律：
  --verify 以"活动工作集实探"为准，把每个节点分级为 LIVE / ECOSYSTEM / ERROR，
  绝不伪称"全绿"或"已实跑"。--verify 仅以 --help 只读探针方式读取子技能元信息，
  不做任何拦截、不对外写。

用法：
  python lgd_gate.py --list
  python lgd_gate.py --verify [--json-out PATH]
  python lgd_gate.py --route <slug>
"""
import os
import sys
import json
import glob
import argparse
import subprocess
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SKILLS_ROOT = os.environ.get("LGD_SKILLS_ROOT") or os.path.dirname(SKILL_DIR)

# GATE 阶段节点（权威来源：governanceos/scripts/governance_flow.py PHASES["gate"]）
# (slug, when-to-use, expected-output)
NODES = [
    ("skill-quality-gate",
     "技能入库前质量门：结构/文档/安全/生态兼容五维评分，未过拦截",
     "质量门判定 + 阻断项"),
    ("publish-quality-gate",
     "对外发布前发布门：四层扫描（密钥/注入/合规/完整性），阻断放行",
     "发布门判定；任一阻断项则拦"),
    ("skill-admission-gate",
     "新技能申请入库的准入门：admit / conditional / reject",
     "准入判定 + 理由"),
    ("publish-review-gate",
     "发布前人工 + 自动评审门：checklist 覆盖",
     "评审判定 + checklist 覆盖"),
    ("release-gate-check",
     "发布时 release 前置校验：发布就绪清单 pass/fail",
     "就绪清单 pass/fail"),
    ("skill-release-gate",
     "技能包发布时的发布门：阻断放行",
     "发布门判定；阻断项则拦"),
    ("human-oversight-gate",
     "高风险动作人工监督门：approver 决策记录",
     "监督决策记录 + approver"),
    ("gate-policy-generator",
     "为新风险类生成门禁策略文档",
     "生成的门禁策略文档"),
]


def find_script(slug):
    d = os.path.join(SKILLS_ROOT, slug)
    if not os.path.isdir(d):
        return None
    # 优先 scripts/*.py，其次顶层 *.py
    cand = sorted(glob.glob(os.path.join(d, "scripts", "*.py")))
    if not cand:
        cand = sorted(glob.glob(os.path.join(d, "*.py")))
    return cand[0] if cand else None


def verify():
    rows = []
    for slug, when, out in NODES:
        d = os.path.join(SKILLS_ROOT, slug)
        if not os.path.isdir(d):
            status = "ECOSYSTEM"   # 声明在路由里，活动工作集无目录（生态/备份层）
            rc = None
            note = "活动工作集无目录 → openclaw plugins install clawhub:%s" % slug
        else:
            script = find_script(slug)
            if script is None:
                status = "PRESENT"
                rc = None
                note = "目录在但无可运行脚本（spec/doc-only，未实跑拦截）"
            else:
                try:
                    r = subprocess.run([sys.executable, script, "--help"],
                                       capture_output=True, text=True, timeout=25)
                    rc = r.returncode
                    status = "LIVE" if rc == 0 else "ERROR"
                    note = "rc=%d" % rc if rc == 0 else "rc=%d（脚本异常）" % rc
                except Exception as e:
                    rc = None
                    status = "ERROR"
                    note = "exec fail: %s" % e
        rows.append({"slug": slug, "status": status, "rc": rc,
                     "when": when, "out": out, "note": note})
    return rows


def main():
    ap = argparse.ArgumentParser(
        prog="lgd-gate",
        description="LGD 门禁中枢 meta 薄分发器（GATE 阶段 %d 节点）" % len(NODES))
    ap.add_argument("--list", action="store_true", help="列出 GATE 阶段全部门禁节点")
    ap.add_argument("--verify", action="store_true", help="实探各节点真实可用性（活动工作集）")
    ap.add_argument("--json-out", help="--verify 时输出 evidence.json 路径")
    ap.add_argument("--route", metavar="SLUG", help="显示某门禁节点的调用说明")
    ap.add_argument("--skills-root", help="覆盖子技能根目录（默认：本技能上级目录）")
    args = ap.parse_args()

    if args.skills_root:
        global SKILLS_ROOT
        SKILLS_ROOT = args.skills_root

    if args.list:
        print("LGD 门禁中枢 (lgd-gate) — GATE 阶段 %d 个门禁节点（薄分发器，按 slug 路由）："
              % len(NODES))
        print("=" * 78)
        for i, (slug, when, out) in enumerate(NODES, 1):
            print("  %d. %-24s | %s" % (i, slug, out))
        print("=" * 78)
        print("探测真实可用性：python lgd_gate.py --verify")
        return 0

    if args.verify:
        rows = verify()
        live = sum(1 for r in rows if r["status"] == "LIVE")
        present = sum(1 for r in rows if r["status"] == "PRESENT")
        eco = sum(1 for r in rows if r["status"] == "ECOSYSTEM")
        err = sum(1 for r in rows if r["status"] == "ERROR")
        print("LGD 门禁中枢 可用性探测（skills-root=%s）：" % SKILLS_ROOT)
        print("=" * 78)
        for r in rows:
            print("  [%-10s] %-24s %s" % (r["status"], r["slug"], r["note"]))
        print("=" * 78)
        print("LIVE=%d  PRESENT(目录在·无脚本)=%d  ECOSYSTEM(生态/备份层)=%d  ERROR=%d"
              % (live, present, eco, err))
        data = {
            "skill": "lgd-gate",
            "scanned_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "skills_root": SKILLS_ROOT,
            "total": len(rows), "live": live, "ecosystem": eco, "error": err,
            "nodes": rows,
        }
        if args.json_out:
            open(args.json_out, "w", encoding="utf-8").write(
                json.dumps(data, ensure_ascii=False, indent=2))
            print("evidence.json -> %s" % args.json_out)
        # 退出码：ERROR 才算失败；ECOSYSTEM 属预期（如实反映）
        return 1 if err else 0

    if args.route:
        for slug, when, out in NODES:
            if args.route == slug:
                print("门禁节点: %s" % slug)
                print("  when-to-use : %s" % when)
                print("  expected-out: %s" % out)
                print("  call        : openclaw plugins install clawhub:%s （其自带 CLI/--help）" % slug)
                return 0
        print("no such gate slug: %s" % args.route)
        return 2

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
