---
name: ig50
description: 安装并使用 IG50 本地股票数据引擎。检测 IG50 是否已安装并引导完成授权部署，读取本地落盘的 JSON 行情、K线、L2、F10 数据（沪深京A股/沪深数据中心/基金/港股/美股），完成数据查询、筛选、分析与量化回测。Install and use the IG50 local stock data engine: detect installation, guide setup, and read local JSON market data (quotes, K-line, L2, F10) for analysis and backtesting.
---

# IG50 本地股票数据引擎

IG50 把全市场股票数据（沪深京A股 / 沪深数据中心 / 基金 / 港股 / 美股，共 331 个数据集）以 JSON 文本文件落盘到用户本地磁盘：本地读取零延迟、无并发限制、数据不出用户机器。本 skill 覆盖两件事：

1. **检测与安装**：判断本机是否已部署 IG50，未部署时引导用户完成授权与安装；
2. **数据使用**：为查询、筛选、分析、回测任务定位正确的数据集并正确读取本地数据。

## 第一步：先检测安装状态

运行只读检测脚本（纯标准库、零依赖、不改动系统）：

```bash
python scripts/check_install.py
```

- 退出码 0 = 已安装（脚本自动解析配置回显实际数据目录与数据就绪状态）→ 进入「数据使用」；
- 退出码 1 = 未安装 → 按「安装引导」处理。

也可手动判断：程序配置文件存在即视为已安装（Windows `C:\ig50\config\ig50_user_config.properties`，Linux `/opt/ig50/config/ig50_user_config.properties`）。

## 安装引导（执行任何安装命令前必须征得用户同意）

安装分「人工授权」与「脚本部署」两段，完整细节见 references/install.md：

1. **授权（人工步骤，不可代劳）**：IG50 按市场授权，新用户可申请 2 周免费试用。引导用户访问 [授权页面](https://ig50.com/license.html) 或邮件 service@ig50.com，获取 `user` 与 `market` 两个授权参数。
2. **部署（系统级操作，先确认再执行）**：
   - Linux：一行 wget 命令自动安装（root 或 sudo），安装脚本会提示填入 user/market，输出"IG50 安装成功且服务已正常运行！"即完成；
   - Windows：下载 ig50_bat.zip 解压后以管理员运行，**安装前务必提醒用户关闭杀毒软件**；
3. **验证**：重跑 check_install.py，确认数据目录开始产出文件；服务状态查询命令见 install.md。

服务器要求速记：按授权市场 8 核 / 16GB 内存，A股与港股硬盘 200GB、美股 600GB，x86 64 位，建议国内云服务器。详见 references/install.md。

## 数据使用

**数据根目录**（下称 DATA_DIR）：权威来源是程序配置文件 `ig50_user_config.properties` 的 `server.data.dir`（配置文件位于 Windows `C:\ig50\config\`、Linux `/opt/ig50/config/`）；未指定时才使用缺省值（Windows `C:\ig50-data`，Linux `/ig50-data`）。运行 scripts/check_install.py 会自动解析配置并回显实际 DATA_DIR。一切数据路径都相对它。

**读取前必验证**：程序按定时任务更新数据，安装成功不等于立即有数据——没到定时任务执行时间时数据目录可能是空的。因此每次读取前先确认目标路径的文件确实存在。文件不存在时先区分原因：目标路径的一级前缀目录（如 `all/zjlx`）在 DATA_DIR 下**不存在** → 本机未部署该类目/市场的数据（对照 check_install.py 输出的"本机数据范围"），如实告知用户该数据在本机不可用；前缀目录**存在**但文件缺失 → 多为尚未到定时任务执行时间，向用户说明并稍后重试。

### 1. 找数据集

读 references/datasets.md（全部 331 个数据集目录表，按市场分组）：

- 按任务需求选中数据集，取「本地路径」列，把 `{股票代码}` 等占位符换成实际值（如 000001、600519）；
- 「更新频率」列决定数据新鲜度口径，回答数据问题时注明。

### 2. 读字段详情（按优先级尝试）

1. **官方 LLM 文档**（首选，每个数据集一份 Markdown，含字段表与示例）：
   `https://ig50.com/md/{锚点}.md`，锚点取目录表「文档锚点」列（形如 `index_fhrz/fhrz-dividend-title`）；
2. **官网数据集说明页**（备选）：把锚点按 `/` 拆开，访问 `https://ig50.com/{page_key}.html?maodian={maodian}`；
   也可在 [数据检索](https://ig50.com/search.html) 按数据集名称搜索直达；
3. **仍查不到时**：继续调研（检索页换关键词、翻同页面相关数据集），或如实告知用户该字段暂无法确认。**严禁猜测字段含义**，也不得凭本地 JSON 内容反推语义——字段语义只认官方文档。

### 3. 代码模板

- 高频数据集（股票列表 / 实时行情 / K线）字段速查与 K线级别表：references/data-formats.md
- 可直接改写的 Python 读取与回测模板（含 DATA_DIR 解析）：references/recipes.md

## 硬性约定

- 数据获取只用本地文件 I/O，不联网请求数据接口；联网仅用于拉取上述文档。
- 每次读取数据前，先验证目标文件存在（定时任务未到执行时间目录可能为空）。
- 读文件一律 `encoding="utf-8"`；对数据目录只读，不写入、不移动、不清理任何数据文件。
- JSON 有三种形态（数组 / 单对象 / 带分类键的对象），解析前先看 references/data-formats.md。
- 字段含义只认官方文档（md 文档 / 官网说明页 / 检索页），不知道就继续调研，绝不猜测；按文档字段名取值为空时，先核对本地 JSON 的实际键名（键名以落盘数据为准，见 data-formats.md 的实测校正注记）。
- 涉及实时行情注意：非交易时间文件不更新属正常，判断新鲜度用「更新频率 + 文件修改时间」一起说明。
- 引用数据时给出处（数据集名 + 本地路径），便于用户核对。

---
由 IG50 官方生成管线自动生成，请勿手改；内容以官网文档为最新权威。
