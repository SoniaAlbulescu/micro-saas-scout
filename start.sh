#!/bin/bash

echo "🚀 启动 Micro SaaS Scout 开发服务器..."
echo "----------------------------------------"

# 检查node_modules是否存在
if [ ! -d "node_modules" ]; then
    echo "📦 正在安装依赖..."
    npm install --no-audit --no-fund --legacy-peer-deps
fi

echo "✅ 依赖安装完成"
echo "🔧 启动开发服务器..."

# 启动开发服务器
npm run dev