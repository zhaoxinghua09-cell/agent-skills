# -*- coding: utf-8 -*-
"""提交 agent-skills 4 个技能到 SkillPie（AppKey 已配置，不进对话）。"""
import subprocess, pathlib, re, time

BASE = pathlib.Path("D:/Workbuddy/05-工具/agent-skills")
CLI_DIR = "C:/Users/Administrator/.workbuddy/skills/skillpie"
NODE = "C:/Users/Administrator/.workbuddy/binaries/node/versions/node24/node.exe"

slugs = ["context-engineering", "ai-cost-cutter", "prompt-injection-shield", "eu-ai-act-companion"]
results = []
for slug in slugs:
    sd = BASE / slug
    sp = sd / "SKILL.md"
    t = sp.read_text(encoding="utf-8")
    m = re.search(r'display_name:\s*"?([^"\n]+)', t)
    title = m.group(1).strip() if m else slug
    try:
        r = subprocess.run(
            [NODE, "scripts/cli.js", "submit", str(sd), "--title", title],
            cwd=CLI_DIR, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=180,
        )
        out = (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        out = "TIMEOUT"
    ok = ("发布成功" in out) or ("成功" in out and "skillpie" in out.lower()) or ("submitted" in out.lower())
    ver = ""
    mm = re.search(r"版本号[:：](\S+)", out)
    if mm:
        ver = mm.group(1)
    results.append((slug, "OK" if ok else "FAIL", ver, out[-200:]))
    print(f"\n### {slug} -> {'OK' if ok else 'FAIL'} {ver}")
    print(out[-400:].strip())
    time.sleep(2)

ok_n = sum(1 for _, s, _, _ in results if s == "OK")
print("\n====汇总====")
print(f"成功 {ok_n} / {len(results)}")
for slug, s, ver, _ in results:
    if s != "OK":
        print("FAILED:", slug)
