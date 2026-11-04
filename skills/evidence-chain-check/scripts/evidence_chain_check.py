#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""evidence-chain-check — 法律证据链完整性校验纵深工具（零依赖）。
校验证据链: 时间单调 / 主体一致 / 哈希链不断(prev==上一项hash)。
理论真源：LGD 凡自治之物三律（MedXpert × SynomosAI）。"""
import argparse, json, sys
NAME = "evidence-chain-check"
def check(chain):
    breaks = []
    subjects = set()
    prev_hash = None
    last_t = None
    for i, e in enumerate(chain):
        subj = e.get("subject")
        if subj: subjects.add(subj)
        t = e.get("time")
        if last_t is not None and t is not None and t < last_t:
            breaks.append("时间倒序 @" + str(i))
        last_t = t
        h = e.get("hash")
        if prev_hash is not None and e.get("prev") != prev_hash:
            breaks.append("哈希链断裂 @" + str(i))
        prev_hash = h
    if len(subjects) > 1:
        breaks.append("主体不一致:" + "/".join(sorted(subjects)))
    return {"breaks": breaks, "complete": len(breaks) == 0, "subjects": sorted(subjects)}
def run_selftest():
    """自检:跑真实 check()/main()——完整链须判 complete 且 main rc=0(须过);
    哈希断裂/时间倒序/主体不一致三类断裂须被逐一标出且 main rc=1(须拦);
    缺 --chain 须 rc=2。只用内置夹具。注:断言助手命名 expect,避免遮蔽本模块 check()。"""
    import contextlib, io
    passed = failed = 0
    def expect(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)
    def call_main(argv):
        old = sys.argv
        sys.argv = ["evidence_chain_check.py"] + argv
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
    good = [{"id": 1, "time": "2026-01-01", "subject": "甲", "hash": "h1", "prev": None},
            {"id": 2, "time": "2026-01-02", "subject": "甲", "hash": "h2", "prev": "h1"}]
    r = check(good)
    expect("完整链 complete 且无断裂", r["complete"] is True and r["breaks"] == [])
    bad = [dict(good[0]), dict(good[1], prev="hX")]
    r = check(bad)
    expect("哈希链断裂被标出", r["complete"] is False and any("哈希链断裂" in b for b in r["breaks"]))
    bad2 = [dict(good[0], time="2026-01-03"), dict(good[1])]
    r = check(bad2)
    expect("时间倒序被标出", any("时间倒序" in b for b in r["breaks"]))
    bad3 = [dict(good[0]), dict(good[1], subject="乙")]
    r = check(bad3)
    expect("主体不一致被标出", any("主体不一致" in b for b in r["breaks"]))
    code, _ = call_main(["--chain", json.dumps(good)])
    expect("main 完整链 rc=0", code == 0)
    code, _ = call_main(["--chain", json.dumps(bad)])
    expect("main 断裂链 rc=1", code == 1)
    code, _ = call_main([])
    expect("main 缺 --chain rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1
def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description=NAME + " · 证据链校验")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--chain", help="证据列表 JSON: [{id,time,subject,hash,prev}]")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.chain: print("用法: --chain <JSON>", file=sys.stderr); sys.exit(2)
    try: chain = json.loads(a.chain)
    except Exception as e: print("chain JSON 解析失败: " + str(e), file=sys.stderr); sys.exit(2)
    r = check(chain)
    if a.json: print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("=== " + NAME + " · 证据链校验 ===")
        print("  断裂点: " + (",".join(r["breaks"]) or "无"))
        print("  结论: " + ("链完整 ✅" if r["complete"] else "链断裂 ⛔"))
    sys.exit(0 if r["complete"] else 1)
if __name__ == "__main__":
    main()
