---
name: dpapi-local-vault
slug: dpapi-local-vault
displayName: 本地 DPAPI 免口令凭据库（Windows）
description: 用 Windows DPAPI 把密钥/口令加密存到本机、仅当前用户可解、明文不落盘、带权限锁与泄漏标注的可复用凭据保管 skill。适合"当前 Windows 账号即信任边界"的本地保管场景。
version: 1.0.0
license: MIT
platforms: [Windows]
author: 老二(Paredros)
category: 安全工具
tags: [凭据管理, DPAPI, 本地加密, 免口令, Windows, 密钥保管]
agent_created: true
---

# 本地 DPAPI 免口令凭据库（Windows）

## 何时用
- 需要在**本机**安全保管一把密钥/口令（如云 API 密钥对、token），且信任边界就是"当前 Windows 登录用户"。
- 想要**免口令**体验：DPAPI 由系统用当前用户凭据透明加解密，无需记忆主口令。
- 不想把明文写进任何文件/日志/云文档；落盘只有 DPAPI 密文 + base64 封装。
- 需要给凭据打**泄漏标注**（如"已在聊天明文暴露、待轮换"），供后续取用前警告。

## 何时不用
- 跨设备/跨账号同步 → 用 `unified-credential-vault`（带主口令、可恢复、全生态同读）。
- 需要多人共享或换机可解 → DPAPI 绑定本机本用户，换机/换账号解不开。
- 极高密级且担心"同账号被拖" → DPAPI 仅防其他用户/其他机，同账号可读，应上主口令保险库。

## 用法
默认保险库目录：`~/.ucvault_local`（即 `C:\Users\<你>\.ucvault_local`）。

### 推荐入口：key_drop.py（密值不进命令行、不进历史）
`~/.ucvault_local/tools/key_drop.py`。三种模式，都不把密值写进命令行参数：

```bash
# 1) 单值，隐藏输入（Git Bash / 支持 tty 的终端）
python ~/.ucvault_local/tools/key_drop.py hunyuan_api_key

# 2) 成对密钥对（如云 SecretId + SecretKey）
python ~/.ucvault_local/tools/key_drop.py tencent_cos --pair

# 3) 记事本模式（最保险，任何终端都能用，密值走 GUI 不经过终端）
python ~/.ucvault_local/tools/key_drop.py tencent_cos --pair --notepad
```

- **模式 3 是最稳的**：不依赖终端能力，密值只经过记事本，导入后临时文件立即删除。
  终端不支持隐藏输入、或旁边有人/在录屏时，一律用它。
- `vault put <label>`（vault.py 自带）只能存**单值**，存不了 SecretId+SecretKey 成对——成对请用 key_drop `--pair`。
- ⚠️ 坑：`getpass.getpass()` 在**无 tty** 环境（管道、CI、部分 Windows 终端）不会抛异常，
  而是挂等 `/dev/tty` 导致命令卡死。先判 `sys.stdin.isatty()` 再决定走 getpass，
  否则退回 `stdin.readline()` 并明确警告用户"输入会显示"。

### 兜底：直接调 store_secret.py（heredoc）
⚠️ heredoc 里的密值会进终端回滚缓冲区与屏幕，仅在无法用 key_drop 时采用：

```bash
python store_secret.py tencent_cos --scope secret --notes "腾讯云COS" \
  --exposed --exposed-where "WorkBuddy聊天" --exposed-at "2026-08-28" <<'EOF'
AKIDxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxKEY
EOF
# 两行 = 密钥对（SecretId / SecretKey）；单行 = 单值
# 输出 STORED_OK 即成功（回环校验通过，不打印明文）
```
- 落盘：`~/.ucvault_local/<label>.enc`（DPAPI 密文）+ `<label>.meta.json`（作用域/泄漏标注）。
- 权限：`icacls /inheritance:r /grant:r <USER>:F` + `chmod 600`，仅当前用户可读。

### 取回
```bash
python get_secret.py tencent_cos            # 默认隐藏密值
python get_secret.py tencent_cos --show      # 显示明文（仅本机内存，不落盘）
```

## 安全要点（落地约束）
- **明文零落盘**：密钥只在 `CryptUnprotectData` 解密后的内存里短暂存在；文件里永远是 DPAPI 密文。
- **不回显**：`get_secret.py` 默认隐藏密值，`--show` 才显；store 的回环校验不打印明文。
- **密钥不进命令行**：密值走 stdin（heredoc），绝不用命令行参数传，防 `ps`/历史泄漏。
- **权限锁当前用户**：写入后立即去继承 + 仅授权当前用户完全控制。
- **泄漏标注**：`--exposed` 会在 meta.json 写 `EXPOSED_PENDING_ROTATION` + 暴露位置/时间，取用前先看到警告。

## 配套文件
- `store_secret.py` — 加密写入（读 stdin；两行=密钥对，单行=单值；可选泄漏标注）。
- `get_secret.py` — 解密取回（默认隐藏密值，`--show` 才显明文）。
- `tools/key_drop.py` — **推荐投递入口**：隐藏输入 / 成对 / 记事本三种模式。
- `vault.py` / `vault.cmd` — 薄封装（`put`/`get`/`list`/`rm`）；`put` 仅支持单值。

## 应用侧读取约定（三级兜底）
应用不要自己解析 `.enc`，统一按此优先级取，改轮换只需换源头、不动代码：

```
1. 环境变量          服务器部署 / CI
2. 本机保险库        ~/.ucvault_local（DPAPI）
3. 项目内文件        .llm_key / .cos.conf（仅兜底）
```

参考实现见 `medxpert-reg-mcp/cred.py`（`llm_key()` / `cos_cred()`，通过
`get_secret.py --show` 取字段，只取长度/布尔判断，绝不打印密值）。
要点：取密值的代码**永远不要 print 密值**，也不要把它写进日志或异常信息。

## 真实案例
本机保险库 `~/.ucvault_local/tencent_cos.enc`（Windows 即 `%USERPROFILE%\.ucvault_local\tencent_cos.enc`）即此法保管的一把腾讯云 COS 密钥（root 级，已标注 EXPOSED_PENDING_ROTATION，待用户在 CAM 禁用/轮换）。
