# lgd-gate 使用示例

## 1. 列出 GATE 阶段全部门禁节点

```bash
python lgd_gate.py --list
```

输出 8 个门禁节点的 slug 与一句话用途。

## 2. 探测真实可用性（诚实分级）

```bash
python lgd_gate.py --verify --json-out evidence.json
```

逐节点探测：有目录 + 脚本 `--help` 退出码 0 → `LIVE`；路由声明但活动工作集无目录 →
`ECOSYSTEM`；脚本异常 → `ERROR`。结尾打印 `LIVE=x ECOSYSTEM=y ERROR=z`。

## 3. 查看单个门禁调用说明

```bash
python lgd_gate.py --route publish-quality-gate
```

## 4. 真实拦截怎么发生

本技能只路由。真实拦截由被路由的子技能执行，例如：

```bash
# 发布前对某个技能目录跑发布门
python ../publish-quality-gate/scripts/check_release.py <skill_dir>
```

退出码非 0 即未通过门禁，应阻断发布。
