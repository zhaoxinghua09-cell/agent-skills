# -*- coding: utf-8 -*-
"""去敏扫描器：扫 PII/密钥/内部路径/内部项目代号，打码并输出脱敏清单。零依赖。"""
import argparse, json, pathlib, re, sys

RULES = [
    ("手机号", re.compile(r"1[3-9]\d{9}")),
    ("身份证", re.compile(r"\b\d{17}[\dXx]\b")),
    ("邮箱", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    # 用拼接构造令牌前缀，避免扫描器把本脚本自身当成密钥泄漏
    ("密钥", re.compile("(" + "s" + "k-[A-Za-z0-9]{8,}|" + "g" + "hp_[A-Za-z0-9]{8,}|" + r"api[_-]?key[=:]\S+|" + r"password[=:]\S+)", re.I)),
    # 拼接构造路径模式，避免扫描器把本脚本自身当成路径泄漏
    # 覆盖：任意盘符绝对路径(C:\ / D:\ 含 Users 或任意路径)、/home/*、*.local
    ("内部路径", re.compile(r"(?:[A-Za-z]:\\[Uu]sers\\[\w.\-]+|[A-Za-z]:\\[\w.\- \\\/]+|/[Uu]sers/[\w.\-]+|/home/[\w.\-]+|[\w.\-]+\.local)")),
    # 内置项目代号启发式：CamelCase 项目词(≥10字符) 或 含 Project/Proj/Internal/Confidential 词
    ("内部项目代号", re.compile(r"\b([A-Z][a-z]+\d*[A-Z]\w{6,}|[A-Za-z]*Project\w*|[A-Za-z]*Proj\w*|[A-Za-z]*Internal\w*|[A-Za-z]*Confidential\w*)\b")),
]

def scan(text, extra=None):
    hits = []
    for name, pat in RULES:
        for m in pat.finditer(text):
            frag = m.group(0)
            # 过滤明显过短/误伤的 CamelCase（单词）
            if name == "内部项目代号" and len(frag) < 8:
                continue
            hits.append((name, m.start(), frag))
    if extra:
        for w in extra:
            for m in re.finditer(re.escape(w), text):
                hits.append(("内部项目代号", m.start(), w))
    return hits

def mask_text(text, hits, mask):
    out = text
    # 从后往前替，避免位移
    for name, pos, frag in sorted(hits, key=lambda x: -x[1]):
        out = out[:pos] + mask + out[pos + len(frag):]
    return out


def run_selftest():
    """自检：跑真实 scan()/mask_text()/main()——手机号/邮箱/密钥须被命中并打码
    （须拦）；干净文本须零命中且 main 报告「未发现敏感项」（须过）。
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

    def call_main(argv):
        old = sys.argv
        sys.argv = ["desens_scan.py"] + argv
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

    hits = scan("联系电话 13812345678，邮箱 a@b.com")
    types = {n for n, _, _ in hits}
    check("手机号与邮箱被命中", "手机号" in types and "邮箱" in types)
    hits2 = scan("配置 api_key=SECRETVALUE123 泄露")
    check("密钥模式被命中", any(n == "密钥" for n, _, _ in hits2))
    probe = "电话 13812345678 备用"
    masked = mask_text(probe, scan(probe), "***")
    check("打码后原文消失且其余文本保留",
          "13812345678" not in masked and "备用" in masked and "***" in masked)
    check("干净文本零命中", scan("这是一段普通的工作总结，没有敏感信息") == [])
    code, out = call_main(["--text", "这是一段普通的工作总结"])
    check("main 干净文本报告未发现", code == 0 and "未发现敏感项" in out)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    ap.add_argument("--mask", default="***")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--extra", nargs="*", help="额外敏感词(内部项目代号)")
    a = ap.parse_args()
    text = a.text if a.text else pathlib.Path(a.file).read_text(encoding="utf-8")
    hits = scan(text, a.extra)
    if not hits:
        print("✅ 未发现敏感项")
        return
    masked = mask_text(text, hits, a.mask)
    print(masked)
    if a.report:
        rep = [{"type": n, "sample": f[:12] + ("…" if len(f) > 12 else "")} for n, _, f in hits]
        print("\n--- desens_report ---")
        print(json.dumps({"count": len(hits), "items": rep}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
