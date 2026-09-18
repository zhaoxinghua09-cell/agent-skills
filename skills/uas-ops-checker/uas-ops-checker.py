# -*- coding: utf-8 -*-
"""无人机运营合规分类判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：《无人驾驶航空器飞行管理暂行条例》(国务院令761号,2024-01-01施行) 第6/12/31/32条 + CCAR-92
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "uas-ops-checker", "version": "1.0.0", "args": [{"name": "mtow", "help": "最大起飞重量(kg)", "required": False}, {"name": "empty_weight", "help": "空机重量(kg)", "required": False}]}

class GateError(Exception):
    pass

def classify_uas(args):
    """无人机机型分类 + 运营合规路径判定。规则源：无人驾驶航空器飞行管理暂行条例(国务院令761号,2024-01-01施行) 第6/12/31/32条 + CCAR-92 分类参数。"""
    mtow = args.get('mtow')          # 最大起飞重量 kg
    empty = args.get('empty_weight') # 空机重量 kg
    if mtow is None and empty is None:
        raise GateError("缺少必要参数：请提供 mtow(最大起飞重量) 或 empty_weight(空机重量)（kg）")
    try:
        m = float(mtow) if mtow is not None else None
        e = float(empty) if empty is not None else None
    except Exception:
        raise GateError("mtow / empty_weight 必须为数字（kg）")
    if (m is not None and m <= 0.25) or (e is not None and e < 0.25):
        grade, oblig, ev = "微型", ["微型无人机在适飞空域（真高≤120m）飞行无需操控员执照", "建议实名登记"], ["暂行条例 第12条"]
    elif (m is not None and m <= 7) and (e is not None and e <= 4):
        grade, oblig, ev = "轻型", ["实名登记", "在适飞空域（真高≤120m）飞行无需执照", "不得突破性能限制（高度/速度/空域）"], ["暂行条例 第12条", "CCAR-92"]
    elif (m is not None and m <= 25) and (e is not None and e <= 15):
        grade, oblig, ev = "小型", ["操控员执照（视具体机型）", "实名登记", "强制责任保险", "在适飞空域外飞行需申请"], ["暂行条例 第16条", "CCAR-92"]
    elif m is not None and m <= 150:
        grade, oblig, ev = "中型", ["运营合格证", "适航许可", "操控员执照", "飞行活动申请", "强制保险"], ["暂行条例 第31/32条"]
    else:
        grade, oblig, ev = "大型", ["运营合格证", "型号合格证/适航证", "操控员执照", "飞行活动申请", "强制保险"], ["暂行条例 第31/32条"]
    notes = ["分类以最大起飞重量与空机重量较低者从严判定（示意逻辑，以官方参数为准）",
             "涉及微型/轻型在管制空域或超限制飞行须申请", "涉外/商业运营需额外审查"]
    return {"grade": grade, "obligations": oblig, "notes": notes, "evidence": ev}


def _run(args):
    res = classify_uas(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="uas-ops-checker", description="无人机运营合规分类判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"mtow": "0.2"}, {"mtow": "5"}, {"mtow": "120"}]
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
