#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""IG50 本地环境检测脚本（只读、零依赖、不改动系统）

判定依据（与官方安装脚本行为对齐）:
    1. 已安装 = 程序配置文件存在（Windows C:\ig50\config\ig50_user_config.properties，
       Linux /opt/ig50/config/ig50_user_config.properties）；
    2. 数据目录 = 配置文件 server.data.dir 指定的目录（安装脚本必定写入该行；该行
       缺失时才回退缺省值 Windows C:\ig50-data、Linux /ig50-data）；
    3. 数据是否就绪必须实际抽查目标目录——程序按定时任务更新，安装成功不代表
       立即有数据，没到定时任务执行时间时数据目录可能为空。

用法:
    python check_install.py [--data-dir 目录]

输出:
    人类可读检查明细，最后一行 RESULT_JSON: 开头的 JSON 摘要（供 Agent 解析）。
    退出码: 0 = 已安装; 1 = 未安装。数据是否就绪看 JSON 的 data_ready 字段。
"""

import argparse
import json
import os
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def detect_platform():
    if os.name == "nt":
        return "windows", r"C:\ig50", r"C:\ig50-data"
    return "linux", "/opt/ig50", "/ig50-data"


def parse_server_data_dir(config_path):
    # 解析配置文件的 server.data.dir（取最后一次出现的有效值）；
    # 兼容等号/冒号分隔、反斜杠转义与 Windows 正斜杠写法
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
                val = rest[1:].strip()
            else:
                continue
            val = val.replace("\\:", ":").replace("\\\\", "\\")
            if val:
                value = val
    return value


def newest_mtime(path):
    mt = None
    try:
        mt = os.path.getmtime(path)
    except OSError:
        pass
    return mt


def sample_dir(path):
    """抽查目录：顶层条目数与最新文件修改时间"""
    try:
        names = os.listdir(path)
    except OSError:
        return 0, None
    newest = None
    for name in names:
        mt = newest_mtime(os.path.join(path, name))
        if mt and (newest is None or mt > newest):
            newest = mt
    return len(names), newest


def data_scope(path):
    """枚举本机已落盘的数据范围：顶层目录 -> 二级类目清单（超40个截断）"""
    scope = {}
    try:
        tops = sorted(os.listdir(path))
    except OSError:
        return scope
    for name in tops:
        p = os.path.join(path, name)
        if not os.path.isdir(p):
            continue
        try:
            subs = sorted(os.listdir(p))
        except OSError:
            subs = []
        count = len(subs)
        if count > 40:
            subs = subs[:40]
        scope[name] = {"count": count, "sample": subs}
    return scope


def main():
    ap = argparse.ArgumentParser(description="IG50 本地环境检测（只读）")
    ap.add_argument("--data-dir", default=None, help="手动指定数据根目录（跳过配置解析）")
    args = ap.parse_args()

    plat, program_dir, default_dir = detect_platform()
    config_file = os.path.join(program_dir, "config", "ig50_user_config.properties")

    print("IG50 环境检测（平台: %s）" % plat)
    print("=" * 50)

    result = {
        "platform": plat,
        "program_dir": program_dir,
        "config_file": config_file,
        "installed": False,
        "server_data_dir_specified": None,
        "data_dir": None,
        "data_ready": False,
        "data_top_entries": None,
        "gplist_present": None,
        "gplist_count": None,
        "realtime_code_files": None,
        "realtime_latest_mtime": None,
    }

    config_ok = os.path.isfile(config_file)
    print("[%s] 程序目录: %s" % ("OK " if os.path.isdir(program_dir) else "--", program_dir))
    print("[%s] 配置文件: %s" % ("OK " if config_ok else "--", config_file))
    if not config_ok:
        print("-" * 50)
        print("结论: 未检测到 IG50 安装（找不到程序配置文件）。")
        print("提示: 请按 references/install.md 引导用户完成授权与安装。")
        print("RESULT_JSON:" + json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    result["installed"] = True
    specified = parse_server_data_dir(config_file)
    result["server_data_dir_specified"] = specified
    data_dir = args.data_dir or specified or default_dir
    result["data_dir"] = data_dir
    if specified:
        print("[OK ] 数据目录（配置 server.data.dir 指定）: %s" % data_dir)
    else:
        print("[-- ] 配置未指定 server.data.dir，使用缺省数据目录: %s" % data_dir)

    top_count, newest = sample_dir(data_dir)
    result["data_top_entries"] = top_count
    result["data_ready"] = top_count > 0
    age = int((time.time() - newest) / 60) if newest else None
    print("[%s] 数据目录抽查: %d 个顶层条目%s" % (
        "OK " if result["data_ready"] else "--", top_count,
        ("，最新修改于 %d 分钟前" % age) if age is not None else ""))

    scope = data_scope(data_dir)
    result["data_scope"] = scope
    if scope:
        print("本机数据范围（顶层目录 -> 二级类目）:")
        for name in sorted(scope):
            info = scope[name]
            print("  %s/ -> %d 个: %s" % (
                name, info["count"], "、".join(info["sample"]) + ("…" if info["count"] > 40 else "")))

    gplist_path = os.path.join(data_dir, "base", "gplist")
    gplist_ok = os.path.isfile(gplist_path)
    count = None
    if gplist_ok:
        try:
            with open(gplist_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                count = len(data)
            else:
                gplist_ok = False
        except Exception:
            gplist_ok = False
    result["gplist_present"] = gplist_ok
    result["gplist_count"] = count
    print("[%s] base/gplist（A股列表抽查）: %s" % (
        "OK " if gplist_ok else "--",
        ("股票列表 JSON，%s 条" % count) if count is not None
        else ("不存在——仅授权港股/美股时不生成此文件，属正常" if not gplist_ok else gplist_path)))

    real_dir = os.path.join(data_dir, "time", "real")
    code_files, _ = sample_dir(real_dir)
    result["realtime_code_files"] = code_files
    result["realtime_latest_mtime"] = newest_mtime(real_dir)
    print("[%s] 实时行情目录抽查: %s（%d 个文件）" % (
        "OK " if code_files > 0 else "--", real_dir, code_files))

    print("-" * 50)
    if result["data_ready"]:
        print("结论: IG50 已安装，数据目录有数据。读取前仍须验证目标文件存在。")
    else:
        print("结论: IG50 已安装，但数据目录暂无数据。")
        print("说明: 程序按定时任务更新，未到执行时间时目录为空属正常，稍后重试。")
    print("提示: 服务状态可用 systemctl status ig50（Linux）"
          "或任务计划程序 IG50Service（Windows）查看。")

    print("RESULT_JSON:" + json.dumps(result, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
