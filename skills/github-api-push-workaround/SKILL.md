---
name: github-api-push-workaround
description: "git 推 GitHub/Gitee/AtomGit 的根因化排查与推送模板：401=凭据问题（helper 链残留死旧 PAT）、超时/挂死=通道问题（代理掐 git 传输，须 no_proxy 直连）、大面积 401=取值前缀坑（--raw 取裸值）。含直连推送模板（令牌走环境变量）、Git Data API 兜底（blob→tree→commit→ref）、Gitee 私有转公开、AtomGit 后端 gitcode 等实测坑。当用户说'推 GitHub'、'git push 失败/401/超时'、'发布仓库到远端'、'令牌失效了'时使用。"
author: 潘布达 (Buda Pan) @SynomosAI
version: 1.2.0
agent_created: true
license: MIT
category: 开发效率
platforms: [WorkBuddy]
tags: [github, git-push, 代理, 凭据, 排查, 发布, gitee, atomgit]
---

# git 远端推送：根因化排查与推送模板

> 2026-09-07 全天实测定版。核心教训：**先归因，再重试**。401 是凭据问题，超时/挂死是通道问题，大面积 401 多半是取值姿势问题——三者根因完全不同，混着盲试只会浪费时间。

## 🔴 推送失败 30 秒决策树（先归因，禁止盲试）

```
git push 失败
├─ 401 Bad credentials → 凭据问题
│   ├─ git credential fill 查返回的是哪把（只看用户名/长度，不打印值）
│   ├─ 常见根因：Windows 凭据管理器（manager helper）残留已吊销旧 PAT，
│   │  排在自建凭据库之前被 git 优先采用 → "昨天能推今天 401" 的元凶
│   └─ 解法：-c credential.helper= 清链 + 内联 helper（见下方模板）；
│      或控制面板→凭据管理器→Windows 凭据，删除对应 github.com 旧条目
├─ 挂死/超时/schannel 断连 → 通道问题（代理掐 git 传输）
│   ├─ curl 走代理通 ≠ git 能通：git 传输走的是另一条 POST 通道
│   └─ 解法：no_proxy="<远端域名>" 直连推送
└─ API 验活大面积 401/40013 → 取值姿势问题
    └─ get_secret.py --show 输出带 "value: " 前缀，脚本把前缀连令牌一起发
       解法：一律 --raw 取裸值（见 dpapi-local-vault 技能）
```

## ✅ 正确推送模板（2026-09-07 实测定版）

凭据只走环境变量，**绝不进命令行参数 / 日志 / 截图**：

```bash
export GT=$(python <skills目录>/dpapi-local-vault/get_secret.py github_api_key --raw | tr -d '\r\n')
GIT_TERMINAL_PROMPT=0 no_proxy="github.com" NO_PROXY="github.com" \
  git -c credential.helper= \
      -c 'credential.helper=!f() { echo username=<用户名>; echo password=$GT; }; f' \
      -c http.version=HTTP/1.1 \
      push <远端URL> main --force
```

- `-c credential.helper=` 必须有：清掉默认 helper 链，否则凭据管理器的死旧 PAT 抢先。
- `no_proxy` 必须有（沙箱/企业代理环境）：代理放行 API 域不代表放行 git 传输。
- 三个远端实测：GitHub `no_proxy=github.com`；Gitee `no_proxy=gitee.com`（默认 helper 链即可用）；AtomGit `no_proxy=atomgit.com,gitcode.com`（后端是 gitcode，同一模板换用户名/令牌标签）。
- GitLink 用 Bearer 头验活（private_token query 形式无效）；HuggingFace 直连被墙走 hf-mirror.com。

## 探测先行（1 秒定通路）

```bash
curl -s --noproxy '*' -o /dev/null -w "%{http_code}" https://github.com   # 200=直连通
```

- 200 → 用上面模板直接推；持续非 200/超时 → 走下方 API 兜底通道。
- ⚠️ 2026-09-07 下午实证：**git 直连推送本来就通**（内联 helper + no_proxy）。此前"唯一通路=沙箱代理"的结论是在 helper 链被死 PAT 污染 + 未去代理双重干扰下得出的，**作废**。

## API 兜底通道（直连也不通时才用）

适用判据：探测持续非 200，但 `curl https://api.github.com/...` 走代理返回 200。

1. **空仓库先落初始提交**：直接建 blob 会 409 "Git Repository is empty"。先 `PUT /repos/{o}/{r}/contents/README.md` 创建首提交。
2. **取 README 真 blob sha**：`GET /contents/README.md` 顶层 `sha` 字段。⚠️ 首提交的 `tree.sha` 不是 blob sha，拿它当 blob 会 422 "not a valid blob"。
3. **其余文件建 blob**：`POST /git/blobs`，`{content: base64, encoding: "base64"}`，二进制（zip/png）同样适用。
4. **建树**：`POST /git/trees`，`{base_tree: <首提交tree.sha>, tree: [{path, mode:"100644", type:"blob", sha}...]}`。
5. **提交+推引用**：`POST /git/commits`（parents=首提交）→ `PATCH /git/refs/heads/main`。
6. 中文/非 ASCII 路径必须 `urllib.parse.quote()` 编码后拼 URL，否则 `UnicodeEncodeError: 'ascii' codec`。
7. 令牌从本地保险库取（`--raw`），只驻内存。

## 各远端差异速查（2026-09-07 实测）

| 远端 | git push | API 验活 | 坑 |
|---|---|---|---|
| GitHub | 内联 helper + no_proxy=github.com | Bearer/token 头 | helper 链可能吐死旧 PAT；api.github.com 走代理可用 |
| Gitee | 默认 helper + no_proxy=gitee.com | `access_token` query | 建仓默认私有，PATCH private=false（公开需实名）；匿名 403 是反爬 |
| AtomGit | 内联 helper + no_proxy=atomgit.com,gitcode.com | `access_token` query 或 Bearer | **后端是 gitcode.com**，API 复核去 api.gitcode.com |
| GitLink | — | Bearer 头 | private_token query 形式无效 |

## 发布平台附加坑（SkillHub 实测）

- 同 slug 同版本被拒 ≠ 被抢注：先 `search` 查归属，多半是自己此前批次发过 → bump patch 版本。
- 发布有频率限制：两次间隔 ≥65s。
- 市场包禁二进制图标（.png/.jpg/.svg 被白名单拒，错误 450033）：出市场版前剔除，源目录保留。
- frontmatter 需跨平台字段：slug/displayName/title/platforms；权属五件套（LICENSE/版权段/知识版权声明/免责声明/attestation）。
