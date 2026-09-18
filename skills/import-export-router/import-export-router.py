# -*- coding: utf-8 -*-
"""医疗器械进出口路径判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：NMPA 进口医疗器械注册规定 + 出口销售证明办理 + FDA/EU MDR
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "import-export-router", "version": "1.0.0", "args": [{"name": "direction", "help": "方向: import/export", "required": True}, {"name": "is_registered", "help": "境内是否已注册/上市: yes/no", "required": False}, {"name": "dest_region", "help": "目的国/地区: cn/us/eu/other", "required": False}]}

class GateError(Exception):
    pass

def classify_importexport(args):
    """医疗器械进口/出口路径判定。规则源：NMPA 进口医疗器械注册规定 + 《医疗器械出口销售证明》办理 + 目的国法规(FDA/EU MDR)。"""
    direction = (args.get('direction') or '').lower()      # import/export
    registered = (args.get('is_registered') or '').lower() # yes/no
    dest = (args.get('dest_region') or '').lower()         # cn/us/eu/other
    if not direction:
        raise GateError("缺少必要参数：direction(import/export) 必填")
    if direction == 'import':
        if registered in ('yes', 'true'):
            route, docs, warns = "凭境内注册证进口", ["境内医疗器械注册证/备案凭证", "进口报关单", "中文标签/说明书"], []
        else:
            route, docs, warns = "须先申请进口医疗器械注册（NMPA）", ["进口注册检验", "境外生产企业质量体系核查", "技术审评"], ["未获注册证不得进口销售"]
    else:  # export
        if registered in ('yes', 'true'):
            base = "可办理《医疗器械出口销售证明》（省级药监局）"
            docs = ["境内注册证/生产许可", "出口销售证明申请表", "质量承诺"]
        else:
            base, docs = "须先取得境内注册/生产资质方可办理出口证明", ["境内注册证/生产许可"]
        if dest == 'us':
            route = base + "；境外上市须走 FDA 510(k)/PMA 等路径"
        elif dest == 'eu':
            route = base + "；境外上市须 CE 认证（EU MDR 技术文件+公告机构）"
        elif dest == 'cn':
            route = base
        else:
            route = base + "；境外上市依目的国法规办理"
        warns = []
    oblig = ["进口：境内未注册不得销售", "出口：凭出口销售证明+目的国准入", "跨境须符合双边/多边监管要求"]
    notes = ["FDA/EU MDR 为境外准入，独立于境内注册", "时限与材料以官方最新规定为准", "本判定为路径建议，非监管结论"]
    return {"route": route, "required_docs": docs, "obligations": oblig,
            "notes": notes, "evidence": ["NMPA 进口规定", "出口销售证明办理", "FDA/EU MDR"], "warnings": warns}


def _run(args):
    res = classify_importexport(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="import-export-router", description="医疗器械进出口路径判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    if ns.demo:
        demos = [{"direction": "import", "is_registered": "no"}, {"direction": "export", "is_registered": "yes", "dest_region": "us"}, {"direction": "export", "is_registered": "yes", "dest_region": "eu"}]
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
