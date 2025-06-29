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

source /home/bobo/kook/123/venv/bin/activate #如何进入虚拟环境
pm2 logs kook_bot #查看日志
pm2 stop kook_bot #终止进程
pm2 restart kook_bot #重启进程

以下是地图文件目录 包括恐龙分布 资源分布 请遵循以下格式部署文件相关文件地址我会贴出后期
kook_bot/
├── resource_translations.json   # 地图翻译文件（如果有）
├── maps/
│   ├── The Island/
│   │   ├── resource1.png
│   │   ├── resource2.png
│   │   └── ...
│   ├── Ragnarok/
│   │   ├── resource1.png
│   │   ├── resource2.png
│   │   └── ...
│   ├── Extinction/
│   │   ├── resource1.png
│   │   ├── resource2.png
│   │   └── ...
│   ├── Aberration/
│   │   ├── resource1.png
│   │   ├── resource2.png
│   │   └── ...
│   └── ...  # 其他地图
└── setup_kook_bot.sh  # 安装脚本
