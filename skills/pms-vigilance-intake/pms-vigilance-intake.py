# -*- coding: utf-8 -*-
"""医疗器械不良事件报告路径判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：《医疗器械不良事件监测和再评价管理办法》(总局令 第1号)
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "pms-vigilance-intake", "version": "1.0.0", "args": [{"name": "severity", "help": "严重度: death/serious/possible_serious/other", "required": True}, {"name": "event_type", "help": "事件类型: fault/use_error/design_defect", "required": False}]}

class GateError(Exception):
    pass

def classify_pms(args):
    """个例不良事件报告路径判定。规则源：《医疗器械不良事件监测和再评价管理办法》(国家市场监督管理总局令 第1号)。"""
    sev = (args.get('severity') or '').lower()             # death/serious/possible_serious/other
    etype = (args.get('event_type') or '').lower()         # fault/use_error/design_defect
    if not sev:
        raise GateError("缺少必要参数：severity(死亡/严重伤害/可能严重伤害/其他) 必填")
    if sev == 'death':
        path, deadline, trigger = "持有人立即报告（导致死亡→即时，经营企业/使用单位 20 日内）", "即时", True
    elif sev == 'serious':
        path, deadline, trigger = "个例不良事件报告（严重伤害）", "20 日内（经营企业/使用单位→持有人）", False
    elif sev == 'possible_serious':
        path, deadline, trigger = "重点关注/定期汇总分析", "按定期监测上报", etype in ('design_defect',)
    else:
        path, deadline, trigger = "一般记录/纳入定期分析", "定期", False
    warns = []
    if trigger:
        warns.append("可能触发召回或再评价——须同步启动召回决策评估（recall-decision-checker）")
    oblig = ["持有人为监测责任主体", "死亡/严重伤害事件须时限内上报", "开展风险评价与再评价"]
    notes = ["群体不良事件→立即报告并采取紧急控制措施", "时限以官方最新规定为准", "本判定为报告路径建议，非监管结论"]
    return {"report_path": path, "deadline": deadline, "trigger_recall": trigger,
            "obligations": oblig, "notes": notes,
            "evidence": ["不良事件监测和再评价管理办法"], "warnings": warns}


def _run(args):
    res = classify_pms(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="pms-vigilance-intake", description="医疗器械不良事件报告路径判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    if ns.demo:
        demos = [{"severity": "death"}, {"severity": "serious"}, {"severity": "possible_serious", "event_type": "fault"}]
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
