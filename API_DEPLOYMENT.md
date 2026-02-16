# API 部署指南

## 问题诊断

之前后端显示404的原因是Vercel路由配置错误：
1. 所有 `/api/(.*)` 请求都被重定向到 `/api/hello.py`
2. FastAPI应用没有被正确配置为Serverless Function

## 修复方案

已修复以下文件：

### 1. `vercel.json` - 路由配置
```json
{
  "builds": [
    {
      "src": "api/index.py",  // 添加FastAPI应用
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"  // 指向FastAPI应用
    }
  ]
}
```

### 2. `api/index.py` - 简化FastAPI应用
- 移除了数据库依赖（Vercel Serverless Functions中需要特殊配置）
- 简化了端点路径（Vercel会自动添加 `/api/` 前缀）
- 保留了核心功能

## 本地测试

### 启动开发服务器
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
./start_api.sh
# 或
uvicorn api.index:app --host 0.0.0.0 --port 8000 --reload
```

### 测试API端点
```bash
# 运行测试脚本
python test_api.py

# 手动测试
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/hello
curl http://localhost:8000/docs
```

## Vercel部署

### 部署步骤
1. **推送代码到GitHub**
   ```bash
   git add .
   git commit -m "修复API路由配置"
   git push origin main
   ```

2. **Vercel自动部署**
   - Vercel会自动检测到代码变更
   - 根据 `vercel.json` 重新配置路由
   - 部署完成后会获得新的URL

3. **验证部署**
   ```bash
   # 使用生产URL测试
   python test_api.py https://your-project.vercel.app/api
   ```

### 预期端点
部署后应该可以访问以下端点：
- `https://your-project.vercel.app/api/` - API根目录
- `https://your-project.vercel.app/api/health` - 健康检查
- `https://your-project.vercel.app/api/hello` - Hello端点
- `https://your-project.vercel.app/api/docs` - API文档

## 故障排除

### 如果仍然显示404
1. **检查Vercel部署日志**
   - 登录Vercel控制台
   - 查看项目部署日志
   - 检查是否有构建错误

2. **验证路由配置**
   ```bash
   # 检查vercel.json语法
   cat vercel.json | python -m json.tool
   ```

3. **测试本地构建**
   ```bash
   # 使用Vercel CLI模拟部署
   vercel dev
   ```

### 数据库连接问题
当前版本移除了数据库依赖以简化部署。如果需要数据库功能：
1. 使用Vercel Postgres或外部数据库服务
2. 配置环境变量 `DATABASE_URL`
3. 重新添加数据库相关代码

## 下一步优化

### 阶段1：基础API（当前）
- ✅ 简单的健康检查端点
- ✅ Hello端点
- ✅ API文档
- ✅ CORS配置

### 阶段2：数据API（后续）
- 需求数据端点 `/api/demands`
- 爬虫端点 `/api/crawl`
- 统计分析端点 `/api/stats`

### 阶段3：完整功能
- 用户认证
- 数据持久化
- 定时任务
- 监控告警

## 技术支持

如有问题，请检查：
1. Vercel部署日志
2. API响应状态码
3. 网络连接和CORS配置
4. 环境变量设置