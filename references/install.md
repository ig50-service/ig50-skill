# IG50 安装指引

在用户服务器上部署 IG50 的完整流程。**执行任何安装命令前，先向用户确认**；授权参数必须由用户自行获取。

## 1. 获取授权（人工步骤）

- IG50 按市场（A股 / 港股 / 美股）授权，新用户可申请 2 周免费试用；
- 授权入口：https://ig50.com/license.html ｜ 客服邮箱：service@ig50.com；
- 授权参数为 `user`（授权用户 id）与 `market`（授权市场，可选值 CN / HK / US）两个值，安装时脚本会提示填入；
- 授权信息写入授权文件 `config/ig50.license`（Linux `/opt/ig50/config/`，Windows `C:\ig50\config\`）；
- 支持"先安装后补授权"：先跳过授权完成安装，之后把授权文件整体覆盖
  （Linux `/opt/ig50/config/ig50.license`，Windows `C:\ig50\config\ig50.license`），再重启程序生效。

## 2. 服务器要求

| 市场 | CPU | 内存 | 硬盘 |
|------|-----|------|------|
| A股 | 8 核心 | 16 GB | 300 GB |
| 港股 | 8 核心 | 16 GB | 300 GB |
| 美股 | 8 核心 | 16 GB | 800 GB |

- 指令集架构：x86 64 位；
- 以上为 IG50 专用配置，同机装其他程序请自行评估加配；
- 数据服务器集群在国内，为最低延迟建议国内云服务器；不推荐海外服务器；
- 每份授权对应一台独立服务器（每个市场至少几千只股票同时更新）。

已适配系统：

| 类型 | 系列 | 适配明细 | glibc 版本 |
|------|------|---------|-----------|
| Linux | Debian | Debian 11+、Ubuntu 22.04+（及 Linux Mint、Deepin、Kali 等） | >= 2.31（`ldd --version`） |
| Linux | CentOS | CentOS 9（及 RHEL 9、Rocky Linux 9、AlmaLinux 9、Fedora 等） | >= 2.34（`rpm -q glibc`） |
| Linux | SUSE | openSUSE 15.5+ | >= 2.31 |
| Windows | - | Windows 10（兼容 Windows 11 及 Windows Server 2016+） | - |

## 3. Linux 安装

以 root 或有 sudo 权限的用户执行。安装命令（任意目录下执行，会同时下载更新与卸载脚本）：

```bash
wget -qO ig50_shell.tar https://gitee.com/igtrade/ighub/releases/download/last/ig50_shell.tar && tar xf ig50_shell.tar && rm -f ig50_shell.tar && sed -i 's/\r$//' ./ig50_install.sh && chmod +x ./ig50_install.sh && ./ig50_install.sh
```

- 脚本会提示填入 `user` 与 `market` 授权参数；
- 输出"IG50 安装成功且服务已正常运行！"即安装完成；程序注册为系统服务，开机自启动，24 小时运行。

服务管理：

```bash
systemctl status ig50     # 状态
systemctl start ig50      # 启动
systemctl stop ig50       # 停止
systemctl restart ig50    # 重启
```

更新脚本：`./ig50_update.sh`；卸载脚本：`./ig50_uninstall.sh`。

## 4. Windows 安装

1. 下载安装包：https://gitee.com/igtrade/ighub/releases/download/last/ig50_bat.zip
2. **提醒用户临时关闭杀毒软件**（否则可能误报拦截）；
3. 解压到任意目录，以管理员身份运行 `ig50_install.bat`，按提示填入授权参数；
4. 程序注册为「任务计划程序」中的 `IG50Service`，开机自动后台运行。

服务管理（PowerShell，管理员）：

```powershell
Start-ScheduledTask -TaskName IG50Service    # 启动
Stop-ScheduledTask -TaskName IG50Service     # 停止
```

更新脚本 `ig50_update.bat`；卸载脚本 `ig50_uninstall.bat`。

## 5. 数据目录

- 数据存储目录在安装时可指定（安装脚本会指引）；未修改时默认：Linux `/ig50-data`，Windows `C:\ig50-data`；
- 程序默认安装目录（Linux `/opt/ig50`，Windows `C:\ig50`）不可修改；
- 安装后可改 `ig50_user_config.properties` 的 `server.data.dir` 参数（Linux `/opt/ig50/config/`，Windows `C:\ig50\config\`），保存后重启程序生效。

## 6. 安装验证

与官方安装脚本行为对齐的可靠验证方式：

1. **程序与配置**：安装目录下存在 `config/ig50_user_config.properties`
   （Linux `/opt/ig50/config/`，Windows `C:\ig50\config\`）即视为已安装；
2. **确定实际数据目录**：读取配置文件中的 `server.data.dir`——安装脚本必定写入该行
   （用户自定义值或缺省值；Windows 配置中以正斜杠存储，如 `C:/ig50-data`）；
   该行缺失时才回退缺省值（Linux `/ig50-data`，Windows `C:\ig50-data`）；
3. **数据就绪抽查**：检查数据目录下是否已有数据文件（如 `base/gplist`，或任意顶层文件）。
   **注意：程序按定时任务更新，安装成功不等于立即有数据**——没到定时任务执行时间时
   数据目录为空属正常，稍后重查即可；
4. **授权检查**：授权文件 `config/ig50.license` 应含 `user=` 与 `market=`（可选值 CN/HK/US）。
   授权缺失时安装脚本会跳过启动服务并提示补救方案；补填后执行
   `systemctl restart ig50`（Linux）或启动 `IG50Service`（Windows）即可；
5. **服务状态**：Linux `systemctl status ig50`；Windows 在「任务计划程序」查看 `IG50Service`；
6. 程序日志：Linux `/opt/ig50/logs`，Windows `C:\ig50\logs`。

最快路径：直接运行 `scripts/check_install.py`，它自动完成上述 1-3 步并输出结论。

## 7. 安装失败排查

1. **网络**：安装脚本需从远程下载程序包，确认服务器可访问外网；
2. **权限**：Linux 用 root/sudo；Windows 用管理员；
3. **杀毒拦截（Windows）**：临时关闭杀毒软件后重试；
4. **系统不兼容**：核对上表系统与 glibc 版本要求；
5. 以上均无效：把安装日志发给客服（service@ig50.com）协助排查。

## 8. 升级与卸载

- 升级免费，执行更新脚本即可（Linux `ig50_update.sh`，Windows `ig50_update.bat`），通常 1-2 分钟；
- 升级期间数据更新短暂暂停，建议盘后执行；不影响已落盘历史数据；
- 所有授权套餐均含持续免费升级。

---

数据集文档：https://ig50.com/dataset-overview.html ｜ 数据检索：https://ig50.com/search.html
