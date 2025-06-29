#!/bin/bash

# 1. 克隆 GitHub 仓库
echo "🌐 克隆 GitHub 仓库..."
git clone https://github.com/mzk602400288/kook_bot.git /home/bobo/kook/123

# 2. 更新系统和安装必要的依赖
echo "🌐 更新系统包列表..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv npm curl git

# 3. 安装 PM2（如果未安装）
if ! command -v pm2 &> /dev/null
then
    echo "⚡ 安装 PM2..."
    sudo npm install pm2@latest -g
else
    echo "✅ PM2 已安装"
fi

# 4. 检查虚拟环境是否已创建，如果未创建则创建虚拟环境
if [ ! -d "/home/bobo/kook/123/venv" ]; then
    echo "🛠️ 创建虚拟环境..."
    python3 -m venv /home/bobo/kook/123/venv
fi

# 5. 激活虚拟环境
echo "🔧 激活虚拟环境..."
source /home/bobo/kook/123/venv/bin/activate

# 6. 安装必要的 Python 包
echo "📦 安装必要的 Python 包..."
pip install --upgrade pip
pip install websocket-client

# 7. 复制 resource_translations.json 文件到目标位置
echo "📁 复制资源翻译文件..."
cp /home/bobo/kook/123/resource_translations.json /home/bobo/kook/123/resource_translations.json

# 8. 使用 PM2 启动 'kook_bot.py'
echo "🚀 启动 KOOK Bot..."
pm2 start /home/bobo/kook/123/kook_bot.py --interpreter python3 --name kook_bot

# 9. 配置 PM2 开机自启动
echo "🔄 设置 PM2 开机自启动..."
pm2 startup
pm2 save

# 10. 完成
echo "✅ KOOK Bot 已成功启动并设置为开机自启动!"
