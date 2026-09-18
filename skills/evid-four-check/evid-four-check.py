# -*- coding: utf-8 -*-
"""电子证据四性审查判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：最高法《关于民事诉讼证据的若干规定》第14/93-95条 + 《人民法院在线诉讼规则》第12-18条
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "evid-four-check", "version": "1.0.0", "args": [{"name": "type", "help": "证据类型(如 合同/聊天记录/邮件/日志/音视频)", "required": False}, {"name": "has_signature", "help": "有电子签名/区块链存证: yes/no", "required": False}, {"name": "source_verifiable", "help": "来源可验证: yes/no", "required": False}, {"name": "integrity_check", "help": "完整性哈希校验: yes/no", "required": False}, {"name": "relevance", "help": "与案件关联: yes/no", "required": False}]}

class GateError(Exception):
    pass

def classify_evid(args):
    """电子证据"四性"审查。规则源：最高法《关于民事诉讼证据的若干规定》第14/93-95条 + 《人民法院在线诉讼规则》第12-18条。"""
    typ = args.get('type') or ''
    sig = args.get('has_signature')      # 电子签名/区块链存证: yes/no
    src = args.get('source_verifiable')  # 来源可验证: yes/no
    integ = args.get('integrity_check')  # 完整性哈希校验: yes/no
    rel = args.get('relevance')          # 与案件关联: yes/no
    four = {
        "真实性": "PASS" if (sig in ('yes',) or src in ('yes',)) else "FAIL",
        "合法性": "PASS" if typ else "FAIL",
        "关联性": "PASS" if rel in ('yes',) else "FAIL",
        "完整性": "PASS" if integ in ('yes',) else "FAIL",
    }
    guide = []
    if four["真实性"] == "FAIL": guide.append("补强：电子签名/可信时间戳/区块链存证以证真实性")
    if four["完整性"] == "FAIL": guide.append("补强：提供哈希值/原始载体比对以证完整性")
    if four["关联性"] == "FAIL": guide.append("补强：说明证据与待证事实的逻辑关联")
    if four["合法性"] == "FAIL": guide.append("补强：说明取证手段合法（非窃录/侵入）")
    cap = "具备证据能力" if all(v == "PASS" for v in four.values()) else "证据能力待补强"
    return {"four_properties": four, "conclusion": cap, "remediation": guide,
            "notes": ["四性审查为清单化决策支持", "最终采信由司法机关认定"],
            "evidence": ["证据规定 第14/93-95条", "在线诉讼规则 第12-18条"]}


def _run(args):
    res = classify_evid(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="evid-four-check", description="电子证据四性审查判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"type": "合同", "has_signature": "yes", "source_verifiable": "yes", "integrity_check": "yes", "relevance": "yes"}, {"type": "聊天记录", "has_signature": "no", "integrity_check": "no", "relevance": "yes"}]
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
