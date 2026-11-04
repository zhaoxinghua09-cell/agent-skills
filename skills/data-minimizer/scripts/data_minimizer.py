# -*- coding: utf-8 -*-
"""给AI前脱敏器：交给 AI 之前，先把文本里的敏感信息打码。零依赖。

规则：手机号 / 邮箱 / 证件号(18位) / 银行长号(13-19位) / 指定人名(--names)。
输出：脱敏文本 + 脱敏报告（各类命中数）。--json 给结构化结果。
三律映射：LGD-III 有门禁 —— 交给 AI 前的最后一道脱敏门。

用法：
  python data_minimizer.py --file input.txt --out masked.txt
  python data_minimizer.py --text "找张三 13812345678" --names 张三 李四 --json
"""
import argparse, json, pathlib, re, sys

PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
IDCARD = re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")
LONGNUM = re.compile(r"(?<!\d)\d{13,19}(?!\d)")
MASKS = {"phone": "〔手机号〕", "email": "〔邮箱〕", "idcard": "〔证件号〕", "longnum": "〔长号〕", "name": "〔人名〕"}


def mask_phone(m):
    s = m.group(0)
    return s[:3] + "****" + s[-2:]


def mask_id(m):
    s = m.group(0)
    return s[:4] + "***********" + s[-2:]


def run(text, names):
    counts = {}
    def sub(pat, repl, key):
        nonlocal text
        text, n = pat.subn(repl, text)
        counts[key] = counts.get(key, 0) + n
    sub(IDCARD, mask_id, "idcard")          # 先证件（18位含长号前缀，防误吞）
    sub(PHONE, mask_phone, "phone")
    sub(EMAIL, MASKS["email"], "email")
    sub(LONGNUM, MASKS["longnum"], "longnum")
    for nm in names or []:
        if nm:
            sub(re.compile(re.escape(nm)), MASKS["name"], "name")
    return text, counts



def run_selftest():
    """自检：跑真实 run()/main() 脱敏——手机号/邮箱/人名/证件号须被打码且计数对
    （须过原样保留干净文本、须拦敏感原文）；证件号不得被长号规则二次误吞。
    只用内置夹具文本。注：模块级 run() 即本技能脱敏逻辑，自检的主入口驱动改名 call_main。"""
    import contextlib, io
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    def call_main(argv):
        old = sys.argv
        sys.argv = ["data_minimizer.py"] + argv
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

    masked, counts = run("联系张三 13812345678，邮箱 zhang@example.com", ["张三"])
    check("手机号打码且计数=1",
          "138****78" in masked and "13812345678" not in masked and counts.get("phone") == 1)
    check("邮箱打码且计数=1",
          "〔邮箱〕" in masked and "zhang@example.com" not in masked and counts.get("email") == 1)
    check("人名打码且计数=1",
          "〔人名〕" in masked and "张三" not in masked and counts.get("name") == 1)
    masked2, counts2 = run("证件号 110101199001011234 登记", [])
    check("证件号打码计数=1 且不被长号误吞",
          counts2.get("idcard") == 1 and counts2.get("longnum", 0) == 0
          and "110101199001011234" not in masked2)
    masked3, counts3 = run("普通文本，没有任何敏感信息", [])
    check("干净文本原样通过且零命中",
          masked3 == "普通文本，没有任何敏感信息" and all(v == 0 for v in counts3.values()))
    code, out = call_main(["--text", "电话 13812345678", "--json"])
    d = json.loads(out)
    check("main --json 与 run() 结果一致",
          code == 0 and "138****78" in d["masked_text"] and d["counts"].get("phone") == 1)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="给AI前脱敏器 · 发给 AI 前先脱敏")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="输入文件")
    src.add_argument("--text", help="输入文本（内联 / @文件 / 纯路径）")
    ap.add_argument("--names", nargs="*", default=[], help="要打码的人名/代号")
    ap.add_argument("--out", help="脱敏文本输出路径")
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
    masked, counts = run(text, a.names)
    if a.out:
        outp = pathlib.Path(a.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(masked, encoding="utf-8")
    if a.json:
        print(json.dumps({"masked_text": masked, "counts": counts, "out": a.out},
                         ensure_ascii=False, indent=2))
    else:
        print("=== 脱敏文本 ===")
        print(masked)
        print("=== 脱敏报告 ===")
        for k, n in counts.items():
            print(f"  {MASKS.get(k, k)}：{n} 处")
        if a.out:
            print(f"已写出：{a.out}")
    sys.exit(0)


if __name__ == "__main__":
    main()
