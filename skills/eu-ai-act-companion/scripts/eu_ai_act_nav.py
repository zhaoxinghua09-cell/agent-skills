# -*- coding: utf-8 -*-
"""EU AI Act 导航分类器（零依赖 stdlib，参考框架非法律意见）。

输入用例描述 + 角色，输出风险级 + 该角色义务 + 相关时间节点。
风险判定基于 Annex III 高风险领域关键词 + 禁止类/透明类关键词启发式。

用法：
  python eu_ai_act_nav.py --use "招聘简历筛选AI" --role provider
  python eu_ai_act_nav.py --use "客服聊天机器人" --role deployer
"""
import argparse, sys

# 禁止类关键词
BANNED = ["社会评分", "social scoring", "实时远程生物识别", "realtime biometric", "潜意识操纵", "subliminal"]
# 高风险领域（Annex III 启发式；同义词已归并：信贷≈贷款≈借贷≈信用评估）
HIGH = ["招聘", "recruit", "信贷", "credit", "贷款", "loan", "借贷", "放贷", "信用评估", "信用评分", "credit scoring",
        "教育", "education", "招生", "考试评分", "exam scoring",
        "关键基础设施", "critical infrastructure",
        "医疗", "medical", "医械", "medical device", "器械", "device", "诊断辅助",
        "保险", "insurance", "保费定价", "pricing",
        "雇佣", "用工", "在职评估", "绩效评估", " employment", "employment",
        "安防", "law enforcement", "签证", "visa", "移民", "migration",
        "边境", "border", "司法", "justice", "简历", "resume", "筛选", "screening"]
# 有限风险（透明义务）
LIMITED = ["聊天机器人", "chatbot", "深度伪造", "deepfake", "情绪识别", "emotion", "合成", "synthetic"]

ROLE_OBLIG = {
    "provider": ["风险管理系统", "数据治理", "技术文档", "合格评定", "CE标志", "EU数据库登记", "人类监督", "上市后监测(PMS)"],
    "deployer": ["人员能力与培训", "按使用说明部署", "监控与记录", "若自训数据则数据治理", "重大风险上报"],
    "importer": ["确保提供方已合规", "留供应链证据", "违法时联动提供方"],
    "distributor": ["验证CE/文档完整", "留供应链证据"],
}

TIMELINE = [
    ("2024-08", "法案生效"),
    ("2025-02", "禁止类适用"),
    ("2025-08", "治理实践 / GPAI 义务起始"),
    ("2026-08", "高风险大部分义务适用"),
    ("2027-08", "全量义务适用"),
]


def classify(use: str):
    u = use.lower()
    if any(k.lower() in u for k in BANNED):
        return "unacceptable", "禁止类：原则上不得投放欧盟市场"
    if any(k.lower() in u for k in HIGH):
        return "high", "高风险：须走合格评定 + CE 标志 + 全套义务"
    if any(k.lower() in u for k in LIMITED):
        return "limited", "有限风险：须满足透明义务（告知用户在与 AI 交互）"
    return "minimal", "最小风险：基本无强制义务，建议自愿守约"



def run_selftest():
    """自检：跑真实 classify()/main() 风险判定——禁止/高/有限/最小四级须各命中
    对应用例（须过类与须拦类兼具：禁止类与高风险不得漏判）；空用例须被
    argparse 拦下 rc=2。只用内置夹具文本。"""
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
        sys.argv = ["eu_ai_act_nav.py"] + argv
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

    lvl, _ = classify("社会评分系统")
    check("社会评分→禁止类 unacceptable", lvl == "unacceptable")
    lvl, _ = classify("招聘简历筛选AI")
    check("招聘筛选→高风险 high", lvl == "high")
    lvl, _ = classify("客服聊天机器人")
    check("聊天机器人→有限风险 limited", lvl == "limited")
    lvl, _ = classify("天气播报助手")
    check("天气播报→最小风险 minimal", lvl == "minimal")
    code, out = call_main(["--use", "医疗诊断辅助软件", "--role", "provider"])
    check("main 高风险用例输出 high 与提供方义务",
          code == 0 and "risk level = high" in out and "合格评定" in out)
    code, _ = call_main(["--use", "  "])
    check("空用例→argparse 拦下 rc=2", code == 2)
    print(f"SELFTEST: {passed} passed, {failed} failed — {'PASS' if failed == 0 else 'FAIL'}")
    return 0 if failed == 0 else 1

def main():
    if "--selftest" in sys.argv[1:]:
        sys.exit(run_selftest())
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="自检（临时夹具，不触碰真实文件）")
    ap.add_argument("--use", required=True, help="用例描述")
    ap.add_argument("--role", default="provider", help="provider/deployer/importer/distributor")
    args = ap.parse_args()
    # 空输入不判级（避免误判为最小风险），友好退出 rc=2
    if not args.use.strip():
        ap.error("用例描述为空，无法判定风险级：请提供 AI 用例的具体描述")

    level, note = classify(args.use)
    role = args.role.lower()
    obl = ROLE_OBLIG.get(role, ROLE_OBLIG["provider"])

    print(f"风险级 risk level = {level}   （{note}）")
    print(f"角色 role = {role}")
    print("该角色核心义务：")
    for o in obl:
        print(f"  - {o}")
    print("关键时间节点：")
    for d, ev in TIMELINE:
        print(f"  {d}  {ev}")
    print()
    print("⚠️ 本工具为参考框架，非法律意见；落地以欧盟官方公报最新版为准。")


if __name__ == "__main__":
    main()
