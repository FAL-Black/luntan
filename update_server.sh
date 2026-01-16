#!/bin/bash

# 开启错误检查，遇到错误立即停止
set -e

echo "🚀 开始更新论坛系统..."

# 1. 更新代码
echo "📦 正在拉取最新代码..."
cd /var/www/luntan
sudo git fetch --all
sudo git reset --hard origin/main

# 2. 后端更新
echo "🐍 正在更新后端..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "安装依赖..."
pip install -r requirements.txt

# 3. 前端更新
echo "🎨 正在更新前端..."
cd ../frontend
echo "安装前端依赖..."
npm install
echo "构建前端资源..."
npm run build

# 4. 重启服务
echo "🔄 重启服务..."
sudo systemctl restart luntan-backend
# Nginx 通常不需要重启，除非改了 nginx 配置文件
# sudo systemctl restart nginx 

echo "✅ 更新完成！"
