from fastapi import FastAPI, Depends, HTTPException
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
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "micro-saas-scout-api",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/")
async def root():
    """API根端点"""
    return {
        "message": "Welcome to Micro SaaS Scout API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "hello": "/hello"
        }
    }

@app.get("/hello")
async def hello():
    """Hello端点"""
    return {
        "message": "Hello from Micro SaaS Scout API!",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/stats")
async def system_stats():
    """系统统计信息"""
    try:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system": "Micro SaaS Scout",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "api_version": "1.0.0",
            "status": "operational"
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Vercel Serverless Functions需要这个入口点
# 注意：Vercel会自动处理FastAPI应用，不需要额外的handler
# 这个文件作为FastAPI应用的入口点即可