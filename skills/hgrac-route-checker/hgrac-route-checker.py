# -*- coding: utf-8 -*-
"""人类遗传资源事项路径判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：《人类遗传资源管理条例》(国务院令717号)+实施细则(2023-07-01施行) 第8-22条
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "hgrac-route-checker", "version": "1.0.0", "args": [{"name": "action", "help": "事项: collect/store/use/transfer/coop", "required": True}, {"name": "foreign_involved", "help": "是否涉外: yes/no", "required": False}, {"name": "scale", "help": "重要种类/累计人份: big/normal", "required": False}]}

class GateError(Exception):
    pass

def classify_hgrac(args):
    """人类遗传资源事项路径判定。规则源：人类遗传资源管理条例(国务院令717号)+实施细则(2023-07-01施行) 第8-22条。"""
    action = (args.get('action') or '').lower()      # collect/store/use/transfer/coop
    foreign = args.get('foreign_involved')           # 是否涉外: yes/no
    scale = args.get('scale')                        # 重要种类/累计人份: big/normal
    if action in ('collect', '采集'):
        if scale in ('big',) or foreign in ('yes',):
            route, ev = "审批（科技部）", ["条例 第8-11条"]
        else:
            route, ev = "备案", ["条例 第8-11条"]
    elif action in ('store', '保藏'):
        route, ev = "审批（保藏审批）", ["条例 第12-13条"]
    elif action in ('use', '利用'):
        route, ev = "备案 / 审批（依规模涉外）", ["条例 第14-16条"]
    elif action in ('transfer', '对外提供', 'coop', '国际合作'):
        route, ev = "审批（对外提供/国际合作科学研究）", ["条例 第17-22条"]
    else:
        raise GateError("action 必填：collect/store/use/transfer/coop")
    warns = []
    if foreign in ('yes',):
        warns.append("涉外环节须通过国际合作行政审批，不得私下对外提供")
    oblig = [f"路径：{route}", "提交材料清单（依托单位+伦理+合同）", "取得批件/备案号后方可实施"]
    return {"route": route, "obligations": oblig,
            "notes": ["生命科学企业涉外必踩", "错一步涉行政处罚"],
            "evidence": ev, "warnings": warns}


def _run(args):
    res = classify_hgrac(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="hgrac-route-checker", description="人类遗传资源事项路径判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"action": "collect", "scale": "big"}, {"action": "store"}, {"action": "transfer", "foreign_involved": "yes"}]
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
