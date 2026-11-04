#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evolution_check.py — agent-evolution 配套检查器（能力卡进化记录校验）

本技能（SKILL.md）的流程第 1 步读「作战室能力卡」第六节的逐席行，
第 5 步把进化记录按固定格式回写该席行的「进化记录」栏：

    [日期] 沉淀：<技能名/记忆主题> — <该席能力如何升级>

本检查器只校验这一件**有文档格式定义的产物**：

  · 能力卡模式：文件中存在表头含「进化记录」的 Markdown 表格时，
    校验表格结构（须有「进化记录」栏 = 回写落点；每行须有席位标识），
    并逐条校验「进化记录」栏内的条目。
  · 日志模式：无此表格时，把每个非空、非注释（# 开头）行视为一条进化记录逐条校验。

  每条进化记录的校验项（格式 + 完整性）：
    1. 格式合规：[YYYY-MM-DD] 沉淀：<目标> — <升级说明>，三段均非空；
    2. 日期是真实日历日期，且不晚于今天（未来日期 = 不可能的回写）；
    3. 同一席（日志模式为全文件）内无完全重复条目（重复 = 双重回写）；
    4. 同一席内条目日期不递减（进化记录为只追加日志，乱序提示错位/篡改）。

明确不在本检查器范围（宿主流程，无独立可校验产物格式，不臆造检查）：
  · SkillManage 的实际调用（建/改技能）与记忆文件的实际回写——宿主动作；
  · 自评分数的「人工按证据校准」——SKILL.md 只定纪律、未定评分记录格式，
    校准本身是人工步骤，本检查器不发明评分记录格式去「校验」它；
  · 条目所指技能/记忆是否真实存在于宿主机——依赖宿主状态，离线不可判。

用法：
  python evolution_check.py <能力卡.md|进化日志.txt>
  python evolution_check.py --selftest

退出码：0 = 全部合规；1 = 发现违规；2 = 用法/IO 错误。
零第三方依赖（stdlib only），不联网、不写任何文件。
"""
import argparse
import datetime
import re
import sys

ENTRY_RE = re.compile(
    r"^\[(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})\]\s*沉淀\s*[:：]\s*"
    r"(?P<target>.+?)\s+[—–]\s+(?P<desc>.+)$"
)
PLACEHOLDERS = {"", "—", "-", "–", "无", "暂无", "无记录", "N/A", "n/a"}
CELL_SPLIT_RE = re.compile(r"<br\s*/?>|；|;", re.IGNORECASE)


def parse_entry(text):
    """解析一条进化记录。返回 (date_obj, target, desc) 或 None（格式不合）。"""
    m = ENTRY_RE.match(text.strip())
    if not m:
        return None
    try:
        dt = datetime.date(int(m.group("y")), int(m.group("m")), int(m.group("d")))
    except ValueError:
        return "INVALID-DATE"
    return (dt, m.group("target").strip(), m.group("desc").strip())


def check_entries(entries, today, violations):
    """对一组 (定位, 原文) 条目做格式/日期/重复/顺序校验。返回有效条目数。"""
    seen = {}
    last_date = None
    valid = 0
    for loc, raw in entries:
        parsed = parse_entry(raw)
        if parsed is None:
            violations.append("%s: 条目格式不合（应为「[YYYY-MM-DD] 沉淀：<目标> — <升级说明>」）：%s"
                              % (loc, raw))
            continue
        if parsed == "INVALID-DATE":
            violations.append("%s: 日期不是真实日历日期：%s" % (loc, raw))
            continue
        dt, _target, _desc = parsed
        if dt > today:
            violations.append("%s: 日期 %s 晚于今天 %s（未来日期的回写不可能存在）"
                              % (loc, dt.isoformat(), today.isoformat()))
            continue
        key = raw.strip()
        if key in seen:
            violations.append("%s: 与 %s 完全重复（双重回写）：%s" % (loc, seen[key], raw))
            continue
        seen[key] = loc
        if last_date is not None and dt < last_date:
            violations.append("%s: 日期 %s 早于上一条 %s（只追加日志乱序）"
                              % (loc, dt.isoformat(), last_date.isoformat()))
            continue
        last_date = dt
        valid += 1
    return valid


def split_cells(line):
    parts = line.strip().split("|")
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def is_separator_row(cells):
    return all(re.fullmatch(r":?-{3,}:?", c or "---") for c in cells) and len(cells) > 0


def check_card(lines, today):
    """能力卡模式。返回 (条目总数, 违规列表) 或 None（无进化记录表格）。"""
    header_idx = None
    header_cells = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and "进化记录" in line:
            header_idx = i
            header_cells = split_cells(line)
            break
    if header_idx is None:
        return None
    violations = []
    total = 0
    evo_col = header_cells.index("进化记录")
    for j in range(header_idx + 1, len(lines)):
        line = lines[j]
        if not line.strip().startswith("|"):
            break
        cells = split_cells(line)
        if is_separator_row(cells):
            continue
        loc = "第 %d 行" % (j + 1)
        seat = cells[0] if cells else ""
        cell = cells[evo_col] if evo_col < len(cells) else ""
        entries = []
        if cell.strip() not in PLACEHOLDERS:
            entries = [(loc, e.strip()) for e in CELL_SPLIT_RE.split(cell) if e.strip()]
        if entries and not seat:
            violations.append("%s: 有进化记录但席位标识为空" % loc)
        total += check_entries(entries, today, violations)
    return total, violations


def check_log(lines, today):
    """日志模式：每个非空、非注释行一条进化记录。"""
    entries = []
    for i, line in enumerate(lines):
        s = line.strip()
        if s and not s.startswith("#"):
            entries.append(("第 %d 行" % (i + 1), s))
    violations = []
    total = check_entries(entries, today, violations)
    return total, violations


def check_text(text, today=None):
    """核心检查：返回 (模式, 条目总数, 违规列表)。"""
    today = today or datetime.date.today()
    lines = text.splitlines()
    card = check_card(lines, today)
    if card is not None:
        total, violations = card
        return "能力卡", total, violations
    total, violations = check_log(lines, today)
    return "进化日志", total, violations


def run_selftest():
    """自检：临时夹具跑真实 check_text/main 逻辑——合规能力卡须过；
    坏日期/缺段/未来日期/重复/乱序/缺进化记录栏/空席位逐项被拦（须拦）。"""
    import contextlib
    import io
    import tempfile
    from pathlib import Path

    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("  [FAIL] " + name)

    today = datetime.date.today()
    future = (today + datetime.timedelta(days=30)).isoformat()

    good_card = (
        "# 作战室能力卡\n\n## 第六节 能力矩阵\n\n"
        "| 席位 | 本周学习重点 | 进化记录 |\n"
        "|---|---|---|\n"
        "| medical-device-reg-expert | EUDAMED 字段 | [2026-08-26] 沉淀：kdocs-hub-migrate — "
        "导入自动带 .html 后缀<br>[2026-11-01] 沉淀：UDI 校验口径 — 复用资料库硬门清单自查 |\n"
        "| cfo | 现金流模型 |  |\n"
        "| chairman-twin | 行业扫描 | 暂无 |\n"
    )
    mode, total, v = check_text(good_card, today)
    check("合规能力卡→零违规", mode == "能力卡" and v == [])
    check("合规能力卡→条目计数=2", total == 2)

    bad_date = good_card.replace("[2026-08-26]", "[2026-02-30]")
    _, _, v = check_text(bad_date, today)
    check("不存在的日历日期(02-30)被拦", any("真实日历日期" in x for x in v))

    missing_desc = good_card.replace(
        "[2026-08-26] 沉淀：kdocs-hub-migrate — 导入自动带 .html 后缀",
        "[2026-08-26] 沉淀：kdocs-hub-migrate")
    _, _, v = check_text(missing_desc, today)
    check("缺升级说明段被拦", any("格式不合" in x for x in v))

    future_card = good_card.replace("[2026-08-26]", "[%s]" % future)
    _, _, v = check_text(future_card, today)
    check("未来日期被拦", any("晚于今天" in x for x in v))

    dup_card = good_card.replace(
        "<br>[2026-11-01] 沉淀：UDI 校验口径 — 复用资料库硬门清单自查",
        "<br>[2026-08-26] 沉淀：kdocs-hub-migrate — 导入自动带 .html 后缀")
    _, _, v = check_text(dup_card, today)
    check("完全重复条目被拦", any("完全重复" in x for x in v))

    ooo_card = good_card.replace("[2026-08-26]", "[2026-11-02]").replace(
        "[2026-11-01]", "[2026-10-01]")
    _, _, v = check_text(ooo_card, today)
    check("日期乱序被拦", any("乱序" in x for x in v))

    no_col = ("| 席位 | 本周学习重点 | 备注 |\n|---|---|---|\n"
              "| cfo | 现金流 | [2026-08-26] 沉淀：x — y |\n")
    mode, _, v = check_text(no_col, today)
    check("无进化记录栏→按日志模式且不误报合规",
          mode == "进化日志" and len(v) >= 1)

    empty_seat = ("| 席位 | 进化记录 |\n|---|---|\n"
                  "|  | [2026-08-26] 沉淀：x — y |\n")
    _, _, v = check_text(empty_seat, today)
    check("有记录但席位为空被拦", any("席位标识为空" in x for x in v))

    good_log = ("[2026-08-26] 沉淀：kdocs-hub-migrate — 导入自动带 .html 后缀\n"
                "[2026-11-01] 沉淀：UDI 校验口径 — 复用资料库硬门清单自查\n")
    mode, total, v = check_text(good_log, today)
    check("合规进化日志→零违规且计数=2", mode == "进化日志" and v == [] and total == 2)

    bad_log = good_log + "2026-11-02 沉淀：缺方括号日期 — 不合格式\n"
    _, _, v = check_text(bad_log, today)
    check("日志坏行被拦并带行号", any("格式不合" in x and "第 3 行" in x for x in v))

    # main() 全流程退出码：合规文件 rc=0；违规文件 rc=1；不存在的文件 rc=2
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        ok_file = td / "card.md"
        ok_file.write_text(good_card, encoding="utf-8")
        bad_file = td / "bad.md"
        bad_file.write_text(future_card, encoding="utf-8")

        def run_main(path):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = main([str(path)])
            return rc, buf.getvalue()

        rc, out = run_main(ok_file)
        check("main 合规文件→rc=0", rc == 0 and "违规 0 条" in out)
        rc, out = run_main(bad_file)
        check("main 违规文件→rc=1", rc == 1 and "违规 1 条" in out)
        rc = main([str(td / "no-such-file.md")])
        check("main 文件不存在→rc=2", rc == 2)

    print("SELFTEST: %d passed, %d failed — %s"
          % (passed, failed, "PASS" if failed == 0 else "FAIL"))
    return 0 if failed == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="evolution_check",
        description="校验能力卡「进化记录」栏 / 进化日志的格式与完整性"
                    "（agent-evolution 流程第 5 步回写产物的独立检查）")
    ap.add_argument("file", nargs="?", help="能力卡 .md 或进化日志 .txt 路径")
    ap.add_argument("--selftest", action="store_true",
                    help="自检（临时夹具，不触碰真实文件）")
    args = ap.parse_args(argv)

    if args.selftest:
        return run_selftest()
    if not args.file:
        ap.print_usage(sys.stderr)
        print("evolution_check: 需要给出待校验文件路径（或 --selftest）", file=sys.stderr)
        return 2
    try:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print("evolution_check: 无法读取 %s：%s" % (args.file, e), file=sys.stderr)
        return 2

    mode, total, violations = check_text(text)
    print("进化记录校验（%s模式）：%s" % (mode, args.file))
    for v in violations:
        print("  [违规] " + v)
    print("条目 %d 条合规，违规 %d 条 — %s"
          % (total, len(violations), "PASS" if not violations else "FAIL"))
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
