# -*- coding: utf-8 -*-
"""UDI 数据库提交合规判定器 — 零依赖单文件 CLI · JSON IR 输出。规则源：NMPA《医疗器械唯一标识系统规则》/ FDA 21 CFR 830 + GUDID / EU MDR Art 27-29 + EUDAMED"""
import argparse
import json
import sys

META = {"slug": "udi-db-submission-check", "version": "1.0.0", "args": [{"name": "market", "help": "目标市场: cn/us/eu（必填）"}, {"name": "is_registered", "help": "境内是否已取得注册证/备案: yes/no"}, {"name": "has_di", "help": "是否已分配 DI: yes/no"}, {"name": "has_pi", "help": "是否已分配 PI（生产标识）: yes/no"}, {"name": "reusable", "help": "是否可重复使用: yes/no"}, {"name": "implant", "help": "是否植入类: yes/no"}, {"name": "sterile", "help": "是否无菌: yes/no"}]}


class GateError(Exception):
    code = "E_RUNTIME"
    def __init__(self, msg, code=None):
        super().__init__(msg)
        if code:
            self.code = code


def check_udi_submission(args):
    """UDI 数据库提交合规判定。规则源：NMPA《医疗器械唯一标识系统规则》/ FDA 21 CFR 830 + GUDID / EU MDR Art 27-29 + EUDAMED。"""
    market = (args.get("market") or "").lower()
    if market not in ("cn", "us", "eu"):
        raise GateError("--market 必填，且必须为 cn / us / eu 之一", "E_ENUM_INVALID")
    has_di = (args.get("has_di") or "").lower()
    has_pi = (args.get("has_pi") or "").lower()
    reusable = (args.get("reusable") or "").lower()
    implant = (args.get("implant") or "").lower()
    sterile = (args.get("sterile") or "").lower()
    registered = (args.get("is_registered") or "").lower()

    db, timing, issuer = "", "", ""
    fields = ["器械标识（DI）", "器械名称", "标签人/注册人", "型号规格", "生产日期与失效日期（如适用）"]
    if market == "cn":
        db = "国家药监局·医疗器械唯一标识数据库（UDI 数据库）"
        timing = "产品上市销售前完成数据上传与维护；实施范围按 NMPA 分批公告推进，以最新公告为准"
        issuer = "GS1 / 中关村工信 / 阿里健康（合规发码机构）"
        fields += ["注册证号/备案号", "是否植入", "是否无菌", "是否可重复使用"]
    elif market == "us":
        db = "FDA GUDID（Global Unique Device Identification Database，公开检索：accessgudid.nlm.nih.gov）"
        timing = "器械投入商业流通前完成 GUDID 提交并持续维护"
        issuer = "FDA 认可的发码机构（GS1 / HIBCC / ICCBBA）"
        fields += ["Device Description", "Labeler DUNS", "是否植入 / 是否单次使用 / 是否无菌（GUDID 指示项）"]
    else:
        db = "EU EUDAMED（European Database on Medical Devices）"
        timing = "EUDAMED 各模块分阶段强制生效，具体义务以欧盟委员会最新公告为准（Art 27/29）"
        issuer = "GS1 / HIBCC / ICCBBA（issued entity）"
        fields += ["Basic UDI-DI", "SRN（单一注册号）", "器械风险等级"]

    warns = []
    if has_di in ("no", "false", ""):
        warns.append("缺失 DI（器械标识）——DI 为数据库提交的基础字段，未就绪即无法提交")
    need_pi = (reusable in ("yes", "true") or implant in ("yes", "true"))
    if need_pi and has_pi in ("no", "false", ""):
        warns.append("可重复使用或植入类器械须具备 PI（生产标识）以实现追溯，当前缺失，属高风险缺口")
    if registered in ("no", "false") and market == "cn":
        warns.append("境内尚未取得注册证/备案——中国 UDI 数据库提交通常与注册信息绑定，请先厘清注册状态")

    oblig = [
        "UDI 载体（标签/包装）与数据库数据须一致，任一变更须同步更新",
        "数据库维护是持续义务，非一次性提交",
        "发码机构须为法规认可机构，自编码不被接受（除非法规另有规定）",
    ]
    notes = [
        "本判定为「提交义务与控制项」清单，不代替数据库账号操作指引",
        "各辖区实施范围与过渡期以官方最新公告为准",
        "数据库入口与字段以官方系统实时界面为准",
    ]
    return {
        "market": market, "database": db, "submit_timing": timing, "issuing_agency": issuer,
        "core_fields": fields,
        "formatters_present": {"DI": has_di or "未提供", "PI": has_pi or "未提供"},
        "obligations": oblig, "notes": notes,
        "evidence": ["NMPA 医疗器械唯一标识系统规则", "FDA 21 CFR 830 / GUDID",
                     "MDR (EU) 2017/745 Art 27-29 / EUDAMED"],
        "official_portals": ["https://udi.nmpa.gov.cn/", "https://accessgudid.nlm.nih.gov/", "https://ec.europa.eu/tools/eudamed"],
        "warnings": warns,
    }


def _call(args):
    fn_name = "check_udi_submission"
    res = globals()[fn_name](args)
    return res


def main():
    p = argparse.ArgumentParser(prog="udi-db-submission-check", description="UDI 数据库提交合规判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, default=None, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR")
    ns = p.parse_args()
    names = [a["name"] for a in META["args"]]

    if ns.demo:
        ok = True
        for d in [{"market": "cn", "is_registered": "yes", "has_di": "yes", "has_pi": "no", "implant": "yes"}, {"market": "us", "is_registered": "yes", "has_di": "yes", "has_pi": "yes", "reusable": "yes"}, {"market": "eu", "has_di": "no"}]:
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
