#!/bin/bash

set -e  # 出错自动退出

INSTALL_DIR="/etc/kook/kook_bot"

# 1. 克隆 GitHub 仓库
echo "🌐 正在克隆 KOOK Bot 仓库到 $INSTALL_DIR ..."
sudo rm -rf "$INSTALL_DIR"
sudo git clone https://github.com/mzk602400288/kook_bot.git "$INSTALL_DIR"

# 2. 安装系统依赖
echo "📦 安装系统依赖（python3、pip、venv、npm、git）..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv npm curl git

# 3. 安装 PM2（如未安装）
if ! command -v pm2 &> /dev/null; then
    echo "⚡ 安装 PM2..."
    sudo npm install -g pm2
else
    echo "✅ PM2 已安装"
fi

# 4. 创建虚拟环境
cd "$INSTALL_DIR"
if [ ! -d "venv" ]; then
    echo "🛠️ 创建虚拟环境..."
    python3 -m venv venv
fi

# 5. 激活虚拟环境并安装依赖
echo "🔧 激活虚拟环境并安装依赖包..."
source venv/bin/activate
pip install --upgrade pip
pip install requests websocket-client

# 6. 启动 KOOK Bot（使用虚拟环境的 Python）
echo "🚀 使用 PM2 启动 KOOK Bot..."
pm2 start kook_bot.py --name kook_bot --interpreter "$INSTALL_DIR/venv/bin/python"

# 7. 设置 PM2 开机自启
echo "🔄 配置 PM2 开机自启..."
pm2 save
pm2 startup | tail -n 1 | bash

echo ""
echo "✅ KOOK Bot 已成功部署并运行！"
echo "📜 查看日志：pm2 logs kook_bot"
echo "📋 进程状态：pm2 list"
