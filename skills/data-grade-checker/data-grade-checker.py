# -*- coding: utf-8 -*-
"""数据分类分级判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：GB/T 43697-2024《数据安全技术 数据分类分级规则》(2024-10-01实施)
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "data-grade-checker", "version": "1.0.0", "args": [{"name": "industry", "help": "行业: finance/energy/transport/bio/health/geo/population/gov/key_infra 等", "required": False}, {"name": "core_interest", "help": "是否涉及国家核心利益: yes/no", "required": False}, {"name": "scale", "help": "规模/敏感度: high/mid/low", "required": False}, {"name": "cross_border", "help": "是否出境: yes/no", "required": False}]}

class GateError(Exception):
    pass

def classify_data(args):
    """数据分类分级判定。规则源：GB/T 43697-2024《数据安全技术 数据分类分级规则》(2024-10-01实施)。"""
    industry = (args.get('industry') or '').lower()
    core = args.get('core_interest')  # 是否涉及国家核心利益: yes/no
    scale = args.get('scale')         # 规模/敏感度: high/mid/low
    cross = args.get('cross_border')  # 是否出境: yes/no
    if core in ('yes', True):
        grade = "核心数据"
        oblig = ["出境安全评估 + 审批", "最高级保护义务", "原则上不得出境"]
    elif industry in ('finance','energy','transport','bio','health','geo','population','gov','key_infra') or scale in ('high',):
        grade = "重要数据"
        oblig = ["分类分级管理 + 加密", "出境安全评估/备案", "重要数据目录报送", "定期风险评估"]
    else:
        grade = "一般数据"
        oblig = ["基础保护义务（保密/完整/可用）", "出境按个保法/标准合同办理"]
    warns = []
    if cross in ('yes', True) and grade != "一般数据":
        warns.append("出境须走数据出境安全评估/标准合同/认证路径")
    return {"grade": grade, "obligations": oblig,
            "notes": ["行业敏感清单以官方附录为准", "跨部门数据按'就高'原则定级"],
            "evidence": ["GB/T 43697-2024"], "warnings": warns}


def _run(args):
    res = classify_data(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="data-grade-checker", description="数据分类分级判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"core_interest": "yes"}, {"industry": "finance", "scale": "high"}, {"industry": "retail"}]
        allok = True
        out_list = []
        for d in demos:
            try:
                res, rc = _run(dict(d))
                out_list.append({"tool": META["slug"], "input": d, "result": res, "rc": rc, "aigc_mark": AIGC})
            except GateError as e:
                allok = False
                out_list.append({"tool": META["slug"], "input": d, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC})
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
        sys.exit(0 if allok else 2)
    args = {k: getattr(ns, k) for k in argnames}
    try:
        res, rc = _run(args)
    except GateError as e:
        ir = {"tool": META["slug"], "version": META["version"], "input": args, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC}
        print(json.dumps(ir, ensure_ascii=False, indent=2))
        sys.exit(2)
    ir = {"tool": META["slug"], "version": META["version"], "input": args, "result": res, "rc": rc, "aigc_mark": AIGC}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)

if __name__ == "__main__":
    main()
