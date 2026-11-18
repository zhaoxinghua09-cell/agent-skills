#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LGD 技能评测引擎（零依赖）。

对任意 SKILL.md 技能包做 6 维评分，输出可复跑的分数、整改清单与复测命令。
设计原则：每一维都必须能指向具体文件与具体行，不做印象打分。

用法：
    python review.py <skill_dir>            # 人读报告
    python review.py <skill_dir> --json     # 机读结果（ok/error_id/data）
    python review.py <skill_dir> --run      # 额外尝试跑 tests/run_*.py 验证可复跑

退出码：0 全部维度达标（≥60 且无阻断项）；1 有阻断项；2 参数错误。
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import OrderedDict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 维度权重（合计 100）
WEIGHTS = OrderedDict([
    ("structure", 20),      # 结构与元数据完整
    ("consistency", 25),    # 声明与实现一致（行业通病，权重最高）
    ("reproducible", 20),   # 可复跑证据
    ("hygiene", 15),        # 去敏与安全
    ("discoverable", 15),   # AI 可发现性
    ("licensing", 5),       # 许可与署名
])

BLOCKING = {
    # 任一命中即为阻断项（总分再高也不给"可发"
    "declared_command_missing": "声明了不存在的命令/参数（体系最忌讳：声明与实现不符）",
    "secret_leak": "包内含明文密钥或真实个人敏感信息",
    "no_skill_md": "缺少 SKILL.md",
}

SENSITIVE = [
    (r"sk-[A-Za-z0-9]{16,}", "疑似 API Key"),
    (r"(?<!\d)1[3-9]\d{9}(?!\d)", "疑似手机号"),
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|cn|org|net)", "疑似真实邮箱"),
    (r"[A-Za-z]:\\Users\\[^\\<\s]{2,}", "本机绝对路径"),
]


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def frontmatter(skill_md):
    """极简 YAML frontmatter 解析（零依赖，只取顶层 key: value 与列表）。"""
    m = re.match(r"^---\n(.*?)\n---", skill_md, re.S)
    if not m:
        return {}
    body = m.group(1)
    fm, key, buf = {}, None, []
    for line in body.splitlines():
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s*", line):
            if key:
                fm[key] = "\n".join(buf).strip()
            key, val = line.split(":", 1)
            buf = [val.strip()]
        elif line.strip().startswith("-") and key:
            buf.append(line.strip())
        elif key:
            buf.append(line.strip())
    if key:
        fm[key] = "\n".join(buf).strip()
    # 去包裹引号：别人常写 version: "2.3.1"，不去引号会被误判为非 SemVer
    for k, v in list(fm.items()):
        if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
            fm[k] = v[1:-1].strip()
    return fm


def walk(root):
    out = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in (".git", "__pycache__")]
        for fn in fns:
            out.append(os.path.join(dp, fn))
    return out


def scripts_text(root):
    parts = []
    for p in walk(root):
        if p.endswith(".py"):
            parts.append(read(p))
    return "\n".join(parts)


# ---------------- 各维度 ----------------

def d_structure(root, fm, files):
    got, notes = 0, []
    req = ["name", "description", "version"]
    miss = [k for k in req if not fm.get(k)]
    if miss:
        notes.append("frontmatter 缺 %s" % "、".join(miss))
    else:
        got += 6
    if not re.match(r"^\d+\.\d+\.\d+$", str(fm.get("version", ""))):
        notes.append("version 不是 SemVer：%r" % fm.get("version"))
    else:
        got += 4
    depth_bad = [os.path.relpath(p, root) for p in files
                 if len(os.path.relpath(p, root).split(os.sep)) > 3]
    if depth_bad:
        notes.append("层级 >3 段：%s" % depth_bad[0])
    else:
        got += 4
    if any(p.endswith((".pyc", ".zip")) or "__pycache__" in p for p in files):
        notes.append("含 junk 文件（.pyc/.zip/__pycache__）")
    else:
        got += 3
    if fm.get("displayName") or fm.get("display_name") or fm.get("name"):
        got += 3
    else:
        notes.append("缺展示名")
    return got, notes


def d_consistency(root, fm, files):
    """最狠的一维：description 里提到的 --flag / 子命令，脚本里到底有没有。"""
    got, notes, blocking = 0, [], []
    desc = " ".join(str(fm.get(k, "")) for k in ("description", "description_en", "description_zh"))
    skill_md = read(os.path.join(root, "SKILL.md"))
    # 只在「真正给出的命令行」里取参数声明；正文里举例讲别人的缺陷（如 --draft）不算我们的承诺
    cmd_lines = [l for l in skill_md.splitlines() if re.search(r"python[3]?\s+\S+\.py", l)]
    declared_flags = set()
    for l in cmd_lines:
        declared_flags |= set(re.findall(r"--[a-z][a-z0-9\-]{1,20}", l))
    declared_cmds = set()
    for l in cmd_lines:
        m = re.search(r"\.py\s+([a-z][a-z0-9_\-]{1,20})", l)
        if m:
            declared_cmds.add(m.group(1))

    have_flags = set(re.findall(r'add_argument\(\s*"--([a-z0-9\-]+)', scripts_text(root)))
    have_flags = {"--" + f for f in have_flags}
    have_cmds = set(re.findall(r'add_parser\(\s*"([a-z0-9_\-]+)', scripts_text(root)))

    # 只校验「我们的脚本」承诺的 flag，避免把目标平台自身的 CLI 参数误判为我们的声明
    ours = {f for f in declared_flags if f in have_flags}
    unknown = {f for f in declared_flags
               if f not in have_flags and re.search(r"我们的?工具|本技能提供|子命令|脚本支持", skill_md)}
    if have_flags:
        got += 10
        missing = unknown - have_flags
        if missing:
            for f in sorted(missing)[:5]:
                notes.append("声明了未实现的参数 %s" % f)
                blocking.append("declared_command_missing:%s" % f)
        else:
            got += 5
    else:
        notes.append("未检出任何脚本参数声明（如无脚本可忽略）")

    if have_cmds:
        got += 5
        bad = {c for c in declared_cmds if c not in have_cmds and c not in ("run", "py")}
        if bad:
            notes.append("SKILL 提到的子命令脚本内不存在：%s" % "、".join(sorted(bad)[:3]))
        else:
            notes.append("子命令与实现一致：%s" % "、".join(sorted(have_cmds)))
    if "不编" in desc + skill_md or "faithful" in desc.lower():
        got += 5
    return got, notes, blocking


def d_reproducible(root, files, do_run):
    got, notes = 0, []
    has_golden = any(re.search(r"tests[/\\].*\.json", p) for p in files)
    has_runner = any(re.search(r"tests[/\\]run_.*\.py", p) for p in files)
    has_demo = any(re.search(r"demo[/\\]", p) for p in files)
    if has_golden:
        got += 6
    else:
        notes.append("无测试用例文件（tests/*.json）")
    if has_runner:
        got += 6
    else:
        notes.append("无测试执行器（tests/run_*.py），别人无法复跑")
    if has_demo:
        got += 4
    else:
        notes.append("无 demo，首次使用者无从验证")
    if has_runner and do_run:
        runner = [p for p in files if re.search(r"tests[/\\]run_.*\.py", p)][0]
        try:
            r = subprocess.run([sys.executable, runner], cwd=root, capture_output=True,
                               text=True, encoding="utf-8", timeout=120)
            tail = (r.stdout or r.stderr or "").strip().splitlines()
            last = tail[-1] if tail else ""
            if r.returncode == 0:
                got += 4
                notes.append("实跑通过：%s" % last[:80])
            else:
                notes.append("实跑失败（rc=%d）：%s" % (r.returncode, last[:80]))
        except Exception as ex:  # noqa: BLE001
            notes.append("实跑异常：%s" % ex)
    elif has_runner:
        notes.append("未加 --run，未验证测试是否真能跑通")
    return got, notes


def d_hygiene(root, files):
    got, notes, blocking = 0, [], []
    hits, contact = [], []
    CONTACT_CTX = re.compile(r"contact|联系|security|安全报告|报告漏洞|email me|来信|邮箱", re.I)
    for p in files:
        if not p.lower().endswith((".md", ".json", ".txt", ".py", ".yaml", ".yml", ".svg")):
            continue
        body = read(p)
        lines = body.splitlines()
        for pat, label in SENSITIVE:
            for m in re.finditer(pat, body):
                # 邮箱若出现在「联系方式 / 安全报告」语境里，属作者主动公开，不算泄露
                if "邮箱" in label or "email" in label.lower():
                    ln = body[:m.start()].count("\n")
                    ctx = " ".join(lines[max(0, ln - 3):ln + 2])
                    if CONTACT_CTX.search(ctx):
                        contact.append((os.path.relpath(p, root), m.group(0)))
                        continue
                hits.append((os.path.relpath(p, root), label, m.group(0)[:24]))
    if hits:
        for h in hits[:5]:
            notes.append("%s：%s（%s）" % (h[0], h[1], h[2]))
            blocking.append("secret_leak:%s" % h[0])
    else:
        got += 8
        if contact:
            notes.append("检出公开联系方式（%d 处，语境为 Contact/安全报告，按主动公开处理，不计泄露）：%s"
                         % (len(contact), contact[0][1]))
            notes.append("提示：公开仓里的邮箱会被爬虫抓取，建议改用 GitHub issue 或别名邮箱")
    # 是否有明确的安全/边界声明
    md = read(os.path.join(root, "SKILL.md"))
    if re.search(r"安全边界|不输出|脱敏|边界与异常|降级", md):
        got += 7
    else:
        notes.append("SKILL.md 未声明安全边界或降级规则")
    return got, notes, blocking


def d_discoverable(root, fm, files):
    got, notes = 0, []
    tags = fm.get("tags", "")
    n_tags = len(re.findall(r"^\s*-\s", tags, re.M)) or len([t for t in tags.split(",") if t.strip()])
    if n_tags >= 3:
        got += 5
    else:
        notes.append("标签 %d 个，建议 ≥3（当前 %r）" % (n_tags, tags[:40]))
    md = read(os.path.join(root, "SKILL.md"))
    if re.search(r"Triggers?|触发", md, re.I):
        got += 4
    else:
        notes.append("缺触发词段（AI 检索主要靠它）")
    if re.search(r"同系列|生态|系列技能", md):
        got += 3
    else:
        notes.append("缺互链段（无法形成生态入口网络）")
    if any(re.search(r"(ai-index\.json|llms\.txt)", p) for p in files):
        got += 3
        notes.append("已提供机器可读索引")
    else:
        notes.append("未提供 ai-index.json / llms.txt（AI 读取入口缺失）")
    return got, notes


def d_licensing(root, fm, files):
    got, notes = 0, []
    if fm.get("author"):
        got += 2
    else:
        notes.append("缺 author")
    if fm.get("license"):
        got += 2
    else:
        notes.append("缺 license 字段")
    if any(p.lower().endswith(("license.md", "license", "license.txt")) for p in files):
        got += 1
        notes.append("有独立许可文件")
    else:
        notes.append("无独立许可文件（仅 frontmatter 声明）")
    return got, notes


TYPE_PROFILES = {
    "meeting": {
        "label": "会议纪要 / 逐字稿",
        "keywords": ["会议纪要", "纪要", "逐字稿", "录音", "transcript", "minutes", "meeting", "standup"],
        "expected": [
            (["references/adapters", "adapter", "适配"], "来源适配说明",
             "不同平台导出的说话人格式不同，没有适配说明，实际只能处理一种输入"),
            (["citecheck", "citation", "溯源", "证据"], "证据溯源",
             "纪要里的数字与承诺必须能追回原句，否则无法核验"),
            (["golden.json", "tests/"], "黄金集",
             "纪要最容易在边界句上出错（否定、条件、部门归属），需要固定用例锁住"),
        ],
    },
    "debug": {
        "label": "调试 / 故障定位",
        "keywords": ["调试", "排错", "报错", "堆栈", "stack trace", "debug", "troubleshoot", "错误定位"],
        "expected": [
            (["不编", "faithful", "未确认", "unconfirmed"], "证据纪律声明",
             "调试类最大的风险是给出一个像样但错误的原因，必须声明未观察即不推断"),
            (["复现", "repro", "reproduction"], "复现分级",
             "没有复现分级的定位结论，可信度无法判断"),
            (["demo/", "sample", "样例"], "失败样例",
             "至少要有一份真实报错输入与期望输出"),
        ],
    },
    "content": {
        "label": "内容 / 选题",
        "keywords": ["选题", "标题", "公众号", "爆款", "推文", "topic", "headline", "content"],
        "expected": [
            (["红线", "合规", "red line", "compliance"], "合规红线",
             "内容类技能必须把不能碰的边界单独列出，而不是埋在正文"),
            (["不承诺", "阅读量", "不得", "no fabricated"], "不作虚假承诺",
             "不得承诺无法知道的阅读量或转化率"),
        ],
    },
    "reviewer": {
        "label": "技能评测 / 质量门禁",
        "keywords": ["评测", "评审", "审查", "打分", "质量", "review", "audit", "score", "gate"],
        "expected": [
            (["tests/", "golden.json"], "自检套件",
             "评测器本身若不被自检，就无法证明它既会放行也会拦截"),
            (["scoring", "口径", "细则"], "评分口径公开",
             "口径不公开的评分无法被第三方复核"),
            (["demo/", "闭环"], "闭环演示",
             "必须能演示「坏包→整改→复测」的实际效果"),
        ],
    },
    "general": {"label": "通用", "keywords": [], "expected": []},
}


def detect_type(fm, skill_md):
    text = " ".join(str(fm.get(k, "")) for k in ("description", "description_zh", "description_en")) + " " + skill_md
    low = text.lower()
    hits = {}
    for t, p in TYPE_PROFILES.items():
        if t == "general":
            continue
        hits[t] = sum(1 for kw in p["keywords"] if kw.lower() in low)
    best = max(hits, key=hits.get) if hits else "general"
    return (best if hits.get(best, 0) >= 2 else "general"), hits


def type_advice(root, fm, files, skill_type):
    """类型策略：按技能类型检查「该类技能该有但没有」的东西。不参与计分，只出建议。"""
    t = skill_type or detect_type(fm, read(os.path.join(root, "SKILL.md")))[0]
    prof = TYPE_PROFILES.get(t, TYPE_PROFILES["general"])
    blob = (read(os.path.join(root, "SKILL.md")) + " " + " ".join(files)).lower()
    missing = []
    for kws, title, why in prof["expected"]:
        if not any(kw.lower() in blob for kw in kws):
            missing.append({"item": title, "why": why})
    return {"type": t, "label": prof["label"], "expected_count": len(prof["expected"]),
            "missing": missing}


def review(root, do_run=False, skill_type=None):
    skill_md_path = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill_md_path):
        return {"ok": False, "error_id": "R001", "msg": "目录下没有 SKILL.md", "root": root}
    files = walk(root)
    fm = frontmatter(read(skill_md_path))

    detail, notes_all, blocking = {}, [], []
    for name, fn in (
        ("structure", lambda: d_structure(root, fm, files)),
        ("consistency", lambda: d_consistency(root, fm, files)),
        ("reproducible", lambda: d_reproducible(root, files, do_run)),
        ("hygiene", lambda: d_hygiene(root, files)),
        ("discoverable", lambda: d_discoverable(root, fm, files)),
        ("licensing", lambda: d_licensing(root, fm, files)),
    ):
        r = fn()
        if len(r) == 3:
            got, notes, blk = r
            blocking += blk
        else:
            got, notes = r
        full = WEIGHTS[name]
        detail[name] = {"score": got, "max": full,
                        "pct": round(100.0 * got / full, 1) if full else 0,
                        "notes": notes}
        notes_all += ["[%s] %s" % (name, n) for n in notes]

    total = sum(v["score"] for v in detail.values())
    verdict = "PASS"
    if blocking:
        verdict = "BLOCK"
    elif total < 60:
        verdict = "FAIL"
    elif total < 80:
        verdict = "WARN"

    # 类型策略：不影响分数，只补「这类技能该有什么」
    try:
        tinfo = type_advice(root, fm, files, skill_type)
    except Exception as e:  # 绝不让类型策略拖垮主评测
        tinfo = {"type": "unknown", "label": "未判定", "missing": [], "error": str(e)}
    type_actions = [{"priority": "P2", "issue": "[%s] 建议补：%s" % (tinfo["type"], m["item"]),
                     "fix": m["why"]} for m in tinfo.get("missing", [])]

    actions = []
    for b in blocking:
        actions.append({"priority": "P0", "issue": b.split(":")[0],
                        "fix": BLOCKING.get(b.split(":")[0], "修复该阻断项")})
    for n in notes_all:
        if re.search(r"缺|未|无|失败|建议", n):
            actions.append({"priority": "P1", "issue": n[:100],
                            "fix": "按该项补齐后复测"})

    return {
        "ok": True,
        "error_id": None,
        "data": {
            "root": root,
            "name": fm.get("name"),
            "version": fm.get("version"),
            "total": total,
            "max": sum(WEIGHTS.values()),
            "pct": round(100.0 * total / sum(WEIGHTS.values()), 1),
            "verdict": verdict,
            "dimensions": detail,
            "blocking": blocking,
            "type": tinfo,
            "actions": actions[:12] + type_actions,
            "rerun": "python review.py \"%s\" --run" % root,
        },
    }


def main():
    ap = argparse.ArgumentParser(description="LGD 技能评测引擎（6 维，零依赖）")
    ap.add_argument("path", help="技能目录")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--run", action="store_true", help="额外尝试实跑 tests/run_*.py")
    ap.add_argument("--type", default=None,
                    choices=["auto", "meeting", "debug", "content", "reviewer", "general"],
                    help="技能类型策略（默认自动识别），只出建议不参与计分")
    a = ap.parse_args()

    if not os.path.isdir(a.path):
        print(json.dumps({"ok": False, "error_id": "R002", "msg": "路径不是目录"},
                         ensure_ascii=False))
        sys.exit(2)

    r = review(os.path.abspath(a.path), a.run,
               None if (a.type in (None, "auto")) else a.type)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        sys.exit(0 if r.get("data", {}).get("verdict") in ("PASS", "WARN") else 1)

    if not r["ok"]:
        print("评测失败：%s" % r["msg"])
        sys.exit(2)

    d = r["data"]
    print("技能：%s  v%s" % (d["name"], d["version"]))
    t = d.get("type", {})
    print("类型：%s（%s）  %s" % (t.get("label", "-"), t.get("type", "-"),
                                 ("建议 %d 项" % len(t.get("missing", []))) if t.get("missing") else "该类关键项齐备"))
    print("总分：%d/%d（%.1f%%）  判定：%s" % (d["total"], d["max"], d["pct"], d["verdict"]))
    print()
    for k, v in d["dimensions"].items():
        print("  %-13s %2d/%-2d (%5.1f%%)" % (k, v["score"], v["max"], v["pct"]))
    if d["blocking"]:
        print("\n阻断项：")
        for b in d["blocking"]:
            print("  ✗ " + b)
    if d["actions"]:
        print("\n整改清单：")
        for x in d["actions"]:
            print("  [%s] %s" % (x["priority"], x["issue"]))
    print("\n复测：%s" % d["rerun"])
    sys.exit(0 if d["verdict"] in ("PASS", "WARN") else 1)


if __name__ == "__main__":
    main()
