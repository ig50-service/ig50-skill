# Python 读取与回测模板

以下模板可直接改写使用。数据根目录下称 DATA_DIR（Windows 默认 `C:\ig50-data`，Linux 默认 `/ig50-data`）。

## 0. 定位数据根目录

数据根目录以配置文件 `ig50_user_config.properties` 的 `server.data.dir` 为准（安装时已写入）；
未指定时才使用缺省值（Windows `C:\ig50-data`，Linux `/ig50-data`）。

```python
import os

def _parse_server_data_dir(config_path):
    value = None
    key = "server.data.dir"
    with open(config_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("!"):
                continue
            if not line.startswith(key):
                continue
            rest = line[len(key):]
            if rest[:1] in ("=", ":"):
                val = rest[1:].strip().replace("\\:", ":").replace("\\\\", "\\")
                if val:
                    value = val
    return value

def find_data_dir():
    for c in (r"C:\ig50\config\ig50_user_config.properties",
              "/opt/ig50/config/ig50_user_config.properties"):
        if os.path.isfile(c):
            d = _parse_server_data_dir(c)
            if d:
                return d
            break  # 找到配置但未指定 server.data.dir，回退缺省值
    for d in (r"C:\ig50-data", "/ig50-data"):
        if os.path.isdir(d):
            return d
    raise FileNotFoundError("未找到 IG50 数据目录，请先运行 scripts/check_install.py 检测")

DATA_DIR = find_data_dir()
```

注意：程序按定时任务更新数据，安装成功后没到执行时间时目录可能为空。
**每次读取前先确认目标文件存在**（`os.path.isfile`），不存在不是故障，稍后重试即可。

## 1. 读取股票列表（base/gplist）

```python
import json
import os

with open(os.path.join(DATA_DIR, "base", "gplist"), "r", encoding="utf-8") as f:
    stocks = json.load(f)

print(f"共 {len(stocks)} 只股票")
for s in stocks[:5]:
    print(s.get("dm"), s.get("mc"), s.get("jys"))
```

`dm` 代码、`mc` 名称、`jys` 交易所（sh 上证 / sz 深证 / bj 北证）。完整字段见 references/data-formats.md。

## 2. 读取实时行情（time/real/{代码}）

```python
import json
import os

path = os.path.join(DATA_DIR, "time", "real", "000001")
with open(path, "r", encoding="utf-8") as f:
    q = json.load(f)

print(q.get("dm"), q.get("mc"), "现价", q.get("p"), "涨跌幅", q.get("pc"))
```

## 3. 读取 K线（time/real/time/{代码}/{级别}）

```python
import json
import os

# 级别参数见 references/data-formats.md 的 K线级别表
path = os.path.join(DATA_DIR, "time", "real", "time", "000001", "Day")
with open(path, "r", encoding="utf-8") as f:
    k = json.load(f)

print(k.get("d"), "开", k.get("o"), "高", k.get("h"), "低", k.get("l"), "收", k.get("c"))
```

## 4. 全市场批量回测骨架

```python
import json
import os
import time

def load_kline(code, level="Day"):
    path = os.path.join(DATA_DIR, "time", "real", "time", code, level)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

start = time.time()
results = []
with open(os.path.join(DATA_DIR, "base", "gplist"), "r", encoding="utf-8") as f:
    stocks = json.load(f)

for s in stocks:
    code = s.get("dm")
    k = load_kline(code, "Day")
    if not k:
        continue
    # 在此处替换为你的策略逻辑
    results.append({"dm": code, "mc": s.get("mc"), "close": k.get("c")})

print(f"处理 {len(results)} 只，耗时 {time.time() - start:.2f} 秒")
```

注意：本地单文件为最新快照（存量历史 K线序列以官网对应数据集文档说明为准），批量任务建议先小样本验证再全量跑。

## 5. pandas 快速分析

```python
import json
import os
import pandas as pd

with open(os.path.join(DATA_DIR, "base", "gplist"), "r", encoding="utf-8") as f:
    df = pd.DataFrame(json.load(f))

print(df["jys"].value_counts())
print("科创板数量:", (df["isKcb"] == 1).sum())
```

## 6. 其他数据集的通用读法

1. 在 references/datasets.md 目录表按需求找到数据集，拿到本地路径与更新频率；
2. 按 SKILL.md 的优先级拉取该数据集文档，确认 JSON 形态与字段含义；
3. 路径中的 `{股票代码}` 替换为实际代码后用同样的 `open + json.load` 读取。

```python
import json
import os

def read_dataset(rel_path):
    """rel_path 形如 time/f10/dividend/000001（来自目录表，占位符已替换）"""
    path = os.path.join(DATA_DIR, *rel_path.split("/"))
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
```
