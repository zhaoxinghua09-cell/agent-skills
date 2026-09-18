# -*- coding: utf-8 -*-
"""PMCF 评价报告完整性检查器 — 零依赖单文件 CLI · JSON IR 输出。规则源：MDR (EU) 2017/745 Annex XIV Part B + Art 86 / MDCG 2020-7、2020-8"""
import argparse
import json
import sys

META = {"slug": "pmcf-evaluation-report-check", "version": "1.0.0", "args": [{"name": "device_class", "help": "风险等级: IIa/IIb/III（必填）"}, {"name": "implant", "help": "是否植入类: yes/no"}, {"name": "has_scope", "help": "含范围与器械标识: yes/no"}, {"name": "has_method", "help": "含数据来源与采集方法: yes/no"}, {"name": "has_data", "help": "含数据汇总与分析: yes/no"}, {"name": "has_conclusions", "help": "含结论与受益-风险影响: yes/no"}, {"name": "has_actions", "help": "含所采取措施/CAPA: yes/no"}, {"name": "has_signoff", "help": "含评价人资质/日期/签署: yes/no"}]}


class GateError(Exception):
    code = "E_RUNTIME"
    def __init__(self, msg, code=None):
        super().__init__(msg)
        if code:
            self.code = code


def check_pmcf_report(args):
    """PMCF 评价报告完整性检查。规则源：MDR (EU) 2017/745 Annex XIV Part B + Art 86 / MDCG 2020-7、2020-8。"""
    cls = (args.get("device_class") or "").upper()
    if cls not in ("IIA", "IIB", "III"):
        raise GateError("--device_class 必填，且必须为 IIa / IIb / III 之一", "E_ENUM_INVALID")
    implant = (args.get("implant") or "").lower()
    sections = {
        "has_scope": "评价范围与适用器械标识",
        "has_method": "数据来源与采集方法（含 PMCF 计划引用）",
        "has_data": "数据汇总与分析",
        "has_conclusions": "结论与对受益-风险比的影响",
        "has_actions": "所采取措施 / CAPA / 更新触发",
        "has_signoff": "评价人资质、日期与签署",
    }
    missing = [cn for k, cn in sections.items() if (args.get(k) or "").lower() not in ("yes", "true", "1")]
    if cls == "III" or (cls == "IIB" and implant in ("yes", "true")):
        psur, basis = "至少每年一次（PSUR）", "MDR Art 86：III 类及植入类 IIb 器械"
    else:
        psur, basis = "至少每 2 年一次，必要时提高频次", "MDR Art 86：IIa 类及其他 IIb 类器械"
    warns = []
    if missing:
        warns.append("报告要素缺失：" + "、".join(missing) + "——提交前须补齐，否则易被公告机构发补")
    if (args.get("has_actions") or "").lower() not in ("yes", "true", "1"):
        warns.append("未填写「所采取措施」——PMCF 的价值在于闭环，缺此节等同于无输出")
    oblig = [
        "PMCF 评价报告须与 PMCF 计划对应，且纳入技术文件动态更新",
        "报告周期与 PSUR 联动，不得超期",
        "结论须明确是否维持受益-风险比为正，否则触发更新/风险控制",
    ]
    notes = [
        "本节清单以 MDR Annex XIV Part B 与 MDCG 2020-7/2020-8 为骨架，属结构完整性核查",
        "内容充分性（方法是否恰当、样本是否足够）超出本工具能力，须专业评价者判断",
        "周期以法规原文及公告机构要求为准",
    ]
    cls = {"IIA": "IIa", "IIB": "IIb"}.get(cls, cls)
    return {
        "device_class": cls, "report_period": psur, "period_basis": basis,
        "missing_sections": missing, "complete": len(missing) == 0,
        "obligations": oblig, "notes": notes,
        "evidence": ["MDR (EU) 2017/745 Annex XIV Part B", "MDR Art 86", "MDCG 2020-7", "MDCG 2020-8"],
        "warnings": warns,
    }


def _call(args):
    fn_name = "check_pmcf_report"
    res = globals()[fn_name](args)
    return res


def main():
    p = argparse.ArgumentParser(prog="pmcf-evaluation-report-check", description="PMCF 评价报告完整性检查器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, default=None, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR")
    ns = p.parse_args()
    names = [a["name"] for a in META["args"]]

    if ns.demo:
        ok = True
        for d in [{"device_class": "III", "implant": "yes", "has_scope": "yes", "has_method": "yes", "has_data": "yes", "has_conclusions": "yes", "has_actions": "yes", "has_signoff": "yes"}, {"device_class": "IIa", "has_scope": "yes", "has_method": "yes", "has_data": "yes", "has_conclusions": "no", "has_actions": "no", "has_signoff": "yes"}]:
            try:
                res = _call(dict(d))
                rc = 1 if (res.get("warnings") or []) else 0
                print(json.dumps({"tool": META["slug"], "input": d, "result": res,
                                  "rc": rc, "error_code": None}, ensure_ascii=False))
            except GateError as e:
                ok = False
                print(json.dumps({"tool": META["slug"], "input": d, "errors": [str(e)],
                                  "rc": 2, "error_code": e.code}, ensure_ascii=False))
        sys.exit(0 if ok else 2)

    args = {k: getattr(ns, k) for k in names}
    if not any(v not in (None, "") for v in args.values()):
        p.print_help()
        sys.exit(0)
    try:
        res = _call(args)
    except GateError as e:
        print(json.dumps({"tool": META["slug"], "version": META["version"], "input": args,
                          "errors": [str(e)], "rc": 2, "error_code": e.code},
                         ensure_ascii=False, indent=2))
        sys.exit(2)
    rc = 1 if (res.get("warnings") or []) else 0
    ir = {"tool": META["slug"], "version": META["version"], "input": args,
          "result": res, "rc": rc, "error_code": None,
          "aigc_mark": {"standard": "GB 45438-2025", "is_generated": True,
                        "generator": META["slug"] + "@MedXpert",
                        "content_type": "decision_support_output",
                        "disclaimer": "决策支持非权威结论，须人工复核；以官方最新文件为准"}}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)


if __name__ == "__main__":
    main()
