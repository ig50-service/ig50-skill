<!-- IG50 官方 Agent Skill -->

<div align="center">

# IG50 Agent Skill

**让本地 Agent 会装 IG50、更会用 IG50 的数据**

[官网首页](https://ig50.com) ｜ [数据集文档](https://ig50.com/dataset-overview.html) ｜ [数据检索](https://ig50.com/search.html) ｜ [获取授权](https://ig50.com/license.html)

GitHub：https://github.com/ig50-service/ig50-skill ｜ Gitee：https://gitee.com/igtrade/ig50-skill

</div>

---

## 这是什么

[IG50](https://ig50.com/home.html) 是本地运行的股票数据引擎：331 个数据集覆盖沪深京A股、沪深数据中心、基金、港股、美股，行情与档案数据以 JSON 文本文件持续落盘到用户本地，读取零延迟、无并发限制、策略不出本地。

本仓库提供标准 **Agent Skill**（SKILL.md 格式）。安装到你的本地 Agent（Claude Code 等）后，Agent 可以：

- 检测本机 IG50 部署状态（数据目录、股票列表、行情文件新鲜度）；
- 未部署时引导你完成授权申请与脚本安装（含 Windows 关杀毒提醒、服务验证）；
- 按任务需求在 331 个数据集中定位正确的数据集与路径，拉取字段文档，写出正确的读取与回测代码。

## 安装 Skill

将本仓库克隆为名为 `ig50` 的目录，放入 Agent 的 skills 目录即可：

```bash
# Claude Code（用户级，对所有项目生效）
git clone --depth 1 https://github.com/ig50-service/ig50-skill ig50 ~/.claude/skills/ig50

# 或项目级（仅当前项目生效）
git clone --depth 1 https://github.com/ig50-service/ig50-skill ig50 .claude/skills/ig50
```

Gitee 用户把克隆地址换成 https://gitee.com/igtrade/ig50-skill 即可，两个仓库内容一致。

## 前提

- 使用数据需要 IG50 授权（按市场开通，新用户可申请 2 周免费试用）：https://ig50.com/license.html
- 无授权也可以先安装 skill，Agent 会引导你完成申请与部署。

## 试试对 Agent 说

- 「检测一下 IG50 装好了没有」
- 「看看今天主力净流入排名前 10 的股票」
- 「用本地日线数据写个双均线策略回测平安银行」
- 「读取贵州茅台的分红记录」

## 目录结构

| 文件 | 作用 |
|------|------|
| `SKILL.md` | skill 入口：检测 → 安装 → 数据使用的工作流 |
| `references/install.md` | 安装指引：授权、服务器要求、分平台命令、验证、排障 |
| `references/datasets.md` | 全部 331 个数据集目录表（名称/路径/更新频率/文档锚点） |
| `references/data-formats.md` | JSON 形态、高频字段速查、K线级别、日期格式 |
| `references/recipes.md` | Python 读取与回测代码模板 |
| `scripts/check_install.py` | 只读安装检测脚本（零依赖） |

## 相关仓库

- [ig50-official](https://github.com/ig50-service/ig50-official)（GitHub）/ [ighub](https://gitee.com/igtrade/ighub)（Gitee）：IG50 文档镜像站（安装包下载、331 个数据集文档）

## 许可

本仓库内容（文档、示例代码、脚本）采用 CC BY-NC-SA 4.0 许可。IG50 软件本身的授权请参考[官网授权页面](https://ig50.com/license.html)。

---

<div align="center">

© 2026 ig50.com · 数据本地落盘，策略再无牵绊

</div>
