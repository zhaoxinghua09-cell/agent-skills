# Agent Skills Collection（Agent 技能合集）

> 针对 GitHub 头部 Agent Skills 生态的实证弱点，提出并落地的一组差异化技能。方法论调研见 [`docs/`](docs/)。

## 这是什么

2026-09 对 GitHub 头部技能仓库（anthropics/skills、planning-with-files、claude-mem、distilly、alirezarezvani/claude-skills、addyosmani/agent-skills 等，头部集合仓库聚合数千个技能）做内容级弱点分析后，把自家已实战验证的技能按优先级整理发布。每个技能针对头部生态的一个实证弱点：

| 弱点（头部实证） | 对应技能 |
|---|---|
| 崩溃恢复只还原"文件快照"、跨项目被主动隔离 | **session-continuity-protocol** — 跨会话/跨工作区/跨项目连续性协议 |
| 记忆全量捕获无蒸馏、压缩有损丢过数据 | **ai-brain-learning-memory**（+pro）— 零丢失分层记忆蒸馏 |
| 本地服务无认证、API key 明文、无 secret 扫描 | **dpapi-local-vault** — DPAPI 密钥保险库 + 泄露哨兵 |
| 结构合规 ≠ 效果验证、无发布闸门 | **publish-quality-gate** — 四层敏感扫描 + TRACE 五维自测 |
| 无复盘→固化闭环 | **agent-evolution** — 复盘→固化进化飞轮 |
| 方法论碎片化 | **a3-law-operational** — AI 造 AI 三定律 |

## 目录

```
skills/    8 个技能源码包（7 个主题技能 + 1 个发布通道工具技能 github-api-push-workaround）
release/   对应的打包 zip（去敏质检后版本，含 MD5 台账）
docs/      头部弱点调研报告 + 发布质检台账
```

## 安装

任选其一：
- 直接复制 `skills/<name>/` 到你的 Agent 技能目录（如 `~/.workbuddy/skills/` 或 Claude Code 的 skills 目录）；
- 或使用 `release/<name>-v<version>.zip` 解压。

## 版本与署名

各技能版本与归属见其 SKILL.md frontmatter（版本 + author + license）。LGD 理论线技能（agent-evolution / a3-law-operational / ai-brain-learning-memory-pro）© SynomosAI，理论 CC BY 4.0（DOI 10.5281/zenodo.22456647），参照声明回链 [LGD-theory](https://github.com/zhaoxinghua09-cell/lgd-theory)。

## 链接与获取方式（全渠道）

| 渠道 | 入口 | 说明 |
|---|---|---|
| GitHub | https://github.com/zhaoxinghua09-cell/agent-skills | 主仓（本页），`git clone https://github.com/zhaoxinghua09-cell/agent-skills.git` |
| Gitee | https://gitee.com/stevenzhao26/agent-skills | 国内镜像，`git clone https://gitee.com/stevenzhao26/agent-skills.git` |
| AtomGit / GitCode | https://gitcode.com/gcw_PcK6ZWCL/agent-skills | 第三镜像，`git clone https://atomgit.com/gcw_PcK6ZWCL/agent-skills.git` |
| SkillHub 市场 | `skillhub install session-continuity-protocol` | 已上架 6 件：session-continuity-protocol / dpapi-local-vault / medxpert-brain-learning-memory / agent-evolution / a3-law-operational / publish-quality-gate（namespace `@user_8a3569c1`） |
| Hugging Face | https://huggingface.co/zhaoxinghua09/skills | 51 件批量镜像仓（2026-08-31 发布） |

- **快速安装（SkillHub）**：`skillhub install <skill-name> --namespace user_8a3569c1`
- **快速安装（手动）**：下载 `release/<name>-v<version>.zip` 解压到 `~/.workbuddy/skills/` 或 Claude Code 技能目录
- 三镜像同步发布，内容一致；以后更新以 GitHub 为主仓，Gitee/AtomGit 跟随。

## 踩坑实录：发布通道的根因与正确姿势（2026-09-07 实测）

本仓库发布过程中踩了一轮坑，把**根因**和**验证过的正确做法**固化在这里，避免后来者（包括未来的我们自己）重复踩：

| 现象 | 真正的根因 | 正确做法 |
|---|---|---|
| 令牌验活 200，`git push` 却 401 | Windows 凭据管理器（manager helper）残留一把**已吊销的旧 PAT**，排在自建凭据库之前被 git 优先采用 | `git -c credential.helper=` 清空 helper 链后挂内联 helper；或到「凭据管理器 → Windows 凭据」删除对应 github.com 旧条目 |
| 令牌没问题，`git push` 挂死超时（curl 却正常） | 沙箱/企业代理放行 API 域名，却掐断 git 传输通道 | `no_proxy="<远端域名>"` 直连推送，不走代理 |
| 一轮"令牌全失效"（401/40013），其实令牌全是好的 | 取值工具输出带 `value: ` 标签前缀，脚本把**前缀+令牌**整段当凭据用 | 脚本取值用 `--raw` 出裸值；用格式化输出必须按前缀截断 |
| 空仓库走 Git Data API 报 409 | 空仓库没有基线提交 | 先用 contents API 落一个初始提交，再 blob→tree→commit→ref |
| Gitee 建仓后匿名访问 404 | 新仓库默认私有 | PATCH `private=false` 转公开 |
| 同名同版本发布被拒，怀疑被抢注 | 多半是自己此前批次发过 | 先 `search` 查归属，再决定 bump patch 还是跳过 |

**正确推送模板**（凭据只走环境变量，不进命令行 / 日志 / 截图）：

```bash
export GT=$(python get_secret.py <label> --raw)     # 从本地保险库取令牌
git -c credential.helper= \
    -c 'credential.helper=!f() { echo username=<用户名>; echo password=$GT; }; f' \
    -c http.version=HTTP/1.1 push <远端URL> main
```

> 排查口诀：**先探测、再归因（401=凭据 / 超时=通道 / 大面积401=取值）、后重试**；禁止不归因连环盲试。完整决策树见 [`skills/github-api-push-workaround/`](skills/github-api-push-workaround/SKILL.md)。

## License

- 代码与文档：MIT（各包附 LICENSE）
- LGD 理论内容：CC BY 4.0

本仓库零数据收集、零遥测；技能均为本地优先设计。
