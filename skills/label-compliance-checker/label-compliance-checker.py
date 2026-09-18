# -*- coding: utf-8 -*-
"""医疗器械标签合规核对器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：《医疗器械说明书和标签管理规定》(总局令 第6号) 第10-11条
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "label-compliance-checker", "version": "1.0.0", "args": [{"name": "has_name", "help": "含产品名称: yes/no", "required": False}, {"name": "has_reg_no", "help": "含注册证号/备案号: yes/no", "required": False}, {"name": "has_manufacturer", "help": "含生产企业名称地址: yes/no", "required": False}, {"name": "has_indications", "help": "含适用范围/禁忌症: yes/no", "required": False}, {"name": "has_warnings", "help": "含警示/注意事项: yes/no", "required": False}, {"name": "has_lot", "help": "含批号/日期/有效期: yes/no", "required": False}, {"name": "has_udi", "help": "含UDI标识(若适用): yes/no", "required": False}]}

class GateError(Exception):
    pass

def classify_label(args):
    """标签/说明书要素完整性核对。规则源：《医疗器械说明书和标签管理规定》(原总局令 第6号) 第10-11条。"""
    fields = {
        "has_name": "产品名称",
        "has_reg_no": "注册证号/备案号",
        "has_manufacturer": "生产企业名称/地址/联系方式",
        "has_indications": "适用范围/禁忌症",
        "has_warnings": "警示/注意事项/使用说明",
        "has_lot": "生产批号/生产日期/有效期",
        "has_udi": "UDI 标识（若适用）",
    }
    missing = [cn for k, cn in fields.items() if (args.get(k) or '').lower() not in ('yes', 'true', '1')]
    compliant = len(missing) == 0
    oblig = ["标签须含产品名称、注册证号、生产企业、批号等法定要素", "说明书须含适用范围、禁忌、警示、使用方法", "植入类须注明注意事项与随访要求"]
    notes = ["要素以《规定》第10条(标签)/第11条(说明书)为准", "UDI 标识依产品风险类别适用", "本核对为清单化自查，非合规证明"]
    warns = []
    if not compliant:
        warns.append("存在缺失要素：" + "、".join(missing) + "——上市前须补齐")
    else:
        warns.append("要素齐全，但内容准确性仍须与注册证/技术要求一致核对")
    return {"compliant": compliant, "missing_fields": missing, "obligations": oblig,
            "notes": notes, "evidence": ["说明书和标签管理规定 第6号 第10-11条"], "warnings": warns}


def _run(args):
    res = classify_label(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="label-compliance-checker", description="医疗器械标签合规核对器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    if ns.demo:
        demos = [{"has_name": "yes", "has_reg_no": "yes", "has_manufacturer": "yes", "has_indications": "yes", "has_warnings": "yes", "has_lot": "yes", "has_udi": "yes"}, {"has_name": "yes", "has_reg_no": "no", "has_manufacturer": "yes", "has_indications": "no", "has_warnings": "no", "has_lot": "yes", "has_udi": "no"}]
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
