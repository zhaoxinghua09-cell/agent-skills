# -*- coding: utf-8 -*-
"""引用覆盖率检查器：扫描文章的引用覆盖率。零依赖。

对含数字/日期/百分比/强论断的句子，检查是否带来源标注
（据/来源/source/链接/《》/参考文献/https）。低于阈值 rc=1，逐句列缺口。
三律映射：LGD-II 有证 —— 论断要带出处。

用法：
  python citation_coverage_check.py --file report.md --threshold 0.6
  python citation_coverage_check.py --text "..." --json
"""
import argparse, json, pathlib, re, sys

HAS_NUM = re.compile(r"(\d+(\.\d+)?%?|\d{4}年|\d+月\d+日)")
HAS_SRC = re.compile(r"(据|来源|source|参考|文献|《[^》]{2,40}》|https?://)", re.I)


def run_selftest():
    """自检：跑真实 main() 并断言覆盖率判定——
    论断全带来源→覆盖率 1.0 通过（须过）；论断无来源→覆盖率 0 且 rc=1（须拦）；无论断句→免检通过（须过）。"""
    import contextlib, io
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    def run(text):
        old = sys.argv
        sys.argv = ["citation_coverage_check.py", "--text", text, "--json"]
        buf = io.StringIO()
        code = 0
        try:
            with contextlib.redirect_stdout(buf):
                main()
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
        finally:
            sys.argv = old
        return code, json.loads(buf.getvalue())

    code, r = run("据国家统计局数据，2025年GDP增长5%。来源：新华社报道，失业率为5.1%。")
    check("全带来源→覆盖率 1.0 rc=0",
          code == 0 and r["claims"] == 2 and r["coverage"] == 1.0 and r["pass"] is True)
    code, r = run("公司营收增长了38%，用户突破200万。")
    check("无来源论断→覆盖率 0 rc=1 且列缺口",
          code == 1 and r["coverage"] == 0.0 and r["pass"] is False
          and len(r["uncovered"]) == 1)
    code, r = run("今天天气不错，大家一起去公园散步聊天。")
    check("无论断句→免检通过 rc=0",
          code == 0 and r["claims"] == 0 and r["pass"] is True)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="引用覆盖率检查器 · 论断要带出处")
    ap.add_argument("--selftest", action="store_true", help="自检（内置文本夹具，不读外部文件）")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="文件")
    src.add_argument("--text", help="文本（内联 / @文件 / 纯路径）")
    ap.add_argument("--threshold", type=float, default=0.6, help="覆盖率阈值（默认 0.6）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        if a.file:
            text = pathlib.Path(a.file).read_text(encoding="utf-8")
        else:
            q = a.text[1:] if a.text.startswith("@") else a.text
            text = pathlib.Path(q).read_text(encoding="utf-8") if pathlib.Path(q).is_file() else q
    except OSError as e:
        print(f"输入不可读：{e}", file=sys.stderr)
        sys.exit(2)

    claim_sents, uncovered = [], []
    for s in re.split(r"[。！？!?\n]", text):
        s = s.strip()
        if len(s) < 8 or not HAS_NUM.search(s):
            continue
        claim_sents.append(s)
        if not HAS_SRC.search(s):
            uncovered.append(s[:40] + ("…" if len(s) > 40 else ""))
    total = len(claim_sents)
    cov = (1 - len(uncovered) / total) if total else 1.0
    ok = cov >= a.threshold
    result = {"claims": total, "covered": total - len(uncovered),
              "coverage": round(cov, 2), "threshold": a.threshold, "pass": ok,
              "uncovered": uncovered,
              "note": "引用覆盖率过低，缺出处清单见上（rc=1）" if not ok
              else ("覆盖达标" if total else "无论断句，无需检查")}
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"论断句：{total}  有来源：{result['covered']}  覆盖率：{cov:.0%}（阈值 {a.threshold:.0%}）")
        if uncovered:
            print("缺出处清单：")
            for u in uncovered[:10]:
                print("  - " + u)
        print(("⛔ " if not ok else "✅ ") + result["note"])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
