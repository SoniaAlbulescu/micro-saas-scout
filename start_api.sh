#!/bin/bash
# 启动FastAPI开发服务器

echo "🚀 启动Micro SaaS Scout API服务器..."

# 检查Python依赖
echo "📦 检查Python依赖..."
pip install -r requirements.txt

# 设置环境变量
export ENVIRONMENT=development

# 启动FastAPI服务器
echo "⚡ 启动FastAPI服务器..."
uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload

echo "✅ 服务器已启动: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"