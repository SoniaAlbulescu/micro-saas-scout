#!/usr/bin/env python3
"""
Vercel兼容的FastAPI应用
根据Vercel文档，Python函数需要特定的入口点
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Micro SaaS Scout API",
    description="出海工具需求挖掘系统后端API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根端点
@app.get("/")
async def root():
    return {
        "message": "Welcome to Micro SaaS Scout API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": ["/health", "/hello", "/stats"]
    }

# 健康检查
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "micro-saas-scout-api",
        "timestamp": datetime.utcnow().isoformat()
    }

# Hello端点
@app.get("/hello")
async def hello():
    return {
        "message": "Hello from Micro SaaS Scout API!",
        "timestamp": datetime.utcnow().isoformat()
    }

# 统计信息
@app.get("/stats")
async def stats():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "system": "Micro SaaS Scout",
        "status": "operational"
    }

# Vercel需要这个handler
# 根据Vercel文档，Python函数应该导出名为'app'的FastAPI实例
# 或者使用下面的handler格式

# 可选：使用Vercel推荐的handler格式
from mangum import Mangum
handler = Mangum(app)

# 如果不想使用mangum，可以注释掉上面的行，使用下面的方式
# Vercel会自动检测FastAPI应用