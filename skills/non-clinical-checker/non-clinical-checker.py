# -*- coding: utf-8 -*-
"""医疗器械非临床研究判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：GB/T 16886 系列 / YY 0505 / GB 9706.1
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "non-clinical-checker", "version": "1.0.0", "args": [{"name": "device_class", "help": "器械风险类别: I/II/III", "required": False}, {"name": "device_type", "help": "类型: active/passive/implant/ivd", "required": False}, {"name": "contact", "help": "接触性质: surface/insert/implant", "required": False}]}

class GateError(Exception):
    pass

def classify_nonclinical(args):
    """非临床研究项目判定。规则源：GB/T 16886 系列（生物学评价）/ YY 0505（医用电气 EMC）/ GB 9706.1（医用电气安全）。"""
    dclass = (args.get('device_class') or '').upper()       # I / II / III
    dtype = (args.get('device_type') or '').lower()         # active/passive/implant/ivd
    contact = (args.get('contact') or '').lower()           # surface/insert/implant
    if not dclass and not dtype:
        raise GateError("缺少必要参数：请提供 device_class(I/II/III) 或 device_type(active/passive/implant/ivd)")
    studies = []
    # 生物学评价（GB/T 16886）：接触性质+持续时间决定终点
    if contact in ('implant',) or dclass == 'III' or dtype in ('implant',):
        studies += ["生物学评价全套（细胞毒性/致敏/刺激/全身毒性/遗传毒性/血液相容性等，按 GB/T 16886.1 终点表）"]
    elif contact in ('insert',) or dclass == 'II':
        studies += ["生物学评价（细胞毒性/致敏/刺激等基础项，按接触性质+持续时间定终点）"]
    elif contact in ('surface',) or dclass == 'I':
        studies += ["生物学评价（表面接触低风险项，按 GB/T 16886.1 表 A.1 选做）"]
    # 有源设备：EMC + 安规
    if dtype in ('active',) or dclass in ('II', 'III'):
        studies += ["电磁兼容 EMC（YY 0505 / YY 9706.102）", "电气安全（GB 9706.1 通用+专用并列标准）"]
    # 植入 / III 类：追加
    if dtype == 'implant' or dclass == 'III':
        studies += ["植入物专项（疲劳/磨损/动物试验依产品设计）", "若含软件：软件验证与确认（GB/T 20438 / YY/T 0664）"]
    if dtype == 'ivd':
        studies += ["分析性能（准确度/精密度/检出限等）", "稳定性（实时+加速）", "参考区间/干扰研究"]
    oblig = ["委托具备 CMA/CNAS 资质的检测机构", "研究与风险管理输出同步", "结果纳入注册申报资料"]
    notes = ["生物学评价终点以 GB/T 16886.1 表 A.1 接触性质+持续时间为准", "有源器械 EMC/安规为强制", "本判定为项目清单建议，非检测结论"]
    return {"required_studies": studies, "obligations": oblig, "notes": notes,
            "evidence": ["GB/T 16886 系列", "YY 0505", "GB 9706.1"], "warnings": []}


def _run(args):
    res = classify_nonclinical(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="non-clinical-checker", description="医疗器械非临床研究判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    if ns.demo:
        demos = [{"device_class": "III", "device_type": "implant", "contact": "implant"}, {"device_class": "I", "device_type": "passive", "contact": "surface"}, {"device_class": "II", "device_type": "active"}]
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
