# -*- coding: utf-8 -*-
"""医疗器械召回级别判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：《医疗器械召回管理办法》(总局令 第29号)
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "recall-decision-checker", "version": "1.0.0", "args": [{"name": "harm_level", "help": "危害程度: severe/reversible/none", "required": True}, {"name": "use_phase", "help": "使用阶段: on_market/in_use/sold", "required": False}]}

class GateError(Exception):
    pass

def classify_recall(args):
    """召回级别判定。规则源：《医疗器械召回管理办法》(原国家食品药品监督管理总局令 第29号)。"""
    harm = (args.get('harm_level') or '').lower()          # severe/reversible/none
    phase = (args.get('use_phase') or '').lower()         # on_market/in_use/sold
    if not harm:
        raise GateError("缺少必要参数：harm_level(严重健康危害/可逆可控危害/一般不会危害) 必填")
    if harm == 'severe':
        level, days, oblig = "一级（使用该器械可能或已经引起严重健康危害）", 1, ["1 日内通知到有关单位", "启动一级召回", "向省局报告"]
    elif harm == 'reversible':
        level, days, oblig = "二级（可能引起危害但可逆/可控）", 3, ["3 日内通知", "启动二级召回", "向省局报告"]
    else:
        level, days, oblig = "三级（一般不会危害健康，但需召回）", 7, ["7 日内通知", "启动三级召回", "向省局报告"]
    warns = []
    if harm == 'severe':
        warns.append("一级召回为最高级——须立即控制流通与使用")
    notes = ["召回级别随危害严重程度与可逆性判定", "境外召回须同步上报", "时限以官方最新规定为准"]
    return {"recall_level": level, "notify_within_days": days, "obligations": oblig,
            "notes": notes, "evidence": ["医疗器械召回管理办法 第29号"], "warnings": warns}


def _run(args):
    res = classify_recall(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="recall-decision-checker", description="医疗器械召回级别判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    if ns.demo:
        demos = [{"harm_level": "severe"}, {"harm_level": "reversible"}, {"harm_level": "none"}]
        allok = True
        for d in demos:
            try:
                res, rc = _run(dict(d))
                print(json.dumps({"tool": META["slug"], "input": d, "result": res, "rc": rc}, ensure_ascii=False))
            except GateError as e:
                allok = False
                print(json.dumps({"tool": META["slug"], "input": d, "errors": [str(e)], "rc": 2}, ensure_ascii=False))
        sys.exit(0 if allok else 2)
    args = {k: getattr(ns, k) for k in argnames}
    if not any(v not in (None, "") for v in args.values()):
        # 无参数时打印帮助
        p.print_help()
        sys.exit(0)
    try:
        res, rc = _run(args)
    except GateError as e:
        ir = {"tool": META["slug"], "version": META["version"], "input": args, "errors": [str(e)], "rc": 2}
        print(json.dumps(ir, ensure_ascii=False, indent=2))
        sys.exit(2)
    ir = {"tool": META["slug"], "version": META["version"], "input": args, "result": res, "rc": rc,
           "aigc_mark": {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
                         "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)

if __name__ == "__main__":
    main()
