# -*- coding: utf-8 -*-
"""偏见审计：扫群体泛化/刻板归因/单边视角，标信号 + 去偏建议。零依赖。"""
import argparse, json, pathlib, re

GENERIC = ["都适合", "都不适合", "就是", "天生", "本来就该", "普遍不如", "普遍更强",
           "all", "naturally", "born to", "just are"]
GROUP_TERMS = ["男", "女", "女生", "男生", "男性", "女性", "老人", "年轻人", "某地", "北方人", "南方人",
               "women", "men", "old", "young", "region"]
STEREOTYPE_BIND = [("技术", "男"), ("沟通", "女"), ("理性", "男"), ("细心", "女")]

def audit(text):
    findings = []
    for g in GENERIC:
        for i in re.finditer(re.escape(g), text):
            findings.append(("群体泛化", g, "改为个体表述，避免全称判断"))
    for gt in GROUP_TERMS:
        if gt in text:
            findings.append(("群体提及", gt, "仅当相关时保留，避免以偏概全"))
    for ability, grp in STEREOTYPE_BIND:
        if ability in text and grp in text:
            findings.append(("刻板归因", f"{ability}↔{grp}", "能力与群体无必然绑定，去绑"))
    if len(findings) == 0:
        findings.append(("无显著信号", "", "未发现明显群体泛化/刻板归因"))
    return findings

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text = a.text if a.text else pathlib.Path(a.file).read_text(encoding="utf-8")
    fs = audit(text)
    if a.json:
        print(json.dumps({"findings": [{"type": t, "hit": h, "fix": fx} for t, h, fx in fs]}, ensure_ascii=False, indent=2))
    else:
        for t, h, fx in fs:
            icon = "✅" if t == "无显著信号" else "⚠️"
            print(f"  {icon} [{t}] 命中：{h}  建议：{fx}")

if __name__ == "__main__":
    main()
