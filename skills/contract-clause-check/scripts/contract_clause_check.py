import argparse, json, re, sys

MUST = ["违约", "争议", "管辖"]
RISKY = [
    ("最终解释权", "单方保留最终解释权条款，多被认定无效且显失公平"),
    ("自动续期", "含自动续期/自动续约，注意退出窗口与通知期"),
    ("永久保密", "永久保密义务需评估对等性与期限合理性"),
    ("放弃诉讼", "放弃诉权类条款效力存疑，请律师复核"),
]


def run_selftest():
    """自检：跑真实 main() 条款扫描——必备条款齐全须 PASS rc=0（须过）；
    缺必备条款须 FAIL rc=1、高违约金与最终解释权/自动续期须被标风险（须拦）。
    只用内置夹具文本。"""
    import contextlib, io
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    def run(argv):
        old = sys.argv
        sys.argv = ["contract_clause_check.py"] + argv
        buf = io.StringIO()
        code = 0
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
                main()
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
        finally:
            sys.argv = old
        return code, buf.getvalue()

    good = "双方违约责任明确，发生争议由甲方所在地法院管辖解决。"
    code, out = run(["--text", good, "--json"])
    d = json.loads(out)
    check("必备齐全→pass rc=0", code == 0 and d["pass"] is True and d["missing_must"] == [])
    bad = "本协议最终解释权归甲方所有，合同到期自动续期，违约金为合同额的40%。"
    code, out = run(["--text", bad, "--json"])
    d = json.loads(out)
    terms = [r["term"] for r in d["risky"]]
    check("缺必备条款→FAIL rc=1（缺争议/管辖）",
          code == 1 and d["pass"] is False and len(d["missing_must"]) == 2)
    check("最终解释权/自动续期/违约金40% 被标风险",
          "最终解释权" in terms and "自动续期" in terms
          and any(t.startswith("违约金40") for t in terms))
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="contract-clause-check · 合同高危条款扫描（零依赖）")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--text", required=True, help="合同文本（可粘贴要点）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    t = a.text
    problems, risky = [], []
    for k in MUST:
        if k not in t:
            problems.append("缺少必备条款关键词：" + k)
    for k, why in RISKY:
        if k in t:
            risky.append({"term": k, "why": why})
    penalty = re.search(r"违约金[^\d]{0,6}(\d{1,2}(?:\.\d+)?)\s*%", t)
    if penalty and float(penalty.group(1)) > 30:
        risky.append({"term": "违约金" + penalty.group(1) + "%", "why": "违约金超损失30%部分可能被法院调减（民法典585条）"})
    if a.json:
        print(json.dumps({"pass": not problems, "missing_must": problems, "risky": risky},
                         ensure_ascii=False, indent=2))
    else:
        print("必备条款：")
        for k in MUST:
            print(("  [x] " if k in t else "  [ ] ") + k)
        if risky:
            print("风险提示：")
            for r in risky:
                print("    - " + r["term"] + "：" + r["why"])
        print("  判定：" + ("PASS" if not problems else "FAIL 缺必备条款"))
        print("  免责：本工具为初筛，不构成法律意见，重要合同请律师复核。")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
