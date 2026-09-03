# 数据格式与字段速查

## JSON 三种形态

落盘数据均为 JSON 文本，解析前先分辨形态：

| 形态 | 结构 | 读取方式 |
|------|------|---------|
| 数组 | `[{...}, {...}]` | 遍历列表，每元素一条记录 |
| 单对象 | `{...}` | 直接取键 |
| 带分类键的对象 | `{"分类A": [{...}], "分类B": [...]}` | 先取外层键再遍历 |

通用守则：`encoding="utf-8"` 读取；对数据目录只读；单文件过大时用 `ijson` 流式解析或按需读取。

## 高频数据集字段速查

以下字段表由官网文档解析生成，与线上文档一致；其余数据集字段请按 SKILL.md 的优先级拉取对应文档。


### 沪深京A股列表

本地路径：`base/gplist`

| 字段 | 类型 | 说明 |
|---|---|---|
| dm | string | 股票代码（如：000001） |
| mc | string | 股票名称（如：平安银行） |
| jys | string | 交易所（"sh"表示上证/"sz"表示深证/"bj"表示北证） |
| isCyb | number | 是否属于创业板（0否/1是） |
| isKcb | number | 是否属于科创板（0否/1是） |
| isSt | number | 是否ST（0否/1是） |
| isNew | number | 是否是新股（0否/1是） |


### 实时行情数据（3秒落盘）

本地路径：`time/real/{股票代码}`

| 字段 | 类型 | 说明 |
|---|---|---|
| dm | string | 代码 |
| mc | string | 名称 |
| t | string | 更新时间（yyyy-MM-ddHH:mm:ss） |
| sud | string | 数据时间（yyyy-MM-ddHH:mm:ss） |
| p | number | 当前价格（元） |
| yc | number | 昨收价（元） |
| o | number | 开盘价（元） |
| h | number | 最高价（元） |
| l | number | 最低价（元） |
| jp | number | 均价（元，成交量加权平均价） |
| ud | number | 涨跌额（元） |
| pc | number | 涨跌幅（%） |
| zf | number | 振幅（%） |
| bpl | number | 涨停价（元） |
| spl | number | 跌停价（元） |
| v | number | 成交量（股） |
| lv | number | 现量（最新一笔成交量，手） |
| cje | number | 成交额（元） |
| kje | number | 开盘金额（元，集合竞价阶段的成交金额） |
| lb | number | 量比 |
| hs | number | 换手率（%） |
| lzs | number | 量涨速（%，成交量变化速率） |
| zs | number | 涨速（%） |
| dhs | number | 短换手（%，短周期换手率） |
| sz | number | 总市值（元） |
| lt | number | 流通市值（元） |
| ts | number | 总股本（万股） |
| fs | number | 流通股本（万股） |
| ped | number | 市盈率（动态） |
| pettm | number | 市盈率TTM（滚动市盈率） |
| pes | number | 市盈率（静态） |
| sjl | number | 市净率 |
| eps | number | 每股收益（元） |
| na | number | 每股净资产（元） |
| dyp | number | 股息率（%） |
| lzds | number | 连续涨跌天数（正数=连涨，负数=连跌） |
| nzt | number | 年内涨停天数 |
| np | number | 内盘（主动卖成交量，手） |
| wp | number | 外盘（主动买成交量，手） |
| szab | number | AB股总市值（元） |
| yysr | number | 营业收入（万元） |
| z20 | number | 20日涨幅（%） |
| ytd | number | 年初至今涨幅（%） |
| mtd | number | 月初至今涨幅（%） |
| z1y | number | 年内涨幅（%） |
| z1 | number | 昨日涨幅（%） |
| z2 | number | 前日涨幅（%） |
| z3 | number | 3日涨幅（%） |
| z5 | number | 5日涨幅（%） |
| z10 | number | 10日涨幅（%） |
| z60 | number | 60日涨幅（%） |
| jabl | number | 连续竞价买入上限（元，涨停价约束） |
| jasl | number | 连续竞价卖出下限（元，跌停价约束） |
| javr | number | 竞价昨比（集合竞价量与昨日同期量的比值） |
| ah | string | AH股对应代码（A股对应H股代码） |
| c10 | number | 日内涨幅%10:00 |
| c1030 | number | 日内涨幅%10:30 |
| c11 | number | 日内涨幅%11:00 |
| c1130 | number | 日内涨幅%11:30 |
| c1330 | number | 日内涨幅%13:30 |
| c14 | number | 日内涨幅%14:00 |
| c1430 | number | 日内涨幅%14:30 |


### 最新K线

本地路径：`time/real/time/{股票代码}/{分时级别}`

| 字段 | 类型 | 说明 |
|---|---|---|
| d | string | 交易时间（短分时级别格式为yyyy-MM-ddHH:mm:ss，日线及以上级别为yyyy-MM-dd） |
| ud | string | 更新时间（短分时级别格式为yyyy-MM-ddHH:mm:ss） |
| o | number | 开盘价（元） |
| h | number | 最高价（元） |
| l | number | 最低价（元） |
| c | number | 收盘价（元） |
| v | number | 成交量（股） |
| e | number | 成交额（元） |
| zf | number | 振幅（%） |
| hs | number | 换手率（%） |
| zd | number | 涨跌幅（%） |
| zde | number | 涨跌额（元） |
| sz | number | 昨收价（元） |

> **实测校正**（基于真实落盘数据样本，A股与港股 K线键集合一致）：最新 K线 JSON 中昨收价的实际键名为 `zs`（上表照录官网文档的 `sz` 与落盘不符，取值以落盘的 `zs` 为准，数值经 收盘价/(1+涨跌幅%) 反推核验一致）；落盘数据另含官网文档未列出的键 `ltgb`（流通股本，股）。按文档字段名取值为空时，先核对本地 JSON 的实际键名。


## K线级别

A股与港股 K线支持以下 19 种级别（美股 K线级别与 A股一致）：

| 类别 | 级别参数 |
|------|---------|
| 分钟级别 | `5` `15` `30` `60` |
| 日线 | `Day`（不复权） `Day_qfq`（前复权） `Day_hfq`（后复权） |
| 周线 | `Week` `Week_qfq` `Week_hfq` |
| 月线 | `Month` `Month_qfq` `Month_hfq` |
| 季线 | `Quarter` `Quarter_qfq` `Quarter_hfq` |
| 年线 | `Year` `Year_qfq` `Year_hfq` |

基金 K线仅支持 `Day` `Week` `Month` `Quarter` `Year` 5 种级别（无复权）。

K线路径：`time/real/time/{股票代码}/{级别}`，如 `time/real/time/000001/Day`。

历史深度：A股短分时两年；港股、美股短分时 4 万根 K线；日线及以上为全部历史。

## 日期与时间格式

- 短分时级别字段 `d`：`yyyy-MM-dd HH:mm:ss`；
- 日线及以上级别字段 `d`：`yyyy-MM-dd`；
- 实时行情字段 `t`：`yyyy-MM-dd HH:mm:ss`。

## 数据新鲜度判断

- 每个数据集的更新频率以 references/datasets.md「更新频率」列为准；
- 程序 24 小时运行，每天凌晨自动检查、修正数据；
- 非交易时间实时行情文件不更新属正常现象；判断新鲜度时组合「更新频率 + 文件修改时间」陈述，不要单凭 mtime 断言数据过期。
