# -*- coding: utf-8 -*-
"""团队AI使用守则生成器：一键生成一页《团队 AI 使用守则》。零依赖。

三律映射：LGD-III 有门禁 —— 把"注意点"写成真规矩。

用法：
  python ai_usage_policy.py --team 运营部 --tools "内部客服bot" "GLM(脱敏后)" \
      --forbidden "客户PII直接粘贴" "合同最终稿自动生成" \
      --escalation "法务-张三 / 安全-李四" --out policy.md
"""
import argparse, datetime, json, pathlib, sys

DEFAULT_FORBIDDEN = ["客户 PII/密钥/内部代号直接粘贴给外部 AI",
                     "用 AI 输出直接对外承诺（合同/报价/法规结论）不经人审",
                     "把 AI 输出当最终事实引用而不核对来源"]


def run_selftest():
    """自检：跑真实 main() 并断言守则生成——全参生成含红线与上报线（须过）、
    缺省红线用通用三条（须过）、--out 落盘一致（须过）、缺必填上报线被拦（须拦）。"""
    import contextlib, io, tempfile
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
        sys.argv = ["ai_usage_policy.py"] + argv
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

    code, out = run(["--team", "运营部", "--tools", "内部客服bot",
                     "--forbidden", "客户PII直接粘贴",
                     "--escalation", "法务-张三", "--json"])
    pol = json.loads(out).get("policy", "") if code == 0 else ""
    check("全参守则含队名/红线/上报线",
          code == 0 and "# AI 使用守则 · 运营部" in pol
          and "⛔ 客户PII直接粘贴" in pol and "法务-张三" in pol)
    code, out = run(["--team", "测试部", "--escalation", "安全-李四", "--json"])
    pol = json.loads(out).get("policy", "") if code == 0 else ""
    check("缺省红线用通用三条", DEFAULT_FORBIDDEN[0] in pol)
    with tempfile.TemporaryDirectory() as td:
        outp = str(pathlib.Path(td) / "policy.md")
        code, out = run(["--team", "运营部", "--escalation", "法务-张三",
                         "--out", outp, "--json"])
        on_disk = pathlib.Path(outp).read_text(encoding="utf-8") \
            if pathlib.Path(outp).is_file() else ""
        check("--out 落盘与生成文本一致",
              code == 0 and on_disk == json.loads(out).get("policy"))
    code, _ = run(["--team", "运营部"])
    check("缺必填 --escalation 被拦 rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="团队AI使用守则生成器 · 一页守则")
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--team", required=True, help="团队/部门名")
    ap.add_argument("--tools", nargs="*", default=[], help="批准使用的 AI 工具")
    ap.add_argument("--allowed-for", nargs="*", default=["草拟/总结/翻译/内部问答"], help="允许场景")
    ap.add_argument("--forbidden", nargs="*", default=[], help="禁止场景（缺省用通用三条）")
    ap.add_argument("--escalation", required=True, help="出事上报线（人/角色）")
    ap.add_argument("--out", help="输出 Markdown 路径")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    fb = a.forbidden or DEFAULT_FORBIDDEN
    tools = a.tools or ["（待批准清单）"]
    md = ["# AI 使用守则 · " + a.team, "",
          f"- **生效日期**：{datetime.date.today().isoformat()}　**上报线**：{a.escalation}", "",
          "## 一、批准工具", ""] + [f"- {t}" for t in tools] + \
         ["", "## 二、允许用于", ""] + [f"- {x}" for x in a.allowed_for] + \
         ["", "## 三、禁止（红线）", ""] + [f"- ⛔ {x}" for x in fb] + \
         ["", "## 四、出事怎么办",
          f"1. 立即停用相关会话/智能体，保留现场；2. 当天报 {a.escalation}；"
          "3. 用 ai-incident-log 入账，复盘后更新本守则。", "",
          "> 本守则对应 LGD 三律：批准工具与责任人有籍、输出核对有证、红线与上报线有门禁。"]
    text = "\n".join(md)
    if a.out:
        outp = pathlib.Path(a.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(text, encoding="utf-8")
    if a.json:
        print(json.dumps({"policy": text, "out": a.out}, ensure_ascii=False, indent=2))
    else:
        print(text)
        if a.out:
            print("\n已写出：", a.out)
    sys.exit(0)


if __name__ == "__main__":
    main()
