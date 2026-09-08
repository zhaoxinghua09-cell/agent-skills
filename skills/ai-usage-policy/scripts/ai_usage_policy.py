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


def main():
    ap = argparse.ArgumentParser(description="团队AI使用守则生成器 · 一页守则")
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
