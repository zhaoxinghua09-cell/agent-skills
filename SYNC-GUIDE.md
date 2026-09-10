# agent-skills 仓库同步根治方案

> 2026-09-11 立 · 替代此前所有"手工补传"做法
>
> **一句话**：本地是唯一真源，远端是它的镜像。所有同步走 `git push`，永远不再用 GitHub API 单文件写。

---

## 一、问题是什么（不是"推送失败"，是"两套账本"）

此前反复出问题，根因**不在某次推送失败**，而在架构上有两条互不知情的写入通道：

| 通道 | 表现 |
|---|---|
| 本地 git | 有提交历史（5 个 commit）、405 个已跟踪文件，但**从未配置 `origin`**，新增文件长期 untracked |
| GitHub API 单文件写 | 每次 `PUT /contents/{path}` 生成一个**独立 commit**，但**不在本地 git 对象库里** |

后果：本地 `git log` 看不到远端那些 commit；远端 HEAD 已前进导致 `git push` 被拒；本地工作区文件内容却可能一致 → **"内容一样但历史分叉"的诡异状态**。人工比对成为唯一手段，必然反复出错。

### 叠加的三个环境陷阱（都已清理）

| # | 陷阱 | 症状 | 处置 |
|---|---|---|---|
| 1 | `http.curloptresolve=github.com:443:140.82.114.3` | 硬编码 IP，连接到错误主机，fetch 假成功但 refs 不落地 | 已删除 |
| 2 | `credential.helper` 指向 Git Credential Manager + `gh.exe` | 抢答提供**过期缓存凭据** → 401 | 已删除，改为单一保险库 helper |
| 3 | 本地 repo 级 `credential.helper` 指向 `_git_cred.py` | 覆盖全局配置，行为不可预测 | 已删除 |

### 结构错位（根治的核心）

| | 本地（旧） | 远端 |
|---|---|---|
| 技能位置 | **根目录**直放 | `skills/` 子目录 |
| 根文件 | `.gitignore` `README.md` | `LICENSE` `CHANGELOG.md` `docs` `release` |

两套结构 + 无共同祖先 → 171 个 `add/add` 冲突。**已统一到 `skills/` 并对齐。**

---

## 二、现在的架构（根治后）

```
本地 D:/Workbuddy/05-工具/agent-skills/   ← 唯一真源（single source of truth）
        │
        │  git push（唯一写入通道）
        ▼
GitHub zhaoxinghua09-cell/agent-skills    ← 镜像
```

**三条铁律：**

1. **本地即真源。** 所有修改先在本地完成。
2. **单一写入通道。** 一律 `python scripts/sync.py`。禁止手工 `git push`；**禁止用 GitHub API 写文件**。
3. **禁止强推。** 同步前先检查远端有无本地不知道的提交，有则先合并。

---

## 三、配置基线（已生效）

```ini
# ~/.gitconfig 关键项
[http "https://github.com"]
    proxy = http://127.0.0.1:12315
[http]
    sslBackend = schannel
    lowSpeedLimit = 0
    lowSpeedTime = 999999
[credential]
    helper = !C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe C:/Users/Administrator/.ucvault_local/git-credential-ucvault.py
```

**设计意图：**

- **代理只对 github.com 生效** —— 不污染内网 git（gitee / gitcode 等）。
- **单一 credential helper** —— 从 DPAPI 保险库实时读 token，**不落盘、不进命令行、不进环境变量**。helper 协议见 `git-scm.com/docs/gitcredentials`。
- **`lowSpeedLimit=0`** —— 代理链路慢时不误判超时中断。

**为什么用 helper 而不是把 token 写进 URL：**
写进 URL（`https://user:token@github.com/...`）会进进程 argv，可能被日志/进程列表捕获。helper 走 stdin/stdout 管道，仅内存可见。

---

## 四、日常操作（只有两条命令）

### 体检（随时看是否漂移）

```bash
python scripts/drift-check.py --fix-hint
```

四段输出：git 血缘 → 工作区状态 → 内容差异 → 结论。退出码 `0` 一致 / `1` 有漂移 / `2` 环境不可用。

### 同步（改了东西要上远端）

```bash
python scripts/sync.py -m "feat: 新增 xxx 技能"
```

自动完成：`add -A`（含 untracked）→ commit → 检查远端 → 合并（如需）→ push → 收尾校验。
**这是唯一推送入口。** 演练用 `--dry-run`。

### 校验（提交前跑）

```bash
python scripts/validate.py
```

七条规则：R1 每个目录含 SKILL.md · R2 frontmatter 完整 · R3 有 name/description · R4 name 与目录名一致 · R5 有 LICENSE · R6 有 README · R7 无明文密钥。

---

## 五、异常处置速查

| 现象 | 定性 | 处置 |
|---|---|---|
| `401` / `Authentication failed` | 凭据 | `git config --global --get-all credential.helper` 应**只有一项**（保险库 helper）。多项则清理 |
| `502` / `CONNECT tunnel failed` / 超时 | 代理/通道 | 检查代理是否在跑：`curl -x http://127.0.0.1:12315 -o /dev/null -w "%{http_code}" https://github.com` |
| `schannel: server closed abruptly` | TLS 抖动 | 重试（链路间歇性）。持续失败查代理 |
| fetch 报成功但 `origin/main` 不存在 | ref 写入异常 | `git fetch origin "+refs/heads/main:refs/remotes/origin/main"`；仍不行则 `git update-ref refs/remotes/origin/main <sha>` |
| `push` 被拒（non-fast-forward） | 远端有未知提交 | `python scripts/sync.py` 会自动合并。**绝不用 `--force`** |
| 目录层级对不上 | 结构漂移 | 跑 `drift-check.py` 看 [3] 段；按需迁移后提交 |

---

## 六、为什么这能根治（而不是再打一次补丁）

| 补丁式做法 | 本方案 |
|---|---|
| 再写个脚本手工补传 | **建立单一血缘**：`merge --allow-unrelated-histories` 让两侧共享历史，此后 `git diff origin/main` 可**机器化**暴露任何差异 |
| 继续用 API 写远端 | **收敛为单一写入通道**：移除 API 写入，一切走 `git push` |
| 靠人记住要同步 | **自动化校验**：`drift-check` + `validate` 让漂移在**执行时立刻失败**，而非几周后人工比对才发现 |

**关键转变：一致性从"依赖人的记忆"变成"由工具在每次写入时强制保证"。**

---

## 七、可选加固（尚未做，按需启用）

- [ ] **GitHub Actions 校验** —— 每次 push 自动跑 `gen_index` + `git diff --exit-code`，索引与目录不符即失败。
- [ ] **lefthook / pre-commit** —— 本地提交前自动跑 `validate.py`，半成品进不了仓。
- [ ] **SSH 替代 HTTPS** —— 若代理链路持续不稳，可切 SSH over 443（已验证 TCP 可达，仅需在 GitHub 网页添加一次公钥）。当前 PAT 只有 `repo` scope，缺 `admin:public_key`，无法自动注册。

---

## 八、备份位置

```
D:/Workbuddy/05-工具/agent-skills/_backup/
  git-obj-<ts>.tgz              # .git 对象库
  full-pre-migrate-<ts>.tgz     # 结构迁移前全量快照
```

紧急回退：解压 `full-pre-migrate-*.tgz` 覆盖工作区。
