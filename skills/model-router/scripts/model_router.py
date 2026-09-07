# -*- coding: utf-8 -*-
"""模型路由：按任务复杂度定级，推荐模型档位 + 成本占比 + 回退建议。零依赖。"""
import argparse, json, re

TIERS = {
    0: {"name": "本地/小模型", "cost": 0.0, "cap": "抽取/分类/短改写/模板"},
    1: {"name": "中端", "cost": 1.0, "cap": "摘要/翻译/多步指令"},
    2: {"name": "旗舰", "cost": 8.0, "cap": "强推理/长上下文/代码/规划"},
    3: {"name": "旗舰+复核", "cost": 16.0, "cap": "高风险对外/金融/医疗结论"},
}
HARD = ["设计", "架构", "规划", "推理", "debug", "调试", "代码", "方案", "分析", "论证", "research", "plan", "architect", "reason", "code"]
RISK = ["金融", "医疗", "对外", "合同", "法律", "投资", "诊断", "financial", "medical", "legal", "public"]
LONG = ["长文", "报告", "论文", "文档", "总结全文", "long", "report", "document", "essay"]

def classify(task):
    t = task.lower()
    score = 0
    if any(k in t for k in HARD):
        score = max(score, 2)
    if any(k in t for k in RISK):
        score = 3
    if any(k in t for k in LONG):
        score = max(score, 2)
    if any(k in t for k in ["分类", "抽取", "关键词", "情感", "改写", "填", "classify", "extract", "summ", "tag"]):
        score = min(score, 1) if score < 2 else score
    if score == 0:
        score = 1  # 默认中端，避免裸落到本地
    return score

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    lv = classify(a.task)
    tier = TIERS[lv]
    share = tier["cost"] / TIERS[2]["cost"] * 100
    fb = "升级一档重试(上限2次)" if lv < 3 else "已是最高档，转人工复核"
    if a.json:
        print(json.dumps({"task": a.task, "level": lv, "tier": tier["name"],
                          "cost_index": tier["cost"], "cost_share_vs_flagship": round(share, 1),
                          "capability": tier["cap"], "fallback": fb}, ensure_ascii=False, indent=2))
    else:
        print(f"任务：{a.task}")
        print(f"复杂度：L{lv}  推荐档位：{tier['name']}  能力：{tier['cap']}")
        print(f"成本指数：{tier['cost']}  (约为旗舰的 {share:.0f}%)  回退：{fb}")

if __name__ == "__main__":
    main()
