#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""summarize-pro 本地工具链（零依赖、纯标准库、不联网）。

它做三件事，且只做这三件事：
  1. extract    把 txt/md/docx 读成纯文本，抽取可核验的事实线索（日期/数字/人名/待办句/决策句/条件句），
                并按指定的格式族生成「骨架」Markdown。不做语义总结 —— 那是 Agent 的工作。
  2. citecheck  把一份「输出」逐句抽事实 token，回原文比对，列出无法溯源的清单。
                这是把「忠实性纪律」从口号变成可跑断言的核心。
  3. selfcheck  检查一份输出是否满足格式族的机器可判要素（如纪要必须有待办区且含责任人或期限列）。

错误码（固定，便于上层脚本判断）：
  S001 输入文件不存在   S002 编码不可读   S003 内容为空
  S004 未知输出格式     S005 输出目录不可写 S006 原文过短（<50 字，按边界规则不套格式族）

退出码：0 成功；1 业务失败（带错误码）；2 参数错误。

用法：
  python summarize_pro.py extract  --file demo/sample_transcript.md --format minutes --out demo_out
  python summarize_pro.py citecheck --file demo_out/sample_transcript.minutes.md --source demo/sample_transcript.md
  python summarize_pro.py selfcheck --file demo_out/sample_transcript.minutes.md --format minutes
  （任意子命令加 --json 输出机读结果，字段固定 ok/error_id/data）
"""
import argparse
import json
import os
import re
import sys
import zipfile

FORMATS = ("minutes", "compare", "timeline", "bullets", "card")

# ---------- 事实抽取规则（全部可解释、可复核） ----------
DATE_PATTERNS = [
    r"\d{4}-\d{2}-\d{2}",
    r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*[日号]",
    r"\d{4}\s*年\s*\d{1,2}\s*月",
    r"\d{1,2}\s*月\s*\d{1,2}\s*[日号]",
    r"\d{1,2}\s*月",
    # 相对日期（原文保留，可用 normdates 追加 ISO 锚点）
    r"(?:下下周|下周|下星期|本周|这周|本星期)\s*[一二三四五六日天1-7]",
    r"今天|今日|明天|明日|后天",
    r"本月底|月底",
    r"下个?月\s*\d{1,2}\s*[日号]",
]
NUM_PATTERN = r"(?<![\w-])\d+(?:\.\d+)?(?:%|％|万|亿|元|美元|人|天|小时|分钟|个|份|页|条|台|次|版)?"
NEGOTIABLE = re.compile(r"要|需|必须|应当|负责|跟进|截止|前完成|待办|下一步|行动项|TODO"
                        r"|出初稿|由我|我来|我来发|我发|我写|我出|我看看|回头说|再说"
                        r"|跟.{0,8}对接|对接|谁去|下次会|挂到"
                        r"|跟一下|跟进一下|盯一下|排一下|安排一下|确认一下|看一下")
DECISION = re.compile(r"决定|确定|定了|结论|批准|同意|一致认为|拍板|裁定"
                      r"|改为|改到|写死|定为|释放|退回|不做|只做|先行|定\s*\d"
                      r"|建议|提议|暂定|暂时|先按|初步|可以考虑")
CONDITION = re.compile(r"如果|若|一旦|在.{0,12}条件下|以.{0,12}为前提|前提是|除非")
SPEAKER = re.compile(r"^\s*([\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9·\.\-_]{1,11})\s*[:：]\s*")
SPK_INLINE = re.compile(r"([\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9·\.\-_]{1,7})[：:]")
NO_NAME = {"结论", "决定", "备注", "议题", "待办", "注意", "说明", "要点", "时间", "地点",
           "参会", "记录", "摘要", "原则", "口径", "结果", "问题", "原因", "方案", "风险",
           "下一步", "决议", "行动", "建议", "分工", "目标", "背景", "现状", "进展", "遗留",
           "主题", "事项", "会议", "内容", "目的", "范围", "版本", "日期", "负责人"}


def is_name(word):
    return bool(word) and word not in NO_NAME
OWNER_HINT = re.compile(r"([\u4e00-\u9fa5]{2,3}|[A-Z][a-z]{2,15})\s*(负责|跟进|来|牵头|owner)", re.I)


def log(msg):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(msg)


def die(code, msg, as_json=False):
    if as_json:
        log(json.dumps({"ok": False, "error_id": code, "error_msg": msg, "data": None},
                       ensure_ascii=False))
    else:
        log("[%s] %s" % (code, msg))
    sys.exit(1)


def read_any(path):
    """读 txt / md / docx（docx 用 zipfile + 正则取段落，不依赖 python-docx）。"""
    if not os.path.isfile(path):
        die("S001", "文件不存在：%s" % path)
    ext = os.path.splitext(path)[1].lower()
    if ext == ".docx":
        try:
            with zipfile.ZipFile(path) as z:
                xml = z.read("word/document.xml").decode("utf-8", "replace")
        except Exception as e:
            die("S002", "docx 解析失败：%s" % e)
        paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
        lines = []
        for p in paras:
            txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
            lines.append(txt)
        text = "\n".join(lines)
    elif ext in (".txt", ".md", ".markdown"):
        raw = open(path, "rb").read()
        text = None
        for enc in ("utf-8", "utf-8-sig", "gbk", "gb18030"):
            try:
                text = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        if text is None:
            die("S002", "编码无法识别（试过 utf-8/gbk/gb18030）")
    else:
        die("S004", "不支持的输入格式：%s（支持 .txt/.md/.docx）" % ext)
    if not text.strip():
        die("S003", "内容为空")
    return text


def sentences(text):
    """按中文标点/换行切句，保留原始顺序（用于逐句溯源）。"""
    parts = re.split(r"(?<=[。！？；\n])", text)
    return [p.strip() for p in parts if p and p.strip()]


def find_all(pattern, text):
    return [m.group(0) for m in re.finditer(pattern, text)]


def speaker_sentences(text):
    """返回 (说话人, 句子) 列表。说话人可出现在行首或句中「X：」，非人名词一律排除。
    Markdown 标题行不计入句子流（否则「# 需求评审会转写」会被当成待办）。"""
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        pos, cur = 0, None
        for m in SPK_INLINE.finditer(line):
            if not is_name(m.group(1)):
                continue
            seg = line[pos:m.start()].strip()
            if seg:
                for s in sentences(seg):
                    out.append((cur, s))
            cur = m.group(1)
            pos = m.end()
        seg = line[pos:].strip()
        if seg:
            for s in sentences(seg):
                out.append((cur, s))
    return out


def extract_facts(text):
    dates, nums, speakers = [], [], []
    for p in DATE_PATTERNS:
        dates += find_all(p, text)
    nums = find_all(NUM_PATTERN, text)
    for line in text.splitlines():
        m = SPEAKER.match(line)
        if m and is_name(m.group(1)):
            speakers.append(m.group(1))
    todos, decisions, conditions, owners = [], [], [], []
    SELF_CLAIM = re.compile(r"我来|我负责|我跟|由我|我出|我发|我接")
    for who, s in speaker_sentences(text):
        is_cond = bool(CONDITION.search(s))
        is_dec = bool(DECISION.search(s))
        if is_cond:
            conditions.append(s)
        if is_cond and not is_dec:
            # 条件句只归入「条件」区，不列成待办：把「如果超过 2% 就要回滚」列成任务会误导执行
            pass
        elif NEGOTIABLE.search(s) and not is_dec:
            # 已定结论不再重复列入待办表，避免同一句既当结论又当任务
            todos.append(s)
        if is_dec:
            decisions.append(s)
        for m in OWNER_HINT.finditer(s):
            if is_name(m.group(1)):
                owners.append(m.group(1))
        if who and SELF_CLAIM.search(s):
            owners.append(who)
    def uniq(seq):
        seen, out = set(), []
        for x in seq:
            if x and x not in seen:
                seen.add(x)
                out.append(x)
        return out
    decisions_graded = resolve_superseded(grade_decisions(decisions))
    commitments_graded = grade_commitments(todos)
    return {
        "chars": len(text),
        "lines": len([l for l in text.splitlines() if l.strip()]),
        "dates": uniq(dates),
        "numbers": uniq(nums),
        "speakers": uniq(speakers),
        "owners_hint": uniq(owners),
        "todo_sentences": uniq(todos),
        "decision_sentences": uniq(decisions),
        "condition_sentences": uniq(conditions),
        "decision_items": decisions_graded,
        "commitment_items": commitments_graded,
        "strength_summary": summarize_strength(decisions_graded, commitments_graded),
    }


# --- 结论强度 / 承诺强度分级（语义维度，可断言） ---
DECISION_FIRM = re.compile(r"决定|确定|定了|拍板|批准|同意|裁定|通过|结论是|已经定")
DECISION_PROVISIONAL = re.compile(r"暂定|暂时|临时|先按|初步|暂以|先这么")
DECISION_PROPOSAL = re.compile(r"建议|提议|可以考虑|要不|是不是可以|倾向")
DECISION_CONDITIONAL = re.compile(r"如果|若|一旦|前提是|除非|在.{0,12}条件下")

COMMIT_COMMITTED = re.compile(r"我来|我负责|我跟|由我|我出|我发|我接|我盯|交给我|我这边"
                              r"|由[\u4e00-\u9fa5A-Za-z]{1,8}(出|写|发|做|负责|跟进|主导)")
COMMIT_NAMED = re.compile(r"跟一下|对接|谁去|让.{1,8}来|需要.{1,8}确认|由.{1,8}负责|请.{1,8}支持")
COMMIT_INTENT = re.compile(r"我看看|我考虑|想想|再看|回头说|再说|有时间|尽量")
# 范围结束不等于未来任务（"本周不铺" ≠ "下周铺货待定"）
SCOPE_NEGATE = re.compile(r"(本|这|下)?周.{0,6}(不|暂不|先不|没有|不铺|不上|不做)"
                          r"|(本月|这个月).{0,6}(不|暂不|先不)"
                          r"|(这一段|现阶段|首发期).{0,6}(不|暂不|先不)")
# 部门/岗位责任不映射到个人
DEPT_WORDS = ("媒介", "运营", "产品", "研发", "市场", "销售", "法务", "财务", "客服",
              "设计", "技术", "供应链", "采购", "人事", "行政", "公关", "品牌")


def grade_decisions(sentences):
    """把决策句分成四档：conditional > provisional > proposal > firm（按语义特异性）"""
    out = []
    for s in sentences:
        if DECISION_CONDITIONAL.search(s):
            level, why = "conditional", "含条件触发词"
        elif DECISION_PROVISIONAL.search(s):
            level, why = "provisional", "含暂定/临时/先按"
        elif DECISION_PROPOSAL.search(s):
            level, why = "proposal", "含建议/提议/可以考虑"
        else:
            level, why = "firm", "含决定/确定/拍板/批准"
        out.append({"text": s, "strength": level, "evidence": why})
    return out


def grade_commitments(sentences):
    """把待办句分成三档：intent_only > named_unconfirmed > committed。

    两条硬规则（对齐成熟会议纪要工具的语义精度）：
      1. 范围结束不生成未来任务：「本周不铺」只说明本阶段不做，不得扩写成「下周铺货待定」；
      2. 部门责任不映射到个人：「媒介跟一下」责任落在部门，不指认具体人。
    """
    out = []
    for s in sentences:
        owner = "（部门）" if any(w in s for w in DEPT_WORDS) and not COMMIT_COMMITTED.search(s) else None
        if SCOPE_NEGATE.search(s):
            level, why = "unstated", "范围否定：本阶段不做，不生成未来任务"
        elif COMMIT_INTENT.search(s) and not COMMIT_COMMITTED.search(s):
            level, why = "intent_only", "仅表达意向（我看看/再说/尽量）"
        elif COMMIT_COMMITTED.search(s):
            level, why = "committed", "明确接活（我来/我负责/由我）"
        elif COMMIT_NAMED.search(s):
            level, why = "named_unconfirmed", "被点名但未明确确认"
        else:
            level, why = "unstated", "未标出责任人"
        item = {"text": s, "strength": level, "evidence": why}
        if owner and level in ("named_unconfirmed", "unstated"):
            item["owner_scope"] = owner
            item["evidence"] = why + "；责任止于部门，未指认个人"
        out.append(item)
    return out


def summarize_strength(decisions, commitments):
    d, c = {}, {}
    for it in decisions:
        d[it["strength"]] = d.get(it["strength"], 0) + 1
    for it in commitments:
        c[it["strength"]] = c.get(it["strength"], 0) + 1
    firm = d.get("firm", 0)
    soft = d.get("provisional", 0) + d.get("proposal", 0) + d.get("conditional", 0)
    commit = c.get("committed", 0)
    unconfirmed = c.get("named_unconfirmed", 0) + c.get("intent_only", 0) + c.get("unstated", 0)
    return {
        "decisions": d,
        "commitments": c,
        "firm_decisions": firm,
        "soft_decisions": soft,
        "committed_owners": commit,
        "unconfirmed_owners": unconfirmed,
        "verdict": "clean" if (soft == 0 and unconfirmed == 0) else "needs_confirmation",
    }


# ---------- P2: 后说覆盖前说（修正优先） ----------
NEGATE_PREV = re.compile(r"不是|不对|更正|说错|以.{0,8}为准|重新定|改成|改到|改为|调成")
ANCHOR_PATTERNS = [
    (r"\d{4}-\d{2}-\d{2}",),
    (r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*[日号]",),
    (r"\d{1,2}\s*月\s*\d{1,2}\s*[日号]",),
    (r"\d{1,2}\s*月",),
    (NUM_PATTERN,),
]


def anchors_of(text):
    out = []
    for p in ANCHOR_PATTERNS:
        out += find_all(p[0], text)
    return [a.replace(" ", "") for a in out if a.strip()]


def resolve_superseded(items):
    """后出现的显式修正覆盖前说：前句保留但标 superseded，不进入当前结论。
    判定依据：后句含否定/更正词，且提及前句的某个日期或数字锚。"""
    n = len(items)
    for j in range(n):
        later = items[j]["text"]
        if not NEGATE_PREV.search(later):
            continue
        for i in range(j):
            if items[i].get("superseded"):
                continue
            for a in anchors_of(items[i]["text"]):
                if a and a in later.replace(" ", ""):
                    items[i]["superseded"] = True
                    items[i]["superseded_by"] = j
                    break
    return items


# ---------- P1: 输入脱敏前置 ----------
REDACT_RULES = [
    ("phone", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), lambda m: m.group(0)[:3] + "****" + m.group(0)[-4:]),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})"),
     lambda m: m.group(0).split("@")[0][:1] + "***@" + m.group(1)),
    ("secret", re.compile(r"(?:sk|ghp|gho|xoxb|AKIA)[-_A-Za-z0-9]{12,}"), lambda m: m.group(0)[:4] + "***"),
    ("password", re.compile(r"(?:密码|口令|password|passwd)\s*[:：=]\s*\S+", re.I),
     lambda m: m.group(0).split(":")[0].split("：")[0].split("=")[0] + ":***"),
]


def redact_text(text, extra_terms=()):
    """返回 (脱敏文本, 报告)。默认脱敏手机号/邮箱/密钥/密码；extra_terms 逐词替换。"""
    clean = text
    report = {"counts": {}, "terms": list(extra_terms), "total": 0}
    for name, pat, repl in REDACT_RULES:
        hits = pat.findall(clean)
        if hits:
            clean = pat.sub(repl, clean)
            report["counts"][name] = len(hits)
            report["total"] += len(hits)
    for t in extra_terms:
        t = t.strip()
        if not t:
            continue
        cnt = clean.count(t)
        if cnt:
            clean = clean.replace(t, "〔已脱敏〕")
            report["counts"]["term:" + t] = cnt
            report["total"] += cnt
    return clean, report


# ---------- P1: facts.json 结构校验 ----------
STRENGTH_ENUM_D = {"firm", "provisional", "proposal", "conditional"}
STRENGTH_ENUM_C = {"committed", "named_unconfirmed", "intent_only", "unstated"}


def validate_facts(facts):
    problems = []
    need = ("chars", "lines", "dates", "numbers", "speakers", "todo_sentences",
            "decision_sentences", "condition_sentences", "decision_items",
            "commitment_items", "strength_summary")
    for k in need:
        if k not in facts:
            problems.append("缺字段 %s" % k)
    for k in ("dates", "numbers", "speakers", "todo_sentences", "decision_sentences"):
        if k in facts and not isinstance(facts[k], list):
            problems.append("%s 应为数组" % k)
    for it in facts.get("decision_items", []):
        if it.get("strength") not in STRENGTH_ENUM_D:
            problems.append("决策档位非法：%r" % it.get("strength"))
        if not it.get("text"):
            problems.append("决策条目缺 text")
    for it in facts.get("commitment_items", []):
        if it.get("strength") not in STRENGTH_ENUM_C:
            problems.append("承诺档位非法：%r" % it.get("strength"))
    ss = facts.get("strength_summary", {})
    if ss.get("verdict") not in ("clean", "needs_confirmation"):
        problems.append("verdict 非法：%r" % ss.get("verdict"))
    # 一致性：已定条数应等于 decisions 里 firm 的计数
    if isinstance(ss.get("decisions"), dict):
        cnt = sum(1 for it in facts.get("decision_items", []) if it.get("strength") == "firm")
        if ss["decisions"].get("firm", 0) != cnt:
            problems.append("firm 计数不一致：summary=%d, items=%d"
                            % (ss["decisions"].get("firm", 0), cnt))
    return {"verdict": "PASS" if not problems else "FAIL", "problems": problems}


SKELETONS = {
    "minutes": """# 纪要骨架（待填）

> 一句话总览：___

## 议题
{topics}

## 结论
{decisions}

## 待办
| 事项 | 责任人 | 期限 |
|---|---|---|
{todos}

## 强度判读
{strength_box}

## 待确认 / 原文未提及
{unknown}
""",
    "compare": """# 对比骨架（待填）

> 一句话总览：___

| 维度 | 对象 A | 对象 B |
|---|---|---|
| ___ | ___ | ___ |

> 只放原文事实，不写原文没有的优劣判断。
""",
    "timeline": """# 时间线骨架（待填）

{items}
""",
    "bullets": """# 要点骨架（待填）

{items}
""",
    "card": """# 卡片骨架（待填）

- 标题：___
- 一句话结论：___
- 关键字段 1：___
- 关键字段 2：___
- 关键字段 3：___
""",
}


def build_skeleton(fmt, facts):
    if fmt == "minutes":
        topics = "\n".join("- (待填) %s" % s[:40] for s in facts["speakers"][:6]) or "- (待填)"
        live = [it for it in facts["decision_items"] if not it.get("superseded")]
        dead = [it for it in facts["decision_items"] if it.get("superseded")]
        dec = "\n".join("- [%s] %s" % (it["strength"], it["text"])
                        for it in live[:8]) or "- 原文未提及"
        todo = "\n".join("| [%s] %s | %s | %s |" % (it["strength"], it["text"][:56], "待填", "原文未提及")
                         for it in facts["commitment_items"][:10]) or "| 原文未提及 | - | - |"
        sup = "\n".join("- （已作废，被后文修正）%s" % it["text"] for it in dead) or "- 无"
        ss = facts["strength_summary"]
        box = "\n".join([
            "- 已定（firm）%d 条；暂定/提案/条件（soft）%d 条" % (ss["firm_decisions"], ss["soft_decisions"]),
            "- 明确接活（committed）%d 条；被点名未确认或仅表意向 %d 条" % (ss["committed_owners"], ss["unconfirmed_owners"]),
            "- 判读：%s" % ("全部为已定且责任明确" if ss["verdict"] == "clean"
                          else "存在未定项或未确认责任，需在会后确认后再对外发布"),
        ])
        unknown = "- 责任人/期限未在原文出现的，已标「原文未提及」，不补全"
        body = SKELETONS[fmt].format(topics=topics, decisions=dec, todos=todo,
                                     strength_box=box, unknown=unknown)
        return body.replace("## 待确认 / 原文未提及",
                            "## 已被后文修正（不作当前结论）\n%s\n\n## 待确认 / 原文未提及" % sup, 1)
    if fmt == "timeline":
        items = "\n".join("%d. %s（日期待核对）" % (i + 1, d) for i, d in enumerate(facts["dates"][:12]))
        return SKELETONS[fmt].format(items=items or "1. (待填)")
    if fmt == "bullets":
        items = "\n".join("%d. %s" % (i + 1, s) for i, s in enumerate(facts["decision_sentences"][:5]))
        if not items:
            items = "\n".join("%d. %s" % (i + 1, s[:80]) for i, s in enumerate(facts["todo_sentences"][:5]))
        return SKELETONS[fmt].format(items=items or "1. (待填)")
    return SKELETONS[fmt]


# ---------- 溯源校验 ----------
def fact_tokens(text):
    toks = []
    for p in DATE_PATTERNS:
        toks += find_all(p, text)
    toks += [n for n in find_all(NUM_PATTERN, text) if len(n) >= 2]
    return toks


def norm(t):
    """只归一化格式差异（空白、日期「日/号」写法），不做任何数值或语义归一。"""
    return re.sub(r"\s+", "", t).replace("日", "号")


def citecheck(output_text, source_text):
    src_norm = norm(source_text)
    missing = []
    checked = 0
    for s in sentences(output_text):
        if re.match(r"^\|[\s:\-|]+\|$", s):
            continue
        toks = fact_tokens(s)
        for t in toks:
            checked += 1
            if norm(t) not in src_norm:
                missing.append({"token": t, "sentence": s[:90]})
    return {"checked": checked, "missing": missing,
            "verdict": "PASS" if not missing else "FAIL"}


# ---------- 结构自检 ----------
def selfcheck(output_text, fmt):
    problems = []
    if fmt == "minutes":
        for need in ("## 议题", "## 结论", "## 待办", "## 待确认", "## 强度判读"):
            if need not in output_text:
                problems.append("缺少区块 %s" % need)
        if "| 事项 | 责任人 | 期限 |" not in output_text:
            problems.append("待办表缺表头（应为 事项/责任人/期限）")
        # 强度标注是 v2.0.2 起的强制项：结论与待办都必须带语义档位
        # （区块内确无内容、已标「原文未提及」时不强制，避免对空结论误报）
        dec_block = output_text.split("## 结论", 1)[-1].split("## 待办", 1)[0]
        if "原文未提及" not in dec_block and not re.search(
                r"\[(firm|provisional|proposal|conditional)\]", dec_block):
            problems.append("结论未标注语义档位（firm/provisional/proposal/conditional）")
        todo_block = output_text.split("## 待办", 1)[-1].split("## 强度判读", 1)[0]
        if "原文未提及" not in todo_block and not re.search(
                r"\[(committed|named_unconfirmed|intent_only|unstated)\]", todo_block):
            problems.append("待办未标注承诺状态（committed/named_unconfirmed/intent_only）")
    elif fmt == "compare":
        if output_text.count("|") < 4:
            problems.append("对比表结构不完整（需维度×对象两列以上）")
    elif fmt == "timeline":
        if not re.search(r"^\d+\.\s", output_text, re.M):
            problems.append("时间线需一行一事（数字编号行）")
    elif fmt == "bullets":
        n = len(re.findall(r"^\d+\.\s", output_text, re.M))
        if not (3 <= n <= 7):
            problems.append("要点族要求 3–7 条，实测 %d 条" % n)
    elif fmt == "card":
        for need in ("标题", "一句话结论"):
            if need not in output_text:
                problems.append("卡片缺字段：%s" % need)
    return {"verdict": "PASS" if not problems else "FAIL", "problems": problems}


# ---------- P1: 日期归一（追加锚点，不替换原文，证据链不断） ----------
WEEK_CN = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6,
           "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6}


def _iso(d):
    return d.strftime("%Y-%m-%d")


def _monday(ref):
    from datetime import timedelta
    return ref - timedelta(days=ref.weekday())


def norm_dates(text, ref_str=None):
    """把相对日期追加 ISO 锚点。返回 (新文本, 归一清单)。原文一字不改。"""
    from datetime import date, timedelta
    try:
        ref = date.fromisoformat(ref_str) if ref_str else date.today()
    except ValueError:
        ref = date.today()
    hits = []

    def already(m):
        # 该词后面已紧跟括号锚点则不重复追加
        return m.string[m.end():m.end() + 1] == "（"

    def sub(pat, fn, txt):
        def cb(m):
            if already(m):
                return m.group(0)
            d = fn(m)
            if d is None:
                return m.group(0)
            hits.append({"raw": m.group(0), "iso": _iso(d)})
            return "%s（%s）" % (m.group(0), _iso(d))
        return pat.sub(cb, txt)

    # 下周X / 本周X
    def wk(m):
        wd = WEEK_CN.get(m.group(2))
        if wd is None:
            return None
        base = _monday(ref)
        return base + timedelta(days=(7 if m.group(1).startswith("下") else 0) + wd)

    text = sub(re.compile(r"(下下周|下周|下星期|本周|这周|本星期)\s*([一二三四五六日天1-7])"), wk, text)

    # 今天 / 明天 / 后天
    def rel(m):
        return ref + timedelta(days={"今天": 0, "今日": 0, "明天": 1, "明日": 1, "后天": 2}[m.group(0)])

    text = sub(re.compile(r"今天|今日|明天|明日|后天"), rel, text)

    # 月底
    def endmonth(m):
        nxt = (ref.replace(day=28) + timedelta(days=4))
        return nxt - timedelta(days=nxt.day)

    text = sub(re.compile(r"本月底|月底"), endmonth, text)

    # 下个月N号
    def nextmonth(m):
        y, mo = ref.year, ref.month + 1
        if mo > 12:
            y, mo = y + 1, 1
        return date(y, mo, int(m.group(1)))

    text = sub(re.compile(r"下个?月\s*(\d{1,2})\s*[日号]"), nextmonth, text)

    # N月N号（同一年；若原文另写了年份则不动）
    def thisyear(m):
        pre = m.string[max(0, m.start() - 8):m.start()]
        if re.search(r"(\d{4}\s*年\s*)$", pre) or re.search(r"(\d{4}-)$", pre):
            return None
        try:
            return date(ref.year, int(m.group(1)), int(m.group(2)))
        except ValueError:
            return None

    text = sub(re.compile(r"(\d{1,2})\s*月\s*(\d{1,2})\s*[日号]"), thisyear, text)

    return text, {"ref": _iso(ref), "count": len(hits), "items": hits}


# ---------- P1: 中性措辞模式（敏感场景不强化负面表述） ----------
NEUTRAL_GROUPS = {
    "personnel": ["裁员", "裁掉", "开除", "辞退", "优化掉", "末位淘汰", "劝退"],
    "performance": ["绩效不合格", "评级垫底", "能力不行", "拖后腿"],
    "medical": ["诊断", "病情", "用药", "病历", "症状"],
    "legal": ["诉讼", "起诉", "违约", "赔偿", "仲裁", "追责"],
    "incident": ["事故", "伤亡", "泄漏", "宕机", "数据丢失", "重大故障"],
}
NEUTRAL_SUGGEST = {
    "裁员": "岗位调整（涉及劳动关系，须经法务确认后表述）",
    "开除": "解除劳动关系（须经法务确认）",
    "辞退": "解除劳动关系（须经法务确认）",
    "劝退": "岗位调整沟通（须经法务确认）",
    "末位淘汰": "绩效改进流程",
    "优化掉": "岗位调整",
    "裁掉": "岗位调整",
    "绩效不合格": "绩效未达预期（按流程记录）",
    "评级垫底": "绩效排名靠后（按流程记录）",
    "能力不行": "当前能力与岗位要求存在差距",
    "拖后腿": "进度受影响",
    "诊断": "医学判断（须由执业医师出具）",
    "病情": "健康状况",
    "用药": "治疗方案",
    "病历": "诊疗记录",
    "症状": "身体表现",
    "诉讼": "法律程序",
    "起诉": "提起法律程序",
    "违约": "合同履行争议",
    "赔偿": "责任承担",
    "仲裁": "争议解决程序",
    "追责": "责任认定",
    "事故": "安全事件",
    "伤亡": "人员伤害情况",
    "泄漏": "信息外泄事件",
    "宕机": "服务中断",
    "数据丢失": "数据完整性受损",
    "重大故障": "重大服务异常",
}


def neutral_scan(text):
    hits = []
    for g, words in NEUTRAL_GROUPS.items():
        for w in words:
            if w in text:
                hits.append({"group": g, "word": w, "suggest": NEUTRAL_SUGGEST.get(w)})
    return {
        "neutral_language_mode": bool(hits),
        "hits": hits,
        "rule": ("命中敏感场景时，对外版本改用中性表述，不评价个人、不强化负面定性；"
                 "本工具只给建议措辞，不自动改写原文（改写须人工确认）。"),
    }


# ---------- P1: 确定性渲染（四视图，首屏每区最多 3 条） ----------
def _split(facts):
    live = [it for it in facts.get("decision_items", []) if not it.get("superseded")]
    firm = [it for it in live if it.get("strength") == "firm"]
    soft = [it for it in live if it.get("strength") != "firm"]
    com = [it for it in facts.get("commitment_items", []) if it.get("strength") == "committed"]
    unc = [it for it in facts.get("commitment_items", []) if it.get("strength") != "committed"]
    return firm, soft, com, unc


def _top(items, n=3):
    return items[:n], max(0, len(items) - n)


def render_view(facts, view="receipt"):
    firm, soft, com, unc = _split(facts)
    ss = facts.get("strength_summary", {})

    def block(items, with_evidence=True):
        out = []
        for it in items[:3]:
            line = "- [%s] %s" % (it.get("strength", "?"), it.get("text", "")[:90])
            if with_evidence:
                line += "\n  · 原句：「%s」" % it.get("text", "")[:60]
            out.append(line)
        rest = len(items) - len(items[:3])
        if rest > 0:
            out.append("- 另有 %d 项，见 facts.json（本节只显示前 3 条）" % rest)
        return "\n".join(out) or "- 原文未提及"

    if view == "executive":
        src = " ".join(
            facts.get("decision_sentences", []) + facts.get("todo_sentences", [])
            + [it.get("text", "") for it in facts.get("decision_items", [])]
            + [it.get("text", "") for it in facts.get("commitment_items", [])])
        nr = neutral_scan(src)
        warn = ""
        if nr["neutral_language_mode"]:
            warn = ("\n> 敏感场景提示：本场命中 %s。对外版本请改用中性表述（如「%s」），"
                    "不评价个人、不强化负面定性。\n"
                    % ("、".join(h["word"] for h in nr["hits"][:5]),
                       nr["hits"][0]["suggest"] if nr["hits"] else "责任确认"))
        firm_block = block(firm, with_evidence=False) if firm else \
            "- 本场无已定（firm）结论，仅有暂定/提案项（见待协调）"
        body = "\n".join([
            "# 管理层纪要（当前有效结论）",
            warn,
            "**结论**",
            firm_block,
            "",
            "**已确认责任**",
            block(com, with_evidence=False) if com else "- 原文未观察到明确接活",
            "",
            "**待协调 / 确认权缺口**",
            block(soft + unc, with_evidence=False),
            "",
            "**下个节点**",
            "- %s" % ("、".join(facts.get("dates", [])[:3]) or "原文未提及"),
            "",
            "> 本版不含直接引文，便于对外；如需追溯，请查 receipt 视图与 facts.json。",
        ])
        return body

    if view == "personal":
        body = "\n".join([
            "# 自用执行纪要",
            "",
            "**已定（firm）**",
            block(firm),
            "",
            "**未定 / 暂定（soft）**",
            block(soft),
            "",
            "**明确接活（committed）**",
            block(com),
            "",
            "**被点名未确认 / 仅表意向**",
            block(unc),
            "",
            "**会后确认消息（可直接发群）**",
            "> 刚才会上确认的事项已整理：%s。未确认的 %d 项请今日回复是否承接。"
            % ("；".join(i.get("text", "")[:40] for i in firm[:2]) or "（待补）", len(unc)),
        ])
        return body

    if view == "receipt":
        body = "\n".join([
            "# 验收回执（receipt）",
            "",
            "**当前有效结论（firm）**",
            block(firm),
            "",
            "**未定 / 暂定（soft）**",
            block(soft),
            "",
            "**明确接活（committed）**",
            block(com),
            "",
            "**被点名未确认 / 仅表意向**",
            block(unc),
            "",
            "**判读**：%s（附原文，任何一条都能回原文核对）"
            % ("全部已定且责任明确" if ss.get("verdict") == "clean"
               else "存在未定项或未确认责任，不可直接对外发布"),
        ])
        return body

    raise ValueError("unknown view")


def render_bundle(facts):
    return {"receipt": render_view(facts, "receipt"),
            "personal": render_view(facts, "personal"),
            "executive": render_view(facts, "executive")}


# ---------- P1: 来源适配（多平台输入识别与预处理建议） ----------
SRC_HINTS = [
    ("tencent_meeting",
     [r"腾讯会议", r"会议主题\s*[:：]", r"参会人\s*[:：]", r".{2,8}的发言"],
     "腾讯会议导出：保留「XX 的发言」前缀与时间戳，两者都是证据锚点，不要删。",
     "python scripts/summarize_pro.py extract --file <本文件> --format minutes"),
    ("feishu_minutes",
     [r"妙记", r"\[\d{1,2}:\d{2}(?::\d{2})?\]", r"发言人\s*\d+"],
     "飞书妙记：[hh:mm:ss] 是证据锚点，保留不删；发言人未知的用「发言人 N」，不要猜姓名。",
     "python scripts/summarize_pro.py extract --file <本文件> --format minutes"),
    ("kimi_work",
     [r"Kimi\s*Work", r"\*\*说话人\*\*", r"对话记录"],
     "Kimi Work：说话人与内容分列，先按行合并成「人：话」再抽取。",
     "python scripts/summarize_pro.py extract --file <本文件> --format minutes"),
    ("workbuddy",
     [r"WorkBuddy", r"##\s*会议纪要", r"##\s*决议"],
     "WorkBuddy：已是纪要结构，直接用 citecheck 核对，不要再次 extract（会重复压缩）。",
     "python scripts/summarize_pro.py citecheck --file <本文件> --source <原始转写>"),
    ("docx",
     [r"^[\s\S]*$"],
     "Word 文档：段落已抽取；表格内容不在段落里，若有表格请另存为 md。",
     "python scripts/summarize_pro.py extract --file <本文件> --format minutes"),
]


def normalize_source(text, source):
    """把平台特有版式折成「人：话」一行一句，供抽取使用。"""
    if source == "tencent_meeting":
        text = re.sub(r"(?m)^\s*([^\s:：]{2,10})\s*的发言\s*[\d:]*\s*$", r"\1：", text)
    elif source == "feishu_minutes":
        text = re.sub(r"(?m)^\s*\[[\d:]+\]\s*(发言人\s*\d+)\s*[:：]?\s*$", r"\1：", text)
        text = re.sub(r"(?m)^\s*\[[\d:]+\]\s*", "", text)
    elif source == "kimi_work":
        text = re.sub(r"(?m)^\s*\*\*(.+?)\*\*\s*$", r"\1：", text)
    # 统一把「人：」独占的行与下一行合并成一句（否则主语与内容分家，待办判不出来）
    text = re.sub(r"(?m)^([^\s#\-*>|][^:：\n]{0,11}[：:])\s*\n(?=\S)", r"\1", text)
    return text


def adapt_detect(path, text):
    ext = os.path.splitext(path)[1].lower()
    hits, best = [], None
    for name, pats, advice, cmd in SRC_HINTS:
        if name == "docx":
            if ext == ".docx":
                best = (name, advice, cmd, ["扩展名 .docx"])
            continue
        matched = [p for p in pats if re.search(p, text)]
        if matched:
            hits.append({"source": name, "signals": [m[:28] for m in matched],
                         "advice": advice, "suggest": cmd})
    if best:
        hits.insert(0, {"source": best[0], "signals": best[3],
                        "advice": best[1], "suggest": best[2]})
    if not hits:
        hits.append({"source": "plain_text",
                     "signals": ["未识别到平台特征"],
                     "advice": "按纯文本处理；若为粘贴内容，先确认说话人前缀是否齐全。",
                     "suggest": "python scripts/summarize_pro.py extract --file <本文件> --format minutes"})
    return {"path": path, "chars": len(text),
            "speaker_lines": len(re.findall(r"(?m)^\S{1,12}\s*[:：]", text)),
            "timestamp_lines": len(re.findall(r"(?m)[\[\(]?\d{1,2}:\d{2}(?::\d{2})?[\]\)]?", text)),
            "candidates": hits,
            "normalized": {}}


# ---------- P1: Markdown → 自包含 HTML（零依赖，打印/粘贴友好） ----------
HTML_CSS = """
body{max-width:820px;margin:40px auto;padding:0 20px;color:#1a2330;
font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;line-height:1.75;font-size:15px}
h1{font-size:22px;border-bottom:2px solid #0f766e;padding-bottom:8px}
h2,h3{font-size:17px;margin-top:26px}
strong{color:#0f766e}
blockquote{margin:16px 0;padding:10px 16px;background:#f2f7f6;border-left:3px solid #0f766e;
color:#3d4a5a}
li{margin:4px 0}
code{background:#f1f3f5;padding:1px 4px;border-radius:3px;font-size:13px}
"""


def md_to_html(md, title="纪要"):
    esc = lambda s: (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    out, in_list = [], False
    for line in md.splitlines():
        s = line.rstrip()
        if not s.strip():
            if in_list:
                out.append("</ul>")
                in_list = False
            continue
        if s.startswith("# "):
            if in_list:
                out.append("</ul>"); in_list = False
            out.append("<h1>%s</h1>" % esc(s[2:]))
        elif s.startswith("## "):
            out.append("<h2>%s</h2>" % esc(s[3:]))
        elif s.startswith("### "):
            out.append("<h3>%s</h3>" % esc(s[4:]))
        elif s.startswith("> "):
            if in_list:
                out.append("</ul>"); in_list = False
            out.append("<blockquote>%s</blockquote>" % esc(s[2:]))
        elif s.startswith("- "):
            if not in_list:
                out.append("<ul>"); in_list = True
            body = esc(s[2:])
            body = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", body)
            out.append("<li>%s</li>" % body)
        else:
            if in_list:
                out.append("</ul>"); in_list = False
            body = esc(s)
            body = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", body)
            body = re.sub(r"`(.+?)`", r"<code>\1</code>", body)
            out.append("<p>%s</p>" % body)
    if in_list:
        out.append("</ul>")
    return ("<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
            "<title>%s</title><style>%s</style></head><body>\n%s\n</body></html>"
            % (esc(title), HTML_CSS, "\n".join(out)))


def main():
    ap = argparse.ArgumentParser(description="summarize-pro 本地工具链（零依赖）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="抽取事实线索并生成骨架")
    e.add_argument("--file", required=True)
    e.add_argument("--format", default="minutes", choices=FORMATS)
    e.add_argument("--out", default=".")
    e.add_argument("--json", action="store_true")

    c = sub.add_parser("citecheck", help="输出逐句回原文溯源")
    c.add_argument("--file", required=True, help="待核对输出")
    c.add_argument("--source", required=True, help="原文")
    c.add_argument("--json", action="store_true")

    s = sub.add_parser("selfcheck", help="格式族结构自检")
    s.add_argument("--file", required=True)
    s.add_argument("--format", default="minutes", choices=FORMATS)
    s.add_argument("--json", action="store_true")

    r = sub.add_parser("redact", help="输入脱敏（手机号/邮箱/密钥/密码/自定义词项）")
    r.add_argument("--file", required=True)
    r.add_argument("--out", required=True, help="脱敏后的文本路径")
    r.add_argument("--report", default=None, help="脱敏报告 JSON 路径（可选）")
    r.add_argument("--term", action="append", default=[], help="追加需脱敏的词项，可多次")
    r.add_argument("--json", action="store_true")

    v = sub.add_parser("validate", help="facts.json 结构校验")
    v.add_argument("--facts", required=True, help="extract 产出的 facts.json")
    v.add_argument("--json", action="store_true")

    n = sub.add_parser("normdates", help="相对日期归一（追加 ISO 锚点，不改原文）")
    n.add_argument("--file", required=True)
    n.add_argument("--out", default=None, help="归一后文本路径（默认覆盖 --file 旁边 .norm.md）")
    n.add_argument("--ref", default=None, help="参考日期 YYYY-MM-DD，默认今天")
    n.add_argument("--json", action="store_true")

    x = sub.add_parser("neutral", help="敏感场景中性措辞检测")
    x.add_argument("--file", required=True)
    x.add_argument("--json", action="store_true")

    rn = sub.add_parser("render", help="facts.json 确定性渲染（receipt/personal/executive/bundle）")
    rn.add_argument("--facts", required=True)
    rn.add_argument("--view", default="receipt",
                    choices=("receipt", "personal", "executive", "bundle"))
    rn.add_argument("--out", default=".", help="输出目录")
    rn.add_argument("--format", default="md", choices=("md", "txt", "html"))
    rn.add_argument("--json", action="store_true")

    ad = sub.add_parser("adapt", help="识别输入来源（腾讯会议/飞书妙记/Kimi/WorkBuddy/docx/纯文本）")
    ad.add_argument("--file", required=True)
    ad.add_argument("--normalize", action="store_true", help="写出规范化文本（人：话）")
    ad.add_argument("--out", default=None, help="规范化文本输出路径")
    ad.add_argument("--json", action="store_true")

    a = ap.parse_args()
    as_json = getattr(a, "json", False)

    if a.cmd == "extract":
        text = read_any(a.file)
        if len(text.strip()) < 50:
            die("S006", "原文仅 %d 字，按边界规则不套格式族（请直接一句话总览）" % len(text.strip()), as_json)
        facts = extract_facts(text)
        body = build_skeleton(a.format, facts)
        try:
            os.makedirs(a.out, exist_ok=True)
            stem = os.path.splitext(os.path.basename(a.file))[0]
            md_path = os.path.join(a.out, "%s.%s.md" % (stem, a.format))
            json_path = os.path.join(a.out, "%s.facts.json" % stem)
            open(md_path, "w", encoding="utf-8").write(body)
            open(json_path, "w", encoding="utf-8").write(
                json.dumps(facts, ensure_ascii=False, indent=1))
        except OSError as ex:
            die("S005", "输出目录不可写：%s" % ex, as_json)
        data = {"format": a.format, "chars": facts["chars"],
                "dates": len(facts["dates"]), "numbers": len(facts["numbers"]),
                "speakers": len(facts["speakers"]),
                "todo_sentences": len(facts["todo_sentences"]),
                "decision_sentences": len(facts["decision_sentences"]),
                "out_md": md_path, "out_json": json_path}
        if as_json:
            log(json.dumps({"ok": True, "error_id": None, "data": data}, ensure_ascii=False))
        else:
            log("已生成 %s\n事实线索：日期 %d / 数字 %d / 说话人 %d / 待办句 %d / 决策句 %d"
                % (md_path, data["dates"], data["numbers"], data["speakers"],
                   data["todo_sentences"], data["decision_sentences"]))
            log("说明：本工具只做抽取与骨架，语义总结由 Agent 完成。")

    elif a.cmd == "citecheck":
        out_text = read_any(a.file)
        src_text = read_any(a.source)
        r = citecheck(out_text, src_text)
        if as_json:
            log(json.dumps({"ok": True, "error_id": None, "data": r}, ensure_ascii=False))
        else:
            log("核对事实 token：%d 个；不可溯源：%d 个；判定：%s"
                % (r["checked"], len(r["missing"]), r["verdict"]))
            for m in r["missing"][:20]:
                log("  ✗ %s  ←  %s" % (m["token"], m["sentence"]))
        sys.exit(0 if r["verdict"] == "PASS" else 1)

    elif a.cmd == "redact":
        text = read_any(a.file)
        clean, rep = redact_text(text, a.term)
        try:
            with open(a.out, "w", encoding="utf-8") as f:
                f.write(clean)
            if a.report:
                with open(a.report, "w", encoding="utf-8") as f:
                    f.write(json.dumps(rep, ensure_ascii=False, indent=1))
        except OSError as ex:
            die("S005", "输出不可写：%s" % ex, as_json)
        if as_json:
            log(json.dumps({"ok": True, "error_id": None,
                            "data": {"out": a.out, "report": a.report,
                                     "redacted_total": rep["total"],
                                     "counts": rep["counts"]}}, ensure_ascii=False))
        else:
            log("脱敏完成：共 %d 处 → %s" % (rep["total"], a.out))
            for k, n in rep["counts"].items():
                log("  %s: %d" % (k, n))
        # 未检出任何敏感项时，明确说明「本文件本来就没有」，避免误以为已处理
        if rep["total"] == 0:
            log("说明：本文件未检出手机号/邮箱/密钥/密码，未做替换。")

    elif a.cmd == "validate":
        with open(a.facts, encoding="utf-8") as f:
            facts = json.load(f)
        res = validate_facts(facts)
        if as_json:
            log(json.dumps({"ok": True, "error_id": None, "data": res}, ensure_ascii=False))
        else:
            log("facts.json 结构校验：%s" % res["verdict"])
            for p in res["problems"]:
                log("  ✗ %s" % p)
        sys.exit(0 if res["verdict"] == "PASS" else 1)

    elif a.cmd == "normdates":
        text = read_any(a.file)
        new_text, rep = norm_dates(text, a.ref)
        out = a.out or (os.path.splitext(a.file)[0] + ".norm.md")
        try:
            with open(out, "w", encoding="utf-8") as f:
                f.write(new_text)
        except OSError as ex:
            die("S005", "输出不可写：%s" % ex, as_json)
        if as_json:
            log(json.dumps({"ok": True, "error_id": None,
                            "data": dict(rep, out=out)}, ensure_ascii=False))
        else:
            log("日期归一：%d 处 → %s（原文未改，仅追加括注）" % (rep["count"], out))
            for it in rep["items"][:10]:
                log("  %s → %s" % (it["raw"], it["iso"]))

    elif a.cmd == "neutral":
        text = read_any(a.file)
        res = neutral_scan(text)
        if as_json:
            log(json.dumps({"ok": True, "error_id": None, "data": res}, ensure_ascii=False))
        else:
            log("中性措辞模式：%s" % ("需启用" if res["neutral_language_mode"] else "未命中敏感场景"))
            for h in res["hits"][:10]:
                log("  ✗ %s（%s）→ 建议：%s" % (h["word"], h["group"], h["suggest"]))

    elif a.cmd == "adapt":
        text = read_any(a.file)
        res = adapt_detect(a.file, text)
        src = res["candidates"][0]["source"]
        norm = normalize_source(text, src)
        res["normalized"]["speaker_lines"] = len(re.findall(r"(?m)^\S{1,12}\s*[:：]", norm))
        res["normalized"]["chars"] = len(norm)
        if getattr(a, "normalize", False):
            out = a.out or (os.path.splitext(a.file)[0] + ".norm.md")
            with open(out, "w", encoding="utf-8") as f:
                f.write(norm)
            res["normalized"]["out"] = out
        if as_json:
            log(json.dumps({"ok": True, "error_id": None, "data": res}, ensure_ascii=False))
        else:
            log("来源识别：%s（%d 字，说话人行 %d，时间戳行 %d）"
                % (src, res["chars"], res["speaker_lines"], res["timestamp_lines"]))
            for c in res["candidates"]:
                log("  · %s  信号=%s" % (c["source"], "、".join(c["signals"])))
                log("    建议：%s" % c["advice"])
                log("    下一步：%s" % c["suggest"])
            log("  规范化后说话人行：%d" % res["normalized"]["speaker_lines"])
            if res["normalized"].get("out"):
                log("  已写出规范化文本：%s" % res["normalized"]["out"])

    elif a.cmd == "render":
        with open(a.facts, encoding="utf-8") as f:
            facts = json.load(f)
        views = (render_bundle(facts) if a.view == "bundle"
                 else {a.view: render_view(facts, a.view)})
        paths = {}
        try:
            os.makedirs(a.out, exist_ok=True)
            stem = os.path.splitext(os.path.basename(a.facts))[0].replace(".facts", "")
            for name, body in views.items():
                p = os.path.join(a.out, "%s.%s.%s" % (stem, name, a.format))
                out_body = md_to_html(body, title="%s.%s" % (stem, name)) if a.format == "html" else body
                with open(p, "w", encoding="utf-8") as f:
                    f.write(out_body)
                paths[name] = p
        except OSError as ex:
            die("S005", "输出目录不可写：%s" % ex, as_json)
        if as_json:
            log(json.dumps({"ok": True, "error_id": None,
                            "data": {"view": a.view, "paths": paths}}, ensure_ascii=False))
        else:
            log("渲染完成（%s）：" % a.view)
            for k, p in paths.items():
                log("  %-10s %s" % (k, p))

    else:
        if as_json:
            log(json.dumps({"ok": True, "error_id": None, "data": r}, ensure_ascii=False))
        else:
            log("结构自检（%s）：%s" % (a.format, r["verdict"]))
            for p in r["problems"]:
                log("  ✗ %s" % p)
        sys.exit(0 if r["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
