#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跑黄金集：逐条断言 summarize_pro 的抽取/骨架/溯源/自检结果。

用法（任意目录）：
    python tests/run_golden.py            # 全部用例
    python tests/run_golden.py --id G01   # 只跑一条

退出码：0 全过；1 有失败。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import summarize_pro as sp  # noqa: E402


def load_cases():
    with open(os.path.join(HERE, "golden.json"), encoding="utf-8") as f:
        return json.load(f)["cases"]


def check(case):
    """返回 (ok, [失败原因])"""
    fails = []
    fmt = case.get("format", "minutes")
    exp = case.get("expect", {})

    # G10 专用于溯源校验
    if fmt == "citecheck":
        good = sp.citecheck(case["good_output"], case["source"])
        bad = sp.citecheck(case["bad_output"], case["source"])
        if good["verdict"] != exp.get("good_verdict"):
            fails.append("good 期望 %s，实际 %s" % (exp.get("good_verdict"), good["verdict"]))
        if bad["verdict"] != exp.get("bad_verdict"):
            fails.append("bad 期望 %s，实际 %s" % (exp.get("bad_verdict"), bad["verdict"]))
        if len(bad["missing"]) < exp.get("bad_missing_min", 0):
            fails.append("bad 检出 %d 处不可溯源，少于期望 %d"
                         % (len(bad["missing"]), exp.get("bad_missing_min", 0)))
        return (not fails), fails

    text = case.get("input", "")
    kind = case.get("kind", "extract")

    # 脱敏类用例
    if kind == "redact":
        clean, rep = sp.redact_text(text, exp.get("terms", []))
        if rep["total"] < exp.get("redacted_min", 0):
            fails.append("脱敏 %d 处，期望 ≥%d（%s）"
                         % (rep["total"], exp.get("redacted_min", 0), rep["counts"]))
        for s in exp.get("not_contains", []):
            if s in clean:
                fails.append("脱敏后仍残留明文：%s" % s)
        for s in exp.get("must_contain", []):
            if s not in clean:
                fails.append("脱敏后应保留：%s" % s)
        return (not fails), fails

    # 来源适配
    if kind == "adapt":
        res = sp.adapt_detect(case.get("path", "x.md"), text)
        src = res["candidates"][0]["source"]
        if src != exp.get("source"):
            fails.append("来源识别 %s，期望 %s" % (src, exp.get("source")))
        norm = sp.normalize_source(text, src)
        n_spk = len(__import__("re").findall(r"(?m)^\S{1,12}\s*[:：]", norm))
        if n_spk < exp.get("speaker_lines_min", 0):
            fails.append("折行后说话人行 %d，期望 ≥%d" % (n_spk, exp.get("speaker_lines_min", 0)))
        return (not fails), fails

    # HTML 渲染自包含
    if kind == "html":
        body = sp.render_view(case["facts"], exp.get("view", "executive"))
        html = sp.md_to_html(body, title="t")
        for s in exp.get("must_contain", []):
            if s not in html:
                fails.append("HTML 缺：%s" % s)
        for s in exp.get("not_contains", []):
            if s in html:
                fails.append("HTML 不该含：%s" % s)
        return (not fails), fails

    # 承诺分级（范围否定 / 部门归属）
    if kind == "commitments":
        items = sp.grade_commitments([s for s in text.split("。") if s.strip()])
        neg = [i for i in items if i.get("evidence", "").startswith("范围否定")]
        dept = [i for i in items if i.get("owner_scope")]
        com = [i for i in items if i["strength"] == "committed"]
        if len(neg) < exp.get("scope_negate_min", 0):
            fails.append("范围否定识别 %d 条，期望 ≥%d" % (len(neg), exp.get("scope_negate_min", 0)))
        if len(dept) < exp.get("owner_scope_min", 0):
            fails.append("部门归属识别 %d 条，期望 ≥%d" % (len(dept), exp.get("owner_scope_min", 0)))
        if len(com) > exp.get("committed_max", 99):
            fails.append("误判 committed %d 条（应 ≤%d）" % (len(com), exp.get("committed_max", 99)))
        return (not fails), fails

    # 日期归一
    if kind == "normdates":
        new_text, rep = sp.norm_dates(text, exp.get("ref"))
        if rep["count"] < exp.get("count_min", 1):
            fails.append("归一 %d 处，期望 ≥%d" % (rep["count"], exp.get("count_min", 1)))
        for s in exp.get("must_contain", []):
            if s not in new_text:
                fails.append("归一后缺：%s" % s)
        for s in exp.get("must_keep", []):
            if s not in new_text:
                fails.append("原文被改写，丢了：%s（本工具只追加锚点）" % s)
        return (not fails), fails

    # 中性措辞
    if kind == "neutral":
        res = sp.neutral_scan(text)
        if res["neutral_language_mode"] != exp.get("mode", True):
            fails.append("neutral 期望 %s，实际 %s" % (exp.get("mode"), res["neutral_language_mode"]))
        groups = {h["group"] for h in res["hits"]}
        for g in exp.get("groups", []):
            if g not in groups:
                fails.append("未命中场景组：%s（实际 %s）" % (g, sorted(groups)))
        return (not fails), fails

    # 确定性渲染
    if kind == "render":
        body = sp.render_view(case["facts"], exp.get("view", "receipt"))
        for s in exp.get("not_contains", []):
            if s in body:
                fails.append("渲染不该含：%s" % s)
        for s in exp.get("must_contain", []):
            if s not in body:
                fails.append("渲染缺：%s" % s)
        return (not fails), fails

    # schema 校验类用例
    if kind == "validate":
        res = sp.validate_facts(case["facts"])
        if res["verdict"] != exp.get("verdict"):
            fails.append("validate 期望 %s，实际 %s（%s）"
                         % (exp.get("verdict"), res["verdict"], res["problems"]))
        return (not fails), fails

    # 期望业务失败（如原文过短）
    if exp.get("expect_error"):
        short = len(text.strip()) < 50
        if exp["expect_error"] == "S006" and not short:
            fails.append("期望 S006（原文过短），但样本长度 %d" % len(text.strip()))
        return (not fails), fails

    facts = sp.extract_facts(text)

    if "dates_min" in exp and len(facts["dates"]) < exp["dates_min"]:
        fails.append("日期抽取 %d 个，期望 ≥%d：%s" % (len(facts["dates"]), exp["dates_min"], facts["dates"]))
    if "todo_min" in exp and len(facts["todo_sentences"]) < exp["todo_min"]:
        fails.append("待办句 %d 条，期望 ≥%d" % (len(facts["todo_sentences"]), exp["todo_min"]))
    if "decision_min" in exp and len(facts["decision_sentences"]) < exp["decision_min"]:
        fails.append("决策句 %d 条，期望 ≥%d" % (len(facts["decision_sentences"]), exp["decision_min"]))
    if "condition_min" in exp and len(facts["condition_sentences"]) < exp["condition_min"]:
        fails.append("条件句 %d 条，期望 ≥%d" % (len(facts["condition_sentences"]), exp["condition_min"]))
    if "owners_contain" in exp:
        have = " ".join(facts["owners_hint"]) + " " + " ".join(facts["speakers"])
        for who in exp["owners_contain"]:
            if who not in have:
                fails.append("未识别到责任人 %s" % who)
    if "numbers_contain" in exp:
        joined = " ".join(facts["numbers"])
        for n in exp["numbers_contain"]:
            if n not in joined:
                fails.append("未抽到数字 %s（实得 %s）" % (n, facts["numbers"]))

    # v2.0.2 起：结论强度 / 承诺强度（语义档位）断言
    ss = facts.get("strength_summary", {})
    if "firm_min" in exp and ss.get("firm_decisions", 0) < exp["firm_min"]:
        fails.append("已定结论 %d 条，期望 ≥%d（实得分布 %s）"
                     % (ss.get("firm_decisions", 0), exp["firm_min"], ss.get("decisions")))
    if "soft_min" in exp and ss.get("soft_decisions", 0) < exp["soft_min"]:
        fails.append("暂定/提案/条件结论 %d 条，期望 ≥%d（实得分布 %s）"
                     % (ss.get("soft_decisions", 0), exp["soft_min"], ss.get("decisions")))
    if "committed_min" in exp and ss.get("committed_owners", 0) < exp["committed_min"]:
        fails.append("明确接活 %d 条，期望 ≥%d（实得分布 %s）"
                     % (ss.get("committed_owners", 0), exp["committed_min"], ss.get("commitments")))
    if "intent_min" in exp:
        got = ss.get("commitments", {}).get("intent_only", 0)
        if got < exp["intent_min"]:
            fails.append("仅表意向 %d 条，期望 ≥%d（实得分布 %s）"
                         % (got, exp["intent_min"], ss.get("commitments")))
    if "todo_max" in exp and len(facts["todo_sentences"]) > exp["todo_max"]:
        fails.append("待办句 %d 条，超过上限 %d（标题行/条件句/已定结论不应计入待办）"
                     % (len(facts["todo_sentences"]), exp["todo_max"]))

    body = sp.build_skeleton(fmt, facts)

    if exp.get("skeleton_has_numbered_lines") and not __import__("re").search(r"^\d+\.\s", body, __import__("re").M):
        fails.append("骨架缺少编号行")
    if "bullets_count_between" in exp:
        import re
        lo, hi = exp["bullets_count_between"]
        n = len(re.findall(r"^\d+\.\s", body, re.M))
        if not (lo <= n <= hi):
            fails.append("要点条数 %d 不在 [%d,%d]" % (n, lo, hi))

    if exp.get("selfcheck") == "PASS":
        sc = sp.selfcheck(body, fmt)
        if sc["verdict"] != "PASS":
            fails.append("结构自检未过：%s" % "; ".join(sc["problems"]))

    return (not fails), fails


def main():
    only = None
    if "--id" in sys.argv:
        only = sys.argv[sys.argv.index("--id") + 1]
    cases = load_cases()
    if only:
        cases = [c for c in cases if c["id"].startswith(only)]
    passed = 0
    for c in cases:
        ok, fails = check(c)
        print(("PASS " if ok else "FAIL ") + c["id"])
        for f in fails:
            print("     - " + f)
        passed += ok
    print("---- %d/%d PASS ----" % (passed, len(cases)))
    sys.exit(0 if passed == len(cases) else 1)


if __name__ == "__main__":
    main()
