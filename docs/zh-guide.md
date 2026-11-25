# 中文导读 · agent-skills

> 五分钟读完：这些技能怎么按三律分类、哪些会被门禁拦下、装进来之后怎么自检。

## 一、这是什么

本仓把 LGD/UIBC 的治理能力**装进通用 Agent 技能生态**（skills.sh 兼容），让任何支持技能包的 Agent 都能直接调用"登记 / 证据 / 门禁"三类能力，不必自己重写一遍。

## 二、三类技能，对应三律

| 类别 | 干什么 | 对应律 |
|---|---|---|
| **登记类** | 给 agent 或技能登记身份、能力声明、版本 | 有籍 |
| **证据类** | 把一次执行打包成证据、封签、供离线复核 | 有证 |
| **门禁类** | 在越权触点判定放行 / 拒绝 / 待确认 | 有门禁 |

**门禁类技能是本仓与别家技能库最不一样的地方**：技能不是"功能清单"，而是**发布前要先过门的资产**。

## 三、哪些技能会被拦下（关键）

skillgate 用 600+ 条规则、25 类风险、17 种语言做发布前门禁。最常见的拦截原因有四条：

1. 声明了网络或文件写入能力，但没有声明数据流向；
2. 依赖未固定版本（下次安装可能换成另一个包）；
3. 提示词里含"忽略以上指令"一类可被劫持的句式；
4. 没有失败处理路径——出错时静默返回空结果（这是最危险的一类）。

## 四、装进来之后怎么自检

```bash
# 1) 先看清它属于哪一律、要什么权限
sed -n '1,40p' <skill>/SKILL.md

# 2) 用 skillgate 过一遍（不联网）
skillgate check <skill>

# 3) 关键动作前，把证据打包并复核
python -m uibc_core.cli submit --path <pkg> --key <key>
```

## 五、与另外两仓的关系

| 仓 | 角色 |
|---|---|
| [lgd-theory](https://github.com/zhaoxinghua09-cell/lgd-theory) | 定义三律（理论 SSOT）与[中文导读](https://github.com/zhaoxinghua09-cell/lgd-theory/blob/main/docs/zh-guide.md) |
| [uibc-core](https://github.com/zhaoxinghua09-cell/uibc-core) | 机器可校验执行层（[中文导读](https://github.com/zhaoxinghua09-cell/uibc-core/blob/main/docs/zh-guide.md)） |
| **agent-skills**（本仓） | 技能层：把上面两层装进通用生态 |

## 六、照实说的缺口

- 技能数量动态变化，以仓内清单为准，本文不重复具体计数。
- **门禁规则的命中率尚无公开基准**——这是下一步要补的数字，不在这里编。
- 中文专栏《凡自治之物》尚未发布，正式链接待回填。

*2026-11-19 写。*
