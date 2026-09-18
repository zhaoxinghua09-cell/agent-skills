# -*- coding: utf-8 -*-
"""lgd-certify · LGD 三律闭环 CLI v1.0
=====================================
对标调研（2026-09-07，GitHub 按 star 从高到低）：治理生态全是单点工具——
运行时门禁（litellm 58k★/NeMo Guardrails 7k★）、内容凭证（C2PA 415★）、
治理平台（verifywise 345★，证据中心强但无护照签发/无部署门禁）、
Agent 护照（FoloToy ai-passport 250★ = 硬件产品，非协议；agent-passport-system 43★ 极早期）。
**无任何项目把「有籍护照签发 → 有证证据链 → 有门禁签发 → 可挂载徽章」做成闭环** —— 本工具占此位。

三律 → 三命令：
  register  有籍 REGISTERED  凡造必登   ：生成算法护照（schema v1.0 三锚一票同源）+ SHA-256 指纹
  evidence  有证 EVIDENCED   凡所行必有证据：扫描六类证据工件 → 链式哈希证据链（防篡改）
  gate      有门禁 GATED     凡演化必经门禁：三律评审 → PASS/FAIL → 签发结论 + 官方徽章嵌入码

零依赖（纯 stdlib）；产物全落 --dir 项目目录；评审徽章指向 medxpert.cn/badge/（已上线）。
© SynomosAI Governance Line · CC BY 4.0 · LGD-Powered
"""
import argparse, hashlib, json, os, sys, datetime as dt

BADGE = "https://medxpert.cn/badge"
SIX = {
    "01-identity":   "身份证据（护照/登记文件/DID）",
    "02-data":       "数据证据（数据集指纹与来源）",
    "03-validation": "验证证据（评测报告/指标带CI/文献）",
    "04-behavior":   "行为边界证据（红线/人机边界/中止规程）",
    "05-change":     "变更证据（变更日志与评估记录）",
    "06-issuance":   "签发证据（门禁结论/签发人/时间戳）",
}
NOW = lambda: dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()

def sha256_obj(obj):
    return "sha256:" + hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()

def load_state(d):
    st = os.path.join(d, "lgd_state.json")
    return json.load(open(st, encoding="utf-8")) if os.path.exists(st) else {}

def save_state(d, st):
    json.dump(st, open(os.path.join(d, "lgd_state.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

# ---------- 有籍 register ----------
def cmd_register(d, name, algo_id, issuer, org="SynomosAI Governance Line"):
    st = load_state(d)
    if st.get("passport"):
        print("[!] 本项目已登记（有籍），如需重签先删除 lgd_state.json 中 passport 字段")
        sys.exit(2)
    passport = {
        "schema_version": "1.0",
        "algorithm_id": algo_id,
        "product": {"model_name": name, "manufacturer": org,
                    "intended_use": "[待填：预期用途，须过 intended-use-check 7 要素]"},
        "identity_anchor": {"regulatory_classification": {}, "market_status": []},
        "memory_anchor": {"training_data_fingerprint": {}, "validation_summary": {}},
        "behavior_anchor": {"safety_limits": [], "human_oversight": {},
                             "kill_switch": {"exists": True, "owner": issuer}},
        "verification_ticket": {"issuer": issuer, "issuance_date": NOW(),
                                "vc_type": "VerifiableCredential"},
        "change_log": [],
        "lifecycle_status": "in_development",
    }
    passport["verification_ticket"]["passport_hash"] = sha256_obj(passport)
    st["passport"] = passport
    st["registered_at"] = NOW()
    save_state(d, st)
    p = os.path.join(d, "passport.json")
    json.dump(passport, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[✓] 有籍 · 护照已签发 → {p}")
    print(f"    algorithm_id={algo_id}  指纹={passport['verification_ticket']['passport_hash'][:27]}…")

# ---------- 有证 evidence ----------
def cmd_evidence(d):
    """有证 · 取证（**append-only**）。

    🔴 2026-09-17 修复（端到端走查发现）：原实现每次重跑都**重建链并丢弃历史块**
    （旧 head 仅作新链首块的 prev），违反"台账只增不减"纪律，且无法回答
    "这份证据件改过没有、改了几次"。现改为：
      · 仅追加新块；同文件哈希变化 → 追加"继任块"并标 `supersedes`（旧块保留）；
      · 全部块落 `evidence_chain_history.jsonl`（append-only 审计流）；
      · 哈希未变则链头不动（幂等重跑）。
    """
    st = load_state(d)
    if not st.get("passport"):
        print("[!] 尚未登记（先跑 register —— 凡造必登，登记先于取证）")
        sys.exit(2)
    ev_dir = os.path.join(d, "evidence")
    missing = [k for k in SIX if not os.path.isdir(os.path.join(ev_dir, k))]
    if missing:
        for k in missing:
            os.makedirs(os.path.join(ev_dir, k), exist_ok=True)
            print(f"[i] 建目录 evidence/{k}/ —— 放：{SIX[k]}")
        print("[!] 证据目录已建好。放入工件后重跑 evidence。已放入的可重跑增量收录。")
    old = st.get("evidence_chain", {})
    chain = list(old.get("blocks", []))
    prev = old.get("head", "genesis")
    latest = {(b["evidence_class"], b["file"]): b["hash"] for b in chain}
    files = []
    for k in sorted(SIX):
        sub = os.path.join(ev_dir, k)
        if os.path.isdir(sub):
            for fn in sorted(os.listdir(sub)):
                fp = os.path.join(sub, fn)
                if os.path.isfile(fp):
                    files.append((k, fn, fp))
    if not files:
        print("[i] 尚无任何证据工件（六类目录均为空）")
        return
    appended = []
    added = updated = skipped = 0
    for k, fn, fp in files:
        h = sha256_file(fp)
        cur = latest.get((k, fn))
        if cur == h:
            skipped += 1
            continue
        block = {"evidence_class": k, "file": fn, "hash": h, "recorded_at": NOW(), "prev": prev}
        if cur is not None:
            block["supersedes"] = cur
            updated += 1
        else:
            added += 1
        block["block_hash"] = sha256_obj(block)
        chain.append(block); appended.append(block); prev = block["block_hash"]
    if not appended:
        print(f"[i] 证据链无变化（{skipped} 个工件哈希一致），链头不变：{prev[:27]}…")
        return
    cur_latest = {}
    for b in chain:
        cur_latest[(b["evidence_class"], b["file"])] = b["hash"]  # 后者覆盖前者 = 取最新
    st["evidence_chain"] = {"head": prev, "blocks": chain,
                            "classes_covered": sorted({k for (k, _f) in cur_latest}),
                            "updated_at": NOW()}
    save_state(d, st)
    with open(os.path.join(d, "evidence_chain_history.jsonl"), "a", encoding="utf-8") as f:
        for b in appended:
            f.write(json.dumps(b, ensure_ascii=False, sort_keys=True) + "\n")
    p = os.path.join(d, "evidence_chain.json")
    json.dump(st["evidence_chain"], open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    cov = ",".join(st["evidence_chain"]["classes_covered"])
    print(f"[✓] 有证 · 证据链 {len(chain)} 块（本次新增 {added} / 继任 {updated} / 未变 {skipped}，覆盖 {cov}）→ {p}")
    print(f"    链头={prev[:27]}…  审计流=evidence_chain_history.jsonl")


# ---------- 防篡改复验 verify（2026-09-17 新增）----------
def cmd_verify(d):
    """防篡改复验：逐件重算哈希 + 链自洽 + 与签发冻结值对齐。任一不符即 rc=1。"""
    st = load_state(d)
    ec = st.get("evidence_chain")
    if not ec or not ec.get("blocks"):
        print("[!] 尚无证据链，无可复验对象")
        sys.exit(2)
    latest = {(b["evidence_class"], b["file"]): b for b in ec["blocks"]}
    problems, checked = [], 0
    for (k, fn), b in sorted(latest.items()):
        fp = os.path.join(d, "evidence", k, fn)
        if not os.path.exists(fp):
            problems.append(f"缺失  {k}/{fn}")
            continue
        checked += 1
        if sha256_file(fp) != b["hash"]:
            problems.append(f"被改  {k}/{fn}（现哈希 ≠ 链上哈希）")
    if st.get("gate_verdict"):
        if st["gate_verdict"].get("evidence_head") != ec["head"]:
            problems.append("链头不一致  证据链头 ≠ 签发时冻结值（签发后证据有变动）")
        cur_pp = st["passport"]["verification_ticket"]["passport_hash"]
        if st["gate_verdict"].get("passport_hash") != cur_pp:
            problems.append("护照不一致  护照指纹 ≠ 签发时冻结值")
    print("=" * 62)
    print("  LGD 防篡改复验 · " + dt.date.today().isoformat())
    print("=" * 62)
    print(f"  复验工件：{checked} 件 ｜ 链块：{len(ec['blocks'])} ｜ 链头：{ec['head'][:27]}…")
    if problems:
        for x in problems:
            print("  [✗] " + x)
        print("  结论：TAMPERED / BROKEN（请勿采信本件证据）")
        print("=" * 62)
        sys.exit(1)
    print("  [✓] 全部工件哈希与链上一致")
    print("  [✓] 链头与签发时冻结值一致")
    print("  结论：VERIFIED")
    print("=" * 62)

# ---------- 有门禁 gate ----------
def cmd_gate(d):
    st = load_state(d)
    ec = st.get("evidence_chain", {})
    classes = set(ec.get("classes_covered", []))
    # 链-盘一致性：防止"改了证据件但不重跑 evidence 就想蒙过门禁"（2026-09-17 加固）
    cur_latest = {}
    for b in ec.get("blocks", []):
        cur_latest[(b["evidence_class"], b["file"])] = b["hash"]
    drift = []
    for (k, fn), h in cur_latest.items():
        fp = os.path.join(d, "evidence", k, fn)
        if not os.path.exists(fp) or sha256_file(fp) != h:
            drift.append(f"{k}/{fn}")
    checks = {
        "L1-有籍 REGISTERED": bool(st.get("passport")),
        "L2-有证 EVIDENCED": bool(ec) and classes >= set(SIX),
        "L3-有门禁 GATED": "06-issuance" in classes,
        "L4-链盘一致 CONSISTENT": not drift,
    }
    verdict = "PASS" if all(checks.values()) else "FAIL"
    print("=" * 62)
    print("  LGD 三律门禁评审 · " + dt.date.today().isoformat())
    print("=" * 62)
    for k, ok in checks.items():
        print(f"  [{'✓' if ok else '✗'}] {k}")
    if drift:
        print("      ↳ 链外改动（请重跑 evidence）：" + "、".join(drift))
    missing = [k for k, ok in checks.items() if not ok]
    print(f"  结论：{verdict}" + (f"（缺：{'、'.join(missing)}）" if missing else ""))
    print("=" * 62)
    if verdict != "PASS":
        sys.exit(1)
    # 签发 + 徽章嵌入码（指向 medxpert.cn 已上线徽章）
    st["gate_reviewed"] = True
    st["gate_verdict"] = {"verdict": "PASS", "reviewed_at": NOW(),
                          "evidence_head": st["evidence_chain"]["head"],
                          "passport_hash": st["passport"]["verification_ticket"]["passport_hash"]}
    save_state(d, st)
    cert = {"schema_version": "1.0", "type": "LGDCertification", "verdict": "PASS",
            "algorithm_id": st["passport"]["algorithm_id"],
            "passport_hash": st["passport"]["verification_ticket"]["passport_hash"],
            "evidence_head": st["evidence_chain"]["head"], "issued_at": NOW(),
            "issuer": st["passport"]["verification_ticket"]["issuer"]}
    cert["cert_hash"] = sha256_obj(cert)
    json.dump(cert, open(os.path.join(d, "certification.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    md = f"""<!-- LGD 三律认证 · 嵌入以下行到 README / 论文顶部 -->
![LGD Registered 有籍]({BADGE}/laws/svg/lgd-registered-en.svg)
![LGD Evidenced 有证]({BADGE}/laws/svg/lgd-evidenced-en.svg)
![LGD Gated 有门禁]({BADGE}/laws/svg/lgd-gated-en.svg)
![LGD-Powered]({BADGE}/powered/svg/lgd-powered-en.svg)
<!-- 认证指纹 {cert['cert_hash'][:27]}… 详见 certification.json -->"""
    open(os.path.join(d, "BADGES.md"), "w", encoding="utf-8").write(md)
    print(f"[✓] 有门禁 · 认证签发 → certification.json（指纹 {cert['cert_hash'][:27]}…）")
    print("[✓] 徽章嵌入码 → BADGES.md（三律徽章 + LGD-Powered，medxpert.cn 已上线资产）")

# ---------- 一键 certify ----------
def cmd_certify(a):
    cmd_register(a.dir, a.name, a.id, a.issuer)
    cmd_evidence(a.dir)
    try:
        cmd_gate(a.dir)
    except SystemExit:
        print("[i] 门禁未过属正常（证据未放齐）。放齐六类工件后依次重跑 evidence → gate。")

def main():
    ap = argparse.ArgumentParser(description="LGD 三律闭环 CLI（有籍·有证·有门禁）")
    ap.add_argument("command", choices=["init", "register", "evidence", "gate", "verify", "certify"])
    ap.add_argument("--dir", default=".", help="项目目录（产物全落此处）")
    ap.add_argument("--name", help="算法/模型名")
    ap.add_argument("--id", dest="id", help="算法唯一 ID（did:web:… 或 UUID）")
    ap.add_argument("--issuer", help="签发人（权属人）")
    a = ap.parse_args()
    os.makedirs(a.dir, exist_ok=True)
    if a.command == "init":
        for k in SIX:
            os.makedirs(os.path.join(a.dir, "evidence", k), exist_ok=True)
        open(os.path.join(a.dir, "evidence", "01-identity", "PUT-PASSPORT-HERE.txt"), "w").close()
        print("[✓] 项目骨架已建：evidence/ 六类目录 + 待填占位")
    elif a.command == "register":
        if not (a.name and a.id and a.issuer):
            ap.error("register 需要 --name --id --issuer")
        cmd_register(a.dir, a.name, a.id, a.issuer)
    elif a.command == "evidence":
        cmd_evidence(a.dir)
    elif a.command == "gate":
        cmd_gate(a.dir)
    elif a.command == "verify":
        cmd_verify(a.dir)
    elif a.command == "certify":
        if not (a.name and a.id and a.issuer):
            ap.error("certify 需要 --name --id --issuer")
        cmd_certify(a)

if __name__ == "__main__":
    main()
