# -*- coding: utf-8 -*-
"""车辆驾驶自动化等级判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：GB/T 40429-2021《汽车驾驶自动化分级》表1
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "aut-grade-checker", "version": "1.0.0", "args": [{"name": "dd", "help": "动态驾驶任务执行方: vehicle/driver/system", "required": True}, {"name": "oedr", "help": "目标事件探测响应方: vehicle/driver/system", "required": True}, {"name": "odd_limited", "help": "是否限定ODD: yes/no", "required": False}, {"name": "takeover_needed", "help": "是否需人工接管: yes/no", "required": False}, {"name": "both_axes", "help": "是否同时执行转向+加减速: yes/no", "required": False}]}

class GateError(Exception):
    pass

def classify_aut(args):
    """车辆驾驶自动化等级 0-5 判定。规则源：GB/T 40429-2021《汽车驾驶自动化分级》表1。"""
    dd = (args.get('dd') or '').lower()
    oedr = (args.get('oedr') or '').lower()
    odd = (args.get('odd_limited') or '').lower()
    takeover = (args.get('takeover_needed') or '').lower()
    both = args.get('both_axes')
    if not dd or not oedr:
        raise GateError("缺少必要参数：dd(动态驾驶任务执行方) 与 oedr(目标事件探测响应方) 必填，取值 system/driver（vehicle 视作 system）")
    sys_dd = dd in ('system', 'vehicle')   # 系统执行横向+纵向控制
    if sys_dd and oedr == 'system':
        # 系统完成全部 DD + OEDR
        if odd == 'no':
            grade = 5          # 无限 ODD → 完全自动驾驶
        elif takeover == 'no':
            grade = 4          # 限定 ODD，系统自主最小风险、无需接管 → 高度自动驾驶
        else:
            grade = 3          # 限定 ODD，需驾驶员接管 → 有条件自动驾驶
    elif sys_dd and oedr == 'driver':
        # 系统执行 DD，驾驶员负责 OEDR
        grade = 2 if both in ('yes', True, 'true') else 1   # 转向+加减速皆控→L2，否则→L1
    else:
        grade = 0              # 驾驶员负责全部，系统仅应急辅助
    resp = {
        0: "驾驶员全程负责（应急辅助）",
        1: "驾驶员负责OEDR与目标事件，系统提供部分辅助",
        2: "系统持续执行转向+加减速，驾驶员负责OEDR",
        3: "系统执行全部DD，有限ODD内运行，需后备用户接管",
        4: "系统执行全部DD+OEDR，有限ODD，系统自主应对",
        5: "系统在所有ODD执行全部DD+OEDR，无限制",
    }[grade]
    warns = []
    if grade in (3,4,5):
        warns.append("L3+ 不得宣称'自动驾驶/L2.9'等误导级别（'L2.9级'乱象可直接据此判定）")
    return {"grade": f"L{grade}", "responsibility": resp,
            "obligations": ["L3+ 须明示分级与责任边界", "宣传不得超实际等级标注"],
            "notes": ["以官方 GB/T 40429-2021 表1 为准", "企业/用户责任边界随等级变化"],
            "evidence": ["GB/T 40429-2021 表1"], "warnings": warns}


def _run(args):
    res = classify_aut(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="aut-grade-checker", description="车辆驾驶自动化等级判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"dd": "system", "oedr": "system", "odd_limited": "yes", "takeover_needed": "yes"}, {"dd": "vehicle", "oedr": "driver", "both_axes": "yes"}]
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
