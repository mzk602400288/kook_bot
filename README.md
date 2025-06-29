# Kook Bot

一个用于与 KOOK API 交互的 Python 机器人，支持自动化操作、服务器查询和倍率查询等功能。

## 一键安装和启动

### 1. 克隆仓库

首先，克隆本仓库到本地：

```bash
git clone https://github.com/mzk602400288/kook_bot.git
cd kook_bot

chmod +x setup_kook_bot.sh  # 给脚本添加执行权限
./setup_kook_bot.sh  # 执行安装脚本

pm2 logs kook_bot #查看日志
pm2 stop kook_bot #终止进程
pm2 restart kook_bot #重启进程

