# -*- coding: utf-8 -*-
"""AI 内容披露生成器：为 AI 参与生成的内容一键生成合规披露声明。零依赖。

依据（口径给量级区间，以官方最新文本为准）：
  - 中国《人工智能生成合成内容标识办法》（2025-09-01 起施行）：AI 生成合成内容应加显式标识
  - EU AI Act 第 50 条：与 AI 交互 / 生成操纵性内容需透明度告知

三律映射：LGD-II 有证 —— 披露即让内容出处"有证"。

用法：
  python ai_content_discloser.py --type article --ai-level assisted --brand "MedXpert"
  python ai_content_discloser.py --type image --ai-level full --json
"""
import argparse, datetime, json, sys

LEVELS = {
    "full": ("AI 全生成", "AI-generated"),
    "assisted": ("AI 辅助创作（人工主创）", "AI-assisted, human-authored"),
    "mixed": ("AI 与人工混合生成", "co-created by AI and human"),
}
TYPES = ["text", "article", "report", "image", "video", "audio", "code"]
PLATFORMS = {
    "wechat": "公众号：在文首或文末正文区加显式声明（不放『阅读原文』之后）",
    "web": "网页：页首可见声明 + HTML meta 标签（见下方隐式标注）",
    "paper": "论文/报告：方法节注明 AI 参与与工具，首页角标",
    "code": "代码仓库：README 声明 + commit message 标注 [ai]",
    "generic": "通用：随内容载体可见位置加显式声明",
}


def run_selftest():
    """自检：跑真实 main() 并断言披露生成——full 级标 ai_generated=true（须过）、
    assisted 级标 false 且英文措辞对应（须过）、非法 --ai-level 被参数门拦下（须拦）。"""
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
        sys.argv = ["ai_content_discloser.py"] + argv
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

    code, out = run(["--type", "article", "--ai-level", "full", "--json"])
    r = json.loads(out) if code == 0 else {}
    check("full 级披露生成 rc=0 且 ai_generated=true",
          code == 0 and r.get("implicit_metadata", {}).get("ai_generated") is True
          and "全生成" in r.get("explicit_zh", ""))
    code, out = run(["--type", "image", "--ai-level", "assisted", "--json"])
    r = json.loads(out) if code == 0 else {}
    check("assisted 级 ai_generated=false 且措辞对应",
          code == 0 and r.get("implicit_metadata", {}).get("ai_generated") is False
          and "AI-assisted" in r.get("explicit_en", ""))
    code, _ = run(["--type", "article", "--ai-level", "bogus", "--json"])
    check("非法 ai-level 被参数门拦下 rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1


def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser(description="AI 内容披露生成器 · 合规披露一键生成")
    ap.add_argument("--selftest", action="store_true", help="自检（内置参数夹具，不写文件）")
    ap.add_argument("--type", required=True, choices=TYPES, help="内容类型")
    ap.add_argument("--ai-level", required=True, choices=list(LEVELS), help="AI 参与度")
    ap.add_argument("--brand", default="", help="署名/品牌（可选）")
    ap.add_argument("--tool", default="", help="使用的 AI 工具名（可选，如 GLM/Claude）")
    ap.add_argument("--platform", default="generic", choices=list(PLATFORMS), help="发布渠道")
    ap.add_argument("--date", default=datetime.date.today().isoformat(), help="披露日期")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    zh_lvl, en_lvl = LEVELS[a.ai_level]
    who = f"（{a.brand}）" if a.brand else ""
    tool = f"，使用工具：{a.tool}" if a.tool else ""
    explicit_zh = (f"本文由 AI {zh_lvl} 产出{who}{tool}，"
                   f"已经人工审核校对。披露日期：{a.date}。依据《人工智能生成合成内容标识办法》"
                   f"与 EU AI Act 第 50 条进行标识；口径以官方最新文本为准。")
    explicit_en = (f"This content is {en_lvl}{(' by ' + a.brand) if a.brand else ''}"
                   f"{(', produced with ' + a.tool) if a.tool else ''}, and has been human-reviewed. "
                   f"Labeled per China's AI Content Labeling Measures and EU AI Act Art.50; "
                   f"latest official text prevails.")
    implicit = {
        "content_type": a.type,
        "ai_generated": a.ai_level == "full",
        "ai_involvement": a.ai_level,
        "tool": a.tool or None,
        "disclosure_date": a.date,
        "human_reviewed": True,
        "note": "隐式标识：写入文件元数据 / HTML meta / 图片 EXIF（字段名以平台规范为准）",
    }
    result = {
        "explicit_zh": explicit_zh,
        "explicit_en": explicit_en,
        "implicit_metadata": implicit,
        "platform_tip": PLATFORMS[a.platform],
        "basis": "《人工智能生成合成内容标识办法》(2025-09-01 施行)；EU AI Act Art.50。本工具为治理辅助，不构成法律意见。",
    }
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    print("=== 显式声明（中文）===")
    print(explicit_zh)
    print("\n=== Explicit statement (EN) ===")
    print(explicit_en)
    print("\n=== 隐式标注（元数据建议）===")
    print(json.dumps(implicit, ensure_ascii=False, indent=2))
    print("\n=== 平台贴法 ===")
    print(PLATFORMS[a.platform])
    print("\n依据：" + result["basis"])
    sys.exit(0)


if __name__ == "__main__":
    main()
